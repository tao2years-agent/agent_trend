"""Compute aggregate ordering of observable reviews and snapshot terminal events, offline."""
import json,sys,hashlib
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'empirical'))
from ingest import parquet,CACHE,KEEP
h=json.loads((R.parent/'empirical/raw/ranges.json').read_bytes())
manifest=h['ranges']
for row in manifest:
    if row['table'] not in ('pull_request','pr_reviews'):continue
    src=CACHE/row['table']/f"{row['start']}-{row['end']}.bin"
    assert hashlib.sha256(src.read_bytes()).hexdigest()==row['sha256']
def times(a):return pd.to_datetime(a,utc=True,format='mixed',errors='raise')
pr=parquet('pull_request',manifest).read(columns=KEEP['pull_request'],use_threads=False).to_pandas().drop_duplicates().set_index('id')
assert pr.index.is_unique
for col in ('created_at','closed_at','merged_at'):pr[col]=times(pr[col])
pr=pr[pr.created_at.between(pd.Timestamp('2025-12-01',tz='UTC'),pd.Timestamp('2026-03-01',tz='UTC'),inclusive='left')].copy()
end=pr.created_at+pd.Timedelta(days=30)
merge=pr.merged_at.between(pr.created_at,end);close=(~merge)&pr.closed_at.between(pr.created_at,end)
pr['terminal']=pr.merged_at.where(merge,pr.closed_at.where(close))
pr['outcome']='no_terminal'
pr.loc[merge,'outcome']='merged';pr.loc[close,'outcome']='closed'
pr['month']=pr.created_at.dt.strftime('%Y-%m')
pf=parquet('pr_reviews',manifest);groups=[]
for i in range(pf.num_row_groups):
    v=pf.read_row_group(i,columns=KEEP['pr_reviews'],use_threads=False).to_pandas()
    v=v[v.pr_id.isin(pr.index)&v.state.str.upper().isin(['APPROVED','CHANGES_REQUESTED'])].copy()
    n=v.user.fillna('').str.casefold()
    person=v.user_type.fillna('').str.casefold().eq('user')&n.ne('')&~n.str.contains(r'\[bot\]$|(?:^|[-_])(?:bot|automation)(?:$|[-_])',regex=True)&~n.isin(['claude','claude-code','cursor-agent','devin-ai','devin-ai-integration','copilot','openai-codex','google-labs-jules'])
    v=v[person];v['submitted']=times(v.submitted_at)
    v=v[v.submitted.between(v.pr_id.map(pr.created_at),v.pr_id.map(end))]
    groups.append(v.groupby('pr_id').submitted.min())
pr['first_decision']=pd.concat(groups).groupby(level=0).min().reindex(pr.index)
pr['order']='no_decision'
d,t=pr.first_decision,pr.terminal
for flag,name in [(d.notna()&t.isna(),'only_decision'),(d<t,'before'),(d==t,'tie'),(d>t,'after')]:
    pr.loc[flag,'order']=name
assert len(pr)==140164 and d.notna().sum()==33017 and (merge.sum(),close.sum())==(94947,30759)
orders=[];queues=[]
for group,p in [('all',pr),*list(pr.groupby('month'))]:
    for (a,b),n in p.groupby(['outcome','order']).size().items():
        orders.append(dict(group=group,outcome=a,order=b,n=int(n)))
    for hr in [1,24,72,168]:
        limit=p.created_at+pd.Timedelta(hours=hr)
        q=p[(p.terminal.isna()|(p.terminal>limit))&(p.first_decision.isna()|(p.first_decision>limit))]
        counts={cat:int((q.order==cat).sum()) for cat in ['before','tie','after','only_decision']}
        counts['terminal_only']=int((q.terminal.notna()&q.first_decision.isna()).sum())
        counts['neither']=int((q.terminal.isna()&q.first_decision.isna()).sum())
        assert sum(counts.values())==len(q)
        queues.append(dict(group=group,age_hours=hr,eligible=len(q),merged=int((q.outcome=='merged').sum()),**counts))
pd.DataFrame(orders).to_csv(R/'orders.csv',index=False)
pd.DataFrame(queues).to_csv(R/'queue.csv',index=False)
print(pd.DataFrame(orders).query("group=='all'").to_string(index=False))
print(pd.DataFrame(queues).query("group=='all'").to_string(index=False))

