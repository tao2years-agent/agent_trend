"""Projection and JSON Schema exercises. Reads published files, no network, no vendor writes."""
from pathlib import Path
import json,hashlib,copy,platform,importlib.metadata
from jsonschema import Draft7Validator,Draft202012Validator,FormatChecker
R=Path(__file__).resolve().parent;B=R.parent.parent
manifest=json.loads((R/'sources.json').read_text(encoding='utf-8'));sources={s['id']:s for s in manifest}
for s in sources.values():assert hashlib.sha256((B/s['path']).read_bytes()).hexdigest()==s['sha256']
def data(k):return json.loads((B/sources[k]['path']).read_bytes())
ce=Draft7Validator(data('CE/cloudevents/formats/cloudevents.json'),format_checker=FormatChecker())
def schema(k):return Draft202012Validator(data('CD/schemas/'+k+'.json'),format_checker=FormatChecker())
def result(schema_id,validator,obj,expect,label):
 errors=[dict(path=list(e.absolute_path),error=e.validator) for e in validator.iter_errors(obj)]
 assert (not errors)==expect,(label,errors);checks.append(dict(label=label,schema=schema_id,valid=not errors,errors=errors))
def make(k,event_id,subject,stamp,content):
 spec=data('CD/schemas/'+k+'.json');t=spec['properties']['context']['properties']['type']['enum'][0]
 return dict(context=dict(specversion='0.5.0',id=event_id,source='urn:example:handoff-projection',type=t,timestamp=stamp),subject=dict(id=subject,content=content))
def wrap(body):
 c=body['context']
 return dict(specversion='1.0',id=c['id'],source=c['source'],type=c['type'],time=c['timestamp'],subject=body['subject']['id'],datacontenttype='application/json',data=body)
def without(obj,*keys):
 x=copy.deepcopy(obj);cursor=x
 for k in keys[:-1]:cursor=cursor[k]
 del cursor[keys[-1]];return x
checks=[];examples={};originals=[]
for group,rel in [('A','evidence/observations.json'),('B','evidence/repeat/observations.json')]:
 p=R.parent/'handoff'/rel;real=json.loads(p.read_bytes());outputs=[]
 for pos,run in enumerate(real['runs']):
  if (run['engine'],run['scenario'])!=('temporal','lost'):continue
  fork='guarded' if run['guarded'] else 'base';label=group+'-'+fork
  assert run['status']=='published' and len(run['invocations'])==2
  stamp=real['finished_utc']
  body=make('taskrunfinished','projection-'+label,'/local/task/'+label,stamp,{'taskName':'publish','outcome':'success'})
  envelope=wrap(body);result('CDEvents taskrunfinished',schema('taskrunfinished'),body,True,label+'-native');result('CloudEvents',ce,envelope,True,label+'-envelope')
  rich=copy.deepcopy(body);rich['customDataContentType']='application/json';rich['customData']={'fixture_record':rel+'#/runs/'+str(pos),'observed_invocations':[i['verdict'] for i in run['invocations']],'target_rows':len(run['effects']),'observed_target_versions':run['effects']}
  result('CDEvents taskrunfinished',schema('taskrunfinished'),rich,True,label+'-with-evidence')
  result('CloudEvents',ce,wrap(rich),True,label+'-envelope-with-evidence')
  examples[label]={'basic':envelope,'with_referenced_observation':wrap(rich)};outputs.append((fork,body['subject']['content'],len(run['effects']),[m['verdict'] for m in run['invocations']]))
 assert len(outputs)==2 and outputs[0][1]==outputs[1][1]
 assert {o[0]:(o[2],o[3]) for o in outputs}=={'base':(2,['insert','insert']),'guarded':(1,['insert','reuse'])}
 originals.append(dict(group=group,path=p.relative_to(B).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),mapped=outputs))
# One document validated twice reproduces ordinary transport replay, not two writes.
dup=examples['A-guarded']['basic'];result('CloudEvents',ce,dup,True,'same-envelope-replayed');result('CloudEvents',ce,without(dup,'source'),False,'negative-missing-source')
stamp='2026-11-20T00:00:00Z'
review=make('changereviewed','review-demo','/pr/8',stamp,{'repository':{'id':'repo-a'}});result('CDEvents changereviewed',schema('changereviewed'),review,True,'review-has-no-reviewer-decision-or-target')
examples['review_without_approval']=wrap(review)
# String-shape checks cannot enforce the textual vocabulary or PURL grammar.
bad_outcome=copy.deepcopy(examples['A-base']['basic']['data']);bad_outcome['subject']['content']['outcome']='not-a-spec-outcome'
result('CDEvents taskrunfinished',schema('taskrunfinished'),bad_outcome,True,'schema-only-nonnormative-outcome');examples['schema_only_nonnormative']=bad_outcome
ops=[]
for ident in ('v1','v2'):
 body=make('servicerolledback','rollback-'+ident,'/services/demo',stamp,{'artifactId':'pkg:generic/demo@'+ident,'environment':{'id':'staging'}})
 body['context']['chainId']='same-investigation';result('CDEvents servicerolledback',schema('servicerolledback'),body,True,'same-chain-'+ident);ops.append(body)
result('CDEvents servicerolledback',schema('servicerolledback'),without(ops[0],'subject','content','environment'),False,'negative-missing-environment')
result('CDEvents servicerolledback',schema('servicerolledback'),without(ops[0],'subject','content','artifactId'),False,'negative-missing-artifact')
examples['same_chain_different_artifacts']=ops
wrong=wrap(review);wrong['id']='different-from-inner';result('CloudEvents',ce,wrong,True,'cross-envelope-mismatch-outer-alone');result('CDEvents changereviewed',schema('changereviewed'),wrong['data'],True,'cross-envelope-mismatch-inner-alone')
assert wrong['id']!=wrong['data']['context']['id'];examples['binding_mismatch_rejected_by_crosscheck_only']=wrong
meta=dict(python=platform.python_version(),jsonschema=importlib.metadata.version('jsonschema'),drafts=['CloudEvents Draft-07','CDEvents Draft 2020-12'],schema_evaluations=len(checks),conforming_documents=sum(r['valid'] for r in checks),invalid_documents=sum(not r['valid'] for r in checks),checks=checks,origin=originals)
(R/'examples.json').write_text(json.dumps(examples,indent=2),encoding='utf-8');(R/'checks.json').write_text(json.dumps(meta,indent=2),encoding='utf-8');print(len(checks),meta['conforming_documents'],meta['invalid_documents'])
