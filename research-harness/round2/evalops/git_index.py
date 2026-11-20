import subprocess,concurrent.futures,tempfile,json
from pathlib import Path
R=Path(__file__).resolve().parent
repos={'T':'promptfoo/promptfoo','L':'langchain-ai/langsmith-sdk','F':'langfuse/langfuse','O':'comet-ml/opik','P':'Arize-ai/phoenix','B':'braintrustdata/eval-action'}
def go(item):
 k,repo=item
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
  def g(*cmd):
   import time
   for i in range(4):
    p=subprocess.run(['git','-c','http.proxy=','-c','http.version=HTTP/1.1','-C',t,*cmd],capture_output=True,timeout=120)
    if not p.returncode:return p.stdout
    time.sleep(i+1)
   raise RuntimeError(k,p.stderr[-350:])
  g('init','--bare');g('fetch','--filter=blob:none','--depth=1','--no-tags','https://github.com/'+repo+'.git','HEAD');sha=g('rev-parse','FETCH_HEAD').decode().strip();files=g('ls-tree','-r','--name-only',sha).decode().splitlines()
  (R/(k+'-tree.json')).write_text(json.dumps(dict(repo=repo,sha=sha,files=files)),encoding='utf-8')
  print(k,sha,len(files),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:
  result=[e.submit(go,i) for i in repos.items()]
  for f in concurrent.futures.as_completed(result):
   try:f.result()
   except Exception as err:print(str(err)[:250],flush=True)
