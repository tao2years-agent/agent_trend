# 采购对象的源码看到哪一层

研究截止 2026-11-20。对 35 个购买候选逐项核对公开代码，能指向 **10 项直接交付产品的具体核心模块**，其中 9 个来自首轮同一采购对象，另一个是 GitLab Duo Workflow Service。Sentry Seer 另有真实宿主服务的交接记录可读。其余 24 项分别落在集成客户端 11、扩展示例 7、相邻实现 3、对应实现未核到 3。这里的单位是购买项。10 也只表示读到相关模块，不能据此推定完整服务开放、租户采用相同版本，或持有可再分发权利。逐项结论、未核事项和验收动作均在同一台账。[35 项台账](ledger.csv) · [互斥分层复算](coverage.json) · [原采购口径](../buyers/result.md)

**采购前最容易漏查的是状态属于谁。** GitLab 中供画布显示的节点已结束，可以与仍在等待用户输入同时成立。Argo 中的暂停可以因计时到期自行结束。Sentry 宿主已写入交接状态后，另一服务仍可能没有承认该代理。合同要求“能接管”时，应写清用户看的是申请、工具调用、控制器还是下游实体，撤回后在哪个系统检查持久结果。下面各项给出可以复查的判断分支。[GitLab 中断][gitlab] · [Argo 暂停][argo] · [Sentry 状态同步][sentry]

## 归属规则与旧证据如何复用

从采购台账逐项读取购买任务、发行形态和接受产物。然后固定供应方仓库的 commit、取完整文件并记录 SHA-256，检查文件在哪个运行单元被使用。产品内部 CLI、控制器或工作流服务中的实现归“核心模块”。另一服务为该产品保存的交接记录归“宿主侧子系统”。SDK、Terraform provider、旧版客户端归“集成客户端”。模板、插件清单、示范 hook 归“扩展示例”。同厂研究 CLI、单独基础引擎、不同版次归“相邻实现”。对不上时记录“未核到实现”，保留可用的文档证据与验收请求。归类适用本批资料，后续产品发布或获得供应商证明可以改判。[44 份固定仓库文件](sources.json) · [两份跨产品归属说明](attribution-docs.json) · [123 份原采购证据](../buyers/sources.json)

首轮 36 个已审源码对象中，9 个直接对应上述 35 项，6 个属于容易混淆的相邻对象，余下 21 个未对采购项做源码归属。GitHub Actions Runner 和 gh-aw 都不能补作 Copilot cloud agent 的服务端；Claude Agent SDK for Python 也没有覆盖云 Scheduled tasks 调度器。四个真实 tag 差分分别映射到 Atlantis 执行器、PR-Agent Actions 入口、Argo dashboard CLI、Sourcegraph 历史 src-cli。最后一组在 8.2.0 移除了对照文件；Argo 那组只涉及 dashboard 监听地址。即使表里品牌相同，也要保留差分涉及的层级。[36 项逐项对照](first-round-map.csv) · [4 组版本差分](diff-map.csv) · [版本变化原报告](../evolution/result.md)

## 五种直接候选的实际判断分支

以下五项均取自直接采购项的产品代码，本次所读文件补充了此前的 scheduler、automerge、分析控制器或产品文档。随附上游测试只代表维护者定义的断言；本次执行了 GitLab 的指定测试模块，其他四项按静态阅读记录。完整 SHA、文件路径、精确行号和定位标记在可复算的明细中。[24 个代码/测试行段](mechanisms.csv)

|采购候选和入口|实际判定和副作用|异常、反例及采购验收|
|---|---|---|
|Aider，GitRepo.commit，5dc9490bb3|指定文件时逐个 git add，再用路径限定 commit；未指定文件时传 -a。只有 git_commit_verify 关闭才加入 --no-verify。成功返回短 SHA 和消息。|add 失败会记录错误并继续构造命令；commit 抛出 Git 异常则记录错误并隐式返回 None。验收应在临时仓产生一次不通过的 hook 和一份无关改动，核正确认对象、返回值、实际提交。该函数没有检查远端合并规则。[提交实现][aider]|
|GitLab Duo，NodeLifecycleCallbackHandler，ed4ff29900|带 graph:step 标签且能识别组件才记录 STARTED。GraphInterrupt 记 ENDED，普通异常记 ERRORED。终止时按 run_id 弹出，重复或没打开的终止回调被忽略。另一个服务测试期望只收到一次 INPUT_REQUIRED checkpoint。|节点结束码自身无法区分正常结束和待输入。验收要同时观察业务状态和运行 ID，验证恢复后的新 ID；另查共享数据库或外部 PR 的写入回执。[状态处理][gitlab] · [通知用例][gitpause]|
|goose，process_inspection_results，ea5dded738|先按工具请求 ID 取权限检查器结论，缺失则进入待审批。随后叠加其他检查器结果，Deny 会把同一请求从通过和待批集合移除；后续 RequireApproval 先查拒绝集合。|维护者测试既有拒绝不能被待审批“复活”，并交换结果顺序。这个函数改变判定集合；对已经发送到后端的写入没有撤销语义。验收要分开记录调用前拒绝和调用后撤回。[判定入口][goose] · [优先级测试][goosetest]|
|Argo Rollouts，requiresManualAction、CompletedCanaryPauseStep，458eab520f|无法定论的分析/实验、无期限金丝雀暂停、显式关闭蓝绿自动晋升进人工路径；金丝雀条件清除且 ControllerPause 已设置，或已超过指定等待时长，均可结束当前暂停。|看到 pause 不能推断“必须一人批准”。用同一版本分别配置有时长和无时长暂停，直到流量观测和控制器状态均满足才记恢复；本次没有启动 Kubernetes 集群。[人工条件][argo] · [计时分支][argotime]|
|Renovate，getPrHourlyCount，c5b6ec78ab|读取宿主 PR 列表，排除 onboarding，按配置分支前缀和严格晚于本 UTC 整点过滤。普通读取异常记录错误后返回 0，ExternalHostError 原样上抛；相邻并发计数遍历已知分支。|0 既可能来自确实无新 PR，也可能来自读取故障。不能从计数 helper 断言整个系统放行或组织有严格总限额。用两个仓、边界时间和两类 API 错误验收，分别捕捉读数、日志与实际创建量。[小时计数][ren] · [故障测试][rentest]|

