"""Replay the product's published panel SQL on real MySQL and embedded PostgreSQL, using only local inputs."""
from pathlib import Path
import csv,datetime as dt,hashlib,json,math,os,subprocess,sys,tarfile,tempfile,time,uuid,zipfile
from fixture import statements,upstream
from engine_inputs import R,CACHE,hashfile

def panel(path,engine):
    panels=json.loads(path.read_bytes())['panels']
    query=next(x for x in panels if x['id']==86)['targets'][0]['rawSql']
    if engine=='postgres':
        replacements={"${project:csv}":'study',"${project:singlequote}":"'study'",
            '$__timeFrom()':"'2026-05-01'",'$__timeTo()':"'2026-05-31'"}
    else:
        replacements={"${project}":"'study'","$__timeFilter(max(cdc.finished_date))":"max(cdc.finished_date) BETWEEN '2026-05-01' AND '2026-05-31'"}
    rendered=query
    for variable,value in replacements.items():rendered=rendered.replace(variable,value)
    assert '$' not in rendered,(path,rendered)
    return rendered,hashlib.sha256(query.encode()).hexdigest()

def unpack_zip(archive,where):
    with zipfile.ZipFile(archive) as bundle:
        assert all((where/name).resolve().is_relative_to(where.resolve()) for name in bundle.namelist())
        bundle.extractall(where)

def execute_mysql(folder,tasks):
    binaries=next(folder.glob('mysql-*/bin'))
    daemon=binaries/'mysqld.exe'
    config=['--no-defaults','--basedir='+str(binaries.parent),'--datadir='+str(folder/'db')]
    initialization=subprocess.run([daemon,*config,'--initialize-insecure'],capture_output=True,timeout=180)
    if initialization.returncode:
        raise RuntimeError(initialization.stderr.decode(errors='replace'))
    memory='devlakeaudit_'+uuid.uuid4().hex
    logfile=folder/'mysqld.log'
    with logfile.open('wb') as logs:
        server=subprocess.Popen([daemon,*config,'--skip-networking','--shared-memory','--shared-memory-base-name='+memory,'--mysqlx=OFF','--console'],
             stdout=logs,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        client=[binaries/'mysql.exe','--no-defaults','--user=root','--protocol=MEMORY','--shared-memory-base-name='+memory,'--batch','--skip-column-names']
        try:
            for _ in range(160):
                if server.poll() is not None:raise RuntimeError(logfile.read_text(errors='replace')[-2400:])
                probe=subprocess.run(client+['-e','SELECT 1'],capture_output=True)
                if probe.returncode==0:break
                time.sleep(.25)
            else:raise RuntimeError('Local shared-memory server did not become ready: '+probe.stderr.decode(errors='replace'))
            script=["SET SESSION sql_mode='ANSI_QUOTES';","CREATE DATABASE IF NOT EXISTS devlake_replay;","USE devlake_replay;","SELECT VERSION();"]
            for t in tasks:
                script.extend([t['fixture'],t['query'].rstrip(';')+';'])
            output=subprocess.run(client,input='\n'.join(script),text=True,encoding='utf8',capture_output=True,timeout=120,check=True).stdout.splitlines()
            assert len(output)==len(tasks)+1,output
            return {'version':output[0],'result':{t['id']:None if val=='NULL' else float(val) for t,val in zip(tasks,output[1:])}}
        finally:
            if server.poll() is None:
                subprocess.run(client+['-e','SHUTDOWN'],capture_output=True,timeout=15)
                try:server.wait(timeout=25)
                except subprocess.TimeoutExpired:server.terminate();server.wait(timeout=20)

def main():
    versions={'beta12-mysql':('v1.0.3-beta12.json','mysql'),'pr-mysql':('proposed.json','mysql'),
              'beta13-mysql':('beta13-mysql-dora-details-change-failure-rate.json','mysql'),
              'beta13-pg':('beta13-postgresql-dora-details-change-failure-rate.json','postgres'),
              'beta19-mysql':('beta19-mysql.json','mysql'),'beta19-pg':('beta19-postgresql.json','postgres')}
    workload={'mysql':[],'postgres':[]}
    hashes={};ground={}
    for version,(file,engine) in versions.items():
        query,hashes[version]=panel(R/'raw'/file,engine)
        for scenario in ('six_from_four','six_from_six','five_from_one','no_incidents','no_eligible_deployments',
                         'three_commits_one_deploy','last_commit_after_window','lost_relation'):
            fixture,ground[scenario]=statements(scenario)
            workload[engine].append(dict(id=version+'/'+scenario,fixture=fixture,query=query))
        for as_of,scenario in [(False,'upstream_full'),(True,'upstream_only_incidents_created_by_september')]:
            fixture,ground[scenario]=upstream(as_of)
            rendered=query.replace("'study'","'project1'").replace('2026-05-01','2022-09-01').replace('2026-05-31','2022-09-30 23:59:59')
            workload[engine].append(dict(id=version+'/'+scenario,fixture=fixture,query=rendered))
    for item in json.loads((R/'engine-lock.json').read_bytes())['artifacts']:
        assert hashfile(CACHE/item['filename'],'sha256').hexdigest()==item['sha256']
    with tempfile.TemporaryDirectory(prefix='devlake-real-engines-') as scratch:
        tmp=Path(scratch)
        unpack_zip(CACHE/'mysql-8.4.5-winx64.zip',tmp)
        with tarfile.open(CACHE/'pglite-0.3.7.tgz') as bundle:
            bundle.extractall(tmp,filter='data')
        pgwork=tmp/'pg-work.json';pgwork.write_text(json.dumps(workload['postgres']),'utf8')
        pg=subprocess.run(['node',str(R/'pg-run.mjs'),str(tmp/'package/dist/index.js'),str(pgwork)],capture_output=True,text=True,encoding='utf8',timeout=120)
        if pg.returncode:raise RuntimeError(pg.stderr[-3500:])
        pgresults=json.loads(pg.stdout)
        myresults=execute_mysql(tmp,workload['mysql'])
    combined=myresults['result']|pgresults['result'];details=[]
    for key,v in combined.items():
        version,case=key.split('/');target=ground[case]
        details.append(dict(version=version,scenario=case,dashboard=v,fixture_intervention_ratio=target,
            agrees=(v is None and target is None) or (v is not None and target is not None and math.isclose(v,target,abs_tol=.00006))))
    with (R/'replay.csv').open('w',encoding='utf8',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=list(details[0]));writer.writeheader();writer.writerows(details)
    register={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'executions':len(details),'mysql':myresults['version'],'postgresql':pgresults['version'],
              'sql_sha256':hashes,'windows':'May 2026 (synthetic); September 2022 (upstream fixtures)','scope':'eight synthetic histories plus full and date-filtered upstream E2E fixtures; original panel 86 query after Grafana variable substitution; no deployed Grafana or collector',
              'result_sha256':hashfile(R/'replay.csv','sha256').hexdigest()}
    (R/'audit.json').write_text(json.dumps(register,indent=2),'utf8')
    print(json.dumps(register))
if __name__=='__main__':main()

