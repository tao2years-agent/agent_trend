# 三组同题工作流下的采购取舍

截至 2026-11-20。选取八个有现行商业产品材料的候选，额外保留 Google Jules 作为主动淘汰的生命周期对照。九个产品逐项回答同样三组问题，共 27 格。这是对产品合同、操作边界和失败路径的桌面研究。本轮没有商业租户、没有在九个产品上提交任务，也没有相对速度或准确率排名。候选中既有任务执行器，也有仅在某个采购场景可直接替代的评审、整合和批变更产品。

完整记录见 [27 格动作、证据、未知和改判条件](matrix.csv)，原始材料见 [45 条来源注册表](sources.json)。其中 23 份在本轮新增，包括三个 Sourcegraph CLI 固定提交文件；22 份复用上一轮已经固化的官方材料。表内 W 编号指新增快照，L 编号指沿用快照。每条注册表记录带 URL、本地路径、抓取时间与 SHA256。

## 固定任务，先约定什么算成功

| 情境 | 给所有厂商的同一输入与故障注入 | 可审计的验收条件 |
|---|---|---|
| A 定时维护 | 每天 09:00 对过期测试环境发一张维护工单。以环境 ID、过期日期与规则版本作为业务键。第一次外部写成功后模拟回执遗漏；重投同一事件，撤创建人访问，再撤工作服务账号访问，最后恢复。 | 外部系统对该业务键只有一个最终动作。若没有动作，应有重试或待办记录；运行日志能区分权限拒绝、重复、故障、外部已提交但回执丢失。在途与未来运行分别测量。 |
| B 跨仓迁移 | 12 个仓库更换同一内部 API，其中 2 个依赖前序包、1 个没有权限、1 个测试失败。迁移期间换负责人；第二轮把 1 个已开 PR 的仓移出范围。 | 逐仓登记基线、负责人、变更/PR 标识、测试、失败理由。可单仓重试，能解释移出范围的旧 PR 去向。代码和权限均无变化的仓不再创建重复 PR。 |
| C 评审拥堵 | 24 个 PR 分成有依赖的栈。一项 required check 始终失败，一项间歇失败，一项因路径未命中而跳过；评审通过后更新其中一个 PR 的 head。 | 能重建哪一版被批准、哪个组合被测、失败后谁重排。记录排队时间 P50/P90、CI 分钟/合并 PR、必须人工处理的次数、误阻断与漏放。先和现有队列比较，再改变批大小。 |

数量和工单故事是建议的试点输入，不是厂商公布的规模或本次实测数据。专用产品在非核心情境中只记真实可贡献的一步，不能从“未见证据”推断不支持。

## A：少发一张票与不会重发，是两个验收问题

