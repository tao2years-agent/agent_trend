"""Rebuild coverage, old/new crosswalks, and source-level mechanism anchors from local registries."""
from pathlib import Path
import hashlib, json, csv, collections, re
R=Path(__file__).resolve().parent
B=R.parent.parent
def get(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def psv(p):return [i.split('|') for i in p.read_text(encoding='utf-8-sig').splitlines() if i]
def write(p,rows):
    with (R/p).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def hashit(p):return hashlib.sha256(p.read_bytes()).hexdigest()
buyers=readcsv(B/'round2/buyers/ledger.csv')
buy_sources={i['id']:i for i in get(B/'round2/buyers/sources.json')}
baseline=get(R/'buyer-baseline.json')
buy_sources={k:buy_sources[k] for k in baseline['prior_source_ids']}
for item in buyers:
    item['evidence_ids']=baseline['evidence_ids_by_buyer'][item['id']]
    item['chapters']=baseline['chapters_by_buyer'][item['id']]
products={i['id']:i for i in get(B/'corpus/products.json') if i['source_review']}
new={s['id']:s for s in get(R/'sources.json')}
docs=get(R/'attribution-docs.json')
diffs=get(B/'round2/evolution/tag-diffs.json')
ann={row[0]:row[1:] for row in psv(R/'annotations.psv')}
dmap={'atlantis':'BUY27','pr-agent':'BUY20','argo':'BUY25','src-cli':'BUY16'}
direct={}
ledger=[]
for item in buyers:
    id=item['id']; layer,old,repo,seen,boundary=ann[id]
    if old:direct[old]=id
    original=item['evidence_ids'].split()
    assert all(k in buy_sources for k in original)
    extra=[x for x in new if repo and x.startswith(repo+':')]
    if repo:assert extra,repo
    diff=' '.join(x['product'] for x in diffs if dmap[x['product']]==id)
    ledger.append(dict(id=id,product=item['product'],buying_task=item['buying_task'],layer=layer,observed=seen,unverified_and_test=boundary,previous_direct=old,buyer_evidence_ids=' '.join(original),new_evidence_ids=' | '.join(extra),tag_diff=diff,original_chapters=item['chapters']))
write('ledger.csv',ledger)
others={'D01':('BUY13','Actions Runner 是执行底座；不能据此证明 cloud agent worker。'),'F02':('BUY13','gh-aw 是仓库工作流工具；托管 cloud agent 是另一条产品线。'),'E09':('BUY14','Claude Agent SDK for Python 是外部 SDK；云定时器没有包含在所读文件。'),'F01':('BUY02','Symphony 的任务编排可接 Codex；不是 Codex CLI 编排本身。'),'D04':('BUY25','Argo CD 同属 Argo 项目，GitOps 同步目的不同于 Rollouts 灰度控制器。'),'O07':('BUY26','flagd 是同领域开放实现；不能据此绑定 LaunchDarkly 的云判定。')}
mapping=[]
for id,p in products.items():
    code=[s['path'] for s in p['sources'] if Path(s['path']).suffix.lower() in ('.py','.go','.rs','.ts','.tsx','.java','.rb','.js','.c','.cs','.kt','.ex','.cjs','.yaml','.yml')]
    related,reason=others.get(id,('','独立对象；未用于采购项源码归属。'))
    scope='直接采购对象' if id in direct else ('相邻对象' if related else '未对应')
    mapping.append(dict(first_round_id=id,name=p['name'],relation=scope,buyer=direct.get(id,related),reason='同一 CLI、应用或控制器的受核模块。' if id in direct else reason,code_snapshots=' | '.join(code),wiki='wiki/'+id+'.md',source_count=len(p['sources'])))
write('first-round-map.csv',mapping)
dout=[]
for d in diffs:
    assert hashit(B/d['diff_path'])==d['diff_sha256']
    a,c=d['before_after']
    dout.append(dict(buyer=dmap[d['product']],product=d['product'],layer='历史客户端' if d['product']=='src-cli' else ('随产品分发的 dashboard CLI' if d['product']=='argo' else '直接产品模块'),scope=d['path'],before=a['tag'],after=c['tag'],before_sha=a['commit'],after_sha=c['commit'],after_file_present=c['present'],local_diff=d['diff_path'],sha256=d['diff_sha256'],url=d['url']))
write('diff-map.csv',dout)
anchors=[]
for buy,prefix,start,end,token,note in psv(R/'annotations-lines.psv'):
    start,end=int(start),int(end)
    matches=[v for k,v in new.items() if k.startswith(prefix)]
    assert len(matches)==1,(prefix,len(matches))
    s=matches[0]; raw=(B/s['path']).read_text(encoding='utf-8').splitlines();assert 0<start<=end<=len(raw) and token in '\n'.join(raw[start-1:end]),(prefix,start,end,token)
    anchors.append(dict(buyer=buy,locator=note,source_id=s['id'],from_line=start,to_line=end,verified_token=token,local=s['path'],commit=s['commit'],url=s['url']+f'#L{start}-'+('' if 'gitlab.com/' in s['url'] else 'L')+str(end)))
write('mechanisms.csv',anchors)
for s in list(buy_sources.values())+list(new.values())+docs:
    assert hashit(B/s['path'])==s['sha256'],s['path']
for item in mapping:
    assert (B/item['wiki']).exists()
    assert item['code_snapshots'],item['first_round_id']
    for f in filter(None,item['code_snapshots'].split(' | ')):assert (B/f).exists()
assert len(ledger)==len(ann)==35 and len(direct)==9 and len(products)==36 and len(dout)==4
out=dict(buyers=len(ledger),layers=dict(collections.Counter(x['layer'] for x in ledger)),round_one_source_review=len(mapping),round_one_direct=len(direct),round_one_adjacent=len(others),tag_diffs=len(dout),new_files=len(new),extra_attribution_docs=len(docs),previous_buyer_sources=len(buy_sources),anchors=len(anchors),commits=len(set(s['commit'] for s in new.values())),anchor_buyers=len(set(a['buyer'] for a in anchors)))
(R/'coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
report=(R/'result.md').read_text(encoding='utf-8-sig')
for target in re.findall(r'\]\(([^ )]+)\)',report):
    assert target.startswith('http') or (R/target).is_file(),target
assert set(re.findall(r'\]\[([^\]]+)\]',report))<=set(re.findall(r'^\[([^\]]+)\]:',report,re.M))
assert '13 passed' in get(R/'gitlab-test-locked.json')['stdout']
assert get(R/'gitlab-test-locked-direct.json')['stdout'].count('PASS test_')==13
ambient=get(R/'gitlab-test-ambient.json')['stdout']
assert ambient.count('PASS test_')==11 and ambient.count('FAIL test_')==2
print(json.dumps(out,ensure_ascii=False))
