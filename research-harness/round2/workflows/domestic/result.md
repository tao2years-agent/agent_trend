# 国内直接候选：五个产品如何接管任务、确认计划和接入原有门禁

基线 2026-11-20。这里的“国内”按有中文官方产品与面向国内团队的入口选取，不推断数据驻留、模型来源、私有化资格或集团采购条款。复核了 5 个厂商产品的 22 份官方原文。没有使用生产凭据、安装 CLI、启动商业会话或现场测试。下表沿用全球组的三个场景：A 为定时维护的权限变化与重复执行，B 为跨仓迁移与负责人交接，C 为评审拥堵与合并约束。表内“可验证”指官网给出了明确操作或输出；不代表本次已测。

| 产品、形态与可得性 | A．人何时能叫停、换权限 | B．计划与迁移交付物 | C．怎样进入现有合并门禁 | 尚缺的采购证据 |
|---|---|---|---|---|
| **Qoder**；旧 Qoder IDE Quest 视窗已退，现行 Qoder 是官方迁移目标；Editor 窗另行保留 | 新 Qoder 默认 Ask every time，但工作区内读写仍可自动运行；运行命令或改工作区外文件等有另一套条件。旧 Quest 的暂停/恢复说明只描述旧窗 | 新 Qoder 的 `/plan` 允许人复核目标、涉及文件、风险与验证；Review 可按 last turn、未提交或已暂存范围审查，逐文件撤改或暂存 | 从 Review 选择 commit/push，将实质代码交给 Git 托管平台。旧 Quest 具备创建 PR 的说明，不能拿来证明新入口的必检语义 | 建议撤销已有会话凭据后重试、核对并行任务的 staged 变更。没有验证原企业门禁、定时幂等或 12 仓统一对账 |
| **腾讯 CodeBuddy Code Agent Teams**；终端团队模式，codebuddy CLI 可另配 GitLab CI 作业 | v2.95.0 支持 lead 发起关停握手，默认 15 秒未响应则强制终止成员进程。v2.140.0 修复主回合结束但成员仍运行时停止键被吞、取消误及其他会话的情况 | 领导可要求成员先出方案，成员可被退回继续规划；lead 端的计划审批有别于工具权限批准。共享任务表记录依赖与状态，成员可直接互发消息 | 独立 GitLab CI 接入使用 runner、CI 凭据和配置，通过 MR 交付供原有分支保护与评审。单个本地任务显示 completed 不能充当绿灯 | 需证明终止后外部写入是否继续、12 仓是否共用可信台账，以及团队计划批准是否关联最终 SHA |
| **华为云码道 CodeArts 代码智能体**；IDE、企业控制台和小程序是不同入口 | IDE 26.10.0+ 的内置智能体/AgentTeam 可用 `/goal`。暂停会让正在进行的迭代步骤执行完，再停自动循环。退出小程序不会中止云端任务 | 规范开发先产出可修改的 `spec.md`、`design.md`、`tasks.md`，再运行 `/sdd-apply`。这些文件可按仓库流程审阅 | 官方最佳实践给出开发人员在代码托管端创建 MR、Committer 审核合入的路径。由托管端设置的授权与检查决定能否合入 | 计划能改不等于禁止未批准实施。需测当前迭代仍可能完成哪些写入；未核验可由企业控制台对在途任务即时撤权 |
| **阿里云云效 Codeup 代码评审 AI 助手**；已有 Codeup 的组织按产品条件开通，可按目标分支等设置触发 | 自动触发可按目标分支筛选，评审可从 MR 中发起。关闭今后触发与取消当前在途评审是不同操作，后者尚无本组证据 | AI 对变更及提交说明给出建议；可以组织级配置规则或启用评审记忆。适合作为迁移 PR 的复核环节，所查材料没有证明其生成 12 仓变更 | AI 行内意见、人工“通过/暂不通过/仅评论”和自动检测结果是不同对象。代码检测要同时设阈值和保护分支的必检任务，才成为相应硬门禁 | 需测 AI 行评是否进入“待解决”卡点、更新 head 后意见是否仍有效。不能把每条模型建议都算作硬阻断，也不能用评论数代替质量 |
| **TRAE**；TRAE SOLO 先升级为 TraeWork，后与 TraeCode 融合为统一 TRAE；旧企业授权页有专属域名限制 | Handoff 要求任务完成或先手动停止。在接续开始前取消不改状态；开始后中断不自动回退所有已执行步骤，重试时重新核验代码、权限与任务 | 本地与云端同分支分歧时可选 AI 处理或明确保留一侧；部分路径创建备份分支，涉及本地未提交修改时可生成提交。接续不是实时搬运一个运行中的任务 | 企业 TraeWork 桌面/网页 GitHub 集成支持发起 PR。该文档指出通过专属域名登录时不能直接完成 GitHub 授权；升级后的身份与连接范围需在租户重新验证 | 没有证明 Handoff 覆盖任意 Git 托管、能够复原外部副作用或把多库状态对齐成发布批次。需对照迁移前后审批与审计归属 |

