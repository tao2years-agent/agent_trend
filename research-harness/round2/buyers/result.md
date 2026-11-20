# 严格采购口径：35 个能接手研发工作的产品

统计日期为 2026-11-20。这里用 **35 个去重产品、10 个主采购任务** 回答“有哪些竞品”。其中 23 个复用已读证据，新增 12 个；它们可以接管的工作从产出代码补丁到排查线上事故，不能相加得出任一子市场的竞争者数量。把清单限制在能产出代码、PR、调查结论、合并结果、实际基础设施状态或发布判定的产品后，仍然达到 30 个。35 也不是对“最佳”、市场份额或真实 ROI 的排名。

[逐产品对照台账](ledger.csv)为每个产品列出触发、验收件、人的接管点、适用形态/版本和未证实边界；[证据注册表](sources.json)把表内编号映射到官方 URL、内容哈希与本地文件。此前的 [三组同题场景](../workflows/result.md) 和 [国内产品的批准与门禁对照](../workflows/domestic/result.md)继续保留；此处没有重抓它们的原文。

## 一项产品为什么能计数

1. **有人能采用。** 有公开可使用的商业服务、客户可启用的功能，或可自行运行的成品应用。付费平台上的公开测试功能注明适用客户与阶段。仅论文原型、正在退场的历史入口不计。
2. **有人能委派。** 已知哪个事件、命令、授权请求或人工操作会启动实际工作。仅为下游开发提供 API 库、存储、身份模型、运行时或仪表盘不够。
3. **有人能验收。** 有可独立核对的终点或证据，包括带来源的“原因不明”，不要求自动合并或自动改生产。单纯向模型发一段文本、提供通用遥测或等待人输入不足以计数。
4. **按真正可替换的任务比较。** 每个产品只有一个主采购任务；跨组能力在分析中说明。例如 GitLab 为 T2 计一次，其修复失败流水线的 flow 同时可作为 T10 的比选对象。SDK、CLI、Bot、扩展、连接器、企业版等同一工作产品的交付形态不重复计数。
5. **证据有上下文。** 35 项产品另经独立审稿，每项从快照或源码核验两条具体主张；日期、版本、权限和动作范围的修订已进入逐项表。[70 项主张的独立审稿](../buyer-audit/result.md) 本轮增加的 12 个产品均有至少两份官方正文，未对它们登录租户或运行试验。35 按产品计而非按独立母公司计。例如 Qoder 以开发工作台交付补丁，云效 Codeup 以 MR 评审服务交付意见，它们可以被独立采用，也不因为集团归属而被说成彼此直接竞争。

## 同一采购任务下，谁能替换谁

| 主采购任务 | 数量与计入产品 | 对照需要固定的验收条件 |
|---|---|---|
| T1．交给开发者工作台并获得可查补丁 | **9**。Aider、OpenAI Codex CLI、Cline、OpenCode、Qoder、腾讯 CodeBuddy Code、华为云码道、TRAE、Google Antigravity | 同一仓库、任务和隐藏回归测试；审核实际 Git 差异，记录审批与撤销后仍存的副作用。终端、IDE 与多端有不同采购前提。 |
| T2．委派项目或周期工程任务 | **6**。Factory Droid、Cognition Devin、GitLab Duo Agent Platform、GitHub Copilot cloud agent、Claude Code Scheduled tasks、goose | 相同业务键下的重复触发、任务取消后的外部写入、可追溯 PR。需要用户提供 recipe 的 goose 与可根据目标自行拆分的 Bot 有不同启动成本。 |
| T3．对组织中的一组仓库执行迁移 | **3**。Sourcegraph Batch Changes、Moderne Platform、AWS Transform custom | 输入相同清单、规则和未授权仓库，验收逐仓 diff、失败恢复与发布范围；能查多个仓库仅满足前置条件。 |
| T4．持续评审代码变更 | **4**。CodeRabbit、PR-Agent、云效 Codeup AI 评审、SonarQube Server | 同一组 PR 注入真实缺陷和无害改动。比较建议、规则判定及真正强制的 Git 门禁；确定性静态扫描与语义评审只在相同完成条件下可替代。 |
| T5．合并已评审的 PR | **2**。Graphite Merge Queue、Mergify | 给相同到达序列和一处 flaky test，测等待 P90、重复 CI 分钟和最新目标分支上的漏放。它们可与 T4 同时采用。 |
| T6．在推广中按指标决定是否继续 | **2**。Argo Rollouts、LaunchDarkly Guarded Rollouts | 条件限定为同一业务指标和预设恶化。前者控制 Kubernetes workload，后者控制 flag variation。两者只有在两条路径都能控制目标用户暴露时才形成替代。 |
| T7．将基础设施计划安全地应用 | **2**。Atlantis、Spacelift | 让计划变化、基线过期或竞争 PR 同时出现，核对审批者、计划摘要与实际 apply；生产凭据由组织自行控制。 |
| T8．维护依赖并交付升级 PR | **2**。Renovate、Snyk Open Source | 用双方支持的同一语言生态，分别测已知漏洞和仅有新版本的依赖；评估开放 PR 上限、回归及最终合并权。 |
| T9．分诊线上告警或异常 | **4**。incident.io Investigations、Rootly AI SRE、Datadog Bits Investigation、Sentry Seer | 由人工事后归因作为参照，混入需明确报“无法判定”的事故。前三项可比较跨遥测调查；Seer 在已有 Sentry issue 和代码关联时与它们重叠，并可继续生成补丁。 |
| T10．用失败 CI 上下文产生修复候选 | **1 主计数＋1 跨组候选**。CircleCI Chunk；另一项 GitLab Duo 的 Fix CI/CD Pipeline 已在 T2 去重 | 比较失败日志、定位原因、修复后的 CI 结果，以及工程师是否可决定合入。若企业不能更换 CI，这两条通常是平台内置选择，不能当作没有迁移代价的替代。 |

