"""Read exact published npm archives, verify SRI, capture manifests and implementation excerpts."""
from pathlib import Path
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import requests,tarfile,io,json,hashlib,base64,datetime,re
B=Path(__file__).resolve().parent;RAW=B/'raw';RAW.mkdir(exist_ok=True)
packages=[(p,v) for p in ['react','react-dom'] for v in ['17.0.2','18.2.0','19.0.0']]+[('@testing-library/react',v) for v in ['12.1.5','13.4.0','16.1.0']]+[('@testing-library/dom',v) for v in ['8.20.1','9.3.4','10.4.0']]+[('jsdom','24.1.3')]
def fetch(pair):
    pkg,v=pair;u=f'https://registry.npmjs.org/{quote(pkg,safe="@")}/{v}';r=requests.get(u,timeout=20);r.raise_for_status();m=r.json()
    dist=m['dist'];r=requests.get(dist['tarball'],timeout=30);r.raise_for_status();buf=r.content
    alg,dig=dist['integrity'].split('-',1);assert base64.b64encode(hashlib.new(alg,buf).digest()).decode()==dig
    sha=hashlib.sha256(buf).hexdigest();pref=pkg.replace('/','-').replace('@','')+'-'+v;path=RAW/(pref+'-'+sha[:12]+'.tgz')
    if not path.exists():path.write_bytes(buf)
    manifest=[];anchors=[]
    with tarfile.open(fileobj=io.BytesIO(buf),mode='r:gz') as t:
        p=json.loads(t.extractfile('package/package.json').read());assert p['name']==pkg and p['version']==v
        meta={k:p[k] for k in ['name','version','main','exports','peerDependencies','peerDependenciesMeta','dependencies','engines'] if k in p}
        (RAW/(pref+'.manifest.json')).write_text(json.dumps(meta,indent=2),'utf8')
        if pkg=='@testing-library/react':
            for member in ['package/dist/pure.js','package/dist/act-compat.js']:
                code=t.extractfile(member).read();local=pref+'-'+member.split('/')[-1]+'.txt';(RAW/local).write_bytes(code)
                for i,l in enumerate(code.decode().splitlines(),1):
                    if re.search(r'react-dom/client|createRoot\(|ReactDOM\.render|ReactDOM\.unmountComponentAtNode|typeof .*\.act|DeprecatedReactTestUtils\.act|ReactTestUtils\.act|Supports.*React|unmount\(\)',l):
                        anchors.append(dict(file='raw/'+local,line=i,code=l.strip()[:230]))
        if pkg=='react-dom':
            for name in ['package/index.js','package/client.js']:
                if name in t.getnames():
                    code=t.extractfile(name).read();local=pref+'-'+name.split('/')[-1]+'.txt';(RAW/local).write_bytes(code)
    print(pkg,v,sha[:12],flush=True)
    return dict(name=pkg,version=v,url=u,tarball=dist['tarball'],integrity=dist['integrity'],tgz_sha256=sha,git_head=m.get('gitHead'),tarfile=path.relative_to(B).as_posix(),manifest='raw/'+pref+'.manifest.json',source_anchors=anchors,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if __name__=='__main__':
    with ThreadPoolExecutor(5) as pool:result=list(pool.map(fetch,packages))
    (B/'sources.json').write_text(json.dumps(result,indent=2),'utf8')
