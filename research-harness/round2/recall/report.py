from select_fetch import *
from collections import Counter
from math import sqrt

def interval(k,n,N):
    p=k/n
    if n==N:return p,p
    z=1.959963984540054
    d=1+z*z/n
    center=(p+z*z/(2*n))/d
    err=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,center-err),min(1,center+err)

if __name__=='__main__':
    frame=load(BASE/'ledger.tsv'); abstracts=load(BASE/'abstracts.tsv')
    dec=[s.split('|') for s in (BASE/'decisions.txt').read_text(encoding='utf8').splitlines()]
    assert len(abstracts)==len(dec)==128
    triage={'R':'relevant','A':'adjacent','O':'off-topic','U':'unknown'}
    results=[]
    for i,(a,(k,decision,why)) in enumerate(zip(abstracts,dec),1):
        assert int(k)==i and a['title']==a['modal_title'] and len(a['abstract'])>120
        assert sha256((BASE/a['path']).read_bytes()).hexdigest()==a['sha256']
        results.append(dict(sample_id=a['sample_id'],uuid=a['id'],venue=a['venue'],stratum=a['stratum'],rules=a['v2'],title=a['title'],decision=triage[decision],rationale=why,authors=a['author_affiliations'],url=a['url'],path=a['path'],sha256=a['sha256']))
    tsv(BASE/'review.tsv',results)
    counts=[]
    for v in dict.fromkeys(r['venue'] for r in frame):
        for s in ['new-hit','still-miss']:
            pop=sum(r['venue']==v and r['stratum']==s for r in frame)
            ss=[r for r in results if r['venue']==v and r['stratum']==s]
            totals={k:sum(r['decision']==k for r in ss) for k in triage.values()};n=len(ss);k=totals['relevant']
            lo,hi=interval(k,n,pop)
            counts.append(dict(venue=v,stratum=s,frame=pop,sampled=n,**totals,rate=k/n,wilson95_low=round(lo,4),wilson95_high=round(hi,4)))
    tsv(BASE/'coverage.tsv',counts)
    picks=[]
    for n,decision,fact,pilot,why in json.loads((BASE/'picks.json').read_text(encoding='utf8')):
        r=results[n-1];assert r['decision']=='relevant'
        picks.append(dict(id=r['sample_id'],title=r['title'],venue=r['venue'],stratum=r['stratum'],question=decision,source_finding=fact,falsification=pilot,retrieval=why,url=r['url'],path=r['path']))
    tsv(BASE/'picks.tsv',picks)
    previous={r['id'] for r in load(FRAME/'sample-review.tsv')} | {r['uuid'] for r in load(BASE.parent/'venue-review'/'review.tsv')}
    assert not previous.intersection(r['uuid'] for r in results)
    total=Counter(x['stratum'] for x in frame);sr={s:Counter(r['decision'] for r in results if r['stratum']==s) for s in ['new-hit','still-miss']}
    text=['# 第二次检索：以工作对象找回漏检，再用新摘要盲抽','',
          f'首轮 1,738 个研究轨题名中有 {total["excluded"]} 个已知条目，不再用于泛化检验。剩余 {total["new-hit"]+total["still-miss"]:,} 个题名内，新词表召回 {total["new-hit"]} 个，仍未命中 {total["still-miss"]:,} 个。两层各检查 64 个此前未审阅的官方作者摘要。新增命中层有 {sr["new-hit"]["relevant"]} 个直接相关、{sr["new-hit"]["adjacent"]} 个相邻、{sr["new-hit"]["off-topic"]} 个离题；仍未命中层也有 {sr["still-miss"]["relevant"]} 个直接相关、{sr["still-miss"]["adjacent"]} 个相邻、{sr["still-miss"]["off-topic"]} 个离题。检索修订可发现有价值的工作，也继续遗漏论文。', '',
          '## 冻结与复算','',
          'V1 的 142 个题名命中、37 个已核摘要、F01–F06 和原 P 系列、R2 papers 的已知题名以 UUID/规范题名取并集排除。固定 work item、工作会话、验证对象三组词，按新 salt 对每个会议年×V2 命中/未命中各取前 8 个哈希。全部 128 份官方响应均经 UUID、英文题名与 SHA-256 校验。这里只能保证档案中已知样本没有进入盲抽。研究者已熟悉该领域，没有双人独立、对标题与层别隐藏的盲审。', '',
          '[事前方案](protocol.md) · [V2 精确检索式](rules.json) · [1,738 条逐项账本](ledger.tsv) · [128 条人工判定](review.tsv) · [官方原摘要与 SHA](abstracts.tsv) · [作者谱系](groups.md)', '',
          '## 同一会议年内应如何读这两个比例','', '第一列分母是该层剩余总题名数；比例是固定哈希抽样中直接相关的比例，括号为 95% Wilson 区间。以哈希近似随机抽取的小样本为前提，各轨不确定度很大；这不是原规则的精确率或召回率。研究轨内可同时存在技术、经验和复现工作，未获正式子型时继续标 unknown。', '',
          '|会议年|新增命中池|直接相关/抽核（区间）|仍未命中池|直接相关/抽核（区间）|','|---|---:|---|---:|---|']
    for first,second in zip(counts[::2],counts[1::2]):
        def rate(r):return f'{r["relevant"]}/{r["sampled"]} · {100*r["rate"]:.0f}%（{100*r["wilson95_low"]:.0f}%–{100*r["wilson95_high"]:.0f}%）'
        text.append(f'|{first["venue"].upper()}|{first["frame"]}|{rate(first)}|{second["frame"]}|{rate(second)}|')
    text+=['','样本对 16 个层等额分配，整体池大小与会议结构不等。把两层 64 篇直接相除仅描述已审样本，不是合并八个研究轨的加权相关率。抽样波动不足以给会议排名。三个重点词群也带来明确误检：programmers 可指静息态脑成像，patch 可指专用检测，specification 可指控制参数推断。','',
           '## 五项值得保留的研究','']
    for r in picks:text += [f'### {r["id"]} · {r["question"]}','',r['title']+'。'+r['source_finding'],'',r['falsification']+' '+r['retrieval']+' [官方作者摘要]('+r['url']+')','']
    text+=['## 对首选试点的影响','',
           '有明确退出日期、owner 与兼容判据时，真实依赖迁移仍可以先做。V009 提醒团队把上线前的影子行为比较写进验收；V034 说明跨仓迁移还可能卡在维护人离开，应以该依赖有无承接人分层。CI 失败分诊的对照则需要实质改变：加入 CiDiff 一类只呈现成功/失败差异的轻量基线。若人工从专用 diff 得到同等结论并花费同等时间，停止给这一类失败增加生成式解释。两条路径的优先级仍取决于本组织的待迁移量和失败诊断分钟，论文没有提供跨组织净收益排序。','',
           '自动优化 harness 也有更具体的否决条件。修改规则后需要沿需求和制品追踪受影响范围；用含已有缺陷的任务验证真实揭错能力。若新版本只提高覆盖而未在该类任务上增加真缺陷发现，拒绝推广。五项补充给出产品应做的对照和停机条件，不必把它们全部扩为新的功能线。','',
           '## 剩余盲区与下一次更新','',
           'V009 只说 cloud-scale authorization，V080 只说统计错误，V121 只说 contamination；这些工作在题名不直接写出组织工作对象。反过来将所有验证、上下文和安全名词全部加入词表，会使筛选量膨胀。下轮可先在独立年份用有限预算做摘要或引文追踪，并检测这三种盲区是否复现，不能再用这 128 篇作验证集。','',
           '这项研究对指定八份研究轨目录有完整题名清单，对命中和漏检区有二阶段摘要核查；其他年份、SEIP、非英语出版源、工业白皮书和所有未命中项的人工全文判定不在该抽样框。主题划分与评级仍包含分析者判断，置信区间仅衡量抽样误差，未校正标签误分、同一研究组聚类、不同会议年框架差异或多重区间。如此不能声称这是穷尽领域的系统综述。','',
           '离线重算时运行 python select_fetch.py、python groups.py、python report.py。新增的五项均为作者摘要级复核，未独立复现实验，勿计作八篇既有全文新增数。']
    (BASE/'result.md').write_text('\n'.join(text)+'\n',encoding='utf8')
    print(total,sr);print([(r['venue'],r['stratum'],r['frame'],r['relevant']) for r in counts])
