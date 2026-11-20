"""Run each matrix cell in a fresh root with the public registry and without lifecycle/post/audit actions."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess as sp,os,shutil,json,csv,re,tempfile,datetime,hashlib,sys
B=Path(__file__).resolve().parent
WORK=Path(tempfile.mkdtemp(prefix='js-peer-matrix-'))
LOCK=B/'locks';EVID=B/'results';LOCK.mkdir(exist_ok=True);EVID.mkdir(exist_ok=True)
NPM=shutil.which('npm.cmd');NODE=shutil.which('node')
CLI=Path(NODE).parent/'node_modules/npm/bin/npm-cli.js'
REACT=['17.0.2','18.2.0','19.0.0'];RTL=['12.1.5','13.4.0','16.1.0']
def run_process(cmd,cwd,timeout=300):
    env=os.environ.copy();env.update(NODE_ENV='development',NPM_CONFIG_UPDATE_NOTIFIER='false',NPM_CONFIG_FUND='false',NPM_CONFIG_AUDIT='false')
    res=sp.run(cmd,cwd=cwd,env=env,stdout=sp.PIPE,stderr=sp.PIPE,encoding='utf8',errors='replace',timeout=timeout)
    return res.returncode,res.stdout,res.stderr
def sanitize(log,wd):
    x=log.replace(str(wd),'<project>').replace(str(WORK),'<temporary-run>')
    for n in ['LOCALAPPDATA','APPDATA','USERPROFILE','TEMP']:
        if os.environ.get(n):x=x.replace(os.environ[n],'<local-cache>')
    x=re.sub(r'(?mi)^npm error A complete log of this run can be found in:.*$','',x)
    return x.strip()
def one(item,mode):
    react,rtl,dom,group=item
    id=('control-' if group=='negative' else '')+f'r{react}-rtl{rtl}-dom{dom}-{mode}'
    dest=WORK/id;dest.mkdir()
    pkg={'name':'local-peer-compat-probe','private':True,'version':'1.0.0','dependencies':{'react':react,'react-dom':react,'@testing-library/react':rtl,'@testing-library/dom':dom,'jsdom':'24.1.3'}}
    (dest/'package.json').write_text(json.dumps(pkg),encoding='utf8')
    opt=['--strict-peer-deps=true','--legacy-peer-deps=false'] if mode=='strict' else ['--strict-peer-deps=false','--legacy-peer-deps=true']
    cmd=[NODE,str(CLI),'install',*opt,'--force=false','--no-audit','--no-fund','--ignore-scripts','--registry=https://registry.npmjs.org/','--prefer-offline','--fetch-retries=1','--fetch-timeout=30000','--loglevel=warn']
    exitcode,out,err=run_process(cmd,dest)
    log=sanitize(out+'\n'+err,dest);(EVID/(id+'.install.txt')).write_text(log,encoding='utf8')
    install='installed' if exitcode==0 else 'peer_rejected' if 'ERESOLVE' in log else 'install_error'
    result=dict(id=id,group=group,react=react,renderer=react,rtl=rtl,root_dom=dom,mode=mode,install=install,install_exit=exitcode,probe=None,lockfile=None)
    if install=='installed':
        lock=LOCK/(id+'.json');shutil.copyfile(dest/'package-lock.json',lock);result['lockfile']=lock.relative_to(B).as_posix()
        ret,o,e=run_process([NODE,str(B/'probe.cjs')],dest,60)
        d=json.loads(o);d['process_exit']=ret;d['stderr']=sanitize(e,dest);result['probe']=d
    (EVID/(id+'.json')).write_text(json.dumps(result,indent=2),'utf8');print(id,install, (result['probe'] or {}).get('passed'),flush=True)
    return result
if __name__=='__main__':
    rows=[(r,t,'10.4.0','matrix') for r in REACT for t in RTL]+[('19.0.0','16.1.0','9.3.4','negative')]
    with ThreadPoolExecutor(3) as pool:strict=list(pool.map(lambda x:one(x,'strict'),rows))
    failures=[i for i,s in zip(rows,strict) if s['install']=='peer_rejected']
    with ThreadPoolExecutor(3) as pool:legacy=list(pool.map(lambda x:one(x,'legacy'),failures))
    (B/'matrix.json').write_text(json.dumps(strict+legacy,indent=2),'utf8')
    (B/'environment.json').write_text(json.dumps(dict(node=run_process([NODE,'--version'],WORK)[1].strip(),npm=run_process([NODE,str(CLI),'--version'],WORK)[1].strip(),platform=sys.platform,jsdom='24.1.3',root_DOM='10.4.0',date_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),strict_runs=len(strict),legacy_runs=len(legacy)),indent=2),'utf8')
