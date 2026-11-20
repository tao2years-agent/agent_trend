"""Audit full case join and replay the same 7-day temporal split using pre-request proxies."""
from extract import feature_table,BASE,CACHE
import json
import numpy as np,pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,average_precision_score

def main():
    df=feature_table()
    pairs=pd.read_csv(CACHE/'paired.tsv.gz',sep='\t',dtype={'prior_codes':'string'}).set_index('row')
    df=df.join(pairs).sort_values(['date_of_recheck','key']).reset_index(drop=True)
    dt=pd.to_datetime(df.date_of_recheck);cut1=dt.iloc[int(.6*len(df))];cut2=dt.iloc[int(.8*len(df))]
    gap=pd.Timedelta(days=7); tr=dt<cut1-gap; dv=(dt>=cut1)&(dt<cut2-gap);te=dt>=cut2
    good=df.time_agrees.eq(1)&df.before.eq(1)&df.previous_failure.eq(1)
    strict=good & df.after.eq(1) & df.label_agrees.eq(1) & df.seqgap.eq(1)
    cohorts={'all':np.ones(len(df),bool),'train':tr,'validation':dv,'test':te}
    cohorts.update({f'year_{yr}':dt.dt.year==yr for yr in sorted(dt.dt.year.unique())})
    rows=[];quant=[]
    for name,sub in cohorts.items():
        x=df.loc[sub];both=x.nprev.gt(0)&x.npost.gt(0)
        st=strict[sub]; sb=st&both
        rows.append(dict(cohort=name,n=len(x),paired=int(x.nprev.notna().sum()),both_empty=int(x.both_empty.sum()),
            prev_only_empty=int((x.nprev.eq(0)&x.npost.gt(0)).sum()),current_only_empty=int((x.npost.eq(0)&x.nprev.gt(0)).sum()),both_nonempty=int(both.sum()),
            previous_failure=int(x.previous_failure.sum()),request_match=int(x.time_agrees.sum()),label_match=int(x.label_agrees.sum()),sequence_adjacent=int(x.seqgap.eq(1).sum()),
            prev_clock_present=int(x.prev_to_request_s.notna().sum()),post_clock_present=int(x.request_to_post_s.notna().sum()),prev_before=int(x.before.sum()),post_after=int(x.after.sum()),
            safe_prior=int(good[sub].sum()),strict_pair=int(st.sum()),strict_both_nonempty=int(sb.sum()),changed_recorded_all=int(x.changed.sum()),
            changed_both_nonempty=int(x.loc[both,'changed'].sum()),changed_strict=int(x.loc[st,'changed'].sum()),changed_strict_nonempty=int(x.loc[sb,'changed'].sum()),
            bare_name_changed_strict_nonempty=int(x.loc[sb,'name_changed'].sum()),bots_changed_strict_nonempty=int(x.loc[sb,'bot_changed'].sum()),
            additions_strict_nonempty=int(x.loc[sb,'added'].gt(0).sum()),removals_strict_nonempty=int(x.loc[sb,'removed'].gt(0).sum()),
            additions_and_removals_strict_nonempty=int((x.loc[sb,'removed'].gt(0)&x.loc[sb,'added'].gt(0)).sum())))
        if sb.any():
            for col in ['prev_to_request_s','request_to_post_s','nprev','npost']:
                q=x.loc[sb,col].quantile([.1,.5,.9])
                quant.append(dict(cohort=name,field=col,n=int(sb.sum()),p10=q.loc[.1],median=q.loc[.5],p90=q.loc[.9]))
    pd.DataFrame(rows).to_csv(BASE/'roster-counts.csv',index=False)
    pd.DataFrame(quant).to_csv(BASE/'quantiles.csv',index=False)
    hist={int(c):v for c,v in json.loads((CACHE/'hist.json').read_text()).items()}
    global_job=sum(v[0] for v in hist.values())/sum(v[1] for v in hist.values())
    rates={c:(s+20*global_job)/(n+20) for c,(s,n) in hist.items()}
    def history(x):
        if pd.isna(x) or not x:return global_job
        return min(rates.get(int(c),global_job) for c in x.split())
    mins=df.prior_codes.map(history).astype(float)
    train=df.loc[tr];base=train.label.mean()
    prior=train.groupby('project').label.agg(['sum','size']);prior=(prior['sum']+20*base)/(prior['size']+20)
    project=df.project.map(prior).fillna(base)
    past=pd.DataFrame(dict(available=good.astype(int),prev_jobs=np.log1p(df.nprev.where(good,0)),prev_success=np.log1p(df.prev_success.where(good,0)),
           prev_failed=np.log1p(df.prev_failed.where(good,0)),prev_reporters=np.log1p(df.prev_posts.where(good,0)),
           prior_age=np.log1p(df.prev_to_request_s.where(good,0)),empty=df.nprev.eq(0).where(good,False).astype(int)))
    # The frozen prior-job history is a separate ranker. Fit the metadata model without job/label-history aggregates,
    # so training rows never receive their own outcome or a future training job profile as covariates.
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=300));model.fit(past[tr],df.label[tr])
    predict=model.predict_proba(past)[:,1]
    scores={'always':np.repeat(base,len(df)),'project':project.to_numpy(),'published_current_result_roster':df.jobs_success_ratio.where(df.jobs_success_ratio.between(0,1),base).fillna(base).to_numpy(),'prior_roster_frozen_job_history':mins.to_numpy(),'prior_report_metadata':predict}
    y=df.label.to_numpy(bool); out=[]
    for nm,s in scores.items():
        positive=np.sort(s[dv & y]);th=float(positive[int(np.floor((1-.95)*len(positive)))])
        for group,mask in [('all_test',te),('strict_both_nonempty_test',te & strict & df.nprev.gt(0) & df.npost.gt(0))]:
            pred=s[mask]>=th;truth=y[mask]
            out.append(dict(method=nm,cohort=group,threshold=th,n=len(truth),green=int(truth.sum()),rerun=int(pred.sum()),missed_green=int((~pred&truth).sum()),avoided_red=int((~pred&~truth).sum()),
                retain_green=float((pred&truth).sum()/truth.sum()),auc=roc_auc_score(truth,s[mask]),ap=average_precision_score(truth,s[mask])))
    pd.DataFrame(out).to_csv(BASE/'policy.csv',index=False)
    (BASE/'replay.json').write_text(json.dumps(dict(cut1=str(cut1),cut2=str(cut2),embargo_days=7,training=int(tr.sum()),validation=int(dv.sum()),test=int(te.sum()),
        training_green=int(y[tr].sum()),validation_green=int(y[dv].sum()),test_green=int(y[te].sum()),training_prev_job_pairs=len(hist),training_prev_jobs=int(sum(v[1] for v in hist.values())),training_prev_green_job_fraction=global_job,prior_clock_available_test=int((te&good).sum()),prior_nonempty_test=int((te&good&df.nprev.gt(0)).sum()))),encoding='utf8')
    print(pd.DataFrame(rows).iloc[:4].to_string(index=False));print(pd.DataFrame(out).query("cohort=='all_test'").to_string(index=False))
if __name__=='__main__':main()
