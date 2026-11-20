"""Local experiment. Only mlflow.genai writes versions, tags or aliases. Other SQLite access is read-only."""
from pathlib import Path
import hashlib,json,os,sys,socket,tempfile,time,sqlite3,multiprocessing as mp
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
NAME='ordinary-notice'
TEMPLATES=['Agenda: {{topic}}.','Next meeting: {{topic}}.','Reminder: {{topic}}.']
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def worker(pipe,db):
    env={'MLFLOW_DISABLE_TELEMETRY':'true','DO_NOT_TRACK':'1','MLFLOW_TRACKING_URI':'sqlite:///'+db.as_posix(),'MLFLOW_REGISTRY_URI':'sqlite:///'+db.as_posix(),'MLFLOW_USER':'fixture','USERNAME':'fixture','USER':'fixture','LOGNAME':'fixture'}
    os.environ.update(env)
    os.chdir(db.parent)
    for k in ['MLFLOW_ALIAS_PROMPT_CACHE_TTL_SECONDS','MLFLOW_VERSION_PROMPT_CACHE_TTL_SECONDS','MLFLOW_WORKSPACE','DATABRICKS_TOKEN','DATABRICKS_HOST']:
        os.environ.pop(k,None)
    blocked=[]
    def no_connect(event,args):
        if event=='socket.connect':
            blocked.append(event);raise RuntimeError('socket connection disabled in registry experiment')
    sys.addaudithook(no_connect)
    try:
        import mlflow
        from mlflow import genai
        from mlflow.environment_variables import MLFLOW_ALIAS_PROMPT_CACHE_TTL_SECONDS
        mlflow.set_tracking_uri(env['MLFLOW_TRACKING_URI']);mlflow.set_registry_uri(env['MLFLOW_REGISTRY_URI'])
        pipe.send({'ready':True,'mlflow':mlflow.__version__,'alias_default_ttl_s':MLFLOW_ALIAS_PROMPT_CACHE_TTL_SECONDS.get()})
    except Exception as e:
        pipe.send({'ready':False,'type':type(e).__name__,'message':str(e)});return
    held={}
    def summarize(p):
        val={'name':p.name,'version':p.version,'template':p.template,'model_config':p.model_config}
        return {**val,'template_sha256':digest(p.template),'release_content_sha256':digest(val),'rendered':p.format(topic='Friday planning')}
    while True:
        q=pipe.recv();op=q['op']
        try:
            if op=='close':pipe.send({'ok':True,'socket_connect_denied':len(blocked)});break
            if op=='register':
                p=genai.register_prompt(name=NAME,template=q['text'],commit_message='Synthetic notice',model_config={'model_name':'synthetic-local','temperature':0.1});out=summarize(p)
            elif op=='set_alias':genai.set_prompt_alias(NAME,q['alias'],q['version']);out=None
            elif op=='config':genai.set_prompt_model_config(NAME,q['version'],{'model_name':'synthetic-local','temperature':q['temperature']});out=None
            elif op=='held':out=summarize(held[q['handle']])
            elif op=='load':
                ref=q['ref'];kwargs={'cache_ttl_seconds':q['ttl']} if 'ttl' in q else {}
                p=genai.load_prompt('prompts:/'+NAME+('/'+str(ref) if isinstance(ref,int) else '@'+ref),link_to_model=False,**kwargs)
                if 'hold' in q:held[q['hold']]=p
                out=summarize(p)
            else:raise ValueError(op)
            pipe.send({'ok':True,'value':out})
        except Exception as e:
            pipe.send({'ok':False,'type':type(e).__name__,'message':str(e)[:700],'error_code':getattr(e,'error_code',None)})
class Client:
    def __init__(self,ctx,db,role):
        self.role=role;self.pipe,child=ctx.Pipe()
        self.proc=ctx.Process(target=worker,args=(child,db));self.proc.start();child.close()
        assert self.pipe.poll(130),'worker startup timeout'
        self.ready=self.pipe.recv();assert self.ready['ready'],self.ready
    def call(self,q):
        self.pipe.send(q);assert self.pipe.poll(100),'command timeout'
        return self.pipe.recv()
    def stop(self):
        r=self.call({'op':'close'});self.proc.join(20)
        return {'closed':r,'process_exit':self.proc.exitcode}
