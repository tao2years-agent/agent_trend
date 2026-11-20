from pathlib import Path
import os,requests,hashlib,json,concurrent.futures as cf,subprocess,datetime
from xml.etree import ElementTree as ET
HERE=Path(__file__).resolve().parent; root=HERE.parents[1]; temp=Path(os.environ['TEMP'])/'eng-research-20261120'
repo={'symphony':'openai/symphony','ghaw':'github/gh-aw','sandbox':'opensandbox-group/OpenSandbox'}
files={'symphony':['SPEC.md','elixir/lib/symphony_elixir/orchestrator.ex','elixir/WORKFLOW.md'],'ghaw':['actions/setup/js/process_safe_outputs.cjs','docs/adr/68724-infer-read-permissions-for-staged-safe-output-handlers.md','.changeset/patch-skip-write-permissions-staged-safe-outputs.md'],'sandbox':['README.md','server/opensandbox_server/integrations/idle_pause/decision.py','docs/guides/auto-pause-wake.md']}
pages={'tessl':[('https://docs.tessl.io/improving-your-skills/evaluate-skill-quality-using-scenarios',''),('https://docs.tessl.io/changelog-web',''),('https://tessl.io/blog/introducing-task-evals-measure-whether-your-skills-actually-work','2026-02-17')],'routines':[('https://code.claude.com/docs/en/routines.md',''),('https://claude.com/resources/articles/introducing-routines-in-claude-code','2026-04-14')],'ghaw':[('https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/','2026-10-28'),('https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/','2026-02-13')]}
def git(k,*a):return subprocess.check_output(['git','-C',str(temp/k),*a]).decode().strip()
def get(url):
 for i in range(4):
  try:
   with requests.Session() as s:
    s.trust_env=bool(i%2)
    resp=s.get(url,timeout=18);resp.raise_for_status();return resp.content
  except Exception:
   if i==3:raise
def save(k,url,download,b,name,day,kind):
 h=hashlib.sha256(b).hexdigest()
 p=HERE/'raw'/k/h[:16]/name
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
 return k,dict(url=url,download_url=download,path=p.relative_to(root).as_posix(),date=day,sha256=h,kind=kind,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
def source(k,n):
 sha=git(k,'rev-parse','HEAD'); date=git(k,'log','-1','--format=%cI')[:10]
 u=f'https://raw.githubusercontent.com/{repo[k]}/{sha}/{n}';b=get(u)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==git(k,'rev-parse',sha+':'+n)
 return save(k,f'https://github.com/{repo[k]}/blob/{sha}/{n}',u,b,Path(n).name,date,'source' if n.endswith(('.py','.ex','.cjs')) else 'documentation')
def page(k,u,d):return save(k,u,u,get(u),'page.md' if u.endswith('.md') else 'page.html',d,'documentation')
def atom(k):
 b=(temp/(k+'.atom')).read_bytes()
 e=ET.fromstring(b).findall('{*}entry')[0]
 return save(k,e.find('{*}link').attrib['href'],f'https://github.com/{repo[k]}/releases.atom',b,'releases.atom',e.findtext('{*}updated')[:10],'release')
if __name__=='__main__':
 meta={}
 with cf.ThreadPoolExecutor(8) as ex:
  futures=[ex.submit(source,k,n) for k,ls in files.items() for n in ls]+[ex.submit(page,k,u,d) for k,ls in pages.items() for u,d in ls]+[ex.submit(atom,k) for k in ('symphony','sandbox')]
  for f in futures:
   try:
    k,d=f.result(); meta.setdefault(k,[]).append(d);print(k,d['url'],flush=True)
   except Exception as err:print(err,flush=True)
 (HERE/'sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),'utf8')
