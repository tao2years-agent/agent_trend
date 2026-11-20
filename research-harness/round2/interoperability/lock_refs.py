from pathlib import Path
import subprocess,tempfile,concurrent.futures,re,json,time
R=Path(__file__).resolve().parent
choices={'CE':('cloudevents/spec','v1.0.2'),'CD':('cdevents/spec','v0.5.0'),'OT':('open-telemetry/semantic-conventions','latest'),'AI':('open-telemetry/semantic-conventions-genai','latest'),'IT':('in-toto/attestation','latest'),'GH':('github/rest-api-description','HEAD')}
def capture(x):
 k,(repo,ref)=x;u='https://github.com/'+repo+'.git'
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
  def git(*args):
   for i in range(4):
    q=subprocess.run(['git','-C',t,'-c','http.proxy=','-c','http.version=HTTP/1.1',*args],capture_output=True,timeout=100)
    if q.returncode==0:return q.stdout
    time.sleep(.4+i)
   raise ValueError(k,q.stderr[-180:])
  git('init','--bare')
  tags=[]
  if ref=='latest':
   remote=git('ls-remote','--tags','--refs',u).decode();tags=[t.split('/tags/')[-1] for t in remote.splitlines() if re.fullmatch(r'v?\d+\.\d+\.\d+',t.split('/tags/')[-1])]
   tags.sort(key=lambda t:tuple(int(v) for v in t.lstrip('v').split('.')),reverse=True);ref=tags[0] if tags else 'HEAD'
  git('fetch','--depth=1','--no-tags','--filter=blob:none',u,'HEAD' if ref=='HEAD' else 'refs/tags/'+ref);sha=git('rev-parse','FETCH_HEAD^{commit}').decode().strip();date=git('show','-s','--format=%cI',sha).decode().strip();paths=git('ls-tree','-r','--name-only',sha).decode().splitlines();print(k,ref,sha[:10],date,len(paths),flush=True)
  (R/(k+'-index.json')).write_text(json.dumps(dict(repo=repo,ref=ref,sha=sha,commit_date=date,latest_stable_tags=tags[:5],paths=paths)),encoding='utf-8')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for _ in ex.map(capture,choices.items()):pass