## GitLab 可复跑反例：直接调用正确，整张图仍可能断言失败

把 4 个同 SHA 上游文件放进临时目录，包含完整 test_node_lifecycle.py 以及它依赖的生产 callback、命名解析和常量。使用确定性的本地状态图与内存检查点，禁用追踪，无 GitLab 租户、模型调用或远端仓写入。相同 13 个上游测试函数，在原环境 LangGraph 0.2.71 / LangChain Core 0.3.34 下有 11 个通过，真实图流和中断恢复的事件序列断言失败。在隔离环境按上游锁文件安装 LangGraph 1.2.14、Core 1.7.7、checkpoint、prebuilt、SDK、pytest 与 pytest-asyncio 七个精确版本后，用同一逐函数驱动通过 13/13，改用原生 pytest 再通过 13/13。关联是整组依赖环境，未逐依赖二分根因；没有将第一次失败记成 GitLab 服务缺陷。[旧环境原始输出](gitlab-test-ambient.json) · [匹配版本同驱动](gitlab-test-locked-direct.json) · [匹配版本 pytest](gitlab-test-locked.json) · [复跑脚本](replay.py)

锁定环境的通过用例实际经历了 interrupt → 暂停 → Command(resume="yes")。第一次的 approval 已记录 ENDED，恢复后同名节点获得新的 run_id，随后进入 finalize。这证明了指定源码与依赖组合能在本地重现该状态转移。上面另引的 FakeExecutor INPUT_REQUIRED 通知用例只读了源码，本次未启动完整 Duo 服务执行它。用例也没有证明批准者身份与 commit 的绑定、云租户版本、远端写入一次性或取消后的补偿。[真实图测试][gitgraph] · [上游锁文件][lock]

## 哪些公开仓库只能回答半个采购问题

**调查交给编码代理。** Sentry 的 create_seer_run_coding_agent_handoff 按组织查运行，不存在则记日志并返回；存在则尝试保存提供方、代理 ID、状态和可得的仓标识。sync_coding_agent_status 先尝试保存本地状态，再按 provider 区分后续路径；在已有非 Cursor handoff 分支可以返回 known_to_seer=False。它说明客户可在哪里寻求关联回执，却没有暴露 Seer 调查模型如何选择根因。incident.io、Rootly、Datadog 的 Terraform provider 仅足以核对模板、工作流任务或 incident type。四家进入同一分诊试点时，应拿同一故障和同样的数据权限，分别要求原始证据、交接 ID、生成的工单或 PR，记录哪一步需要人做。[Sentry 状态同步][sentry] · [三家 provider 的定位](ledger.csv)

**PR 阻断。** PR-Agent 的版本差分可核实 GitHub Actions 入口对工具错误的处理，最终阻合并仍取决于分支规则。SonarQube Community Build 的实际门禁求值器遇缺失度量可用 fallback，小变更可按配置对特定条件记 OK，只要评估条件都未报 ERROR，汇总便为 OK，上游测试包括空门禁。其代码出处标明社区版；采购 SonarQube Server 时要在目标付费版重测同样案例。选择交互式评审或指标门禁取决于验收的是审阅发现、必需检查还是失败的合并。可把“没有任何规则命中”和“评审进程故障”分别送入候选，记录实际 mergeability。[求值器][sonar] · [社区版测试][sonartest] · [PR-Agent 的版本证据](../evolution/result.md)

