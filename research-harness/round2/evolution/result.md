# 六条产品线的版本复盘

截至 2026-11-20，最容易改变采购判断的三种更新是：工具失败究竟是否传到合并检查，审批过的对象发生变化后是否仍能执行，以及工程师点击结束之后系统是否还在运行。这三项在窗口中都有可定位的变化。单看当前功能清单，会把托管产品的自审设置算给开源产品，也会把有明确前身的自动化能力记成第一次出现。

## 窗口与分母

按 2026-05-01 至 2026-11-20（起止均包含）筛发布单元。选了 5 条仍可使用的产品线与 1 个退场案例，涉及渐进发布、基础设施变更、代码审查、批量迁移、托管代理。Sourcegraph 以公开 CLI 发布为版本分母，云端更新仅作对照。GitHub 单元是发布页的发布时间，含预发布；云产品单元是官方页面上一个有日期的公告或更新组。相同日期可以有多个 GitHub 版本，一个 Devin 更新组可以包含多项变化。113 是不同单位的人工工作量分母，不能用于比较厂商发版速度。

|产品|边界和停止条件|窗口单元|进入时间线|研究聚焦|
|---|---|---:|---:|---|
|Argo Rollouts|GitHub Releases 第 1 页，读到 3/20；窗口内含 2 个 RC|9|4|中止后的控制器状态、值班入口的默认地址及其回补|
|Atlantis|第 1–2 页，第二页读到 4/21 及更早版本|11|5|重新计划后的审批、锁服务失联、已批准计划的完整性|
|PR-Agent|第 1–3 页，第三页读到 4/2 及更早版本|21|6|评审结果能否进入门禁、失败与自审谁负责|
|Sourcegraph Batch Changes 的 src-cli|第 1 页末条 4/30；窗口内含 1 个 RC|9|4|批执行边界、可移除的内部命令|
|Devin|《2026》页共 85 个有日期的更新组，5/1–11/16 共 62 组|62|8|评审触发、运行中策略、预检、停止和已读/完成|
|Jules|单页共 45 条带日期公告；窗口内只出现 10/29 一条|1|1|退场公告、导出和实际切换日期|
|合计|GitHub 7 页、两份官方完整日志页|113|28|3 个 RC 计入分母，只有与主题相关者进入时间线|

已逐条解析上述发布单元正文。每个产品先围绕一条具体的控制问题设置检索式，再复读命中条目的上下文、去除无关解释并对照具体改动。本轮保留 28 项，其中有 3 个维护分支 tag 对应同一次默认值调整，还有 1 项项目自身的托管机器人配置，特别保留用于纠错。其余 85 个单元未命中收窄后的专题筛选。这个数字不能解释成这些版本毫无研究价值。[113 项筛查台账](screening.csv) · [筛选规则与计数](coverage.json) · [28 项逐条时间线](timeline.csv)

## 四次逐 tag 的源码对照

以下均在临时 Git 仓库取两个公开 tag，解析到 commit 后执行限定文件路径的 git diff。PR diff 则用于识别相邻 tag 内其他同时发生的改动。没有使用线上客户仓库、云账户或生产故障演练。[含完整 commit 和 SHA-256 的对照注册表](tag-diffs.json)

