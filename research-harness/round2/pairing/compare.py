"""Recompute paired benchmark outcomes. Reads only issue identifiers and pass/fail labels."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
import datetime, hashlib, json
import pandas as pd, requests
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
rev='40f164d5b8f1d249bf95a6df8b74b577fd8e519d'
site=R/'leaderboard-20261120.html'
soup=BeautifulSoup(site.read_bytes(),'html.parser')
groups=json.loads(soup.select_one('#leaderboard-data').string)
board=next(v['results'] for v in groups if v['name']=='Verified')
inputs=[]; eligible=[]
for r in board:
    name=(r['name']+r['folder']).lower().replace('-','')
    selected='sonnet' in name and '20241022' in name and ('3.5' in name or '35' in name)
    inputs.append({'name':r['name'],'folder':r['folder'],'decision':'selected' if selected else 'outside preselected named revision'})
    if selected:eligible.append(r)
pd.DataFrame(inputs).to_csv(R/'screen.csv',index=False)
raw=R/'raw';raw.mkdir(exist_ok=True)
universe=pd.read_parquet(R.parent/'oracles/raw/verified.parquet',columns=['instance_id']).instance_id
assert len(set(universe))==500
def fetch(x):
    tag=x['folder']
    received=[]
    for p in ['results/results.json','metadata.yaml','README.md']:
        u=f'https://raw.githubusercontent.com/SWE-bench/experiments/{rev}/evaluation/verified/{tag}/{p}'
        dest=raw/(tag+'--'+Path(p).name)
        if not dest.exists():
            for attempt in range(3):
                try:
                    res=requests.get(u,timeout=20);res.raise_for_status();break
                except requests.RequestException:
                    if attempt==2:raise
            dest.write_bytes(res.content)
        received.append(dict(url=u,path=dest.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
    data=json.loads((raw/(tag+'--results.json')).read_text('utf8'))
    hits=set(data['resolved'])
    assert hits <= set(universe) and len(hits)/5==x['resolved']
    return tag,hits,received
with ThreadPoolExecutor(5) as pool:runs=list(pool.map(fetch,eligible))
manifest=[s for _,_,files in runs for s in files]+[dict(path=site.name,url='https://www.swebench.com/',sha256=hashlib.sha256(site.read_bytes()).hexdigest())]
(R/'manifest.json').write_text(json.dumps(manifest,indent=2),'utf8')
matrix=pd.DataFrame({'instance_id':universe,'repo':universe.str.rsplit('-',n=1).str[0]})
for name,hits,_ in runs:matrix[name]=universe.isin(hits).astype('int8')
matrix.to_csv(R/'scores.csv',index=False)
out=[]
for (a,_,_),(b,_,_) in combinations(runs,2):
    for repo,subset in [('ALL',matrix),*matrix.groupby('repo')]:
        x,y=subset[a].astype(bool),subset[b].astype(bool)
        out.append(dict(first=a,second=b,repo=repo,n=len(x),both=int((x&y).sum()),first_only=int((x&~y).sum()),second_only=int((y&~x).sum()),neither=int((~x&~y).sum()),gap_pp=100*(x.mean()-y.mean())))
pd.DataFrame(out).to_csv(R/'pairs.csv',index=False)
print([(len(h),tag) for tag,h,_ in runs])
