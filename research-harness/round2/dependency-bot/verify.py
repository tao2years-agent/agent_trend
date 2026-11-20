"""Check available evidence offline and compare the two independent fixture runs."""
from pathlib import Path
import gzip,hashlib,importlib.util,json,tarfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text('utf8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    for f in load(R/'sources.json')['files']:
        by=(R/'raw'/f['file']).read_bytes()
        assert sha(by)==f['sha256']
        if 'decoded_sha256' in f:
            plain=gzip.decompress(by);assert sha(plain)==f['decoded_sha256'] and len(json.loads(plain)['releases'])==f['release_keys']
    with tarfile.open(R/'raw/renovate-44.256.0.tgz') as tar:
        for p in (R/'raw').glob('package--*'):assert tar.extractfile(p.name.replace('--','/')).read()==p.read_bytes()
    spec=importlib.util.spec_from_file_location('judge',R/'judge.py');j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
    rows=j.extract();assert rows==load(R/'candidates.json') and len(rows)==12
    lookup=0
    for row in rows:
        d=R/'runs'/row['case'];o=load(d/'observation.json')
        assert o['returncode']==0 and not o['canary_before_explicit_test'] and not o['remotes'] and not o['git_worktree_status'] and o['git_head_unchanged']
        if o['mode']=='extract':assert o['canary_positive']=={'exit':0,'marker':True} and not o['requests']
        logs=[json.loads(x) for x in (d/'cli.log').read_text('utf8').splitlines() if x.startswith('{')]
        assert any(x.get('renovateVersion')=='44.256.0' for x in logs) and len(row['deps'])==2
        if o['mode']=='lookup':
            http=next(x for x in logs if x['msg']=='HTTP statistics')
            assert set(http['hosts'])=={'127.0.0.1'} and http['requests']==len(o['requests']);lookup+=http['requests']
    byid={r['case'][:2]:r for r in rows}
    assert byid['02']['branches']==byid['06']['branches']
    assert not byid['07']['branches'] and not byid['08']['branches'] and len(byid['07']['lookups'])==1
    assert len(byid['03']['branches'])==1 and len(byid['12']['branches'])==2 and len(byid['11']['branches'])==3
    def sig(u):return (u['package'],u['old'],u['new'])
    assert {sig(u) for b in byid['03']['branches'].values() for u in b}=={sig(u) for b in byid['12']['branches'].values() for u in b}
    compat=R.parent/'compat'
    previous=load(compat/'matrix.json')+load(compat/'bridge.json')
    res=load(R/'consumer-results.json')
    def key(r):return (r['family'],r['consumer'],r['dependency'],r['provider'])
    wanted=set()
    for row in rows:
        if row['case']=='11-unrestricted':continue
        wanted.add(j.cell(row['pins']))
        for branch in row['branches'].values():
            pins={k.lower():v for k,v in row['pins'].items()};pins.update({u['package'].lower():u['new'] for u in branch});wanted.add(j.cell(pins))
    assert {key(r) for r in res}==wanted
    for r in res:
        old=next(x for x in previous if key(r)==key(x))
        assert old['upstream']==r['upstream'] and r['installed'] and r['wsgi_asgi_request']['ok']
        f,v,d,w=key(r);xml=R/'downstream'/f'{f}-{v}_{d}-{w}'/'pytest.xml'
        tests=ET.parse(xml).getroot().find('testsuite')
        assert all(int(tests.attrib[k])==r['upstream'][k] for k in ('tests','errors','failures','skipped'))
    print(f'{len(rows)} CLI runs; {lookup} loopback GETs; {len(res)} installation combos; {sum(r["upstream"]["tests"] for r in res)} upstream test executions; {sum(r["upstream"]["failures"] for r in res)} failed; offline evidence checks passed.')
if __name__=='__main__':main()
