from pathlib import Path
import json,hashlib,platform
import pandas as pd
import pyarrow as pa
P=Path(__file__).resolve().parent
def tab(name):return pd.read_csv(P/'tables'/(name+'.csv'))
a=tab('agent-30d'); audit=json.loads((P/'audit.json').read_text('utf8'));regs=audit['windows']['30']; sw=regs['weighted_percent']
def pct(n,d):return f'{100*n/d:.1f}%'
def se(k):
 y=a[k]/a.n
 return 1.96*100*(((a.eligible/a.eligible.sum())**2*(1-a.n/a.eligible)*y*(1-y)/(a.n-1)).sum()**.5)
def tr(r):return '| '+' | '.join(map(str,r))+' |'
agent_rows=[tr([r.agent.replace('_',' '),r.eligible,r.n,r.repositories,r.merged,r.closed_unmerged,r.no_terminal_by_horizon,r.personal_decision,r.draft_transition])for r in a.itertuples()]
q=tab('outcome-30d').set_index('outcome')
aggregate_rows=[tr([label,regs['totals'][k],pct(regs['totals'][k],audit['sampled']),f'{sw[k]:.2f}%',f'{sw[k]-se(k):.2f}%–{sw[k]+se(k):.2f}%'])for k,label in [('merged','截至 30 日已合并'),('closed_unmerged','截至 30 日关闭未合并'),('no_terminal_by_horizon','截至 30 日未见终态'),('personal_decision','有可识别个人账户正式决定'),('draft_transition','留有草稿转换事件')]]
url='https://huggingface.co/datasets/hao-li/AIDev/tree/'+json.loads((P/'raw/tree.json').read_text('utf8'))['revision']
res=f'''# 关闭、合并与人的判断：对 1,545 个真实 agent PR 的等窗口观察

**一个合并状态无法回答“谁验收了它”。** 在本研究抽中的 978 个 30 天内合并的 PR 中，310 个（31.7%）能在同一窗口中找到个人账户提交的正式同意或要求修改。另 668 个有合并记录，但这一狭义字段没有人工决策记录。反过来，414 个关闭未合并的 PR 中，9 个同一窗口里出现过个人账户 APPROVED。合并和批准分别描述交付结果与一次正式意见，均不足以单独度量组织效率。

## 选择了什么

采用 AIDev 作者发布的 v5 热门仓库子集（作者定义为超过 100 星的仓库），固定版本日期截止到 2026-03-31；本次获取于 2026-11-20。基础表 361,296 条，以 UTC 2026 年 2 月创建为唯一月份条件得到 67,327 个 PR，涉及 8,700 个仓库和六个作者标注的 agent。按代理分层，哈希排序每组最多取 300 个；Jules 该月仅 45 个合格，全部纳入。最终 1,545 个不同 PR 分布于 764 个仓库，观察窗口以每条 PR 自己的创建时间为起点，均具有完整的 30 天日历随访。仅选已经创建的 PR；工单未产生 PR、人工放弃创建、失败于补丁提交之前的工作都不在分母。[作者论文](https://arxiv.org/abs/2602.09185) · [作者固定版本与数据卡]({url}) · [本地预登记方案](preregister.md)

| 30 日指标 | 分层样本数 | 样本占比 | 按二月合格 PR 数加权 | 加权抽样近似 95% 区间 |
|---|---:|---:|---:|---:|
{chr(10).join(aggregate_rows)}

前三行互斥且穷尽；后两行可以出现在任何终态。加权估计以各 agent 的全量二月合格 PR 数作权重，估计对象只限这 67,327 个。区间视哈希排序为独立的无放回等概率抽样，按层计算有限总体修正；只反映 PR 抽样波动，识别错误、仓库选择与事件缺失没有进入区间。仓库层面的决策存在相关性，不应将区间解读为不同企业或市场的外推范围。

## 不同代理进入了不同仓库

| 作者代理标签 | 二月合格 | 抽样 | 样本仓库 | 合并 | 关闭未合并 | 未见终态 | 有个人账户正式决定 | 有草稿转换 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(agent_rows)}

仓库列在层间可能重叠。Devin 的 300 个样本只来自 24 个仓库；Claude Code 的 300 个来自 233 个。Jules 只有三个仓库。代理识别依赖作者的账号、分支或归属规则，不同团队的接入方式和提交习惯还影响能观察到哪些 PR。任务类型、难度、仓库审批要求和商业产品当时的采用期都未随机化，因此不能用这张表评出“谁的模型更好”。[按代理明细](tables/agent-30d.csv) · [仓库限额敏感性](tables/repo-cap5-30d.csv)

## 如何观察“人提出了什么决定”

从正式 review 表按 PR ID 关联；只取创建到观察终点之间的记录。要求 GitHub 的 user_type 为 User，再排除机器人后缀、明显自动化账号模式及列明的代理账号，仅计算 APPROVED 或 CHANGES_REQUESTED。30 天内按去重后的 PR 计，320 个获同意，40 个被要求修改，26 个两者都有，故有决定的 PR 为 334。对照是 728 个有任意 review 的 PR，后者包括机器人和 COMMENTED，不能替代前者。就记录行而言，能辨认的个人账户提交了 402 条同意、56 条要求修改；同一 PR 可有多条。已忽略超出 30 天窗口的 32 条正式 review 记录。[意见与账号类型交叉表](tables/review-labels-30d.csv)

关闭未合并中有 13/414 个留有个人账户正式决定，未见终态中有 11/153 个。用户账号可能服务于自动化，亦可能有真人通过评论、线下或分支规则完成审查。数据记载的是公开关联字段；审批人的组织权限、是否真正阅读、判断是否先于合并，以及是否有人在其他渠道接管，都不能从“同窗出现”推出。GitHub 的 review 状态也可能后来被 dismiss，最终状态快照难以还原每次历史意见。关闭未合并包括重复工作、重开、替代实现和维护策略等情况，无证据逐一认定“弃单”。[终态交叉明细](tables/outcome-30d.csv)

## 草稿与右删失

PR 表缺少 draft 布尔值。用有时间戳的 convert_to_draft 或 ready_for_review 事件识别“观察到经历过草稿转换”共 477 项；其中 419 项在 30 天内合并，27 项关闭未合并，31 项无终态。一条 PR 可以多次转换。没有转换事件的 PR 可能仍以草稿创建并在窗口结束时保持草稿，所以只能将 477 当作有可见草稿历史的下界，不能把其他 PR 全部判作正式稿。抽中 PR 对应的原始 timeline 有 2,274 条缺少时间戳，无法用于等长窗口；另有 664 条晚于第 30 天，均排除。[事件词表](tables/timeline-event-vocabulary.csv)

到第 7 天，934 项合并、324 项关闭未合并、287 项未见终态；到第 30 天分别为 978、414、153。只看一周就把未决记失败，会把观察终点错当最终结果。到第 30 天仍无终态的 153 项属于右删失，本研究不会猜测它们随后是否成功。达到时间点但在终点前发生过重开也会使单个 closed_at 有歧义；30 日窗识别了 10 个出现过 reopened 的 PR。用带时标的关闭、合并和重开事件复核，410 个已关闭及 975 个已合并有独立 timeline 对应；另 4 个关闭、3 个合并仅 PR 表给出终态，其余带明确时间线终态的记录与主分类未冲突。两张表共用 GitHub 上游，不能作为数据准确性的独立外部验证。[7 日分层](tables/agent-7d.csv) · [时间线复核](tables/timeline-crosscheck-30d.csv)

## 哪种团队规则值得试

一种常见指标是“代理 PR 被合并的占比”。它看不到合并前的意见、没有 PR 的工单、后来被替代的变更、评审人花掉的分钟和发布后问题。试点可把工单、PR、审查决定、负责处理的人和生产观察窗分开记录，再提出一个可以测的问题：对同类工单，接管者收到带版本的失败证据后，是否更快给出可执行且正确的处置？本研究能支持按此拆分观察对象，不能估算这项改动的收益。

敏感性分析将每个“代理 × 仓库”最多保留五条，余 1,166 项；合并 736（63.1%），有个人正式决定 250（21.4%）。与未截对照的样本占比 63.3%、21.6% 接近，但此限制把 Devin 从 300 条压至 70 条、Jules 从 45 条压至 11 条，所以不能掩盖单代理仓库集中带来的外推局限。这个敏感性比例没有加权，不与上面的二月总体估计直接相减。

## 可复算与数据最小化

固定上游版本、预登记校验值及列区块摘要在 [摄取清单](raw/ranges.json)。只请求三份 Parquet 的 131 个必要列区块（64,236,126 字节）及文件尾元数据，未读取 PR 标题、正文、评论正文、diff 或仓库 URL。另有 upstream 文件树及原始 README。所有发布的明细仅含散列 PR/仓库标识、代理标签、相对排序与计数状态；无账号和正文。PR 与仓库键属于可复算的公开标识散列，不能承诺不可逆识别。官方脚注提示，2026 年 10 月曾修复子资源每 PR 截断到 30 项的采集问题。补采内容可能晚于宣称的 3 月截止，本研究对评论和事件逐行过滤时间；无法撤回后续对状态的编辑。

- 只复算派生表：在本目录运行 `python verify.py`，不需联网；用 [最小化样本](tables/sample-minimal.csv) 可复算按 agent、仓库截限和事件类目。
- 从官方数据复算：按 [运行说明](README.md) 下载同一 SHA 的必要字节，再执行 analyze.py、verify.py、report.py。依赖版本与数据文件摘要见 [manifest](manifest.json)。
'''
(P/'result.md').write_text(res,'utf8')
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
man={'revision':'b8dc67df93e7c11f6f20c84129db7232eb1ec253','retrieved_utc':json.loads((P/'raw/ranges.json').read_text('utf8'))['completed_utc'],'versions':{'python':platform.python_version(),'pandas':pd.__version__,'pyarrow':pa.__version__},'artifacts':{f.relative_to(P).as_posix():digest(f)for f in sorted([*(P/'raw').glob('*'),*(P/'tables').glob('*'),*P.glob('*.py'),P/'preregister.md',P/'audit.json',P/'result.md',P/'README.md']) if f.is_file()}}
(P/'manifest.json').write_text(json.dumps(man,indent=2),'utf8')
