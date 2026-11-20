from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,hashlib,requests,gzip
R=Path(__file__).resolve().parent
REV='40f164d5b8f1d249bf95a6df8b74b577fd8e519d'
def fetch(name):
    base='https://raw.githubusercontent.com/SWE-bench/experiments/'+REV+'/evaluation/verified/'+name+'/results/results.json'
    if 'mini-v1.7' in name:base=base.replace('results/results.json','per_instance_details.json')
    f=R/'raw'/('verified-'+name+'.json')
    s=requests.Session();s.trust_env=False;q=s.get(base,timeout=20);q.raise_for_status()
    if f.exists():assert f.read_bytes()==q.content
    else:f.write_bytes(q.content)
    return dict(url=base,path=f.name,sha256=hashlib.sha256(q.content).hexdigest(),retrieved=datetime.now(timezone.utc).isoformat())
def analyze():
    data=json.loads(gzip.decompress((R/'raw/author-score-labels.json.gz').read_bytes()))['labels'];out=[]
    for n,rows in data.items():
        k=n.removeprefix('audit_');j=json.loads((R/'raw'/('verified-'+k+'.json')).read_text('utf8'))
        if 'resolved' not in j:j={'resolved':[i for i,v in j.items() if v['resolved']], 'no_generation':[],'no_logs':[]}
        unresolved=set(rows)-set(j['resolved'])
        for scope,keys in [('unresolved',unresolved),('unresolved_with_generation',unresolved-set(j.get('no_generation',[]))),('unresolved_with_log_and_generation',unresolved-set(j.get('no_generation',[]))-set(j.get('no_logs',[])))]:
            v=[rows[i][1] for i in sorted(keys)]
            out.append(dict(agent=n,scope=scope,n=len(v),first=sum(a[0] for a in v),majority=sum(sum(a)>=3 for a in v),all_draw=sum(sum(a) for a in v),pbt_failed=sum(not rows[i][0] for i in keys),resolved_but_pbt_fails=sum(not rows[i][0] for i in set(rows)&set(j['resolved']))))
    (R/'swe-joined.json').write_text(json.dumps(out,indent=2),'utf8')
    for a in out:
        if a['scope']=='unresolved_with_log_and_generation':print(a['agent'][:25],a['n'],a['first'],a['majority'],a['all_draw'],a['pbt_failed'])
if __name__=='__main__':
    import sys
    if '--fetch' in sys.argv:
        labs=json.loads(gzip.decompress((R/'raw/author-score-labels.json.gz').read_bytes()))['labels']
        with ThreadPoolExecutor(5) as e:refs=list(e.map(fetch,[k for k in labs if not k.startswith('audit_')]))
        (R/'swe-sources.json').write_text(json.dumps(refs,indent=2),'utf8')
    analyze()