|产品、tag 与文件|旧版与新版的可见差异|怎样影响验收|
|---|---|---|
|Atlantis v0.44.0 → v0.44.1，server/events/apply_command_runner.go|旧路径记录警告并依赖回退标志；新版在检查全局锁出错时设 CommandHasErrors，尝试更新失败状态和发表评论，随即 return。|断开锁存储后，同时断言计划未执行、调用方能看到失败。评论写失败也要核对执行结果。[本地 diff](diffs/atlantis-v0.44.0--v0.44.1.diff) · [PR 6533](https://github.com/runatlantis/atlantis/pull/6533)|
|PR-Agent v0.46.0 → v0.47.0，pr_agent/servers/github_action_runner.py|新增按次初始化的运行结果和 _fail_on_recorded_tool_error，默认检查工具已记录的失败。主机可选择旧行为。|7 月已有 GitHub Checks 出口，10 月才发布本次特定失败路径的语义。验收时应制造评审工具故障，检查 Action 是否失败，同时核对分支是否将该项列为必需。[本地 diff](diffs/pr-agent-v0.46.0--v0.47.0.diff) · [PR 3712](https://github.com/The-PR-Agent/pr-agent/pull/3712)|
|Argo Rollouts v1.10.0 → v1.10.1，pkg/kubectl-argo-rollouts/cmd/dashboard/dashboard.go|新 CLI 把 address 写入服务器选项，默认 127.0.0.1。对应 PR 同步改动服务器、部署清单和测试。1.8.5、1.9.2、1.10.1 三条支线均在 10/12 发布该回补。|维护分支升级也可能让自定义 Service 后面的值班面板不可达；验收应从实际值班网络打开，而非只看 Pod 就绪。[本地 diff](diffs/argo-v1.10.0--v1.10.1.diff) · [PR 5098](https://github.com/argoproj/argo-rollouts/pull/5098)|
|Sourcegraph src-cli 8.0.0 → 8.2.0，cmd/src/batch_exec.go|旧文件明确标内部使用，用执行器参数运行原始批计划；新 tag 的文件树已无此项。PR 也移除了相关执行器路径，当前公开 preview、apply 各有实现。|脚本若使用内部 exec 需重新验证。不能据这条 11/11 日志将整个 Batch Changes 产品判为已下线。[本地 diff](diffs/src-cli-8.0.0--8.2.0.diff) · [PR 1381](https://github.com/sourcegraph/src-cli/pull/1381)|

## 三处需要纠正的历史叙事

**自审设置属于哪一个实现。** PR-Agent 6/21 的 v0.37.0 发布摘要含 Qodo 自审后批准。对应 PR 只改项目自己的 .pr_agent.toml，注释指明配置由独立托管机器人使用，新增键属于 review_agent 小节。11/7 的 v0.50.0 又删除了开源 pr_code_suggestions 下两个从未影响 /improve 的同名或相近设置。这是两条实现线。把它们接成“开源工具 6 月支持自批，11 月取消自批”，结论就会失真。[6 月项目配置 PR](https://github.com/The-PR-Agent/pr-agent/pull/2463) · [11 月移除无效设置的 PR](https://github.com/The-PR-Agent/pr-agent/pull/4598)

**同一云产品的公告日期和首次开放日期有距离。** Devin 9/9 记载 preflight 卡片与脚本编辑器改版，9/30 才详细说明在每次触发后、代理启动前运行脚本，可转换输入或跳过任务，11/2 又在介绍流程加入 Preflight 步骤。能定位的是 9/9 已存在界面，9/30 公开说明执行语义；首次向所有组织开放的日期仍未知。9/30 已提到 Mark done / Stop session 菜单，11/16 发布的具体变化是个人侧边栏把 Archive 改为 Mark done 且会话继续执行。不能把 11/16 写成代理第一次支持停止。[Devin 2026 发布记录](https://docs.devin.ai/release-notes/2026)

**功能文档仍能访问，服务已经转入只读。** Jules 的计划审批文档仍可阅读。10/29 公告要求在 11/11 之前完成原有会话，此后只读；12/31 是研究截止日之后的计划关闭日。采购候选按 11/20 的已公告阶段剔除，历史机制仍是可比材料。原有 GitHub 分支与 PR 留在 SCM，但任务配置、活动历史与会话补丁需要另行导出。[Jules 退场公告](https://jules.google/docs/changelog/#jules-turndown) · [计划审批文档](https://jules.google/docs/review-plan/)

## 加入采购验收的三个版本测试

1. **已批准的对象发生变化。** Atlantis v0.44.0 的可选 sticky approval 比较策略工具提取的条目，v0.48.0 又要求使用校验后的 managed-plan 快照。分别构造策略输出新增条目、原有批准后 plan 被替换这两种情况，检查是否拒绝并要求复审；录下审批者、计划摘要与实际执行摘要。[v0.44.0](https://github.com/runatlantis/atlantis/releases/tag/v0.44.0) · [v0.48.0](https://github.com/runatlantis/atlantis/releases/tag/v0.48.0)
2. **中止后外部状态是否收敛。** Argo 的 v1.10.0 修复处理灰度中止缩容等待期间副本数改变：控制器更新副本注解，同时保持当时的实例规模，以免下一轮只处理伸缩、跳过流量路由。试点时在中止等待期间改变期望副本数，分别记录中止事件、服务指向和实际流量恢复，三者时间允许不同。[修复 PR](https://github.com/argoproj/argo-rollouts/pull/4919)
3. **从组织监督到工程师收尾。** Devin 将逐 PR 的开关扩展成按账号、仓、文件等组合触发的规则，排除条件优先；后来又将自动修复自己的评审发现拆为单独设置。可用同一 PR 同时命中包含与排除规则，确认不产生自动评审，再验证手工评审、自动修复和 Mark done 对运行状态的各自影响。此处给出试验设计，未进行云端账户实测。[Devin 2026 发布记录](https://docs.devin.ai/release-notes/2026)

## 离线复核与证据边界

[原始发布索引](archive.json)记录分页地址与原文位置。[官方来源总账](sources.json)记录 29 份去重原始证据，含两份复用的正式日志、7 份分页、8 个官方 PR diff、7 份 tag 源文件及 5 份补充文档或源文件。新 tag 中已消失的 Sourcegraph 文件以 git ls-tree 空结果和删除 diff 作证，无虚构的空文件快照。PR 内出现的测试只证明维护者提交了这个断言，本研究的四次 git diff 均为静态核查。

在本目录运行 python ingest.py、python supplement.py、python compile.py 可从已经归档的源重建筛查、时间线和覆盖表。运行 python compare_tags.py 将从上游重新抓取 tag 并计算四个目标文件的 diff，再运行 compile.py 可检验摘要。重新联网解析标签若发现 commit 改变，应建立新的调查快照并与当前 tag-diffs.json 比对。时间线以公开日期计，无法推定私有部署实际升级、租户提前试用、全部服务端发布或未写入公告的日期。
