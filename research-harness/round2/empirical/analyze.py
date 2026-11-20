"""Registered, deterministic cohort, stratified outcomes and sensitivity estimates."""
from pathlib import Path
import io,hashlib,json,re,collections
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ingest import P,KEEP,parquet
REGISTER='d12e7a143d6bef9ae4cd7d9911a1bb46ae91ffb0f4ddda5038f684359ee26af6'
assert hashlib.sha256((P/'preregister.md').read_bytes()).hexdigest()==REGISTER
manifest=json.loads((P/'raw/ranges.json').read_text('utf8'))['ranges']
def code(s):return hashlib.sha256(s.encode()).hexdigest()
def dates(s):return pd.to_datetime(s,utc=True,format='mixed',errors='raise')
OUTPUT=P/'tables';OUTPUT.mkdir(exist_ok=True)
def save(df,f):df.to_csv(OUTPUT/(f+'.csv'),index=False,encoding='utf8',lineterminator='\n')
pr=parquet('pull_request',manifest).read(columns=KEEP['pull_request'],use_threads=False).to_pandas()
assert pr.id.notna().all()
for n in ('created_at','closed_at','merged_at'):pr[n]=dates(pr[n])
pr=pr.drop_duplicates()
conflict=pr[pr.id.duplicated(keep=False)];assert conflict.empty, f'Conflicting PR IDs: {len(conflict)}'
assert pr.created_at.notna().all()
eligible=pr[(pr.created_at>='2026-02-01')&(pr.created_at<'2026-03-01')].copy()
assert eligible[['id','repo_id','agent']].notna().all().all()
eligible['key']=eligible.id.map(lambda i:code('AIDev-r2-20261120|'+str(i)))
sample=eligible.sort_values('key').groupby('agent',sort=True).head(300).copy()
den=eligible.groupby('agent',as_index=False).agg(eligible=('id','size'),eligible_repos=('repo_id','nunique'))
sample=sample.merge(den,on='agent',validate='many_to_one')
sample['repo_key']=sample.repo_id.map(lambda i:code('AIDev-r2-repo|'+str(i))[:18])
sample['repository_rank']=sample.sort_values('key').groupby(['agent','repo_id']).cumcount()+1
assert len(sample.repo_key.unique())==sample.repo_id.nunique()
assert sample.created_at.max()+pd.Timedelta(days=30)<pd.Timestamp('2026-04-01',tz='UTC')
ids=pa.array(sample.id.tolist(),type=pa.int64())
def related(table):
 pf=parquet(table,manifest);pieces=[]
 for i in range(pf.num_row_groups):
  group=pf.read_row_group(i,columns=KEEP[table],use_threads=False)
  pieces.append(group.filter(pc.is_in(group.column('pr_id'),value_set=ids)).to_pandas())
 return pd.concat(pieces,ignore_index=True)
