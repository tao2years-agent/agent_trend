"""Capture published source-tree listings and named artifacts using read-only git object operations."""
from pathlib import Path
import tempfile,subprocess,json,hashlib,datetime
R=Path(__file__).resolve().parent
cache=Path(tempfile.gettempdir())/'dongcha-release-lit';cache.mkdir(exist_ok=True)
def call(*args,working=None):
    p=subprocess.run(['git',*args],cwd=working,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    if p.returncode:raise RuntimeError(p.stderr.decode('utf8','replace')[-400:]); 
    return p.stdout
records=[]
for repo in ['shiwen-song/GUIRevive','EvanXiaa/BDUpdater']:
    d=cache/repo.split('/')[1];url='https://github.com/'+repo+'.git'
    if not (d/'HEAD').exists():call('clone','--bare','--filter=blob:none','--single-branch','--depth','10',url,str(d))
    rev=call('rev-list','-1','--before=2026-11-20T04:50:00Z','HEAD',working=d).decode().strip()
    assert len(rev)==40
    date=call('show','-s','--format=%cI',rev,working=d).decode().strip()
    assert datetime.datetime.fromisoformat(date)<datetime.datetime.fromisoformat('2026-11-20T04:50:00+00:00')
    tree=call('ls-tree','-r',rev,working=d)
    path=R/'raw'/(repo.split('/')[1]+'-'+rev[:12]+'-tree.txt')
    if not path.exists():path.write_bytes(tree)
    records.append(dict(repo=repo,rev=rev,date=date,url='https://github.com/'+repo+'/tree/'+rev,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(tree).hexdigest()))
    print(repo,rev,len(tree.splitlines()),[b.decode(errors='replace').split('\t')[-1] for b in tree.splitlines() if any(x in b.lower() for x in [b'result',b'.csv',b'.xlsx'])][:30])
(R/'git-trees.json').write_text(json.dumps(records,indent=2),'utf8')

