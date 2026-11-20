"""Check every package, lock replay, status boundary and evidence link. Write a reader CSV."""
from pathlib import Path
import json,hashlib,base64,collections,csv,re,zipfile
B=Path(__file__).resolve().parent
def read(name):return json.loads((B/name).read_text('utf-8-sig'))
def main():
    data=read('matrix.json'); replay=read('replay.json'); sources=read('sources.json')
    assert len(data)==16 and len({r['id'] for r in data})==16
    rows=[]
    for s in sources:
        raw=(B/s['tarfile']).read_bytes();assert hashlib.sha256(raw).hexdigest()==s['tgz_sha256']
        assert s['integrity']=='sha512-'+base64.b64encode(hashlib.sha512(raw).digest()).decode()
    for r in data:
        assert (B/'results'/(r['id']+'.json')).exists()
        p=r['probe'];entry={'group':r['group'],'react-dom_pair':r['react'],'rtl':r['rtl'],'direct_dom':r['root_dom'],'mode':r['mode'],'install':r['install'],'probe_result':'not_run','failure_stage':'','diagnostic':'','runtime_dom':'','warnings':''}
        if r['install']=='peer_rejected':
            assert r['mode']=='strict' and p is None
            diag=next(l for l in (B/'results'/(r['id']+'.install.txt')).read_text().splitlines() if l.startswith('npm error peer '))
            entry['diagnostic']=diag.removeprefix('npm error ')
        else:
            assert r['install']=='installed';rep=next(x for x in replay if x['id']==r['id']);assert rep['status_same']
            assert rep['lock_sha256']==hashlib.sha256((B/r['lockfile']).read_bytes()).hexdigest()
            entry.update(probe_result='pass' if p['passed'] else 'fail',failure_stage=(p.get('failure') or {}).get('stage',''),diagnostic=(p.get('failure') or {}).get('message',''),runtime_dom=p['versions']['dom_seen_by_RTL'],warnings=' || '.join(p['warnings']))
        entry['evidence']='results/'+r['id']+'.json';rows.append(entry)
    matrix=[r for r in rows if r['group']=='matrix'];strict=[r for r in matrix if r['mode']=='strict'];legacy=[r for r in matrix if r['mode']=='legacy']
    assert len(strict)==9 and len(legacy)==5 and sum(r['probe_result']=='pass' for r in strict)==4 and sum(r['probe_result']=='fail' for r in legacy)==3
    assert sum(r['group']=='negative' for r in rows)==2 and len(replay)==10 and len(sources)==13
    with (B/'results.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    man=read('locked-archives.json');assert man['archives']==154 and hashlib.sha256((B/'raw/npm-locked-public-archives.zip').read_bytes()).hexdigest()==man['bundle_sha256']
    for p in [B/'result.md',B/'protocol.md']:
        for h in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text('utf-8-sig')):
            if not h.startswith('https://'):assert (B/h.split('#')[0]).exists(),h
    summary=dict(matrix_strict=9,strict_rejected=5,strict_passed_probe=4,legacy_of_strict_rejected=5,legacy_probe_pass=2,legacy_probe_fail=3,negative_control_install_modes=2,offline_replay_of_all_installed=10,selected_release_archives=13,all_locked_unique_archives=154,full_lock_bundle_sha256=man['bundle_sha256'],probes_sha256=hashlib.sha256((B/'probe.cjs').read_bytes()).hexdigest(),checks_passed=True)
    (B/'validation.json').write_text(json.dumps(summary,indent=2),'utf8');print(summary)
if __name__=='__main__':main()