## 新增产品的证据如何改变选型

**无人值守的 CI 修复与线上事故调查分开验收。** CircleCI 在 2026-02-27 为失败 job 提供直达 Chunk 的入口，上下文由流水线送入。其 Cloud 文档仍标 beta，修复按钮依赖相应的 GitHub App 和组织类型；任务可产出 PR，人应重跑原作业后再决定合并。Sentry 的 Seer 则由一个具体 issue 发起，默认停在 root cause，续跑首选 sentry_run_id（UUID），旧数值 run_id 仅兼容；可进一步产生方案、代码和 PR。状态查询端点标示 experimental。只演示 PR 被创建，无法证明 CI 故障已修，也无法证明线上异常不再复现。[CircleCI 工作流](https://circleci.com/docs/guides/toolkit/chunk-setup-and-overview/) · [CircleCI 入口变更](https://circleci.com/changelog/chunk-fix-job-pipelines-page-job-page/) · [Seer 停止点](https://docs.sentry.io/api/seer/start-seer-issue-fix/) · [Seer 状态接口](https://docs.sentry.io/api/seer/retrieve-seer-issue-fix-state/)

**采购 SRE 分诊时，要买到“有根据地不知道”。** Rootly 可以由值班人启动，或由已启用的规则对新告警自动运行。它提供结论、证据、置信级别或 Inconclusive/Blocked；原生工具不能回滚或重启。自动调查会使用团队凭据调用连接器及 Private Agent，某些配置允许外部写入，试点需逐连接器检查实际能力。Datadog Bits 在多个遥测源之间验证假设，证据不足时也能报告 inconclusive；人工纠正还可形成后续调查可选择的 memory，对应新增了维护与删除该知识的责任。incident.io 的 2026-01-15 更新给了独立例子：此前机器人偏重有时间相关性的监控尖峰，更新后更重视频道中由人证实的原因及对应 PR。这个厂商自己的案例可作为试题设计线索，不是准确率测量。对照组应包含观测缺失、变更与告警时间碰巧重合、和值班人提出错误初猜的事故。[Rootly 无人值守访问文档](https://docs.rootly.com/ai/ai-sre/running-an-investigation) · [Rootly 的调查结果](https://docs.rootly.com/ai/ai-sre/reading-the-result) · [Datadog 调查流程](https://docs.datadoghq.com/bits_ai/bits_investigation/investigate_issues/) · [Bits 的人工纠正](https://docs.datadoghq.com/bits_ai/bits_ai_sre/help_bits_learn/) · [incident.io 发布记录](https://incident.io/changelog/a-faster-smarter-incident)

**大规模迁移的验收件是覆盖台账。** Moderne 的 recipe dry run 不立即改库，而是先为所选组织产生逐仓 diff；人再选择开 PR、直接提交等。SaaS v2 对不同规模组织使用不同运行队列，跨仓活动 Changelog 可按条件开启，不能假设所有租户默认具备。AWS Transform custom 在 2025-12-01 GA，组织可重复使用 transformation definition，由 CLI 或流水线触发；变更结果、团队反馈与留存的 learning 需要分别审查。Sourcegraph 则具有明确的 re-apply 语义：重新计算范围后，原有已发布的 changeset 可能被关闭并归档。因此三者要用同一份列有排除库、失败库、已开 PR 和基线版本的清单验收，不能按生成代码量购买。[Moderne dry run](https://docs.moderne.io/user-documentation/moderne-platform/getting-started/running-your-first-recipe/) · [Moderne v2 差异](https://docs.moderne.io/releases/saas-v2-changes/) · [AWS Transform GA](https://aws.amazon.com/about-aws/whats-new/2025/12/transform-custom-organization-wide-modernization/) · [AWS 自定义定义](https://docs.aws.amazon.com/transform/latest/userguide/custom.html) · [Sourcegraph 范围收缩语义](https://sourcegraph.com/docs/batch-changes/faq)

**机器人评论、质量状态、队列与发布验证对应四种终点。** SonarQube Server 的 PR 分析从 Developer Edition 起，在已记录版本中只应用新代码的质量条件；要阻止 GitHub 合并还需将 SonarQube 状态设为 required。Mergify 接在其后：批次失败或超时时可拆分以找出问题 PR，取消依赖旧组合的后续测试；达到指定拆分上限仍未排除者也会出队。LaunchDarkly 在生产流量侧判断新旧 variation，11/20 的定价页把这项权益列入 Release Autopilot，旧 Guardian FAQ 与新套餐的资格差异应按实际合同核对；错误率指标如果误配为“越高越好”，增长反而不会被视为恶化。对前者测漏检与误阻，对队列测重排和 CI 成本，对后者测指标方向、流量、回退时序，各自的“成功率”不能汇总为相同 KPI。[SonarQube PR 分析](https://docs.sonarsource.com/sonarqube-server/2025.1/analyzing-source-code/pull-request-analysis/introduction) · [GitHub 必检配置](https://docs.sonarsource.com/sonarqube-server/2025.6/devops-platform-integration/github-integration/setting-up-at-project-level) · [Mergify 失败批次](https://docs.mergify.com/merge-queue/batches/) · [LaunchDarkly 指标方向](https://launchdarkly.com/docs/integrations/monitoring/error-events) · [新旧发布权益](../economics/result.md)

**基础设施与依赖更新都涉及授权，但实际控制项不同。** Atlantis 的新 plan 哈希限制应用时替换产物。Spacelift 以 tracked run 表达 planning、unconfirmed、confirmed 和实际 applying；autodeploy 与 plan policy 的配置决定是否经过相应人工审核。依赖更新则应比较什么条件会新开 PR，例如 Snyk 自动修复已知问题与主动升级到新版本是两个触发，能限制同时开放的升级 PR；Renovate 能按更新类别、时段、检查、保护分支与合并队列处理。Snyk 和 Mergify 的官方组合案例很直观：一家生成升级 PR，另一家管理多个 PR 的整合，购买两者不表示重复购买同一工作。[Spacelift 生命周期](https://docs.spacelift.io/concepts/run/tracked) · [Spacelift 审批策略](https://docs.spacelift.io/concepts/policy/approval-policy) · [Snyk 两类 PR](https://github.com/snyk/user-docs/blob/main/scan-fix-and-prevent/README.md) · [Snyk 与 Mergify 的职责划分](https://snyk.io/blog/dependency-updates-mergify-snyk/)

## 未计数样本，以及阈值敏感性

- OpenHands Software Agent SDK、Claude Agent SDK、Temporal Python SDK 和 LangGraph 仍是有效机制证据；单独交付 SDK 要让团队再做一层产品，故不计成品竞品。没有由此推断同一品牌的其他成品不存在。
- GitHub Actions Runner、Buildkite Agent、Jenkins Input Step、Conftest、OpenFeature flagd 与 OpenTelemetry Collector 不占名额。它们分别承担执行、等待、检查、控制或采集的一环，能支持上述产品，但本轮核对的是组件接口。
- SWE-agent、mini-SWE-agent 和其他研究原型留在研究与实现参照中。Jules 已进入只读，不作为新采购候选。Qoder 的旧 Quest 窗、TRAE SOLO/TraeWork、Devin 的 Bot 与 cloud session、Sourcegraph 的界面与 CLI 都不另计。
- 分析度量平台、仅提供计量的 dashboard、论文中的 benchmark 没有被加进 35 个。把“部署一套新 SDK”或“展示团队分数”当作交付的团队，可以另立采购任务重筛，但应另报分母。
- 进一步保守地拿掉 beta 的 CircleCI Chunk，全表为 **34**；若进一步只认外部可核对的最终业务产物、不接受纯事故调查报告，剔除 incident.io、Rootly 和 Datadog 三例，仍有 **31**。这里解释统计对边界的敏感度，不主张三类调查产品没有业务价值。

## 复算

运行 `python compile.py` 从既有台账、已固定的国内/全球快照及 [本轮新增清单](fresh.json) 生成 CSV 与来源注册表。脚本检查每种产品至少两条证据编号、唯一名称、全部原始快照哈希和主采购任务数。运行 `python ingest.py` 只能更新本轮新增来源；原文按内容摘要命名，变化会产生新快照。既有材料继续使用原项目账本的时间、版本和相对位置。

35 项由 23 条既有产品案例加 12 个新增产品构成，首次采购盘点引用 123 个不同本地快照路径，其中新增 26 份。11/20 回查 BUY26 的新套餐与定价交叉表，再纳入两份独立官方原页，当前版本共引用 **125 个不同本地快照路径**。路径数不等于独立样本数或独立作者数。第一轮和第二轮选定的少量运行实验仅支持各自的具体机制，不能被解释为这 35 个产品进行了同场跑分。
