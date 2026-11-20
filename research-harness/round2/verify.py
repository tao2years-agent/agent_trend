"""Offline end-to-end checks. Study-specific validators can be run against their original inputs."""
import csv,hashlib,json,re,sys
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from urllib.parse import unquote,urlsplit
from bs4 import BeautifulSoup
from publish import R,P,chapters,md
def read(p):return p.read_text(encoding='utf8')
def data(p):return json.loads((R/p).read_bytes())
def tab(p):
    with (R/p).open(encoding='utf-8-sig',newline='') as fp:return list(csv.DictReader(fp,delimiter='\t' if p.endswith('.tsv') else ','))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(strict=True):
    report={};checks=0
    def check(name,value,expected):
        nonlocal checks
        assert value==expected,(name,value,expected);report[name]=value;checks+=1
    ledger=tab('buyers/ledger.csv');sr=data('buyers/sources.json');refs={s['id']:s for s in sr}
    check('buyer_products',len({x['product'] for x in ledger}),35)
    check('buyer_primary_tasks',len({x['buying_task'] for x in ledger}),10)
    check('buyer_nonempty_fields',all(all(r[k] for k in ['task','trigger','accepted_artifact','human_takeover','availability_version','unknown_or_boundary']) for r in ledger),True)
    check('buyer_refs_unique',len(refs),125)
    check('buyer_evidence_referenced',all(len({refs[i]['url'] for i in x['evidence_ids'].split()})>=2 for x in ledger),True)
    check('buyer_hashes',all(sha(P/s['path'])==s['sha256'] for s in sr),True)
    check('independent_claims',len(tab('buyer-audit/claims.tsv')),70);check('claim_revisions',len(tab('buyer-audit/corrections.tsv')),12)
    check('product_source_map',Counter(x['layer'] for x in tab('product-code/ledger.csv')),data('product-code/coverage.json')['layers'])
    check('release_entries',len(tab('evolution/screening.csv')),113)
    check('release_entries_screened_in',len(tab('evolution/timeline.csv')),28)
    hist=data('product-history/coverage.json')
    check('historical_evidence',[hist['products'],hist['observations'],hist['direct'],hist['index_only'],hist['context']],[35,96,86,2,8])
    check('two_direct_timepoints',hist['status']['直接原件可作先后对照'],33)
    check('procurement_billing_studies',[len(tab('economics/tariffs.csv')),len(data('economics/sources.json'))],[8,27])
    check('assessment_domains',len(tab('evalops/matrix.csv')),6)
    evaluation=data('evalops/probe-results.json')
    check('assertion_denominators',[evaluation['opik_candidate_all_assertions'],evaluation['opik_candidate_omit_both_failed_assertions']],[.5,1.0])
    check('optimizer_source_microtests',len(data('optimizersrc/probe-results.json')),11)
    pairs=tab('pairing/scores.csv');keys=[k for k in pairs[0] if k not in ['instance_id','repo']]
    check('paired_tasks_models',[len(pairs),len(keys)],[500,5]);check('paired_union',sum(any(int(r[k]) for k in keys) for r in pairs),358)
    check('largest_single',max(sum(int(r[k]) for r in pairs) for k in keys),265)
    route=tab('pairing/router.csv');check('routing_losses',sum(float(v['repository_route'])<float(v['global_train']) for v in route),19)
    matrix=data('compat/matrix.json');bridge=data('compat/bridge.json');check('compatibility_cells',[len(matrix),len(bridge)],[18,3])
    check('installable',sum(bool(v['installed']) for v in matrix),15)
    check('green_upstream',sum(isinstance(v.get('upstream'),dict) and v['upstream'].get('exit_code')==0 for v in matrix),12)
    check('green_bridge',sum(v['upstream']['exit_code']==0 for v in bridge),3)
    js=data('js-compat/validation.json')
    check('javascript_transfer',[js[k] for k in ['matrix_strict','strict_rejected','strict_passed_probe','legacy_probe_fail','offline_replay_of_all_installed']],[9,5,4,3,10])
    releases=data('oracle-releases/checks.json')
    check('real_release_oracles',[len(releases),sum(len(r['observations']) for r in releases)],[10,80])
    mutants=data('gates/scores.json')['candidates'];check('mutation_cases',[len(mutants),sum(bool(x['labels_pass']) for x in mutants),sum(bool(x['modules_pass']) for x in mutants)],[49,14,10])
    events=data('interoperability/checks.json');check('event_schema_checks',[events['schema_evaluations'],events['conforming_documents'],events['invalid_documents']],[26,23,3])
    cohorts=data('cohorts/audit.json');check('public_pr_outcomes',[cohorts[k] for k in ['total','repos','merged','closed','no_terminal','formal_observed']],[140164,13657,94947,30759,14458,33017])
    owners=data('ownership/coverage.json');check('reviewer_holdout',[owners[k] for k in ['n_prs','n_repos','n_label30']],[67327,8700,15203])
    q=next(x for x in tab('supervision/queue.csv') if x['group']=='all' and x['age_hours']=='24')
    check('reminder_queue',[int(q[k]) for k in ['eligible','terminal_only','neither']],[37882,16502,13005])
    check('openstack_record_links',data('ci-availability/validation.json')['years_all'],353700)
    github=data('ci-cross/holdout.json')['registered'];policy=next(x for x in github['policies'] if x['target']==.95)
    check('github_recheck_holdout',[github['test'],policy['saved_retries'],policy['missed_green']],[1472,83,43])
    review=tab('venue-review/review.tsv');blind=tab('recall/review.tsv')
    check('conference_frame',len({r['id'] for r in tab('venue-frame/frame.tsv')}),1738)
    check('disjoint_abstract_reviews',[len(review),len(blind),len({x['uuid'] for x in review}&{x['uuid'] for x in blind})],[142,128,0])
    cc=data('cowork/audit.json');check('cowork_public_contract',[cc['task_count'],cc['release']['new_nodes']['sum'],cc['release']['regression_nodes']['sum']],[101,2700,562])
    check('cowork_paper_denominator',cc['paper_table2']['new_nodes'],2699)
    repeat=data('state/independent-checks.json')['validators']
    check('independent_substudy_validators',sum(v['exit']==0 and sha(R/v['script'])==v['sha256'] for v in repeat),13)
    missing=[rel for rel,_,_ in chapters if not (R/rel).is_file()]
    if strict:
        check('required_sections_missing',missing,[])
        abstracts=[json.loads(s) for s in read(R/'abstract-index/abstracts.jsonl').splitlines()]
        check('catalogued_abstract_records',len(abstracts),1738)
        audited=tab('abstract-index/adjudications.tsv')
        check('manually_checked_extension',len({r['uuid'] for r in audited}),32)
        check('no_double_count_with_270',set(x['uuid'] for x in audited).isdisjoint(x['uuid'] for x in review+blind),True)
        check('independent_candidate_adjudication',data('abstract-index/review-agreement.json')['n'],32)
        check('paper_review_agreement',data('abstract-index/review-agreement.json')['exact'],26)
        check('abstract_content_hashes',sum(sha(R/'abstract-index'/v['path'])==v['sha256'] and bool(v['abstract']) for v in abstracts),1738)
        check('abstract_review_conflicts_retained',len(tab('abstract-index/disagreements.tsv')),6)
        ml=data('promotion-replay/validation.json')
        check('registry_replay',[ml[k] for k in ['operations','isolated_worker_processes','sqlite_snapshots','fixture_model_calls']],[51,4,6,0])
        selection=data('selection-effect/summary.json')
        check('developer_trial_selection',[selection[k] for k in ['late_all_exported','late_developers','late_usable_total_time_rows','late_usable_total_time_people']],[1134,57,827,53])
        check('open_vendor_sample_dx',data('eng-intel-vendors/fixture-results.json')['DX_PR_throughput']['value'],1.6)
        lake=tab('devlake/replay.csv')
        check('executed_dashboard_queries',len(lake),60)
        check('upstream_fixture_by_dialect',{r['version']:round(float(r['dashboard']),2) for r in lake if r['scenario']=='upstream_full' and r['version'].startswith('beta13')},{'beta13-mysql':0.4,'beta13-pg':1.2})
        reader=data('state/readers.json')
        check('portable_book_sections',reader['deep-report-v2-desktop']['sections'],len(chapters)+2)
        check('offline_desktop_download',reader['deep-report-v2-desktop']['embedded_download_verified'],True)
        check('reader_errors_and_network',[reader['external_requests'],reader['js_errors']],[[],[]])
        check('share_pages',len(reader['pdf']),4)
        moved=data('state/portable-rebuild.json')
        check('relocated_readers_rebuild_identically',sum(
            values['identical'] and values['relocated']==values['original']==sha(P/'outputs'/file)
            for file,values in moved['hashes'].items()),2)
        check('relocated_verified_search_index',moved['verified_index_size'],1738)
        repo_checks=data('state/snapshot-summary.json')
        check('declared_snapshot_hash_mismatch',repo_checks['mismatches'],[])
        full=BeautifulSoup(read(P/'outputs/deep-report-v2.html'),'html.parser')
        cards=full.select('details.record')
        check('offline_card_count',len(cards),35)
        for card,row in zip(cards,ledger):
            assert row['product'] in card.select_one('summary').get_text() and '版本演进' in card.get_text() and '公开实现所处层级' in card.get_text()
        check('pricing_annotated_cards',sum(any(d.get_text(strip=True)=='计费单位' for d in card.select('dt')) for card in cards),8)
    issues=[]
    for name in ['protocol.md','executive.md','decision.md','conclusion.md','index.md','state/coverage.md']+[r for r,_,_ in chapters if (R/r).is_file()]:
        p=R/name
        for a in BeautifulSoup(md(read(p)),'html.parser').find_all('a',href=True):
            href=a['href'];url=urlsplit(href)
            if url.scheme or not url.path:continue
            if not (p.parent/unquote(url.path)).exists():issues.append([name,href])
    report['unresolved_local_references']=sorted(set(tuple(x) for x in issues))
    if strict:assert not issues,issues
    report['sections_pending']=missing;report['counted_checks']=checks;report['strict']=strict
    report['checked_utc']=datetime.now(timezone.utc).isoformat()
    (R/'state'/('final-audit.json' if strict else 'build-audit.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8')
    print('checks:',checks,'pending:',missing,'broken links:',report['unresolved_local_references'])
if __name__=='__main__':verify('--draft' not in sys.argv)

