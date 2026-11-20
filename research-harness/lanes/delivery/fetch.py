"""Ingest official release feeds and commit-pinned source files. Existing snapshots immutable."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from html import unescape
from xml.etree import ElementTree as ET
import re, json, requests, time, sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
NS={'a':'http://www.w3.org/2005/Atom'}
repos={
'runner':('actions/runner','main',['src/Runner.Worker/JobExtension.cs','docs/adrs/1751-runner-job-hooks.md']),
'buildkite':('buildkite/agent','main',['agent/job_runner.go','README.md']),
'tekton':('tektoncd/pipeline','main',['pkg/reconciler/pipelinerun/pipelinerun.go','docs/pipelineruns.md']),
'argocd':('argoproj/argo-cd','master',['controller/state.go','docs/user-guide/auto_sync.md']),
'rollouts':('argoproj/argo-rollouts','master',['analysis/analysis.go','docs/features/analysis.md']),
'renovate':('renovatebot/renovate','main',['lib/workers/repository/update/branch/automerge.ts','docs/usage/key-concepts/automerge.md']),
'pragent':('The-PR-Agent/pr-agent','main',['pr_agent/commands/pr_reviewer.py','pr_agent/config_security.py']),
'atlantis':('runatlantis/atlantis','main',['server/events/project_command_runner.go','README.md']),
'conftest':('open-policy-agent/conftest','master',['runner/test.go','docs/index.md']),
'temporal':('temporalio/sdk-python','main',['temporalio/worker/_workflow_instance.py','README.md']),
'jenkins':('jenkinsci/pipeline-input-step-plugin','master',['src/main/java/org/jenkinsci/plugins/workflow/support/steps/input/InputStepExecution.java','README.md'])}
def get(url):
 for tries in range(4):
  try:
   r=requests.get(url,timeout=25); r.raise_for_status(); return r
  except requests.RequestException as err:
   if tries==3 or getattr(getattr(err,'response',None),'status_code',None)==404: raise
   time.sleep(1+tries)
def save(id,url,r,dt='',name=''):
 digest=sha256(r.content).hexdigest(); name=name or url.rsplit('/',1)[-1]
 p=ROOT/'raw'/id/(digest[:12]+'-'+name); p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists(): p.write_bytes(r.content)
 return dict(url=url,path=p.relative_to(BASE).as_posix(),date=dt,sha256=digest,retrieved=datetime.now(timezone.utc).isoformat(),resolved_url=r.url,bytes=len(r.content))
def entries(r): return ET.fromstring(r.content).findall('a:entry',NS)
def val(e,k): return e.findtext('a:'+k,'',NS)
def run(pair):
 id,(repo,branch,files)=pair
 base='https://github.com/'+repo
 try:
  cr=get(base+'/commits/'+branch+'.atom'); es=entries(cr); head=next(e for e in es if val(e,'updated')<='2026-11-20T16:00:00Z'); sha=val(head,'id').split('/')[-1]; cd=val(head,'updated')[:10]; assert re.match('^[0-9a-f]{40}$',sha),sha
  src=[save(id,cr.url,cr,cd,'commits.atom')]; releases=[]
  try:
   rr=get(base+'/releases.atom'); rel=save(id,rr.url,rr,'','releases.atom');src.append(rel)
   for e in entries(rr):
    releases.append(dict(tag=val(e,'title'),url=e.find('a:link',NS).get('href'),updated=val(e,'updated'),body=re.sub(r'\n{2,}','\n',unescape(re.sub('<[^>]*>',' ',val(e,'content'))).strip())))
  except Exception as ex: print(id,'FEED',str(ex)[:200])
  for path in files:
   try:
    raw='https://raw.githubusercontent.com/'+repo+'/'+sha+'/'+path; r=get(raw); s=save(id,raw,r,cd); s['repo_path']=path;src.append(s)
   except Exception as ex: print(id,'SOURCE',path,str(ex)[:140])
  res=dict(id=id,repo=repo,sha=sha,date=cd,sources=src,releases=releases)
  (ROOT/(id+'.index.json')).write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
  print(id,sha[:10],cd,len(src),[(e['tag'],e['updated'][:10]) for e in releases[:2]],flush=True)
 except Exception as ex: print(id,'FAIL',repr(ex)[:200],flush=True)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=9) as ex: list(ex.map(run,[(k,v) for k,v in repos.items() if len(sys.argv)==1 or k in sys.argv[1:]]))

