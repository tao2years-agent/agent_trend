"""Offline validation of all count identities, split, chronology, local links, and exported inputs."""
from scan import BASE,CACHE
from pathlib import Path
import json,re,struct,zlib,hashlib
import pandas as pd
from datetime import datetime
def js(s):return json.loads((BASE/s).read_text('utf-8-sig'))
def sec(t):return datetime.fromisoformat(t.replace('Z','').replace('+00:00',''))
def main():
    df=pd.read_csv(BASE/'roster-counts.csv').set_index('cohort')
    for _,r in df.iterrows():
        assert r.paired==r.both_empty+r.prev_only_empty+r.current_only_empty+r.both_nonempty
        assert r.changed_strict_nonempty==r.additions_strict_nonempty+r.removals_strict_nonempty-r.additions_and_removals_strict_nonempty
        assert 0<=r.changed_strict_nonempty<=r.strict_both_nonempty<=r.both_nonempty<=r.n
    assert df.loc[df.index.str.startswith('year_'),'n'].sum()==df.at['all','n']==353700
    assert not any(u['unrecognized'] for u in [js('opcode-audit.json')])
    pol=pd.read_csv(BASE/'policy.csv');orig=pd.read_csv(BASE.parent/'ci'/'policy.csv')
    for _,r in pol.iterrows():
        assert r.rerun+r.missed_green+r.avoided_red==r.n and 0<=r.missed_green<=r.green
    for a,b in [('always','always'),('project','project'),('published_current_result_roster','published_job_field')]:
        left=pol.query("method==@a and cohort=='all_test'").iloc[0]
        right=orig.query("method==@b and cohort=='full_test' and target==.95 and embargo==7").iloc[0]
        for c in ['n','green','rerun','missed_green','avoided_red']:assert left[c]==right[c]
    clocks=js('clock-evidence.json')['cases'];assert len(clocks)==16
    pair_ok=0;api_errors={}
    for r in clocks:
        assert all(r['gerrit'][q] for q in ['prior_reports','current_reports','request_posts'])
        if r['prior']['matched'] and r['current']['matched']:
            pair_ok+=1
            for side in ['prior','current']:
                x=r[side];assert x['patch_matched'] and sec(x['start_time'])<=sec(x['end_time'])<=sec(r['gerrit'][side+'_reports'][0][:26])
        else:
            for side in ['prior','current']:
                code=r[side]['query'].get('http');api_errors[str(code)]=api_errors.get(str(code),0)+1
    assert pair_ok==8 and api_errors=={'404':16}
    bs=js('buildsets.json')
    assert sum(r['prior']['pipeline']!=r['current']['pipeline'] for r in bs)==6
    assert sum(abs(r['current']['request_to_event_seconds'])<=1 for r in bs)==4
    final=js('asof-replay.json')
    for r in final['results']+final['same_reconstructable_cohort']:assert r['n']==r['rerun']+r['missed_green']+r['avoided_red']
    assert sum(final['partition_counts']['test'].values())==70740 and sum(final['partition_counts']['validation'].values())==69750
    m=js('history-member.json');z=zlib.decompressobj(-15);n=0;crc=0;tail=b''
    with (CACHE/'jobs-occurrences.deflate').open('rb') as f:
        while b:=f.read(131072):
            o=z.decompress(b);n+=len(o);crc=zlib.crc32(o,crc);tail=(tail+o)[-4096:]
    assert z.eof and n==m['uncompressed'] and crc==m['zip_crc32']
    partial=final['verified']['remaining_incomplete_document_bytes'];declared=struct.unpack_from('<i',tail[-partial:])[0]
    assert 0<partial<declared
    links=re.findall(r'\[[^\]]+\]\(([^)]+)\)',(BASE/'result.md').read_text('utf-8-sig'))
    missing=[s for s in links if not s.startswith('https://') and not (BASE/s.split('#')[0]).exists()]
    assert not missing
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(BASE.iterdir()) if p.is_file() and p.name!='validation.json'}
    out=dict(validated=True,years_all=int(df.at['all','n']),explicit_zuul_pairs=pair_ok,historical_api_responses_without_clock=api_errors,bson_tail_valid_bytes=partial,bson_tail_declared_bytes=declared,local_links_checked=len([s for s in links if not s.startswith('https://')]),public_files_sha256=hashes)
    (BASE/'validation.json').write_text(json.dumps(out,indent=2),'utf8');print({k:v for k,v in out.items() if k!='public_files_sha256'})
if __name__=='__main__':main()
