from fetch import *
from collections import Counter
from frame import tsv
from decimal import Decimal

def load(p): return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t'))

if __name__=='__main__':
    raw=load(BASE/'abstracts.tsv')
    decisions=[s.split('|') for s in (BASE/'decisions.txt').read_text(encoding='utf8').splitlines()]
    fullnotes=json.loads((BASE/'deep-notes.json').read_text(encoding='utf8'))
    fullids={r[0] for r in fullnotes}
    assert len(raw)==len(decisions)==142
    review=[]; report=[]; triage={'R':'relevant','A':'adjacent','O':'off-topic','U':'unknown'}
    for i,(r,d) in enumerate(zip(raw,decisions),1):
        rank,decision,mechanism,fact,org=d
        assert int(rank)==i and len(r['abstract'])>120 and r['author_affiliations'] and r['url']
        assert sha256((BASE/r['path']).read_bytes()).hexdigest()==r['sha256']
        row=dict(id='H'+rank,uuid=r['id'],venue=r['venue'],title=r['title'],decision=triage[decision],mechanism=mechanism,abstract_evidence=fact,organization_implication=org,authors_and_affiliations=r['author_affiliations'],level='full text' if i in fullids else 'author abstract',url=r['url'],path=r['path'])
        review.append(row)
    tsv(BASE/'review.tsv',review)
    sources={r['id']:r for r in load(BASE/'fulltext-sources.tsv')}
    for num,mech,loc,method,result,limit in fullnotes:
        r=review[num-1]; source=sources[r['id']]
        assert sha256((BASE/source['path']).read_bytes()).hexdigest()==source['sha256']
        report.append(dict(id=r['id'],uuid=r['uuid'],title=r['title'],venue=r['venue'],mechanism=mech,locator=loc,method=method,finding=result,limits_and_test=limit,url=source['url'],path=source['path']))
    tsv(BASE/'fulltext-review.tsv',report)
    tsv(BASE/'coverage.tsv',[dict(venue=v,**{k:sum(r['decision']==k for r in review if r['venue']==v) for k in triage.values()},total=sum(r['venue']==v for r in review)) for v in sorted({r['venue'] for r in review})])
    prior=load(FRAME/'prior-recall.tsv'); pnames={normal(r['name']) for r in prior}
    six={r['frame_id'] for r in load(FRAME/'cases.tsv')}
    assert not any(normal(r['title']) in pnames or r['uuid'] in six for r in report)
    stats=Counter(r['decision'] for r in review)
    body=['# 从题名命中到实际决策证据','',f'冻结的 142 个题名命中全部获得会议官网作者摘要，逐条标注后直接相关 {stats["relevant"]} 项、相邻 {stats["adjacent"]} 项、离题 {stats["off-topic"]} 项、证据不足 {stats["unknown"]} 项。八份作者全文作为其中的第二层复核，分别补充预算、评审、团队学习、计划、满意度及指标效度；它们与原 P01–P20、题名审计 F01–F06 均未重复。', '', '## 证据如何核对','', '研究轨题名分母在 ../venue-frame/frame.tsv。fetch.py 读取会议专轨原页面的公开详情表单，按原 event UUID 请求只读详情，将官方响应、新旧同一 UUID 的题名、可点击 All Details、作者与单位、原始 SHA-256 关联在 abstracts.tsv。review.tsv 依次提供人工分类、具体摘意、机制与组织决策含义。机构字段使用会议页面明示的作者单位，部分作者未列单位，未推断实验室归属。', '', 'relevant 表示出现能回答研究问题的执行、决策或衡量机制；adjacent 表示仅有局部算法或特定领域的迁移价值；off-topic 表示关键词歧义或决策对象不符；unknown 表示资料不足。八篇正文按组织决策差异、是否已有覆盖及一手正文可得性目的抽取，不构成效果排序。全文案例中的量化结论属于作者研究，未独立重运行原实验。', '', '## 八篇新增正文补读','']
    for r in report:body.extend([f'### {r["id"]} · {r["mechanism"]}', '',r['title']+'。'+r['method'],'',r['finding'],'',r['limits_and_test']+' '+f'[{r["locator"]}]({r["url"]})',''])
    body.extend(['## 筛查后可直接改变的试验设计','', '动态续期的强基线是相同任务上的固定预算。至少同时记录解题成功、无补丁终止、总费用与单个难题的排队时间。把审核者工作量、知识覆盖、主观信任与真实缺陷分别保存，可避免把模拟风险比或点击同意错认成开发质量。', '', 'H055 的风险门槛、H064 的知识事件、H093 的指标词表分别回答不同层面的问题。将配置试点按仓库、变更难度和 reviewer 分组，预登记主要结局及人工负担并保留未使用者，才有机会区分执行优化和环节转移。'])
    (BASE/'result.md').write_text('\n'.join(body)+'\n',encoding='utf8')
    print(stats)
