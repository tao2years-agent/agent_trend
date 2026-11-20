"""Derive candidates directly from native CLI logs, then independently install and test."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, sys, tempfile
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text('utf8'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf8')
def extract():
    rows=[]
    for d in sorted((R/'runs').iterdir()):
        obs=read(d/'observation.json')
        messages=[json.loads(x) for x in (d/'cli.log').read_text('utf8').splitlines() if x.startswith('{')]
        data=next((m['config'] for m in messages if m['msg']=='packageFiles with updates'),None)
        if not data:data=next(m['packageFiles'] for m in messages if m['msg']=='Extracted dependencies')
        deps=data['pip_requirements'][0]['deps']
        branches={}
        for dep in deps:
            for u in dep.get('updates',[]):
                branches.setdefault(u['branchName'],[]).append(dict(package=dep['depName'],old=dep['currentVersion'],new=u['newVersion'],update_type=u['updateType'],isBreaking=u.get('isBreaking')))
        rows.append(dict(case=obs['case'],mode=obs['mode'],pins=obs['pins'],lookups=sorted(set(obs['requests'])),deps=[{k:d[k] for k in ('depName','currentValue','skipReason','warnings') if k in d} for d in deps],branches=branches))
    return rows
def cell(pins):
    p={k.lower():v for k,v in pins.items()}
    if 'starlette' in p:return ('Starlette',p['starlette'],'httpx',p['httpx'])
    return ('Flask',p['flask'],'Werkzeug',p['werkzeug'])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--no-tests',action='store_true');args=ap.parse_args()
    rows=extract();put(R/'candidates.json',rows)
    cells=set()
    for row in rows:
        if row['case']=='11-unrestricted':continue  # lookup-only control, outside archived wheel matrix
        cells.add(cell(row['pins']))
        for updates in row['branches'].values():
            pins=row['pins'].copy()
            for u in updates:
                key=next(k for k in pins if k.lower()==u['package'].lower());pins[key]=u['new']
            cells.add(cell(pins))
    if args.no_tests:return
    compat=R.parent/'compat'
    sys.path.insert(0,str(compat))
    spec=importlib.util.spec_from_file_location('compat_runner',compat/'run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    extras=read(compat/'bridge-sources.json')
    for f in extras:assert hashlib.sha256((compat/f['path']).read_bytes()).hexdigest()==f['sha256']
    m.sources.extend(extras)
    with tempfile.TemporaryDirectory(prefix='renovate-downstream-',ignore_cleanup_errors=True) as temp:
        temp=Path(temp);shutil.copytree(compat/'raw',temp/'raw');shutil.copy2(compat/'probe.py',temp/'probe.py');m.R=temp
        with ThreadPoolExecutor(2) as pool:results=list(pool.map(m.run,sorted(cells)))
        shutil.copytree(temp/'results',R/'downstream',dirs_exist_ok=True)
    put(R/'consumer-results.json',results)
    for r in results:print(r['family'],r['consumer'],r['provider'],r.get('upstream'),flush=True)
if __name__=='__main__':main()

