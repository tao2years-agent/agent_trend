"""Deterministic manual-review sample specified before observing candidate order."""
from pathlib import Path
import hashlib,pandas as pd,sys,json
R=Path(__file__).resolve().parent
partial='--partial' in sys.argv
d=pd.read_csv(R/('partial-queue.csv' if partial else 'queue.csv'),dtype=str);d['score']=d.score.astype(float)
if partial:d=d[d.venue.isin(json.loads((R/'complete-venues.json').read_bytes()))]
chosen=[]
for venue,g in d.groupby('venue'):
    g=g.sort_values(['score','uuid'],ascending=[False,True]);top=g.head(2).copy();top['reason']='highest'
    rest=g[(~g.uuid.isin(top.uuid))&(g.stratum=='still-miss')].copy()
    miss=rest.head(1).copy();miss['reason']='highest_unmatched'
    rest=rest[~rest.uuid.isin(miss.uuid)].copy()
    rest['hash']=rest.uuid.map(lambda s:hashlib.sha256(('abstract-audit-v1|'+s).encode()).hexdigest())
    rnd=rest.sort_values('hash').head(1).copy();rnd['reason']='hash_unmatched'
    chosen.extend([top,miss,rnd])
result=pd.concat(chosen);assert not result.uuid.duplicated().any()
filename='audit-selection.tsv' if not partial else ('in-progress.tsv' if '--stage' in sys.argv else 'early-selection.tsv')
result[['uuid','venue','reason','title','abstract','url']].to_csv(R/filename,sep='\t',index=False)
print(result[['venue','reason','title']].to_string(index=False))

