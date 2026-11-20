import subprocess,tempfile,concurrent.futures,json,hashlib,datetime,re,shutil
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent.parent;(R/'diffs').mkdir(exist_ok=True)
pairs=[
 ('atlantis','runatlantis/atlantis','v0.44.0','v0.44.1','server/events/apply_command_runner.go'),
 ('pr-agent','The-PR-Agent/pr-agent','v0.46.0','v0.47.0','pr_agent/servers/github_action_runner.py'),
 ('argo','argoproj/argo-rollouts','v1.10.0','v1.10.1','pkg/kubectl-argo-rollouts/cmd/dashboard/dashboard.go'),
 ('src-cli','sourcegraph/src-cli','8.0.0','8.2.0','cmd/src/batch_exec.go')]
def run(item):
 name,repo,old,new,path=item
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
  repo_dir=Path(tmp)
  def git(*args,check=True):
   for i in range(7):
    p=subprocess.run(['git','-c','http.proxy=','-c','http.version=HTTP/1.1','-C',tmp,*args],capture_output=True,timeout=140)
    if p.returncode==0 or not any(v in p.stderr.lower() for v in [b'tls',b'connection',b'could not fetch',b'timed out',b'ssl']):break
   if check and p.returncode:raise ValueError(item,p.stderr.decode(errors='replace')[-550:])
   return p
  git('init','--bare');git('remote','add','origin','https://github.com/'+repo+'.git');git('config','remote.origin.promisor','true');git('config','remote.origin.partialclonefilter','blob:none')
  for attempt in range(3):
   p=git('fetch','--filter=blob:none','--depth=1','--no-tags','origin','refs/tags/'+old+':refs/tags/'+old,'refs/tags/'+new+':refs/tags/'+new,check=False)
   if not p.returncode:break
  assert p.returncode==0,(repo,p.stderr[-500:])
  diff=git('diff','--no-ext-diff','--no-renames',old,new,'--',path).stdout
  assert len(diff)>120,(repo,path)
  ds=[];st=[]
  for t in [old,new]:
   commit=git('rev-parse',t+'^{commit}').stdout.decode().strip();q=git('show',t+':'+path,check=False)
   if q.returncode:
    assert name=='src-cli' and t==new and not git('ls-tree','-r',t,'--',path).stdout
    st.append(dict(tag=t,commit=commit,present=False));continue
   h=hashlib.sha256(q.stdout).hexdigest();f=R/'raw'/(name+'-'+t+'-'+h[:12]+Path(path).suffix);f.write_bytes(q.stdout);rec=dict(id=name+'-'+t,url='https://github.com/'+repo+'/blob/'+commit+'/'+path,path=f.relative_to(B).as_posix(),sha256=h,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat());ds.append(rec);st.append(dict(tag=t,commit=commit,present=True,source=rec['id']))
  dp=R/'diffs'/(name+'-'+old+'--'+new+'.diff');dp.write_bytes(diff)
  print(name,len(diff),[s['commit'][:9] for s in st],flush=True)
  result=dict(product=name,repo=repo,path=path,before_after=st,diff_path=dp.relative_to(B).as_posix(),diff_sha256=hashlib.sha256(diff).hexdigest(),url='https://github.com/'+repo+'/compare/'+old+'...'+new),ds
  (R/'diffs'/(name+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
  return result
if __name__=='__main__':
 dx=[];ss=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  for row,src in ex.map(run,pairs):dx.append(row);ss.extend(src)
 for n,x in [('tag-diffs',dx),('tag-sources',ss)]:(R/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