## 三个会改变采购路径的发现

**先淘汰已退入口，保留可验证的下一代路径。** Qoder 的通知既列出 2026-10-15 23:59（UTC+8）退场，也提示存量用户分批关闭；个别旧租户今天仍看得到按钮，不能证明新用户能采购这个入口。官方指引在新应用导入数据并重新连接手机设备，账户订阅同步不能替代一次运行中审批的复核。TRAE 的 2026-06-09 v0.1.18 更新将 SOLO 改为 TraeWork 并支持企业版账号登录，其后官方再提供与 TraeCode 融合为统一 TRAE 的迁移说明。对两者都应要求在新安装、新租户、受限角色下演示，先区分历史材料、现行入口与原有 Git 凭据。[Qoder 退场通知](https://docs.qoder.com/release-notes/quest-retirement-notice) · [新 Qoder 计划模式](https://docs.qoder.com/qoder/plan-driven) · [TRAE 版本记录](https://docs.trae.cn/work_changelog) · [TRAE 融合迁移](https://docs.trae.cn/work_traework-to-traecode-data-migration)

**“停止”至少有三个不同的落地时机。** 腾讯文档针对成员进程有等待确认和超时终止，并有跨会话影响的具体修复；华为 `/goal` 的暂停发生在当前迭代完成之后；TRAE 的接续中断允许留下已经完成的步骤。用一个无生产数据的工单替身验证：在工单已创建、回执尚未写回时停止，记录点击、进程结束、最后一次外部写入、重新执行时的业务键和实际工单数。只看到界面变灰不算通过。[CodeBuddy v2.95.0](https://www.codebuddy.cn/docs/cli/release-notes/v2.95.0) · [CodeBuddy v2.140.0](https://www.codebuddy.cn/docs/cli/release-notes/v2.140.0) · [码道 /goal](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0070.html) · [TRAE Handoff](https://docs.trae.cn/ide_handoff?lang=zh)

**已有代码平台应优先比较最短的验证路径。** 既有 GitLab 的团队可用同一 MR 对比腾讯 CLI 作业与原流水线：参与计划审批的人、发起 GitLab 写入的令牌、最终验收提交分别是谁。已有 CodeArts Repo 的团队用 spec/design/tasks 对应变更后再让 Committer 审核。已有 Codeup 的团队可先只收集建议，再只将可复核的检测项纳入保护分支；将“模型未指出问题”“人工同意”“自动检测通过”分别统计，观察哪些步骤实际改变合并结果。对有硬门禁要求的采购，只要新增一次 push 后仍能沿用与旧 SHA 对应的批准，就退回试点查清依据。[腾讯 GitLab CI 接入](https://www.codebuddy.cn/docs/cli/gitlab-ci-cd) · [华为 CodeArts Repo 合并实例](https://support.huaweicloud.com/bestpractice-codeartsagent/codeartsagent_bp_0019.html) · [云效 AI 评审](https://help.aliyun.com/zh/yunxiao/user-guide/ai-intelligent-code-review) · [云效保护分支与检测阈值](https://help.aliyun.com/zh/yunxiao/user-guide/using-the-code-detection-service)

## 来源与覆盖

[来源注册表](sources.json)记录每份有效原文的地址、原始字节、SHA256、抓取时间、定位和能确认的事件时间。Qoder 对照 CN01–04、CN21–22；腾讯 CN05–08；华为 CN09–13；云效 CN14–16；TRAE CN17–20。首次请求收到的五份华为站点验证页单独保留为[失败记录](retrieval-failures.json)，没有算入有效证据；随后重新获取并检查了有正文的原始页面。华为的 26.10.0 是该功能最低适用版本，帮助页更新时间不推定为发布日期。腾讯两份材料直接对应版本号，未用网页抓取时间代替发版日期。