rv=related('pr_reviews').drop_duplicates(); tl=related('pr_timeline').drop_duplicates()
if not rv.empty: assert not rv.id.duplicated().any()
rv['time']=dates(rv.submitted_at);tl['time']=dates(tl.created_at)
table=sample.set_index('id')
for f in [rv,tl]:f['start']=f.pr_id.map(table.created_at); f['ahead_days']=(f.time-f.start).dt.total_seconds()/86400
rv['label']=rv.state.str.upper(); u=rv.user.fillna('').str.lower()
rv['personal']=rv.user_type.fillna('').str.casefold().eq('user')&u.ne('')&~u.str.contains(r'\[bot\]$|(?:^|[-_])(?:bot|automation)(?:$|[-_])',regex=True)&~u.isin(['claude','claude-code','cursor-agent','devin-ai','devin-ai-integration','copilot','openai-codex','google-labs-jules'])
tl['event_normalized']=tl.event.fillna('').str.lower().str.replace('[^a-z]','',regex=True).str.replace(r'event$','',regex=True)
save(tl[tl.ahead_days.between(0,30)].groupby('event_normalized',as_index=False).size().rename(columns={'size':'events_30d'}),'timeline-event-vocabulary')
def build(h):
 x=sample.copy(); horizon=x.created_at+pd.Timedelta(days=h)
 for col in ('closed_at','merged_at'):
  assert not ((x[col].notna())&(x[col]<x.created_at)).any()
 merged=x.merged_at.notna()&(x.merged_at<=horizon);closed=x.closed_at.notna()&(x.closed_at<=horizon)
 x['outcome']='no_terminal_by_horizon';x.loc[closed,'outcome']='closed_unmerged';x.loc[merged,'outcome']='merged'
 r=rv.loc[rv.ahead_days.between(0,h)];t=tl.loc[tl.ahead_days.between(0,h)]
 def ids_for(mask):return set(r.loc[mask,'pr_id'].tolist())
 for lab,flag in [('APPROVED','approve'),('CHANGES_REQUESTED','request_changes')]:
  x[flag]=x.id.isin(ids_for(r.personal & r.label.eq(lab))).astype(int)
 x['personal_decision']=((x.approve+x.request_changes)>0).astype(int)
 x['both_decisions']=(x.approve*x.request_changes)
 x['any_review']=x.id.isin(set(r.pr_id)).astype(int)
 x['any_timeline']=x.id.isin(set(t.pr_id)).astype(int)
 x['draft_transition']=x.id.isin(set(t.loc[t.event_normalized.isin(['converttodraft','convertedtodraft','readyforreview','markreadyforreview']),'pr_id'])).astype(int)
 x['reopen_event']=x.id.isin(set(t.loc[t.event_normalized.isin(['reopen','reopened']),'pr_id'])).astype(int)
 # Registered sensitivity: compare timestamp-derived disposition against dated timeline transitions.
 transitions=t[t.event_normalized.isin(['merged','closed','reopened'])].copy()
 transitions['ordering']=transitions.event_normalized.map({'closed':0,'reopened':1,'merged':2})
 last=transitions.sort_values(['pr_id','time','ordering']).drop_duplicates('pr_id',keep='last').set_index('pr_id').event_normalized
 observed=x.id.map(last).fillna('no_dated_transition').replace({'merged':'merged','closed':'closed_unmerged','reopened':'no_terminal_by_horizon'})
 # A merge cannot be undone by a later closed marker emitted for the same PR.
 observed.loc[x.id.isin(set(transitions.loc[transitions.event_normalized.eq('merged'),'pr_id']))]='merged'
 x['timeline_outcome']=observed.to_numpy()
 cross=x.groupby(['outcome','timeline_outcome'],as_index=False).size()
 save(cross,'timeline-crosscheck-'+str(h)+'d')
 for l in ['merged','closed_unmerged','no_terminal_by_horizon']: x[l]=x.outcome.eq(l).astype(int)
 return x
outcomes=['merged','closed_unmerged','no_terminal_by_horizon']; flags=outcomes+['approve','request_changes','both_decisions','personal_decision','any_review','any_timeline','draft_transition','reopen_event']
def agg(x,g):
 sizes=x.groupby(g,as_index=False).agg(n=('id','size'),repositories=('repo_key','nunique')); sums=x.groupby(g,as_index=False)[flags].sum()
 return sizes.merge(sums,on=g)
ss=[];stats={}
for h in (7,30):
 x=build(h);save(agg(x,['agent']).merge(den,on='agent'),'agent-'+str(h)+'d')
 save(agg(x[x.repository_rank<=5],['agent']),'repo-cap5-'+str(h)+'d')
 save(agg(x,['outcome']),'outcome-'+str(h)+'d')
 x['window_days']=h
 ss.append(x[['key','repo_key','agent','window_days','repository_rank','outcome','timeline_outcome',*flags]])
 strata=agg(x,['agent']).merge(den,on='agent')
 stats[h]={'n':len(x),'repos':x.repo_id.nunique(),'totals':{f:int(x[f].sum())for f in flags},
 'weighted_percent':{f:float((strata[f]/strata.n*strata.eligible).sum()/strata.eligible.sum()*100)for f in flags},'cap5_n':int((x.repository_rank<=5).sum()),'cap5_totals':{f:int(x.loc[x.repository_rank<=5,f].sum())for f in flags}}
save(pd.concat(ss).rename(columns={'key':'pr_key'}),'sample-minimal')
r=rv[rv.ahead_days.between(0,30)];save(r.groupby(['user_type','label','personal'],as_index=False,dropna=False).size(),'review-labels-30d')
audit={'upstream_pop':len(pr),'eligible':len(eligible),'eligible_repos':eligible.repo_id.nunique(),'sample_repos':sample.repo_id.nunique(),'sampled':len(sample),'review_rows_matched':len(rv),'timeline_rows_matched':len(tl),'review_rows_after_30d':int((rv.ahead_days>30).sum()),'timeline_rows_after_30d':int((tl.ahead_days>30).sum()),'review_rows_missing_time':int(rv.time.isna().sum()),'timeline_rows_missing_time':int(tl.time.isna().sum()),'windows':stats}
(P/'audit.json').write_text(json.dumps(audit,indent=2),'utf8')
print(json.dumps(audit,indent=2))
