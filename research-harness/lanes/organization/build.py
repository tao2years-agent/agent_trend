"""Join manual evidence cards against content-hashed source manifests."""
import json
import hashlib
from pathlib import Path

base=Path(__file__).resolve().parent
root=base.parent.parent
def read(p): return json.loads((base/p).read_text(encoding='utf8'))

def checked(record):
    assert hashlib.sha256((root/record['path']).read_bytes()).hexdigest()==record['sha256'],record['path']
    return record

def build():
    files=read('raw/manifest.json')['files']
    extra=read('raw/opencost-manifest.json') if (base/'raw/opencost-manifest.json').exists() else None
    if extra and not any(f['id']=='opencost' for f in files):
        files+=extra['files']
    commits={r['id']:r for r in read('commit-metadata.json')}
    releases={r['id']:checked(r) for r in read('raw/release-pages.json')['files']}
    if extra and 'opencost' not in releases:
        releases['opencost']=checked(extra['release'])
    releases['opencost']['date']='2026-10-13' # release page identifies this as the tag date
    notes=read('review.json')
    cards=[]
    for slug,ident,name,category,scenario,mechanism,human,org,limits,change,insight,experiment,details in notes:
        selection=[checked(f) for f in files if f['id']==slug]
        assert len(selection)==len(details)
        sources=[dict(url=f['url'],path=f['path'],date=commits[slug]['date'][:10],detail=d) for f,d in zip(selection,details)]
        r=releases[slug]
        sources.append(dict(url=r['url'],path=r['path'],date=r['date'][:10],detail=change))
        if slug=='k6':
            runtime=read('runtime/k6.json')
            sources.append(dict(url=runtime['artifact'],path='lanes/organization/runtime/k6.json',
                                date=runtime['tested_at'][:10],detail='本地 Windows 实验记录，含 CLI 输入、标准输出、标准错误、退出码以及官方压缩包 SHA-256。'))
        cards.append(dict(id=ident,name=name,category=category,scenario=scenario,mechanism=mechanism,
                          human=human,org=org,limits=limits,change=change,insight=insight,experiment=experiment,sources=sources))
    assert len({c['id'] for c in cards})==11
    (base/'cases.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False),encoding='utf8')
    print(len(cards),'cards;', sum(len(c['sources']) for c in cards),'evidence pointers')

if __name__=='__main__': build()
