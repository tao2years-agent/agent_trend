"""Replay each successful install, offline and frozen, then compare the independent DOM probe."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,shutil,tempfile,subprocess as sp,os,hashlib,sys,zipfile
from pack_cache import key
B=Path(__file__).resolve().parent
NODE=shutil.which('node');CLI=str(Path(NODE).parent/'node_modules/npm/bin/npm-cli.js')
TMP=Path(tempfile.mkdtemp(prefix='js-peer-ci-'));CACHE=TMP/'isolated-cache'
def check(r):
    lock=B/r['lockfile'];pack=json.loads(lock.read_text());p=pack['packages']['']
    root=TMP/r['id'];root.mkdir()
    (root/'package.json').write_text(json.dumps({'name':p['name'],'private':True,'version':p['version'],'dependencies':p['dependencies']}),'utf8')
    shutil.copyfile(lock,root/'package-lock.json')
    opt=['--strict-peer-deps=true','--legacy-peer-deps=false'] if r['mode']=='strict' else ['--strict-peer-deps=false','--legacy-peer-deps=true']
    env=dict(os.environ,NODE_ENV='development',NPM_CONFIG_UPDATE_NOTIFIER='false')
    cp=sp.run([NODE,CLI,'ci','--offline','--cache',str(CACHE),*opt,'--no-audit','--no-fund','--ignore-scripts','--force=false','--registry=https://registry.npmjs.org/'],cwd=root,env=env,capture_output=True,text=True,timeout=90)
    assert cp.returncode==0,(r['id'],cp.stderr[-700:])
    run=sp.run([NODE,str(B/'probe.cjs')],cwd=root,env=env,capture_output=True,text=True,timeout=45);q=json.loads(run.stdout)
    prior=r['probe']
    assert all(prior[k]==q[k] for k in ['stages','passed','versions','warnings']),r['id']
    assert (prior.get('failure') or {}).get('message')==(q.get('failure') or {}).get('message'),r['id']
    for name,v in pack['packages'].items():
        if not name:continue
        assert v['integrity'].startswith('sha512-') and v['resolved'].startswith('https://registry.npmjs.org/'),name
    assert lock.read_bytes()==(root/'package-lock.json').read_bytes()
    return dict(id=r['id'],offline_ci_exit=cp.returncode,probe_exit=run.returncode,status_same=True,lock_sha256=hashlib.sha256(lock.read_bytes()).hexdigest(),locked_artifacts=len(pack['packages'])-1)
if __name__=='__main__':
    meta=json.loads((B/'locked-archives.json').read_text())
    bundle=B/'raw'/'npm-locked-public-archives.zip'
    assert hashlib.sha256(bundle.read_bytes()).hexdigest()==meta['bundle_sha256']
    with zipfile.ZipFile(bundle) as z:
        for integ in meta['entries']:
            member=key(integ);payload=z.read(member);assert hashlib.sha512(payload).hexdigest()==''.join(member.split('/')[-3:])
            dest=CACHE/member;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload)
    rows=[r for r in json.loads((B/'matrix.json').read_text()) if r['install']=='installed']
    with ThreadPoolExecutor(3) as pool:out=list(pool.map(check,rows))
    (B/'replay.json').write_text(json.dumps(out,indent=2),'utf8');print('offline lockfile replays',len(out))