Devin 的新增证据给出了本轮最具体的派发合同。Automation 的 Preflight 脚本可返回带 ID 的工作项，可选 version 表示同一实体的新一轮工作。无 ID 时采用内容哈希；若输出随时间改变，就可能再次派发。官方翻页示例把游标推进到已发出的最后一项，失败的执行不会被这份脚本自行重新发现。这能帮助消解重复事件，却留下“第一次已经写入还是没有写入”的外部对账问题。优先给 Devin 的试点任务，是同时证明重复派发、漏派、外部副作用三张账能对应上。[W03](https://docs.devin.ai/product-guides/automations.md)

GitLab 暴露另一种更容易漏测的差异。对适用的 runner flow，权限取发起人和服务账号的交集；定时 flow 是明确例外，仅受专属服务账号的角色限制。若企业要求“任务发起人离职，次日排程必定停止”，需要独立验证交接流程是否联动服务账号授权。19.6 的定时自动化于 11 月 19 日进入 beta，已有 19.2 GA 的 Custom Flows 不能用来证明排程也已达到相同成熟度。[W17](https://docs.gitlab.com/user/duo_agent_platform/composite_identity/) · [L12](https://about.gitlab.com/blog/gitlab-scheduled-automations/) · [L22](https://about.gitlab.com/press/releases/2026-07-16-gitlab-19-2-brings-governed-agentic-automation/)

还有三种不同的“首次执行”。Factory 创建已激活的远程定时自动化通常会立即运行，投递到既有 session 则等待计划时间；其本机执行依赖桌面程序处于运行状态。Antigravity 的 App 命令先保存 Paused，试运行可记录权限；无人值守时遇到本应询问的动作会拒绝。GitHub 支持个人与共享排程，部分 GitHub App 生成的事件会被过滤，提升 App 的写权限也不会让这些事件成为触发源。若入参换了发起身份，业务就可能完全不启动。[W01](https://docs.factory.com/workstreams/automations.md) · [W02](https://docs.factory.com/droid-cli/cli-reference.md) · [W05](https://antigravity.google/docs/commands/automation) · [W06](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-automations)

## B：能看到 12 个仓与能处理 12 个变更，是不同能力

对于可明确写出匹配规则的迁移，先测 Sourcegraph Batch Changes。经典 spec 的目标缩小时，已发布且不再匹配的 changeset 会随 re-apply 被关闭和归档；这是会改变外部状态的动作。公开 CLI 源码显示 preview 和 apply 将同一执行路径的 `applyBatchSpec` 分别设置为 false 和 true；公共代码在创建预览 URL 后，依据标志决定返回或继续应用。团队若要求“必须经人审核”，应控制谁可走 apply 入口，仅能打开 preview 页面不足以证明此门禁存在。[W09](https://sourcegraph.com/docs/batch-changes/faq) · [W20](https://github.com/sourcegraph/src-cli/blob/f2901d14d2db58c4f25d0f73736805e01b14f502/cmd/src/batch_apply.go) · [W22](https://github.com/sourcegraph/src-cli/blob/f2901d14d2db58c4f25d0f73736805e01b14f502/cmd/src/batch_preview.go) · [W23](https://github.com/sourcegraph/src-cli/blob/f2901d14d2db58c4f25d0f73736805e01b14f502/cmd/src/batch_common.go)

Agentic Batch Changes 是另一操作面。11 月 2 日版本将 workspace 执行移到后台，使人可在运行中继续交流、让 agent 调查已失败的一项；该更新当时标注只在 Cloud 可用。11 月 9 日加入 thread 移交：要求 agent 空闲后才能完成，新 owner 使用自己的仓库权限和凭据，不可见的 workspace 会被隐藏。相同更新还增加提出合并、点击 Allow 后后台执行并报告各项成败的交互。经典 CLI 的代码证据只证明 CLI 分支，不能替代 Agentic 服务端验证。[W12](https://sourcegraph.com/changelog/agentic-batch-changes-workspace-continuation) · [W11](https://sourcegraph.com/changelog/2026-11-09)

GitHub cloud agent 也必须区分执行面。6 月 2 日的自动化发布说明把排程作用域放在单一仓库。10 月 28 日 cloud sandbox 与新云端体验达到 GA。当前文档载明 Actions-based session 仅写指定仓库，cloud sandbox 可以在同一组织跨仓工作，但两种环境仍限一任务、一分支、一个 PR。要交付 12 个独立 PR，应核实能否分配和跟踪 12 个任务；不能拿多仓上下文直接当作迁移台账。相反，若有硬性的自托管 runner 条件，也不能把云沙箱的多仓功能直接归给 Actions-based session。[W08](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/) · [W21](https://github.blog/changelog/2026-10-28-work-from-anywhere-with-a-new-connected-copilot-cloud-experience/) · [W07](https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/copilot-surfaces/copilot-on-github)

若迁移需要探索设计、实现变化较大，再把 Factory 的里程碑验收与 Devin 的持续目标分解加入对照。前者要展示恢复后确实执行遗留验证，后者要展示失败仓、待补授权与旧 PR 的归属。两者均不能只展示“全部 worker 完成”。[L03](https://docs.factory.com/changelog/release-notes.md) · [L04](https://docs.devin.ai/work-with-devin/bots.md)

## C：先定位等待发生在哪里

若作者等待重复的人肉规范检查，则先用 CodeRabbit 影子评审。2026 年 3 月 11 日发布说明示范了 V2 风格的 YAML；当前文档明确 V3 删除部分内置检查和 `pre_merge_checks` YAML 节点。GitHub Check Run 被发布后，还要在仓库规则里设为 required。修改定义 ID 或目录域可能改变检查身份，未命中路径、跳过评审、根本没收到 webhook 也需要分别核对。记录每一次真正阻止合并的规则，不以“机器人回了评论”作为上线标准。[L16](https://www.coderabbit.ai/blog/pre-merge-checks-built-in-and-custom-pr-enforced) · [L14](https://docs.coderabbit.ai/pr-reviews/pre-merge-checks) · [W16](https://kb.coderabbit.ai/articles/1442026547-troubleshoot-why-coderabbit-reviews-might-not-trigger)

若等待发生在 PR 已审之后，则把预算放在整合试验。Graphite 按 stack 或批进行并行与推测 CI，前序失败会使后续组合失效，能从失败批里再测试子集。对此指标要同时看排队时长与重复 CI 分钟。Sourcegraph 的 rollout windows 可以节流 changeset 发布和部分协调动作，但批量评论、合并、关闭一同执行，不能把一次批合并耗时估计为窗口逐项限速。两种机制解决不同的等待成因。Graphite 在 10 月 30 日曾发生持续 15 小时 20 分钟的合并故障，演练还应覆盖外部队列暂时不可用。[L17](https://graphite.com/docs/merge-queue-optimizations.md) · [L18](https://status.graphite.com/history/1) · [W10](https://sourcegraph.com/docs/admin/config/batch-changes)

## 先淘汰谁、何时改判

| 采购条件 | 首轮留谁与先淘汰谁 | 会改变结论的证据 |
|---|---|---|
| 必须每天无人值守维护，且能区分重放与修复 | 先试 Devin Preflight。已有 GitLab 的组织可加入 Duo，前提是接受 beta 和独立服务身份。Graphite、CodeRabbit 从主执行器候选退出。 | 如果任一专用评审/队列产品能在相同故障中给出受控执行、幂等写入和可审计恢复，就重新纳入。若留存候选一次重复写且无法对账，也应退出自动写入试点。 |
| 变更可声明且有范围移交，12 仓必须逐仓追账 | 优先 Sourcegraph；Factory/Devin 用于更需探索的子集。要求一次任务交付 12 个独立 PR 时，先淘汰单个 Copilot cloud session 的方案。 | 展示外部批次编排可完整对账、授权变更后不越权、新基线不会复用旧验收时，可重新评估多任务 Copilot；若 Sourcegraph 无法保留被收缩范围的审批和对账记录，也应调换顺序。 |
| 客户必须在离线或自托管执行环境内完成 | 将 GitHub Actions、GitHub cloud sandbox、Factory 本机/云机分别报价和试验；不把仅验证云端的能力作为可迁移依据。 | 提供本部署形态的产品支持范围，并在断联、令牌更新和 worker 重启下保持同样的证据链。 |
| 已有足够 PR，但合并排队 | 等待必检建议时先试 CodeRabbit，等待已绿组合时先试 Graphite。Devin Needs you、Antigravity 录屏保留作人工监督补件；不替代队列。 | 使用完全相同的 PR 时间线，若现有原生队列在 P90、故障恢复、CI 成本上更好则不采购；若主要损耗发生在人工判定，则调回质量门禁试点。 |
| 投产后要求承接新任务 | Google Jules 退出。官方退场公告明确 11 月 11 日后只读、计划 12 月 31 日结束；旧文档中离开页面后可能自动批准，也不满足必须显式审批的历史用例。 | 新的正式可用声明、用户所属区域/套餐的实际权限，以及能够现场创建和撤销任务的证据。导出或他牌产品演示均不足。[W18](https://jules.google/docs/changelog/2026-10-29) · [L07](https://jules.google/docs/review-plan/) |

复查时优先对照 W03、W07、W17、W20/W22/W23 与 L14，分别覆盖“派发与成功”“跨仓与多 PR”“交互与排程身份”“可预览与强制批准”“发出检查与真实阻断”。它们是最容易被方案介绍合并成一句话、却会改变试点结果的五组条件。
