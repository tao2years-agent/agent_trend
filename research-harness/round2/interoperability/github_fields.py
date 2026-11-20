from pathlib import Path
import json
R=Path(__file__).resolve().parent;B=R.parent.parent
s=next(s for s in json.loads((R/'sources.json').read_text(encoding='utf-8')) if s['id'].startswith('GH/descriptions/'));d=json.loads((B/s['path']).read_bytes())
routes=[('post','/repos/{owner}/{repo}/check-runs'),('post','/repos/{owner}/{repo}/deployments'),('post','/repos/{owner}/{repo}/deployments/{deployment_id}/statuses'),('get','/repos/{owner}/{repo}/actions/runs/{run_id}/approvals'),('post','/repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments'),('get','/repos/{owner}/{repo}/actions/runs/{run_id}')]
components=['environment-approvals','deployment','deployment-status','check-run','workflow-run']
keep=['required','properties','oneOf','anyOf','type','enum','items']
def head(s):
 return {'required':s.get('required',[]),'properties':{name:{k:v[k] for k in ['type','$ref','enum','default'] if k in v} for name,v in s.get('properties',{}).items()}}
spec=dict(source=s['id'],source_sha256=s['sha256'],api_version='2026-03-10',openapi=d['openapi'],description_version=d['info']['version'],selected={})
for method,path in routes:
 op=d['paths'][path][method];req=op.get('requestBody',{}).get('content',{}).get('application/json',{}).get('schema',{})
 spec['selected'][op['operationId']]={'path':path,'method':method,'request_summary':head(req),'has_alternative_or_combined_constraints':any(k in req for k in ('anyOf','oneOf','allOf')),'successes':{k:v.get('content',{}).get('application/json',{}).get('schema',{}) for k,v in op['responses'].items() if k.startswith('2')}}
spec['response_components']={k:head(d['components']['schemas'][k]) for k in components}
(R/'github-fields.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
