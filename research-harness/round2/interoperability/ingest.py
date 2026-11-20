from pathlib import Path
import requests,concurrent.futures,time,json,datetime,hashlib
R=Path(__file__).resolve().parent;B=R.parent.parent
chosen={
'CE':['cloudevents/spec.md','cloudevents/formats/cloudevents.json','cloudevents/formats/json-format.md'],
'CD':['spec.md','cloudevents-binding.md','links.md','core.md','source-code-version-control.md','continuous-deployment.md','continuous-operations.md','schemas/taskrunfinished.json','schemas/changereviewed.json','schemas/servicerolledback.json','schemas/servicedeployed.json','schemas/incidentresolved.json'],
'OT':['docs/cicd/cicd-spans.md','model/cicd/spans.yaml','docs/gen-ai/README.md'],
'AI':['docs/gen-ai/execute-tool.md','docs/gen-ai/client-invoke-agent.md','README.md','CHANGELOG.md'],
'GH':['descriptions/api.github.com/api.github.com.2026-03-10.json'],
'IT':['spec/predicates/release.md','spec/v1/statement.md','spec/v1/resource_descriptor.md','protos/in_toto_attestation/v1/statement.proto','protos/in_toto_attestation/predicates/provenance/v1/provenance.proto']}
targets=[]
for k,fs in chosen.items():
 d=json.loads((R/(k+'-index.json')).read_text(encoding='utf-8'))
 for f in fs:
  assert f in d['paths'];targets.append((k+'/'+f,'https://raw.githubusercontent.com/'+d['repo']+'/'+d['sha']+'/'+f,d['ref'],d['sha']))
for k,url in [('SL/index','https://slsa.dev/spec/v1.2/'),('SL/provenance','https://slsa.dev/spec/v1.2/build-provenance'),('SL/verification','https://slsa.dev/spec/v1.2/verifying-artifacts'),('GH/checks','https://docs.github.com/en/rest/checks/runs?apiVersion=2026-03-10'),('GH/approvals','https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2026-03-10'),('GH/status','https://docs.github.com/en/rest/deployments/statuses?apiVersion=2026-03-10'),('OT/trace','https://opentelemetry.io/docs/specs/otel/trace/api/'),('OT/rc','https://opentelemetry.io/docs/specs/semconv/cicd/cicd-spans/'),('CD/web','https://cdevents.dev/docs/')]:targets.append((k,url,'web',''))
def fetch(item):
 k,url,ver,rev=item
 man=R/'sources.json'
 if man.exists():
  old=next((a for a in json.loads(man.read_text(encoding='utf-8')) if a['url']==url),None)
  if old and hashlib.sha256((B/old['path']).read_bytes()).hexdigest()==old['sha256']:return old
 for i in range(7):
  try:
   s=requests.Session();s.trust_env=False;r=s.get(url,timeout=(7,70));r.raise_for_status();break
  except Exception as er:
   if i==6 or '404' in str(er):return {'id':k,'error':str(er)[:150]}
   time.sleep(1+i)
 raw=r.content;h=hashlib.sha256(raw).hexdigest();name=k.split('/')[0]+'-'+Path(k.split('/')[-1]).stem+'-'+h[:12]+(Path(k.split('/')[-1]).suffix if rev else '.html');dest=R/'raw'/name
 if not dest.exists():dest.write_bytes(raw)
 return dict(id=k,url=url,version=ver,commit=rev,path=dest.relative_to(B).as_posix(),sha256=h,bytes=len(raw),retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as x:rows=list(x.map(fetch,targets))
 ok=[r for r in rows if 'error' not in r];(R/'sources.json').write_text(json.dumps(ok,indent=2),encoding='utf-8');print(len(ok),[r for r in rows if 'error' in r])