def main():
    temp=Path(tempfile.mkdtemp(prefix='mlflow-prompt-registry-'));db=temp/'registry.sqlite'
    ctx=mp.get_context('spawn');writer=Client(ctx,db,'writer');reader=Client(ctx,db,'reader')
    events=[];fixture_rows=[];stops=[];marks={};people=[writer,reader];sqlite_shots=[]
    info={'method':'official mlflow.genai Python API, local SQLite registry, no network connections allowed in SDK worker','name':NAME,'metadata':writer.ready,'fixture_clock':100,'observed_utc':datetime.now(timezone.utc).isoformat()}
    def cmd(role,label,op,expected=None,expect_error=False,**args):
        response=role.call({'op':op,**args})
        ev={'step':len(events)+1,'label':label,'role':role.role,'op':op,'args':args,'response':response,'monotonic_s':round(time.monotonic()-start,3)};events.append(ev)
        if expect_error:assert not response['ok'],ev;return response
        assert response['ok'],ev;value=response['value']
        if expected is not None:assert value['version']==expected,ev
        return value
    def pin(ref,label,expected,client=None,extra=None):
        return cmd(client or writer,label,'load',expected=expected,ref=ref,**({'ttl':0} if extra is None else extra))
    def alias(label,key,version):
        cmd(writer,label,'set_alias',alias=key,version=version)
    def snap(label):
        con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
        table_info=con.execute('pragma table_info(registered_model_aliases)').fetchall()
        cols=[x[1] for x in table_info];primary_key=[x[1] for x in sorted((r for r in table_info if r[5]),key=lambda r:r[5])]
        detail=con.execute("select version,key,value from model_version_tags where name=? and key in ('mlflow.prompt.text','_mlflow_prompt_model_config') order by version,key",(NAME,)).fetchall()
        versions_detail={}
        for v,k,val in detail:
            versions_detail.setdefault(str(v),{})[k]=json.loads(val) if k=='_mlflow_prompt_model_config' else val
        rows=con.execute('select alias,version from registered_model_aliases where name=? order by alias',(NAME,)).fetchall()
        versions=con.execute('select version from model_versions where name=? order by version',(NAME,)).fetchall()
        sqlite_shots.append({'label':label,'aliases':dict(rows),'versions':[v[0] for v in versions],'alias_table_columns':cols,'alias_primary_key':primary_key,'selected_version_fields':versions_detail});con.close()
    def grant(v,base,expires=200):
        return {'serial':'grant-'+str(len(fixture_rows)),'approved':v['version'],'release_digest':v['release_content_sha256'],'expected_live':base,'expires_at_fixture_tick':expires}
    def guarded(label,receipt,desired,base,spent=None):
        reasons=[]
        if receipt['expires_at_fixture_tick']<=100:reasons.append('expired')
        if receipt['approved']!=desired['version']:reasons.append('candidate_version_drift')
        if receipt['release_digest']!=desired['release_content_sha256']:reasons.append('release_content_drift')
        if receipt['expected_live']!=base['version']:reasons.append('production_predecessor_drift')
        if spent is not None and receipt['serial'] in spent:reasons.append('already_spent')
        fixture_rows.append({'label':label,'receipt':receipt,'candidate_seen':desired['version'],'production_seen':base['version'],'reasons':reasons,'passes_fixture_checks':not reasons})
        return not reasons
    start=time.monotonic()
    try:
        for i,t in enumerate(TEMPLATES,1):cmd(writer,'register-v'+str(i),'register',expected=i,text=t)
        alias('initialize-production','production',1);alias('initialize-candidate','candidate',2);snap('initialized')
        baseline=pin('production','baseline-live',1);cand=pin('candidate','approved-candidate',2);receipt=grant(cand,1)
        alias('candidate-alias-retargeted','candidate',3)
        changed=pin('candidate','candidate-now-v3',3)
        assert not guarded('alias_drift_blocked_by_fixture',receipt,changed,baseline)
        alias('alias-only-workflow-promotes-unapproved-v3','production',changed['version']);pin('production','audit-wrong-version',3);snap('alias-drift')
        alias('rollback-to-v1','production',1);pin('production','rollback-visible-uncached',1);pin(3,'old-v3-still-addressable',3)
        expired=grant(cand,1,expires=99)
        assert not guarded('expired_receipt_blocked_by_fixture',expired,cand,baseline)
        alias('native-set-permitted-without-naming-receipt','production',2);pin('production','after-expired-receipt-fixture',2);snap('native-no-grant-argument')
        alias('reset-for-cache','production',1)
        cached=pin('production','reader-primes-default-and-holds',1,reader,{'hold':'inflight'})
        marks['cache_primed_at']=time.monotonic()
        alias('writer-promotes-to-v2','production',2)
        pin('production','writer-cache-invalidated',2,writer,{})
        warm=pin('production','reader-default-immediately-after-write',1,reader,{})
        pin('production','reader-bypass-sees-new',2,reader)
        pin('production','bypass-does-not-refresh-existing-default-entry',1,reader,{})
        cmd(reader,'already-loaded-inflight-stays-v1','held',expected=1,handle='inflight')
        snap('during-cache-test')
        fresh=Client(ctx,db,'fresh-process');people.append(fresh)
        pin('production','new-process-default',2,fresh,{})
        # Preserve the disputed version's alias and assess mutable configuration while default TTL elapses.
        correct=grant(cand,2)
        cmd(writer,'change-v2-config-without-registering-v4','config',version=2,temperature=0.8)
        drift=pin(2,'same-v2-new-config',2);assert drift['template_sha256']==cand['template_sha256'] and drift['release_content_sha256']!=cand['release_content_sha256']
        current=pin('production','production-still-v2-after-config-change',2)
        assert not guarded('version_and_template_unchanged_config_changed',correct,drift,current)
        cmd(writer,'reject-nonexistent-version','set_alias',alias='production',version=999,expect_error=True)
        pin('production','invalid-target-left-production-intact',2)
        # Reader alone has an older alias cache. Use the actual SDK default TTL plus margin, with the registry stable at v2.
        wait=max(0,marks['cache_primed_at']+writer.ready['alias_default_ttl_s']+1-time.monotonic())
        if wait:time.sleep(wait)
        pin('production','reader-default-after-real-ttl',2,reader,{})
        elapsed=time.monotonic()-marks['cache_primed_at'];info['cache_check_elapsed_seconds']=round(elapsed,3)
        cmd(reader,'inflight-object-even-after-expiry','held',expected=1,handle='inflight')
        # Two decisions observed predecessor 1; another writer promotes 3 before the old decision writes 2.
        alias('reset-before-interleaving','production',1)
        p1=pin('production','first-decider-sees-one',1,writer);p2=pin('production','second-decider-sees-one',1,fresh)
        rec_a=grant(drift,p1['version']);rec_b={**grant(changed,p2['version']),'serial':'separate-B'}
        assert guarded('decision-A-read-only-validated',rec_a,drift,p1) and guarded('decision-B-read-only-validated',rec_b,changed,p2)
        cmd(fresh,'B-writes-v3','set_alias',alias='production',version=3)
        other=pin('production','A-sees-newer-B-on-explicit-recheck',3,writer)
        assert not guarded('fresh-expected-live-rejects-stale-A',rec_a,drift,other)
        alias('stale-A-native-write-overwrites-B','production',2);pin('production','last-write-is-v2',2);snap('stale-writer-overwrite')
        # Return to same predecessor. A version-only check cannot distinguish the generation; demonstrate replay guard.
        alias('rollback-return-to-v1','production',1);restored=pin('production','returned-to-original-predecessor',1)
        assert guarded('ABA-matches-version-and-digest-after-rollback',rec_a,drift,restored)
        assert not guarded('single-use-harness-rejects-ABA',rec_a,drift,restored,{rec_a['serial']})
        new_grant=grant(drift,1)
        assert guarded('valid-new-receipt',new_grant,drift,restored)
        alias('valid-explicit-v2-promote','production',new_grant['approved']);pin('production','final-approved-target',2)
        pin('production','reader-primes-and-takes-v2-before-rollback',2,fresh,{'hold':'before-rollback'})
        alias('final-rollback','production',1);pin('production','final-production',1);snap('final')
        pin('production','other-reader-default-immediately-after-rollback',2,fresh,{})
        pin('production','other-reader-no-cache-after-rollback',1,fresh)
        cmd(fresh,'inflight-v2-remains-usable-after-rollback','held',expected=2,handle='before-rollback')
    finally:
        for p in people:
            if p.proc.is_alive():stops.append({'role':p.role,**p.stop()})
        if sqlite_shots and sqlite_shots[-1]['label']=='final':
            reopened=Client(ctx,db,'after-all-workers-stopped')
            try:
                pin('production','restarted-process-uses-persisted-production',1,reopened,{})
                pin(2,'restarted-process-can-restore-v2',2,reopened)
            finally:stops.append({'role':reopened.role,**reopened.stop()})
        info['sqlite_file_sha256']=hashlib.sha256(db.read_bytes()).hexdigest()
        info.update(events=events,fixture_approvals=fixture_rows,sqlite_snapshots=sqlite_shots,worker_exit=stops)
        (B/'observations.json').write_text(json.dumps(info,indent=2,ensure_ascii=False),'utf8')
    assert all(r['closed']['socket_connect_denied']==0 and r['process_exit']==0 for r in stops),stops
    assert sqlite_shots[-1]['aliases']['production']==1
    print('verified',len(events),'public API events;',len(fixture_rows),'synthetic approval evaluations;',len(sqlite_shots),'SQLite checkpoints')
if __name__=='__main__':main()
