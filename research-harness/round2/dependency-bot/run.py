"""Exercise the published CLI through its local platform. Only GET on the fixture registry."""
import argparse, datetime, gzip, http.server, json, os, subprocess, sys, tempfile, threading
from pathlib import Path
R=Path(__file__).resolve().parent
STAR={'starlette':'0.36.3','httpx':'0.26.0'}
FLASK={'Flask':'2.2.2','Werkzeug':'2.2.3'}
def rule(name,*values,**kw):
    r={'matchPackageNames':[name],**kw}
    if values:r['allowedVersions']='/'+'^('+'|'.join(x.replace('.','\\.') for x in values)+')$/'
    return r
h=rule('httpx','0.26.0','0.28.1')
s=rule('starlette','0.36.3','0.37.2')
sh=rule('starlette','0.36.3')
hh=rule('httpx','0.26.0')
f=rule('flask','2.2.2')
w=rule('werkzeug','2.2.3','2.3.8')
scenarios=[
 ('01-extract','extract',STAR,[sh,h]),
 ('02-provider','lookup',STAR,[sh,h]),
 ('03-group','lookup',STAR,[s,h,{'matchPackageNames':['starlette','httpx'],'groupName':'tested ASGI pair','groupSlug':'tested-asgi-pair'}]),
 ('04-approved-first','lookup',STAR,[s,hh]),
 ('05-approved-second','lookup',{**STAR,'starlette':'0.37.2'},[s,h]),
 ('06-dashboard','lookup',STAR,[sh,h,rule('httpx',dependencyDashboardApproval=True)]),
 ('07-ignore','lookup',STAR,[sh,h,rule('httpx',enabled=False)]),
 ('08-no-update','lookup',STAR,[sh,hh]),
 ('09-flask-provider','lookup',FLASK,[f,w]),
 ('11-unrestricted','lookup',STAR,[]),
 ('12-ungrouped','lookup',STAR,[s,h]),
 ('10-flask-bridge','lookup',FLASK,[rule('flask','2.2.2','2.2.5'),rule('werkzeug','2.2.3')]),
]
def put(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False),'utf8')
class Registry(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        name=self.path.split('/')
        if len(name)!=4 or name[1]!='pypi' or name[3]!='json' or name[2] not in ('flask','werkzeug','httpx','starlette'):
            self.send_error(404);return
        self.server.calls.append(self.path)
        data=gzip.decompress((R/'raw'/(name[2]+'.json.gz')).read_bytes())
        self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
def git(cwd,*args):
    return subprocess.run(['git',*args],cwd=cwd,check=True,capture_output=True,text=True).stdout.strip()
def execute(cli,server,case):
    name,mode,pins,rules=case
    out=R/'runs'/name;out.mkdir(parents=True,exist_ok=True)
    registry=f'http://127.0.0.1:{server.server_port}/pypi/'
    config={'enabledManagers':['pip_requirements'],'dependencyDashboard':True,'packageRules':[{'matchDatasources':['pypi'],'registryUrls':[registry]},*rules]}
    with tempfile.TemporaryDirectory(prefix='renovate-case-',ignore_cleanup_errors=True) as temp:
        tmp=Path(temp);repo=tmp/'repo';repo.mkdir()
        (repo/'renovate.json').write_text(json.dumps(config),'utf8')
        (repo/'requirements.txt').write_text(''.join(f'{k}=={v}\n' for k,v in pins.items()),'utf8')
        (repo/'test_canary.py').write_text("from pathlib import Path\ndef test_consumer():\n    Path('consumer-ran').write_text('entered')\n",'utf8')
        ci=repo/'.github/workflows';ci.mkdir(parents=True)
        (ci/'ci.yml').write_text('name: downstream\non: [pull_request]\njobs:\n  tests:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: python -m pytest test_canary.py\n','utf8')
        git(repo,'init','-b','main');git(repo,'add','.');git(repo,'-c','user.email=fixture@localhost','-c','user.name=Fixture','commit','-m','fixture')
        head=git(repo,'rev-parse','HEAD')
        env={k:v for k,v in os.environ.items() if not any(x in k.upper() for x in ('TOKEN','SECRET','PASSWORD','RENOVATE','PROXY','GITHUB','GITLAB','API_KEY','NPM_CONFIG','BITBUCKET','AWS_','AZURE_'))}
        env.update({'LOG_FORMAT':'json','LOG_LEVEL':'debug','RENOVATE_BASE_DIR':str(tmp/'base'),'RENOVATE_CACHE_DIR':str(tmp/'cache'),'RENOVATE_GIT_AUTHOR':'Fixture <fixture@localhost>','NO_PROXY':'127.0.0.1,localhost','RENOVATE_ALLOWED_HOSTS':'127.0.0.1'})
        start=len(server.calls)
        args=['node',str(cli),'--platform=local','--dry-run='+mode]
        p=subprocess.run(args,cwd=repo,env=env,capture_output=True,encoding='utf8',errors='replace',timeout=150)
        data=(p.stdout+'\n'+p.stderr).replace(str(tmp),'<TEMP>').replace(str(tmp).replace('\\','\\\\'),'<TEMP>').replace(str(server.server_port),'<PORT>')
        (out/'cli.log').write_text(data,'utf8')
        status=git(repo,'status','--porcelain')
        rec=dict(case=name,mode=mode,pins=pins,config=json.loads(json.dumps(config).replace(str(server.server_port),'<PORT>')),returncode=p.returncode,requests=server.calls[start:],canary_before_explicit_test=(repo/'consumer-ran').exists(),git_head_unchanged=head==git(repo,'rev-parse','HEAD'),git_worktree_status=status,remotes=git(repo,'remote'))
        if name=='01-extract':
            positive=subprocess.run([sys.executable,'-m','pytest','-q','test_canary.py'],cwd=repo,capture_output=True,encoding='utf8',timeout=90)
            rec['canary_positive']={'exit':positive.returncode,'marker':(repo/'consumer-ran').exists()}
        put(out/'observation.json',rec)
        print(name,p.returncode,rec['requests'],flush=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cli',type=Path,required=True);ap.add_argument('--case',action='append');args=ap.parse_args()
    cli=args.cli.resolve()
    assert subprocess.check_output(['node',str(cli),'--version'],text=True).strip()=='44.256.0'
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Registry);server.calls=[];threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        for case in scenarios:
            if not args.case or case[0] in args.case:execute(cli,server,case)
    finally:server.shutdown()
if __name__=='__main__':main()