**跨仓迁移。** OpenRewrite RecipeScheduler 的一个 cycle 依次 scan、generate、edit；到达最小轮次且无再次循环原因时结束，还受 maxCycles 和 PANIC 标志约束。能验证 recipe 为什么停，不能由此推出 Moderne 平台如何批量提交、撤回或限制并发。另一侧，Sourcegraph 历史本地执行路径在两个 tag 间被移除，用旧 CLI 源码评价现行服务器有同样问题。对这两家都应给一批可丢弃仓库，选一个仓故意产生冲突，分别验算接受/跳过/重试的变更集、审批者和第二次发布产生的 PR 数量。[OpenRewrite 迭代][moderne] · [Moderne 对产品关系的说明](https://moderne.ai/blog/overview-of-openrewrite-and-moderne) · [Sourcegraph 客户端差分](diff-map.csv)

**上线与恢复。** Argo Rollouts 可直接查清此版本计时或等待人工的条件；LaunchDarkly 的 Go server-side SDK 运行在应用服务进程，只能说明客户端如何消费开关，不提供 Guarded Rollouts 后端的指标判定代码。两者治理对象分别是工作负载/流量和功能开关，受影响的生产面也不同。验收宜预设相同用户可观察的故障结果，保留两套各自的目标版本、实际切换证据和恢复时钟。若同一应用采用两者，两份证据可以互补。[Argo 的判断][argo] · [采购边界](../buyers/ledger.csv)

## 复核方式

在本目录运行 python compile.py，会按路径重算 123 份复用采购来源、44 份本轮仓库文件、2 份归属说明的哈希，以及 4 个已存 tag diff 的哈希，并校对 24 个源码行段。44 份含实现、测试、说明、manifest 及依赖清单；不能都计作新的核心实现。lock.py / ingest.py 可利用保存的 27 个有效仓库引用和固定 SHA 取回所选文件。gitlab-test-locked.json 记录实验室依赖，先按其上游 poetry.lock 的七个组件建立隔离环境，再用 python replay.py --locked 运行正式测试；加 --direct 可重跑同驱动对照。既有源码、历史变更与新文件分列保存，不将一次产品、同一 tag 或一条测试重复计算成多个竞品。[覆盖检查](coverage.json) · [新增源快照索引](sources.json) · [版本差分映射](diff-map.csv)

[aider]: https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repo.py#L296-L318
[gitlab]: https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/ed4ff2990049ace5c675203c70d41676fa55682c/duo_workflow_service/checkpointer/node_lifecycle.py#L148-168
[gitpause]: https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/ed4ff2990049ace5c675203c70d41676fa55682c/integration_tests/duo_workflow_service/test_pause_checkpoint_notifications.py#L60-85
[gitgraph]: https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/ed4ff2990049ace5c675203c70d41676fa55682c/tests/duo_workflow_service/checkpointer/test_node_lifecycle.py#L256-320
[goose]: https://github.com/aaif-goose/goose/blob/ea5dded738a46e1eac591642316ca8500a1e8158/crates/goose/src/permission/permission_inspector.rs#L73-L131
[goosetest]: https://github.com/aaif-goose/goose/blob/ea5dded738a46e1eac591642316ca8500a1e8158/crates/goose/tests/tool_inspection_permission_precedence.rs#L36-L99
[argo]: https://github.com/argoproj/argo-rollouts/blob/458eab520fdbf360d1b34b6f6bc0f05e52ae6258/rollout/pause.go#L138-L156
[argotime]: https://github.com/argoproj/argo-rollouts/blob/458eab520fdbf360d1b34b6f6bc0f05e52ae6258/rollout/pause.go#L168-L209
[ren]: https://github.com/renovatebot/renovate/blob/c5b6ec78ab6c26cd77c033b345d8f578e535c0d9/lib/workers/repository/process/limits.ts#L13-L42
[rentest]: https://github.com/renovatebot/renovate/blob/c5b6ec78ab6c26cd77c033b345d8f578e535c0d9/lib/workers/repository/process/limits.spec.ts#L29-L55
[sonar]: https://github.com/SonarSource/sonarqube/blob/1163558a1e3245a67fa6bb9225ad95fff17ee329/server/sonar-server-common/src/main/java/org/sonar/server/qualitygate/QualityGateEvaluatorImpl.java#L56-L85
[sonartest]: https://github.com/SonarSource/sonarqube/blob/1163558a1e3245a67fa6bb9225ad95fff17ee329/server/sonar-server-common/src/test/java/org/sonar/server/qualitygate/QualityGateEvaluatorImplTest.java#L125-L145
[sentry]: https://github.com/getsentry/sentry/blob/9cced6c5579255999d1b5d71fa16d16b4f885bf5/src/sentry/seer/autofix/coding_agent_handoffs.py#L109-L166
[moderne]: https://github.com/openrewrite/rewrite/blob/6e7ca9fee5b237548551df3396def2bbe410034a/rewrite-core/src/main/java/org/openrewrite/RecipeScheduler.java#L85-L126
[lock]: https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist/-/blob/ed4ff2990049ace5c675203c70d41676fa55682c/poetry.lock
