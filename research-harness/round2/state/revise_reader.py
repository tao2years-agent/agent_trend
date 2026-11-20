"""Keep decision text aligned with the later evidence and the pre-existing four-page brief."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent
def replace(rel,old,new):
    p=R/rel;s=p.read_text('utf8')
    if new in s:return
    if old not in s:raise ValueError((rel,old[:40]))
    p.write_text(s.replace(old,new,1),'utf8')
replace('reader-v2.html','content:"研发效能研究　/　决策洞察　　　　　　　　　2026.11.20"','content:"从 Code Agent 到组织级研发自动化　　·　　2026.11.20　　·　　" attr(data-page)')
replace('share.md','已无法','已无法') if False else None
replace('share.md','**决策动作。** 请平台团队拿出下一季度真实的仓库清单和期限，用已有工具干跑。只有剩余难例值得购买新能力时，才在相同难例上比较 agent＋现有流程和现有流程独立完成的时间、质量与总成本。',
'**决策动作。** 让现有工具在下一季度的真实清单上干跑，确认剩余难例确实消耗工程师时间，再比较新旧流程。若改选 CI，先做分诊。在两个独立的历史留出集中，同类策略在 OpenStack 少派 5,061 次、错过 430 次本可转绿；GitHub Actions 少派 83 次、错过 43 次本可转绿。是否值得跳过重跑，取决于本组织错挡一次的代价。[OpenStack 数据](https://zenodo.org/records/15559526) · [GitHub Actions 研究](https://doi.org/10.1145/3795771)')
replace('share.md','评审活动统计也容易误读。在 AIDev 热门仓库子集的 140,164 个 agent 标记 PR 中，30 天内有 94,947 个合并，33,017 个有可见个人账户的正式评审决定。两种事件可以重叠。一对工具的总体可见评审率差为 −15.37 个百分点。限制到 107 个共同仓库月份，按各组 PR 数汇总是 −4.54，仓月等权变为 −2.80。放宽样本门槛后，两种权重甚至给出相反方向。公开痕迹无法回答具体团队花了多少时间或谁在其他界面审过。[AIDev 固定数据](https://huggingface.co/datasets/hao-li/AIDev/tree/b8dc67df93e7c11f6f20c84129db7232eb1ec253)',
'在 140,164 个公开 PR 上回放“超过一天就叫人”会怎样？24 小时后尚无终态、也无可见个人正式评审的有 37,882 件。其中 16,502 件随后未见正式决定便合并或关闭，13,005 件到第 30 天两种记录都没有。这里无法看到私下审阅，也没给任何人发通知。天数可以帮估计提醒量，是否值得打断人，要看还有哪项决定非他不可。[AIDev 固定数据](https://huggingface.co/datasets/hao-li/AIDev/tree/b8dc67df93e7c11f6f20c84129db7232eb1ec253)')
replace('share.md','对两个固定提交的实现做局部测试，同样能看出选择规则的差异。Meta-Harness 的候选可以改善一道薄弱题，整体领先版本维持原样。AHE 的可选 best-of-n 路径可以从两个都比种子差的子代中选出相对较好的一项。它们说明候选如何被选择；要交给工程团队长期使用，还要有能拒绝两项候选的独立验收。[AHE 原文及实现说明](https://arxiv.org/abs/2604.25850)',
'把验收从“测试过了多少”换成“整件是否交付”，答案也会变。11 月的 SWE-CoWork 预印本用 101 个真实仓库、模拟同事和隐藏验收比较 11 种模型。给两个模型完整需求后，新行为节点通过率分别提高 16.67 和 15.93 个百分点，整项完成率各自仍为 0.99% 和 7.92%。我们逐件复核公开任务配置，比论文分母多一个新行为节点；模型成绩按作者原表引用。真实团队的人时仍须另测。[原文表 2、表 3](https://arxiv.org/pdf/2611.20218v1)')
replace('executive.md','### 平台团队和业务团队各持有什么决策权','''### 有哪些证据会改变产品设计

- **给对人、问对问题、交付正确结果需要分开验收。** SWE-CoWork 中给两种模型完整需求，节点通过率涨约 16 个百分点，整项通过率都维持原水平。在真实公开 PR 上，满 24 小时无决定、无终态的 37,882 件中，16,502 件后来未见正式决定便合并或关闭。对组织级产品，可以把“提醒谁”与“哪个外部条件被解决”分别计量。一个是模拟实验，一个是公共事件回放，均没有测客户工时。[协作 benchmark 及对账](cowork/result.md) · [提醒时机](supervision/result.md)
- **CI 的历史预测值要经过派发时刻检验。** OpenStack 资料中的一项强预测量依赖本次重跑结束时出现的 job 名单。把请求连接到真实调度记录后发现，同 patch 甚至可能关联到数日后另一事件。换数据生态，同类规则的简化盈亏点从 OpenStack 的 11.77 变为 GitHub Actions 的 1.93，其中后者 43 个误挡中 41 个来自同一仓。首发可以给证据、影子建议和覆盖入口；自动阻止要逐客户、逐仓验证。[作业可得性审计](ci-availability/result.md) · [跨生态](ci-cross/result.md)
- **成熟团队已有可借的边界。** Stripe 在完整 CI 的再试之后把分支交人，Ramp 将重复告警挂回原修复，并将候选与已合并变更的差异交给独立评审。可以沿现有平台的 CI、评审和发布接口做接管层；真实的差异化要在反复失败、多人交接和验证还未结束时显现。[四个现场](factories/result.md) · [五组互操作规范](interoperability/result.md)

### 平台团队和业务团队各持有什么决策权''')

