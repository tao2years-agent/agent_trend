from pathlib import Path
import requests,hashlib,json
R=Path(__file__).resolve().parent
g=next(r for r in json.loads((R/'git-trees.json').read_bytes()) if r['repo'].endswith('BDUpdater'))
data=[]
for x in ['data/experiment/rq2/ablation.json','BDUpdater/references/schemas/repair-report.schema.json','README.md']:
    url='https://raw.githubusercontent.com/'+g['repo']+'/'+g['rev']+'/'+x
    res=requests.get(url,timeout=45);res.raise_for_status();raw=res.content
    digest=hashlib.sha256(raw).hexdigest();p=R/'raw'/(digest[:12]+'-'+x.split('/')[-1])
    if not p.exists():p.write_bytes(raw)
    tree=[l.split(chr(9))[0].split()[-1] for l in (R/g['path']).read_text('utf8').splitlines() if l.split(chr(9))[-1]==x];assert len(tree)==1
    assert hashlib.sha1(('blob '+str(len(raw))+'\x00').encode()+raw).hexdigest()==tree[0]
    data.append(dict(path=p.relative_to(R).as_posix(),url=url,sha256=digest,git_blob=tree[0]))
    if x.endswith('ablation.json'):
        d=json.loads(raw);print(type(d),len(d),str(d)[:1300])
(R/'ablation-sources.json').write_text(json.dumps(data,indent=2),'utf8')

