"""Run only synthetic, deterministic rows. No accounts, no model provider, no upload."""
from pathlib import Path
import csv,json,re,datetime,uuid,hashlib,sys,os,subprocess,socket,importlib.util,platform,logging
from collections import Counter
from types import SimpleNamespace
from urllib.parse import urlsplit
R=Path(__file__).resolve().parent;B=R.parent.parent
src={s['id']:s for s in json.loads((R/'sources.json').read_text(encoding='utf-8'))}
def file(k):
 s=src[k];p=B/s['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];return p
rows=[
 ('s1','dev','A:1','approved',0,1,'write','write'),('s2','dev','B:1','revoked',0,1,'hold','hold'),
 ('e1','blind','C:1','approved',0,1,'write','write'),('e2','blind','D:1','expired',0,1,'hold','hold'),
 ('e3','blind','E:1','approved',1,1,'hold','hold'),('e4','blind','F:1','approved',0,0,'hold','hold'),
 ('r3','blind','E:1','approved',1,1,'hold','hold'),('q1','pending','G:1','changed_owner',0,1,'hold','write')]
raw=[dict(id=i,group=group,event_key=key,permission=auth,existing=bool(existing),context_ok=bool(context),review_a=va,review_b=vb,reporter=i+'@example.invalid') for i,group,key,auth,existing,context,va,vb in rows]
deid=[dict(q,reporter=re.sub(r'[\w.-]+@example\.invalid','[masked]',q['reporter'])) for q in raw]
seen=set();distinct=[]
for q in deid:
 if q['event_key'] not in seen:distinct.append(q);seen.add(q['event_key'])
approved=[q for q in distinct if q['review_a']==q['review_b']]
train={q['event_key'] for q in approved if q['group']=='dev'};blind={q['event_key'] for q in approved if q['group']=='blind'}
assert train.isdisjoint(blind) and len(train)==2 and len(blind)==4
def run(q,variant):
 if variant=='before':return 'write'
 if variant=='candidate':return 'write' if q['permission']=='approved' else 'hold'
 return 'write' if q['permission']=='approved' and not q['existing'] and q['context_ok'] else 'hold'
obs=[]
for q in approved:
 for variant in ('before','candidate','control'):
  obs.append(dict(id=q['id'],group=q['group'],variant=variant,expected=q['review_a'],answer=run(q,variant)))
(R/'fixture.json').write_text(json.dumps(dict(raw=raw,redacted_deduplicated=distinct,results=obs),indent=2),encoding='utf-8')
for k in list(os.environ):
 if k.startswith('LANGCHAIN_') or k.startswith('LANGSMITH_'):os.environ.pop(k)
os.environ['LANGSMITH_TRACING']='false'
blocked=Counter()
def deny(*args,**kwargs):
 blocked['socket attempt']+=1;raise OSError('offline probe')
socket.socket.connect=deny;socket.getaddrinfo=deny
import requests,langsmith
from langsmith import evaluate
from langsmith.schemas import Example
def block_send(sess,request,**kwargs):
 target=urlsplit(request.url);blocked[request.method+' '+target.hostname+target.path]+=1;raise requests.ConnectionError('offline probe')
requests.sessions.Session.send=block_send
ds=uuid.UUID(int=3);stamp=datetime.datetime(2026,11,20,tzinfo=datetime.timezone.utc)
xs=[Example(id=uuid.uuid5(ds,str(i)),dataset_id=ds,inputs=q,outputs={'expected':q['expected']},created_at=stamp) for i,q in enumerate(obs)]
def exact(run,example):return {'key':'contract','score':int(run.outputs['answer']==example.outputs['expected'])}
result=evaluate(lambda x:{'answer':x['answer']},data=xs,evaluators=[exact],upload_results=False,max_concurrency=0)
l_sorted=sorted((it['example'].inputs['id'],it['example'].inputs['variant'],it['evaluation_results']['results'][0].score) for it in result)
args=['node','--permission','--allow-fs-read='+str(R),'--disable-warning=ExperimentalWarning',str(R/'promptfoo-probe.mjs'),str(file('T-code1')),str(file('T-code4'))]
proc=subprocess.run(args,input=json.dumps(obs),text=True,capture_output=True,check=True)
t_sorted=sorted(tuple(z) for z in json.loads(proc.stdout))
assert l_sorted==t_sorted and len(t_sorted)==18
spec=importlib.util.spec_from_file_location('opik_public_test_suite',file('O-code1'));module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def opik_pass(skip=()):
 its={}
 for q in obs:
  if q['variant']!='candidate' or q['group']!='blind':continue
  has=q['id'] not in skip;passed=module.is_score_passed(SimpleNamespace(scoring_failed=False,value=int(q['answer']==q['expected'])))
  its[q['id']]=module.ItemResult(dataset_item_id=q['id'],passed=passed,has_assertions=has,runs_passed=int(passed),runs_total=1,configured_runs_per_item=1,pass_threshold=1,test_results=[])
 return module.TestSuiteResult(evaluation_result_=None,items_passed=sum(it.passed for it in its.values()),item_results=its,items_total=len(its)).pass_rate
count={v:{g:[sum(r['answer']==r['expected'] for r in obs if r['variant']==v and r['group']==g),sum(1 for r in obs if r['variant']==v and r['group']==g)] for g in ['dev','blind']} for v in ['before','candidate','control']}
pr=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=platform.python_version(),node=subprocess.run(['node','--version'],capture_output=True,text=True).stdout.strip(),langsmith_sdk=langsmith.__version__,promptfoo_sha=json.loads((R/'T-tree.json').read_text())['sha'],opik_sha=json.loads((R/'O-tree.json').read_text())['sha'],blocked_network_requests=dict(blocked),rows_raw=len(raw),unique=len(distinct),disagreements=[q['id'] for q in distinct if q['review_a']!=q['review_b']],source_ids=['T-code1','T-code4','O-code1'],execution='LangSmith evaluate(upload_results=False), Promptfoo handleEquals through Node permission mode, Opik TestSuiteResult.pass_rate',per_case_agreement=l_sorted,per_split=count,opik_candidate_all_assertions=opik_pass(),opik_candidate_omit_both_failed_assertions=opik_pass(['e3','e4']),threshold='research fixture only: all blind rows must pass; any duplicate external write blocks',external_writes=0)
(R/'probe-results.json').write_text(json.dumps(pr,indent=2),encoding='utf-8');print(count,pr['opik_candidate_all_assertions'],pr['opik_candidate_omit_both_failed_assertions'])

