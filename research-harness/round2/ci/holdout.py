"""Temporal holdout using observed OpenStack rechecks. Does not deserialize executable pickles."""
import ast,hashlib,json,sys,tempfile,zipfile
from pathlib import Path
from datetime import datetime,timezone
import numpy as np,pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss
R=Path(__file__).resolve().parent
arc=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.gettempdir())/'ase25-rechecks-15559526.zip'
with arc.open('rb') as f:digest=hashlib.file_digest(f,'md5').hexdigest()
assert digest=='348cedd8f2a0a0bee139031ad6240813'
prefix='replication_package_rechecks/'
fn=prefix+'features_datasets/final_datasets/features_years_20.csv'
minimal=['key','project','date_of_recheck','label','lines_inserted','lines_deleted','numbers_of_unique_files','queued_hour','queued_day','jobs_success_ratio','bots_success_ratio']
with zipfile.ZipFile(arc) as z:
    with z.open(fn) as f:df=pd.read_csv(f,usecols=minimal)
    with z.open(fn) as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    idx=json.loads(z.read(prefix+'features_creation.ipynb'))
    code='\n\n'.join(''.join(c.get('source',[])) for c in idx['cells'] if c.get('cell_type')=='code')
    (R/'feature-code.txt').write_text(code,'utf8')
    (R/'job-window.py.txt').write_bytes(z.read(prefix+'helper_collections_window/helper_collections_jobs_occurence.py'))
    (R/'author-table.csv').write_bytes(z.read(prefix+'model_results/final/model_results.csv'))
df=df.sort_values(['date_of_recheck','key']).reset_index(drop=True)
dt=pd.to_datetime(df.date_of_recheck)
keys=df.key.str.extract(r'^\((\d+),\s*(\d+),\s*(\d+)\)$').astype(int)
keys.columns=['change_id','patch','rerun'];df=pd.concat([df,keys],axis=1)
assert df.label.isin([0,1]).all() and not df.key.duplicated().any()
cut1=dt.iloc[int(.6*len(df))];cut2=dt.iloc[int(.8*len(df))]
# Seven days of washout ahead of both frozen decision points, with a separate 30-day sensitivity.
out=[];groups=[];results={}
for days in [7,30]:
    gap=pd.Timedelta(days=days)
    tr=df[dt<cut1-gap].copy();dv=df[(dt>=cut1)&(dt<cut2-gap)].copy();te=df[dt>=cut2].copy()
    inside=tr.label.mean()
    covars=['lines_inserted','lines_deleted','numbers_of_unique_files','queued_hour','queued_day','patch','rerun']
    def features(t):
        m=t[covars].copy()
        for c in ['lines_inserted','lines_deleted','numbers_of_unique_files','patch','rerun']:m[c]=np.log1p(m[c].clip(lower=0))
        return m
    fit=make_pipeline(SimpleImputer(strategy='median',add_indicator=True),StandardScaler(),LogisticRegression(max_iter=300))
    fit.fit(features(tr),tr.label)
    historical=tr.groupby('project').label.agg(['sum','size'])
    prior=(historical['sum']+20*inside)/(historical['size']+20)
    def score(t):
        return {'always':np.full(len(t),inside),'project':t.project.map(prior).fillna(inside).to_numpy(),'pre_request':fit.predict_proba(features(t))[:,1],
                'published_job_field':t.jobs_success_ratio.where(t.jobs_success_ratio.between(0,1),inside).fillna(inside).to_numpy()}
    dev=score(dv);test=score(te)
    results[str(days)]={'population':len(df),'training':len(tr),'validation':len(dv),'test':len(te),'training_green':int(tr.label.sum()),'validation_green':int(dv.label.sum()),'test_green':int(te.label.sum()),'projects':int(te.project.nunique()),'pristine_test_changes':int((~te.change_id.isin(set(tr.change_id)|set(dv.change_id))).sum()),'min':dt.min().isoformat(),'max':dt.max().isoformat(),'cut1':cut1.isoformat(),'cut2':cut2.isoformat()}
    for method in dev:
        for retain in [.90,.95,.99]:
            positive=np.sort(dev[method][dv.label.to_numpy()==1])
            threshold=float(positive[max(0,int(np.floor((1-retain)*len(positive))))])
            pred=test[method]>=threshold;y=te.label.to_numpy(dtype=bool)
            cohort={'full_test':np.ones(len(y),bool),'unseen_change':~te.change_id.isin(set(tr.change_id)|set(dv.change_id)).to_numpy(),
                    'known_project':te.project.isin(tr.project).to_numpy(),'new_project':~te.project.isin(tr.project).to_numpy()}
            for label,c in cohort.items():
                keep=pred[c];truth=y[c]
                if not len(truth):continue
                st=dict(embargo=days,method=method,target=retain,cohort=label,threshold=threshold,n=len(truth),green=int(truth.sum()),rerun=int(keep.sum()),missed_green=int((~keep&truth).sum()),avoided_red=int((~keep&~truth).sum()),auc=roc_auc_score(truth,test[method][c]) if len(set(truth))==2 else None,ap=average_precision_score(truth,test[method][c]) if truth.any() else None,brier=brier_score_loss(truth,np.clip(test[method][c],0,1)))
                out.append(st)
            if days==7 and retain==.95:
                for project,g in pd.DataFrame(dict(key=te.project.to_numpy(),green=y,kept=pred)).groupby('key'):
                    groups.append(dict(project_hash=hashlib.sha256(str(project).encode()).hexdigest()[:18],method=method,n=len(g),green=int(g.green.sum()),rerun=int(g.kept.sum()),missed_green=int((g.green&~g.kept).sum())))
pd.DataFrame(out).to_csv(R/'policy.csv',index=False);pd.DataFrame(groups).to_csv(R/'project-check.csv',index=False)
(R/'audit.json').write_text(json.dumps(dict(record=15559526,url='https://zenodo.org/records/15559526',archive_md5=digest,input=fn,input_sha256=sha,cols=minimal,splits=results),indent=2),'utf8')
print(results['7']);print(pd.DataFrame(out).query("embargo==7 and target==.95 and cohort=='full_test'")[['method','n','green','rerun','missed_green','avoided_red','auc','ap','brier']].round(3).to_string(index=False))
