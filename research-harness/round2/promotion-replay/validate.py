"""Validate persisted public outcomes, cache boundaries, synthetic approval checks, and wheel bytes."""
import json,hashlib,zipfile,csv,re
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    o=json.loads((B/'observations.json').read_text());events={e['label']:e for e in o['events']};grants={g['label']:g for g in o['fixture_approvals']}
    def v(name):return events[name]['response']['value']['version']
    assert [v(k) for k in ['register-v1','register-v2','register-v3']]==[1,2,3]
    required={'audit-wrong-version':3,'rollback-visible-uncached':1,'after-expired-receipt-fixture':2,'reader-default-immediately-after-write':1,'reader-bypass-sees-new':2,'bypass-does-not-refresh-existing-default-entry':1,
              'reader-default-after-real-ttl':2,'already-loaded-inflight-stays-v1':1,'inflight-object-even-after-expiry':1,'last-write-is-v2':2,'final-production':1,
              'other-reader-default-immediately-after-rollback':2,'other-reader-no-cache-after-rollback':1,'inflight-v2-remains-usable-after-rollback':2,'restarted-process-uses-persisted-production':1}
    for name,version in required.items():assert v(name)==version,name
    old=events['approved-candidate']['response']['value'];drift=events['same-v2-new-config']['response']['value']
    assert old['version']==drift['version'] and old['template_sha256']==drift['template_sha256'] and old['model_config']['temperature']==0.1 and drift['model_config']['temperature']==0.8
    assert not events['reject-nonexistent-version']['response']['ok'] and v('invalid-target-left-production-intact')==2
    assert not grants['expired_receipt_blocked_by_fixture']['passes_fixture_checks'] and grants['valid-new-receipt']['passes_fixture_checks']
    assert grants['ABA-matches-version-and-digest-after-rollback']['passes_fixture_checks'] and not grants['single-use-harness-rejects-ABA']['passes_fixture_checks']
    assert o['metadata']['mlflow']=='3.18.0' and o['cache_check_elapsed_seconds']>=o['metadata']['alias_default_ttl_s']
    assert all(w['closed']['socket_connect_denied']==0 and w['process_exit']==0 for w in o['worker_exit'])
    assert [s['aliases']['production'] for s in o['sqlite_snapshots']]==[1,3,2,2,2,1]
    assert all(s['versions']==[1,2,3] for s in o['sqlite_snapshots'])
    head=o['sqlite_snapshots'][0]['selected_version_fields']['2'];tail=o['sqlite_snapshots'][-1]['selected_version_fields']['2']
    assert head['mlflow.prompt.text']==tail['mlflow.prompt.text']==old['template']
    assert head['_mlflow_prompt_model_config']['temperature']==0.1 and tail['_mlflow_prompt_model_config']['temperature']==0.8
    matched=json.loads((B/'runtime-source-match.json').read_text());assert len(matched)==6
    for row in matched:assert hashlib.sha256((B/row['extracted']).read_bytes()).hexdigest()==row['installed_sha256']
    for m in json.loads((B/'sources.json').read_text()):assert hashlib.sha256((B/m['file']).read_bytes()).hexdigest()==m['sha256']
    E=json.loads((B/'environment.json').read_text());assert len(E['wheels'])==len((B/'requirements-win-py312.lock').read_text().splitlines())
    with (B/'timeline.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['step','elapsed_s','label','process','api_operation','version_returned','rendered','temperature','succeeded','error_code'])
        for x in o['events']:
            resp=x['response'];val=resp.get('value') or {};w.writerow([x['step'],x['monotonic_s'],x['label'],x['role'],x['op'],val.get('version'),val.get('rendered'),(val.get('model_config') or {}).get('temperature'),resp['ok'],resp.get('error_code')])
    for p in (B/'result.md',B/'protocol.md'):
        for h in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text('utf-8-sig')):
            if not h.startswith('https://'):assert (B/h.split('#')[0]).exists(),h
    r=dict(checked=True,operations=len(o['events']),successful=sum(e['response']['ok'] for e in o['events']),deliberate_native_rejections=sum(not e['response']['ok'] for e in o['events']),fixture_checks=len(grants),sqlite_snapshots=len(o['sqlite_snapshots']),isolated_worker_processes=len(o['worker_exit']),runtime_socket_attempts=0,fixture_model_calls=0,environment_wheels=len(E['wheels']),actual_ttl_wait_seconds=o['cache_check_elapsed_seconds'],native_alias_schema=o['sqlite_snapshots'][0]['alias_table_columns'])
    (B/'validation.json').write_text(json.dumps(r,indent=2),'utf8');print(r)
if __name__=='__main__':main()
