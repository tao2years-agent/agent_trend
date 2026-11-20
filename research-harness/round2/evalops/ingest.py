import hashlib,json,time,requests,concurrent.futures,datetime,threading
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent;B=R.parent.parent
files={
 'B':['LICENSE','action.yml','eval/src/braintrust.ts'],
 'L':['LICENSE','python/langsmith/anonymizer.py','python/langsmith/evaluation/_runner.py'],
 'T':['LICENSE','src/assertions/equals.ts','src/commands/eval.ts','package.json','src/assertions/normalize.ts','src/node/doEval.ts'],
 'F':['LICENSE','web/src/features/prompts/server/utils/updatePromptLabels.ts','web/src/features/annotation-queues/server/annotationQueuesRouter.ts'],
 'O':['LICENSE','sdks/python/src/opik/api_objects/dataset/test_suite/test_suite_result.py','sdks/python/src/opik/evaluation/metrics/heuristics/equals.py'],
 'P':['LICENSE','src/phoenix/server/api/mutations/dataset_split_mutations.py','src/phoenix/server/api/mutations/prompt_version_tag_mutations.py']}
targets=[]
for l in (R/'seed.txt').read_text(encoding='utf-8-sig').splitlines():
 k,v,u=l.split('|');targets.append((k+'-'+v,u,'doc',''))
for k,ps in files.items():
 m=json.loads((R/(k+'-tree.json')).read_text())
 for i,p in enumerate(ps):
  assert p in m['files'];targets.append((k+'-code'+str(i),'https://raw.githubusercontent.com/'+m['repo']+'/'+m['sha']+'/'+p,'code',p))
def fetch(item):
 key,u,fmt,loc=item
 if (R/'sources.json').exists():
  for s in json.loads((R/'sources.json').read_text(encoding='utf-8')):
   if s['id']==key and hashlib.sha256((B/s['path']).read_bytes()).hexdigest()==s['sha256']:return s
 for i in range(5):
  try:
   ss=requests.Session();ss.trust_env=False;resp=ss.get(u,timeout=(6,16));resp.raise_for_status()
   raw=resp.content;a=resp.text
   if len(raw)<40:raise ValueError('tiny')
   p=BeautifulSoup(raw,'html.parser') if fmt=='doc' and ('html' in resp.headers.get('content-type','') or '<html' in a[:1000]) else None
   if p and p.title and ('404' in p.title.get_text() or 'page not found' in p.title.get_text().lower()):raise ValueError('soft 404')
   break
  except Exception as e:
   if i==4 or ('404' in str(e)):return dict(id=key,error=str(e)[:150],url=u)
   time.sleep(.4+i*.3)
 dig=hashlib.sha256(raw).hexdigest();pname=R/'raw'/(key+'-'+dig[:12]+(Path(loc).suffix if fmt=='code' else ('.html' if p else '.md')));pname.write_bytes(raw) if not pname.exists() else None
 return dict(id=key,url=u,resolved_url=resp.url,path=pname.relative_to(B).as_posix(),sha256=dig,locator=loc,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=13) as ex:
  vals=list(ex.map(fetch,targets))
 ok=[v for v in vals if 'error' not in v];bad=[v for v in vals if 'error' in v]
 (R/'sources.json').write_text(json.dumps(ok,ensure_ascii=False,indent=2),encoding='utf-8');(R/'unresolved.json').write_text(json.dumps(bad,ensure_ascii=False,indent=2),encoding='utf-8');print(len(ok),[(v['id'],v['error'][:50]) for v in bad])
