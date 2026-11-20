"""Audit frozen METR study extracts; distinguish observed status from unobserved withheld work."""
from pathlib import Path
import json,csv,hashlib,sys,subprocess,importlib.metadata
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parent
src={s['id']:s for s in json.loads((R/'sources.json').read_text(encoding='utf8'))}
for s in src.values():
    assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
def csv_out(name,rows):
    with (R/name).open('w',newline='',encoding='utf-8-sig') as handle:
        w=csv.DictWriter(handle,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for k,file in (('early','data_complete.csv'),('late','data.csv')):
    code=R/src[k+'-regression.py']['path'];data=R/src[k+'-'+file]['path']
    proc=subprocess.run([sys.executable,str(code),'--input-data',str(data)],capture_output=True,text=True,check=True)
    (R/(k+'-upstream-run.txt')).write_text(proc.stdout+proc.stderr,encoding='utf8')
early=pd.read_csv(R/src['early-data_complete.csv']['path'])
d=pd.read_csv(R/src['late-data.csv']['path'])
assert d.id.is_unique and d.developerId.notna().all() and set(d.treatmentAssignment)=={'AI-allowed','AI-disallowed'}
d['done']=d.status.eq('complete')
d['usable']=d.done & (d.initialImplementationTime+d.postReviewImplementationTime.fillna(0)).gt(0) & d.estimatedTimeWithoutAI.gt(0)
arms=['AI-allowed','AI-disallowed']
statuses=['complete','incomplete','ditched','cheating','corrupted']
status_rows=[]
for cohort,z in [('all',d),('returning',d[d.isPanelDeveloper]),('new',d[~d.isPanelDeveloper])]:
    for arm in arms:
        cut=z[z.treatmentAssignment.eq(arm)]
        status_rows.append(dict(cohort=cohort,assigned_arm=arm,developers=cut.developerId.nunique(),exported=len(cut),
                                **{s:int(cut.status.eq(s).sum()) for s in statuses},eligible_for_total_time=int(cut.usable.sum())))
csv_out('selection-funnel.csv',status_rows)
cutoff=pd.to_datetime(d.lastModified).max()
horizon=(cutoff-pd.to_datetime(d.createdAt)).dt.days
def measurements(label,z):
    g=z.groupby(['developerId','treatmentAssignment']).done.agg(['sum','size','mean']).unstack()
    both=g.dropna()
    block=z.groupby('treatmentAssignment').done.agg(['sum','size','mean'])
    pct=lambda x:round(100*float(x),4)
    def pooled(table):return table.loc['AI-allowed','mean']-table.loc['AI-disallowed','mean']
    both_records=z[z.developerId.isin(both.index)].groupby('treatmentAssignment').done.agg(['sum','size','mean'])
    diffs=both['mean']['AI-allowed']-both['mean']['AI-disallowed']
    # This is resampling the observed people, not an interval for all eligible developers or withheld tasks.
    seed=np.random.default_rng(20261120)
    avg=seed.choice(diffs.to_numpy(),size=(20000,len(diffs)),replace=True).mean(axis=1)
    return dict(window=label,developers=z.developerId.nunique(),records=len(z),both_arm_devs=len(both),both_arm_records=int(both_records['size'].sum()),
                all_task_weighted_gap_pp=pct(pooled(block)),same_people_task_weighted_gap_pp=pct(pooled(both_records)),same_people_equal_person_gap_pp=pct(diffs.mean()),
                equal_person_conditional_boot_p025_pp=pct(np.quantile(avg,.025)),equal_person_conditional_boot_p975_pp=pct(np.quantile(avg,.975)),
                same_people_allowed_complete=int(both_records.loc[arms[0],'sum']),same_people_allowed_records=int(both_records.loc[arms[0],'size']),
                same_people_disallowed_complete=int(both_records.loc[arms[1],'sum']),same_people_disallowed_records=int(both_records.loc[arms[1],'size']))
windows=[('all_exported',d),('no_admin_status',d[d.status.isin(statuses[:3])]),('at_least_30_days_since_assignment',d[horizon>=30]),('returning_only',d[d.isPanelDeveloper]),('new_only',d[~d.isPanelDeveloper])]
rr=[measurements(*x) for x in windows]
csv_out('weights-and-maturity.csv',rr)
funnel={'early_complete':len(early),'early_developers':early.dev_id.nunique(),'early_allowed':int(early.ai_treatment.sum()),
        'early_post_review_time_missing':int(early.post_review_implementation_time.isna().sum()),'late_all_exported':len(d),'late_developers':d.developerId.nunique(),
        'late_overlapping_developers':d[d.isPanelDeveloper].developerId.nunique(),'late_new_developers':d[~d.isPanelDeveloper].developerId.nunique(),
        'late_status_complete':int(d.done.sum()),'late_usable_total_time_rows':int(d.usable.sum()),'late_usable_total_time_people':d[d.usable].developerId.nunique(),
        'late_2026_assignments':int(pd.to_datetime(d.createdAt).dt.year.eq(2026).sum()),'first_randomization':d.createdAt.min(),'last_randomization':d.createdAt.max(),'last_modification':d.lastModified.max(),
        'packages':{n:importlib.metadata.version(n) for n in ('numpy','pandas','statsmodels','scipy')}}
assert (len(d),len(early),int(d.usable.sum()),rr[0]['both_arm_devs'])==(1134,246,827,51)
assert abs(rr[0]['same_people_task_weighted_gap_pp']-4.7604)<.001 and abs(rr[0]['same_people_equal_person_gap_pp']+3.8703)<.001
(R/'summary.json').write_text(json.dumps(funnel,indent=2),encoding='utf8')
print(json.dumps(funnel));print(rr[0])
