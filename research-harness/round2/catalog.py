"""Build the edition's local index from the same chapter registry used by the offline reader."""
from collections import defaultdict
from pathlib import Path
from publish import R,P,chapters
import json
def catalog(strict=False):
    groups=defaultdict(list);missing=[]
    for rel,theme,title in chapters:
        if (R/rel).is_file():groups[theme].append((title,rel))
        else:missing.append(rel)
    if strict:assert not missing,missing
    lines=['# 研发自动化研究 Wiki · 第二版','',
      '读者可以从同一证据库进入[深度分析](../outputs/deep-report-v2.html)、[决策版](../outputs/insights-decision.html)和[四页 PDF](../outputs/insights-decision.pdf)。首轮资料和当时结论留在[原始项目索引](../wiki/index.md)。','',
      '## 从团队的决定开始','',
      '|下次会上要决定什么|应先查什么|决定什么时候需要改|','|---|---|---|',
      '|预算先给谁|[路线选择](decision.md)、[35 产品台账](buyers/ledger.csv)、[版本和部署形态](product-code/result.md)|现有规则能否吃完难例、实测瓶颈是否仍在工程劳动。|',
      '|可以把哪一步交出去|[迁移边界](compat/result.md)、[双引擎](handoff/result.md)、[跨系统回执](interoperability/result.md)|换人、改版本或丢回执后，外部动作能否独立查证。|',
      '|什么时候提醒人|[谁来接手](ownership/result.md)、[提醒时机](supervision/result.md)、[真人研究](attention/result.md)|看到公开审批、找到 owner、真正节约人的时间需要不同证据。|',
      '|让哪种自动化运行到哪一步|[CI 跨生态](ci-cross/result.md)、[特征是否提前可见](ci-availability/result.md)、[选版](optimizersrc/result.md)|时间留出、误阻成本、独立拒绝机制能否支持扩大范围。|',
      '|跟哪些论文和团队|[研究组](labs/result.md)、[共同署名与课题](recall/groups.md)、[摘要全库与检索](abstract-index/result.md)|抽检未命中记录，区分方法、观察对象和可复现实验。|','',
      '## 证据覆盖和研究状态','',
      '[覆盖台账](state/coverage.md) · [本轮检查点](state/checkpoint.md) · [变更日志](state/log.md) · [原始筛查协议](protocol.md) · [独立审稿](state/editorial-review.md)','',
      '## 按专题查证','']
    for name,entries in groups.items():
        lines+=['### '+name,'']+['- ['+title+']('+rel+')' for title,rel in entries]+['']
    lines+=['## 增量维护','',
     '优先从专题表中的稳定 ID、官方 URL、修订、下载哈希追到原始材料。新版本另存快照，再对比旧版；修正进入相应事实源和章节。用 scripts/build.py 更新初版入口，round2/publish.py 生成第二版视图，round2/check_reader.py 校验离线浏览与打印，再运行 round2/verify.py。完整指令及依赖范围见[协议](protocol.md)。']
    (R/'index.md').write_text('\n'.join(lines)+'\n','utf8')
    return missing
if __name__=='__main__':
    import sys
    print('pending chapters:',catalog('--strict' in sys.argv))

