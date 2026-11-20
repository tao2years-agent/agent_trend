"""Compile pre-registered sample, prior-item retrieval and source-specific yields."""
from frame import *
from collections import Counter
from difflib import SequenceMatcher

def loadtsv(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t'))
if __name__=='__main__':
    rows=loadtsv(BASE/'frame.tsv')
    targets=json.loads((BASE/'abstract-targets.json').read_text(encoding='utf8'))
    decisions=[l.split('|') for l in (BASE/'adjudications.txt').read_text(encoding='utf8').splitlines()]
    reviewed=[]; snapshots=[]
    for i,r in enumerate(targets):
        loc='raw/abstracts/'+r['id']+'.html'; data=capture(r['url'],BASE/loc)
        s=BeautifulSoup(data,'html.parser')
        tag=s.select_one('blockquote.abstract')
        if not tag:
            label=s.find(string=lambda t:t and t.strip().casefold()=='abstract')
            tag=label.parent.find_next_sibling() if label else None
        assert tag is not None
        title=s.title.get_text(' ',strip=True)
        assert SequenceMatcher(None,normal(r['title']),normal(title)[:len(normal(r['title']))+14]).ratio()>.74,(title,r['title'])
        abstract=re.sub(r'\s+',' ',tag.get_text(' ',strip=True)).removeprefix('Abstract:').strip()
        assert len(abstract)>100
        decision,reason=decisions[i] if i<32 else ('relevant','目的抽取，详见 cases.tsv')
        reviewed.append(dict(**r,decision=decision,reason=reason,path=loc,abstract=abstract))
        snapshots.append(dict(url=r['url'],path=loc,sha256=sha256(data).hexdigest()))
    assert len(decisions)==32 and sum(r['group']=='preselected' for r in reviewed)==32
    tsv(BASE/'sample-review.tsv',reviewed)
    cases=[]
    for n,cid,mechanism,control,finding,pilot,blindspot in json.loads((BASE/'case-notes.json').read_text(encoding='utf8')):
        source=reviewed[n-1]
        cases.append(dict(id=cid,frame_id=source['id'],title=source['title'],mechanism=mechanism,control=control,finding=finding,pilot_and_limit=pilot,blindspot=blindspot,level='author abstract; no independent execution',url=source['url'],path=source['path']))
    tsv(BASE/'cases.tsv',cases)
    (BASE/'sample-manifest.json').write_text(json.dumps(snapshots,indent=2),encoding='utf8')
    byid={r['id']:r for r in reviewed}
    cov=[]
    for v in VENUES:
        venue=[r for r in rows if r['venue']==v]
        for predicate in (True,False):
            expected=sorted([x for x in venue if bool(x['rules'])==predicate],key=lambda x:sha256(x['id'].encode()).hexdigest())[:2]
            assert all(x['id'] in byid and byid[x['id']]['group']=='preselected' for x in expected)
        hits=[r for r in venue if r['rules']]
        audit=[r for r in venue if r['id'] in byid and byid[r['id']]['group']=='preselected']
        stats={f'{status}_{dec}':sum(byid[r['id']]['decision']==dec and bool(r['rules'])==hit for r in audit) for status,hit in [('hit',True),('miss',False)] for dec in ['relevant','adjacent','off-topic']}
        cov.append(dict(venue=v,frame=len(venue),rule_hits=len(hits),rule_misses=len(venue)-len(hits),**{q:sum(q in r['rules'] for r in venue) for q in RULES},**stats))
    tsv(BASE/'coverage.tsv',cov)
    tsv(BASE/'screening.tsv',[dict(id=r['id'],venue=r['venue'],title=r['title'],rules=r['rules'],screening=r['screening'],abstract_status=byid.get(r['id'],{}).get('decision','not reviewed in frame sample'),audit=byid.get(r['id'],{}).get('group',''),candidate_review='../venue-review/review.tsv' if r['rules'] else '') for r in rows])
    prior=json.loads((BASE.parents[1]/'corpus/papers.json').read_text(encoding='utf8'))
    keys={normal(r['title']):r for r in rows}
    out=[]
    for p in prior:
        r=keys.get(normal(p['name']),{})
        out.append(dict(prior=p['id'],name=p['name'],venue=p['venue'],frame_id=r.get('id',''),rules=r.get('rules',''),status=('hit' if r['rules'] else 'miss') if r else 'outside exact-title frame'))
    tsv(BASE/'prior-recall.tsv',out)
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf8'))
    links={src['venue']:src for src in manifest['sources']}
    for src in manifest['sources']:assert sha256((BASE/src['path']).read_bytes()).hexdigest()==src['sha256']
    body=['# 八个正式研究轨的检索、误命中与盲点','',
          '冻结日期为 2026-11-20。ICSE、FSE、ASE、ISSTA 的 2025 和 2026 年主研究轨共列出 1,738 个不同题名和 1,738 个不同 event UUID，585 条在接受表中提供了可直接提取的 DOI 链接且无重复。预设的五组题名检索式命中 142 篇。首轮已选论文中有 14 篇确实位于此框，题名检索找回 8 篇，漏掉 6 篇。这是对已知小样本的诊断。','',
          '## 每个来源贡献了多少候选','',
          '|官方接受目录|收录题名|命中|未命中|Q1 编排|Q2 交付|Q3 监督|Q4 组织|Q5 评测|','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in cov:
        v=r['venue'];body.append('|['+v.upper()+']('+links[v]['url']+')|'+'|'.join(str(r[k]) for k in ['frame','rule_hits','rule_misses',*RULES])+'|')
    body+=['','同一题名能命中多组；来源命中数按唯一题名计。[全部题名及命中原因](frame.tsv) · [逐条筛选状态](screening.tsv) · [分层复核计数](coverage.tsv) · [所有命中的摘要判定](../venue-review/review.tsv)。','',
           '## 为何不用会议名称检索出版库来定义分母','',
           '八个输入都是各自主研究轨网页的 Accepted Papers 表；时段、主题 session 和混合日程未进入分母。FSE 两年正式规则都写明研究轨论文发表于 PACMSE 的相应 FSE 期，再获邀在会议报告。ISSTA 2025 公告将发表转到 PACMSE，2026 延续该方式；两年均可能接受 Research、Experience 和 Replicability 三种类型。ASE 两届的发布轨名为 Research Papers，征稿明确包含 Technical Research Papers 和 Experience Papers。ICSE 的 Research Track 独立于 SEIP、Journal First 等。该表没有统一子型字段；13 个 ISSTA 题名以括号明确自报 Experience Paper 或 Replicability Study，按题名标记保存。其余 1,725 项记 unknown，描述性副标题不作为正式子型。只使用这些界面可以稳定定义八个轨目录，不能宣称覆盖所有挂名该会议或同期发表的软件工程研究。','',
           '正文卷期、会上报告年份和预印本首次公开年份可以不同。本轮以研究轨的会议年归属，原始 HTML 和 SHA-256 见 [来源清单](manifest.json)。会议小标题、奖项或制品标签没有作为题名的一部分。未在研究轨接受表抓到 DOI 的行仍有 UUID 和来源 HTML，可以通过官网详情表单按 UUID 定位。','',
           '## 随机抽核与错误来源','',
           '每届分别按 SHA-256(event UUID) 升序从命中、未命中两层各取 2 篇，固定 32 篇。命中层的 16 篇有 14 篇直接相关、2 篇相邻。未命中层的 16 篇有 7 篇直接相关、7 篇相邻、2 篇离题。另补 5 个目的抽取，不参与抽样统计；入选 6 个代表案例中 Testora 已在抽样内。每篇记录准确英文题名、作者摘要、来源快照与中文裁定。[32+5 条原文定位与判定](sample-review.tsv)','',
           '直接漏检涵盖用 PR 意图识别行为回归（Testora）、贡献者离开后 PR 流量的准实验、用变更前后成对执行发现意外语义变化（ChangeGuard）、发布说明生成（VerLog）、完整车辆 API 测试流程、基于代码知识的运行故障归因（COCA），以及告警分诊。共同原因是论文用具体操作或领域名词表述工作，没有采用预置词形。命中后仍出现反例，例如路径规划中的 multi-agent、代码检索中的 modality collaboration、区块链事务中的 rollback，以及跨语言训练中的 knowledge transfer。它们分别与软件执行代理、团队协作、发布回滚、工程师知识交接同形异义。','',
           '全部 142 篇命中再以官网作者摘要逐条审查：89 篇直接相关、43 篇相邻、10 篇离题。抽样在每届和每个命中层中等额，不是按总体规模等概率抽取；抽样和目的补充都不宜外推整体真实召回率。单次分析者裁定也可能误判相邻与直接相关的边界。','',
           '## 既有论文被漏掉的具体原因','',
           '20 篇中的 P11 为 ICSE SEIP，P12、P17、P19 为较早届次，P13、P14 属于其他会议；这 6 项不在本框。框内未命中的 P02、P15 由 intent/spec 描述约束，P05 与 P18 使用 LLM agent 而非预列的 agent 组合，P06 从职业开发者的调试实践建构理论，P09 以 chat 和 IDE sessions 描述行为。追加检索可预置 intent/specification、LLM agents、development sessions、developer turnover、debugging practice、release notes 和 behavioral regressions，再在另一年或另一会议盲测。此次保留 v1 的六次已知漏检；事后补词不可写成对原结果的改善。[逐篇匹配](prior-recall.tsv)','',
           '## 六个此前缺少的机制','']
    for case in cases:
        body.extend([f'### {case["id"]} · {case["mechanism"]}','',case['title']+'。'+case['control'],'',case['finding']+' '+case['pilot_and_limit'],'',case['blindspot']+' [作者摘要]('+case['url']+')',''])
    body+=['## 复算','', '在本目录及相邻 venue-review 目录执行下列命令。所需 Python 包为 requests、beautifulsoup4；读取额外八篇 PDF 需 pdftotext。快照存在时直接离线解析，初次补抓需要联网。frame.py 重新计算题名分母，frame_review.py 按事前规则检索、检查抽样、汇总裁定；fetch.py 从相应官方只读详情取回 142 个摘要。', '', '```text','python frame.py','python frame_review.py','python ../venue-review/fetch.py','python ../venue-review/fulltexts.py','python ../venue-review/compile_review.py','```','',
           '报告记录的是研究者观察、作者报告及建议试验。六个新增机制为作者摘要级复核；八篇另行精读的论文有独立方法/结果/效度定位。[八篇正文复核](../venue-review/result.md)']
    (BASE/'result.md').write_text('\n'.join(body)+'\n',encoding='utf8')
    print(cov)
    print(Counter(r['status'] for r in out))
