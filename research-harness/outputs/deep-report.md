# 从 Code Agent 到组织级研发自动化

<!-- second-edition -->
这是第一轮研究地图。当前结论见[第二版深度分析](deep-report-v2.html)与[复核证据索引](../round2/index.md)。
<!-- /second-edition -->

**决策建议｜把第一笔投入放在已有 CI 失败后的诊断与接管。** 平台可以接手归集证据、受限复现和准备修复；让有权限的人裁决例外，让独立测试与上线观测决定何时结束。下一个投资点是把接管失败编译成可回放的 harness 测试。两者共享事件和证据，能分别检验价值。先试一个团队的一类失败，得到团队净耗时和质量数据后再扩到跨仓升级。

截至 2026-11-20，研究覆盖 50 个产品、项目及组件，36 项有固定修订实现证据，5 项完成局部实验；20 项学术工作中 8 项复核了正文具体章节。

## 组织到底购买什么

考虑一次支付库升级。Agent 在 A 仓改完 API，单仓 CI 全绿；B 服务尚运行旧版；平台团队收到第二个相似的失败工单；审批人在群里回复过“可以”。谁能认定这项工作完成？模型可以提出兼容补丁，CI 只能报告它实际运行过的用例，服务 owner 才能确认旧版消费者仍需兼容。部署之后，线上错误率还要跟相同流量的基线比较。这个情境是设计推演；真正要消除的是每次故障都由人重新找工单、版本、负责人和验收证据的成本。[P12](../wiki/P12.md) [P18](../wiki/P18.md) [D08](../wiki/D08.md) [I24](../wiki/I24.md)

上期组织上下文研究给出了提交前补关键验证、阻塞时找对确认人、跨仓查询消费者版本三个候选。本期把它们接到可操作的研发状态上：知道某个测试存在后必须记录是否运行，找到 owner 后需要记录其决定覆盖哪个版本，知道消费者版本后要能推迟发布或批准兼容窗口。三件事任意一件只有检索命中，工作都可能还卡在原处。

|关心的结果|工作单位|观察终点|容易得出的错误结论|
|---|---|---|---|
|执行器能否解题|给定环境下的一道可验收任务|独立检查通过，日志可复核|拿历史公开题的成绩代表交付速度|
|工作流能否代办|一个 issue、告警或升级请求及所有后续尝试|产物提交、未解例外路由或明确放弃|把 agent 退出、PR 打开算作任务完成|
|人能否有效监督|一次异常、拒绝、撤销或超时|有权的人理解原因且能停止/接替|把通知已发送或按钮被点过算作有效监督|
|组织能否更快交付|同期所有符合条件的任务，含失败和放弃|业务验收、发布后守护期、总投入|把合并数、席位活跃、采纳率做收益分母|

### 产业前沿的三种现场

**Stripe 做了一件很具体的事：规定一轮失败有多少次机会消耗整套 CI。** 蓝图先以确定性代码运行 lint 和 push，把需要搜索或修复的部分留给 agent。第一次远端失败先应用可用的自动修复，剩余失败才交给 agent 再尝试一次，第二次提交并运行 CI 后交回人工。团队自报每周超过 1,300 个这类人工审查后合并的 PR。这证明它在 Stripe 的基础设施上运行到了规模；缺少同期全体符合任务的分母、评审时间和返工数据，无法把 PR 数解释为节省工时。可移植的是“重试有上限并附带交接”，上限值应由本队列的 CI 成本和成功分布决定。[I02](../wiki/I02.md) [P03](../wiki/P03.md)

**OpenAI 的路线从让 agent 看见结果，走到了部署后重新开判断。** 先是每个 worktree 都能启动应用并读取隔离的指标、日志与浏览器状态；随后 Symphony 用工单状态替代逐个照看会话，一项工作可以关联多个 PR，或只交付调查。11 月 18 日公布的 Performance Factory 更进一步，让另一轮调查在部署后回到原任务，检查延迟等指标是否恢复。前后来自同一供应方，不作为三个独立企业的交叉证明；它们给出了一个阶段差异：控制对象从会话变成工单，完成条件从“提出修复”变成“观察到服务恢复”。[I01](../wiki/I01.md) [I17](../wiki/I17.md) [F01](../wiki/F01.md) [I16](../wiki/I16.md)

**GitHub 与 Cursor 给出了两种分发路径。** GitHub Agentic Workflows 在 10 月 28 日 GA，将 Markdown 工作流编译为 Actions YAML，复用现有 runner、策略和受限写入。Copilot cloud agent 的仓库自动化另有身份与审批约束，不能把两者的权限假定相同。Cursor 3 月把外部事件接入云沙箱，5 月支持多仓和无仓任务。由此推断，单做“看到通知就叫一个 agent”缺少差异化；企业会继续遇到的决策是由谁授权、重复事件如何处理、多仓何时算完成、什么时候停掉没有产出的自动化。[I04](../wiki/I04.md) [I05](../wiki/I05.md) [I06](../wiki/I06.md) [I07](../wiki/I07.md) [I18](../wiki/I18.md) [F02](../wiki/F02.md)

### SOTA 应按工作环节判断

|环节及候选|已有可核查能力|构成差异的边界|本团队的取舍|
|---|---|---|---|
|个人执行与工具授权：Codex CLI、Gemini CLI、OpenHands|工具调用前能按上下文、规则或风险等级改变允许、拒绝、询问的结果|风险未知、优先级冲突、非交互模式要在具体路径读源码|沿用现有执行器，给关键操作增加可测试的规则和决策来源。[E01](../wiki/E01.md) [E05](../wiki/E05.md) [E06](../wiki/E06.md)|
|长任务及中断：LangGraph、Temporal、Symphony|暂停、恢复、重放、按工单重新领取各有现成机制|节点恢复可能重做前半段；历史工作流仍受当时的语义约束|持久化输入、状态和外部动作凭据；单列重复写入实验。[E10](../wiki/E10.md) [D10](../wiki/D10.md) [I17](../wiki/I17.md)|
|递交与审查：PR-Agent、Renovate、Atlantis|过滤发现、自动合并、保存计划、锁定执行均有工程实现|绿色与批准有具体对象；计划、提交和审查意见可能过期|在既有 PR 页交付可验证证据；业务例外保留原 owner。[D07](../wiki/D07.md) [D06](../wiki/D06.md) [D08](../wiki/D08.md)|
|发布及告警：Argo CD、Argo Rollouts、Alertmanager|能比较目标状态、基于测量判定、按标签和规则抑制匹配的告警|配置一致、指标缺失、告警静默代表完全不同的状态|用已有发布系统；给“未知”和撤销动作独立的状态。[D04](../wiki/D04.md) [D05](../wiki/D05.md) [O09](../wiki/O09.md)|
|质量学习：Phoenix、Langfuse、Promptfoo、AutoRocq|带版本的实验、人工标注、断言聚合和机器检查证明各有所长|评估人、生成器和验收条件可能共同犯错；总分可能掩盖局部严重退化|人工样本留出、独立判据、严重项单独否决。[O04](../wiki/O04.md) [O05](../wiki/O05.md) [O06](../wiki/O06.md) [P16](../wiki/P16.md)|
|组织度量：DevLake、OpenCost、SPACE|串起提交到部署、基础设施成本分摊与多维人因指标|已合并样本漏掉弃单；云资源费用不含评审；使用遥测口径因产品而异|优先打通任务到交付的分母，组织比较保留未知和漏数。[O02](../wiki/O02.md) [O11](../wiki/O11.md) [I23](../wiki/I23.md)|

## 商业产品怎么选：先确定人在哪里作决定

如果痛点是「每做完一项任务，仍要有人分派下一项」，应比较由谁持有持续目标。如果痛点是「变更已经写完，却排在评审和合并队列里」，应先检查下游。对这两支团队，采购更多能够并行写代码的席位，会改变不同环节的负载。

**持续目标与有结束条件的项目，先选一个作为试点。** Cognition 在 2026 年 11 月 17 日推出 Devin Bots。一个 Bot 可围绕目标持续派生会话，把新权限请求、待审 PR 和决策放入 Needs you。共享 Bot 后，获准与它交互的人可以请求它使用已有授权；团队若只想复用做法，可以共享模板。Factory Missions 更适合已有迁移范围、验收里程碑和项目负责人的任务。人先批准计划，随后可暂停并重定向 orchestrator。其 8 月版本专门修复中断恢复后里程碑验证漏跑的问题。验收时应追问「恢复后还有哪项检查没做」，并要求看到对应的运行记录。[M01](../wiki/M01.md) [M02](../wiki/M02.md)

**执行入口决定谁有权放行。** 已在 GitLab 管理 issue、runner 与 MR 的团队，可以在原有交付链中试点 Duo。网页 Developer Flow 在 runner 后台运行，不能沿用启动它的聊天工具审批；IDE 的 Software Development Flow 则把改动暂存给人审阅。19.2 已将自定义流程发布为 GA，11 月 19 日随 19.6 提供的定时自动化仍为 beta，且只支持规定的流程类型。希望从桌面或 CLI 通过计划、diff 和录屏监督并行工作时，可比较 Antigravity。当前文档明确，显式请求 `/plan` 后默认停等批准，即使设置为 Always Proceed，提示中明确要求继续时才改变这个行为。[M04](../wiki/M04.md) [M07](../wiki/M07.md)

**保留生命周期反例。** Jules 的历史计划界面允许人先看计划，但离开后计时器可自动批准。Google 于 10 月 29 日公告，11 月 11 日后转入只读，计划 12 月 31 日结束。11 月 20 日选型应将其作为退出演练样本。代码和 PR 留在 GitHub，计划、活动、排程和配置另行导出；官方提到可用 Antigravity CLI 辅助导出，没有承诺原有授权、会话与排程可以直接重建。[M03](../wiki/M03.md) [M07](../wiki/M07.md)

**评审与合并是可叠加的两笔投资。** 团队若反复争论 PR 有没有达到完成标准，可先让 CodeRabbit 影子评审，再将验证过的检查设为 GitHub 必检。发布 Check Run 本身不会阻止合并，升级配置还要核对 V2 与 V3 的差异。若主要等待发生在检查已绿之后，Graphite 可对相依的 PR 分栈、并行运行 CI 或分批合并；上游失败会引起下游重跑。其官方状态页记录了 10 月 30 日一次持续 15 小时 20 分钟的合并故障，试点需演练队列停摆后的积压处理。[M05](../wiki/M05.md) [M06](../wiki/M06.md)

**核验办法。** 在隔离仓库准备同一组有明确验收件的任务，分别制造需要扩权、验证中断、检查缺席与前序 PR 失败四种情况。记录请求发起者、执行身份、谁可拒绝、停止何时到达执行端、恢复后再次检查的版本，以及人实际花费的处理时间。选型依据应是本团队主要等待环节的变化，同时检查漏放与返工是否增加。如果权限撤销后旧会话还能行动，或批准后提交版本发生变化而检查没有重跑，应先解决执行身份和证据绑定，再扩大自动授权。对于当前没有可靠回归测试的仓库，先以只读建议收集人工判定，再评估是否接入强制门禁。上述商业案例均未登录租户实测。



## 从市场能力到产品设计

### 1. Auto harness 应能改进自己的规则，也要证明这次改进有效

工程上有两条循环。第一条处理一次任务：获取需求与版本，准备环境，运行有限动作，收集外部验证，由人裁决或交付。第二条处理一种失败：把失败轨迹与人的纠正关联，从历史样本里留出未见过的一组，在同一模型与工具条件下比较旧、新策略。通过后才把新规则发布给部分任务，有退化就恢复旧策略。很多案例展示了第一条的局部能力。第二条比较难，因为谁标注失败、哪些旧数据失效、规则版本如何关联历史结果，直接改变你得到的结论。[I14](../wiki/I14.md) [I16](../wiki/I16.md) [O04](../wiki/O04.md) [O05](../wiki/O05.md)

同一失败的四种修法成本不同。若模块压根无法导入，优先修镜像和依赖清单；若不知道验证哪个行为，补业务验收样例；若云端运行已经结束但父会话没有收到结果，修任务完成事件传递；若每次模型调用都重读无关日志，再试上下文裁剪。RISE 的轨迹研究甚至在评测平台找到了错误，北大与字节跳动等合作的 AgentDiet 则证明有些上下文可减。两者合起来说明，先定位失败层能避免把环境故障一律归结为提示词不够好。[P01](../wiki/P01.md) [P05](../wiki/P05.md) [E08](../wiki/E08.md)

**落地对象。** 每个任务绑定输入修订、策略版本、代码修订、环境标识、尝试号、证据和终止原因。模型可建议新 recipe，不能自行通过有外部写入权的规则发布。把“搭建支持环境”的时间单独核算：如果为一个低频任务维护一套镜像和验证数据比人工修复更贵，应该关掉这条自动化。发布或停止由负责该工作流的团队决定，不能只看模型调用方的成本。[E03](../wiki/E03.md) [D01](../wiki/D01.md) [P19](../wiki/P19.md)

### 2. Human on the loop 需要成功接管的证据

**人的工作分布在三个时刻。** 运行前，流程 owner 设定允许的写入对象、影响半径、时间/费用与回滚条件。运行中，过期批准、不可判定的测试、需求冲突、超预算或外部影响扩大才触发接管。运行后，维护者抽样判断误放、误拦和绕过门禁的情况。单次需要判断业务语义的改动仍采用 human-in-the-loop 的事前批准；低风险且可回滚的批量工作可以用 human-on-the-loop 的运行监督。分类取决于任务，而非给整个 agent 一个永久自治级别。[I07](../wiki/I07.md) [E01](../wiki/E01.md) [D08](../wiki/D08.md) [I22](../wiki/I22.md)

|人的动作|界面必须回答的问题|可检验的失败|
|---|---|---|
|审阅或拒绝|这次批准覆盖哪个 commit、计划摘要、目标环境、到期时间？|批准之后又 push，在旧界面继续执行；应让旧批准失效或明确触发重新确认。[D08](../wiki/D08.md) [D11](../wiki/D11.md)|
|暂停或撤销|新任务是否停止领取？已派发动作到哪一步？谁已确认取消？|任务进程已退出但外部写入仍排队。要分别验证禁止新写、在途动作和收尾。[D02](../wiki/D02.md) [D03](../wiki/D03.md)|
|接替诊断|最后确认的好状态、已排除的解释、最小复现和下一项区分性检查是什么？|接管者必须完整重跑或等原作者解释；用交接后首次正确动作的时间测量。[P06](../wiki/P06.md) [I16](../wiki/I16.md)|
|恢复任务|从哪个节点继续？之前提交的写入能否去重？|LangGraph 本机实验中，0.2.71 和 1.2.24 两版的同进程内存检查点上，同节点中断前的计数操作在恢复后累计两次，已完成前驱节点计数仍为一次。[E10](../wiki/E10.md)|
|延后裁决|owner 不在线怎么办？何时退回给原请求人？|无人确认的高风险任务在超时后被默认放行；真实演练应测试节假日与队列拥堵。[O01](../wiki/O01.md) [O08](../wiki/O08.md)|

Endsley 与 Kiris 的经典导航实验表明，自动化出错时，操作者对情境的了解与接管后的决策时间有关。它没有研究研发团队。本期能从专业开发者调试现场得到的对应证据是，人要重建系统解释，往往需要知道尝试过什么和为何排除。产品上值得测试的具体差异是，在同一条故障前，一组只收到告警和日志，另一组拿到原始信号、已排除假设、下一个检查以及可执行的暂停动作；比较谁更快作出正确处置。[I22](../wiki/I22.md) [P06](../wiki/P06.md)

### 3. 验证控制着自动化的上限

最昂贵的错觉是所有步骤都成功，而任务实际未完成。k6 代码显示在没有聚合样本的特定路径上一轮阈值判断可被跳过并返回通过；Argo Rollouts 为无结论、错误及失败保留不同的判定；Promptfoo 的总体阈值可能让某一项失败仍取得足够高的总分。统一展示一个绿勾会损失这些语义。平台应让结果带上测到了什么、覆盖多少、是否存在观察空窗及检验器版本。这里的 k6 无样本路径是源码证据，实际 CLI 对照测试覆盖的是有样本的通过与失败。[O10](../wiki/O10.md) [D05](../wiki/D05.md) [O06](../wiki/O06.md)

对一个候选修复，最低要求可以是“旧版本复现失败，新版本同样环境通过，再运行独立回归”。对于数据迁移还需要双向兼容或回放；对用户体验还要真实交互；对于形式化了的少量属性，检查器可独立核验证明。对照 AutoRocq 的工作可以看到，证明被接受仅保证命题推导，命题是否写对仍需领域判断。有些变更暂时没有廉价、独立的判据，这就是将其留给人或先投资测试的产品依据。[P02](../wiki/P02.md) [P08](../wiki/P08.md) [P16](../wiki/P16.md) [I24](../wiki/I24.md)

**不同终点产生不同的胜负。** USEagent 在混合任务集做消融，去掉 ExecuteTests 后，一类子任务的成绩从 8.7% 到零，同表另一类保持 49.6%。这反对用一个榜单决定是否为所有任务多跑一次工具。工业评审研究也给出另一个方向的证据：自动评论常被标为已解决，但三项目合并观察到平均 PR 关闭时间从 5 小时 52 分变为 8 小时 20 分。评审活动增加、问题修复、等待减少三个效果需要单独测量。[P20](../wiki/P20.md) [P11](../wiki/P11.md)

### 4. 组织产出需要完整分母

要回答“提效了吗”，先冻结试点期间所有符合条件的工作，包括被拒绝、未分派、人工做完、被放弃和到期仍进行中的任务。每个任务记录是否指派自动化、人工实际投入、评审与值班时间、机器费用、墙钟历时、验收结果与观察到的复发。保留同一 issue 关联多个 PR 或零 PR 的可能。验证器、模型、策略和任务来源都要有版本。面板中的缺失显示为未知，有资源成本但没关联到结果的记录应单列。[P18](../wiki/P18.md) [O02](../wiki/O02.md) [O11](../wiki/O11.md)

**三个表面冲突的证据实际回答了三个问题。** Stripe 报自己能交付多少机器编写且人工审查的 PR。METR 早期随机试验问的是原本熟悉仓库的 16 人在 246 个已选任务上用时如何，允许 AI 后实现时间估计增加 19%。METR 在 2026 年又解释为何新招募及并行工作让同一实验设计变得不可靠。11 月，METR 在获得 Anthropic 部分内部数据和访谈权限后开展的研究则观察特定 AI 研发组织的模型能力进展速率；公开报告提示显著加速的可能，也明确关键证据被删节且归因不确定。吞吐、单任务人时、特定组织研发进展速率不能在同一张百分比排行榜相减。[I02](../wiki/I02.md) [I08](../wiki/I08.md) [I09](../wiki/I09.md) [I21](../wiki/I21.md)

**一个能检查成本转移的算例。** 假设某月有 100 个合格失败任务，基线每项人工 40 分钟。新流程每项节省调查 16 分钟，却分别给审查和例外处理增加 6 和 5 分钟，另花 600 分钟维护回放环境。月净变化为 100 × (16 − 6 − 5) − 600 = −100 人分钟；机器使用费尚未计入。这是假设演算。采纳量、单次生成速度很可能都上升，团队仍可能亏损。单独报告工程师人时、墙钟和货币，在财务与团队约定折算前保持各自单位。[I23](../wiki/I23.md) [O11](../wiki/O11.md)

### 哪些研发自动化值得继续投入

采购负责人真正要决定的是，下一批任务是否继续交给自动化。五个商业样本分别看到了工作的一部分。GitHub Copilot 从产品端统计补全生成与接受动作，日活人数不能直接累加成 28 天采用人口。Harness 在开发工作站关联会话和提交，一个 PR 只要含一个归因提交就可能被纳入；其文档给出的采用率分母限于已导入且已安装代理的人。LinearB 可以按开发者当天的 AI 活跃情况标记其提交，再以提交占比标记 PR。同一个人为主、AI 轻度参与的变更，在三个产品里就可能分别表现为一次接受、一个含 AI 的 PR 和多条 AI 辅助提交。[B02](../wiki/B02.md) [B03](../wiki/B03.md) [B04](../wiki/B04.md)

DX 把工具用量、影响和成本与开发者体验并列。其 2026 年第三季度报告显示，在厂商观察样本内，AI 代码占比 20%–40% 的组织，等待首次评审的中位数为 40 分钟；占比 80% 以上的组织为 82 分钟。这个差异支持检查评审队列，两个群体原先的工作量和人员配置却可能不同。云效从业务需求看另一端，每个已上线需求才成为交付分布图上的一点，仍在等待的需求要结合在制品看。评审还承担理解变更和传播知识的工作，单独压低评审时间会漏掉这些收益。[B01](../wiki/B01.md) [B05](../wiki/B05.md) [P12](../wiki/P12.md)

**假设例，非实测。** 同一批 10 个依赖升级任务，过去一周产生 100 次补全、40 次被接受，8 个任务通过业务验收。本周保持 10 个同类任务，仍有 100 次补全，其中 60 次被接受；首评积压，周末只有 5 个通过验收。工具面板显示接受率从 40% 升至 60%；任务台账却显示按期验收率从 80% 降至 50%。两张表都可能算对。再看本周余下 5 项，若 4 项在等评审，应先调接单和分流；若 4 项已被退回且人工重做，才应检查生成策略。只看已上线项的周期会同时漏掉这两种损失。[B02](../wiki/B02.md) [B03](../wiki/B03.md) [B05](../wiki/B05.md)

**如何核验。** 试点开始前冻结符合条件的任务清单及验收期限；每次重试保留相同任务 ID，并连接 PR、评审、部署、撤销和返工工时。对缺失链接抽查，单独公布能归因到生产的比例；DevLake 的实现展示了成功生产部署如何沿 SHA 和 commit diff 回连。再按相似团队分期开放，给每队同时看单位验收成本、首次评审等待、任务积压年龄和上线后缺陷。对账未通过先修采集。连续两个预定窗口内，单位验收成本增加且质量无改善的任务类型，可暂停自动执行、保留建议模式；这个阈值是试点决策约定，仍需负责人结合样本量判断。[O02](../wiki/O02.md) [O11](../wiki/O11.md) [P07](../wiki/P07.md) [P18](../wiki/P18.md)
 
共享制品还需要约定归属。例如 A 团队的代理写了迁移脚本，B 团队完成验收，两边都可记录贡献，组织台账只计一次被验收的交付。复核时把跨队转交与重复立项分别标记，避免协作越多，表上的效率看起来越高。[B04](../wiki/B04.md) [P18](../wiki/P18.md)


## 五个可以单独验证的产品机会

|可试做的能力|用户面临的具体决定|已有技术与剩余缺口|最快的否证办法|
|---|---|---|---|
|审查容量限制派工|维护者周一面对几十个跨仓升级，先处理哪几个？|Symphony 能按工单和可用槽位调度，Graphite 能处理相互依赖的合并队列。可试的增量是让派发同时受有权评审者时段、每服务在途上限和待发布存量限制。[F01](../wiki/F01.md) [M06](../wiki/M06.md) [P11](../wiki/P11.md)|相同团队按周交替采用固定并发和容量约束；若队列缩短但发布验收总数也下降，查真实瓶颈并撤销上限。|
|把“接管”记录成下次可回放的测试|操作人纠正了哪个错误前提，改 recipe 后还会再犯吗？|Tessl 比较同任务有/无 skill，还能观察 skill 是否加载；Phoenix 绑定数据集版本。可加一项业务规则：把有效纠正连到独立验收，维持全程未参与调优的失败集。[F03](../wiki/F03.md) [O05](../wiki/O05.md) [I16](../wiki/I16.md)|对有证据能重放的纠正做配对实验；若载入了 skill 但盲审结果不变，停止推广它。|
|为审批写明对象和有效期|原计划刚获批、新提交改变目标对象，平台应否继续？|Atlantis 将计划完整性与部分执行条件分开验证；Jenkins Input Step 限制谁能提交决定。跨系统时需要把人、对象、内容摘要、时间、作用域放到同一条决策记录。[D08](../wiki/D08.md) [D11](../wiki/D11.md) [O08](../wiki/O08.md)|在沙箱批准 A 后替换成 B 或撤回权限；观察旧授权能否放行，以及正确授权多久能恢复工作。|
|无人持有的自动化转交与退役|创建者调岗后，定时任务用谁的连接器？过去一个月有几次输出被真正使用？|Claude Code Scheduled tasks 由个人拥有，Devin Bots 的 Bot 可拥有自己的权限。相同“无人值守”有不同的身份生命周期。可试做 owner 交接、过期暂停、无人消费退役。[F04](../wiki/F04.md) [M02](../wiki/M02.md) [I06](../wiki/I06.md)|在隔离环境做转岗模拟，跟踪旧连接器最后一次有效使用；低频灾备流程单列，不能因平时少用就删除。|
|按结果计费和选择执行环境|一次耗时回放沉默了，应继续付费还是先休眠？|OpenSandbox 区分没有活动证据与真正空闲，OpenCost 能拆 Kubernetes 资源成本，DevLake 能关联部分交付事件。仍需补 SaaS 调用、没有结果的尝试和人的维护时间。[F05](../wiki/F05.md) [O11](../wiki/O11.md) [O02](../wiki/O02.md)|对相同任务比较保温、休眠和即时创建，记录复苏延迟、重复动作、每次被接纳结果的完整成本；便宜但恢复慢到阻塞人时应收缩。|

共性是把“组织的规则有没有真的改变动作”做成可观察的事实。可由日程、事件和 webhook 触发的工作近乎无限，而愿意维护的规则、能给出验收的人和稳定的生产信号都很有限。选题时优先找已经出现真实排队和重复判断的环节，这比先定义统一的自治等级更容易获得可反驳的结果。

## 同一工单的可实施设计

|事件及输入|持久化对象|状态与人能做的动作|
|---|---|---|
|工单重复到达、任务被拆分|来源系统 + 工单号 + 输入修订；父子任务；owner；策略修订|更高修订让旧批准过期，重复事件合并。暂未分配 owner 的任务只读排查。[F01](../wiki/F01.md) [O01](../wiki/O01.md)|
|接到执行并占用资源|attempt ID、隔离工作区、机器身份、租约与并发上限|有期限的执行权；lease 到期后核验外部动作再重领。重复发起可识别。[F01](../wiki/F01.md) [E11](../wiki/E11.md)|
|验证结论产生|输入修订、验证器版本、环境标识、样本数、预期与实测值、结果链接|成功、失败、无结论、没有数据独立建模。保留首个失败和最终一次测量。[D05](../wiki/D05.md) [O10](../wiki/O10.md)|
|例外出现或超时|待决问题、仍未知事项、可逆/不可逆影响、审批内容摘要和授权主体|可拒绝、延后、暂停新动作、取消在途请求或交接。每个动作记录系统确认时间。[D02](../wiki/D02.md) [D03](../wiki/D03.md) [D08](../wiki/D08.md)|
|修复上线与复核|部署版本、生产观察窗、对照群体、复发与最终 disposition|由发布平台、服务 owner 确认结果。验收失败重开原工单；对已到期日志保留证据失效状态。[I16](../wiki/I16.md) [I24](../wiki/I24.md)|
|维护规则和退出|失败标签、旧新策略、训练/留出数据集、观察窗、适用服务与生效版本|先只读影子运行，再有限推广，可暂停和退回旧版本。商业托管退出时导出工件并实测能否重建。[F03](../wiki/F03.md) [O05](../wiki/O05.md) [M03](../wiki/M03.md)|

这是建议的数据边界，可分批实现。首版可用已有 CI 工单、自定义字段、对象存储及 PR 检查。只在拿到试点增量之后才值得做跨产品的统一控制台。


## 哪些研究团队值得持续跟踪

按是否公开可追踪的数据、工具与方法选样。以下对应的是合著团队和研究线索，不把每项合作成果归属给一所机构，也不按声量给实验室排名。

|研究团队或合作线|读到的研究路径|对研发平台最有价值的复用|
|---|---|---|
|Princeton 主导的 SWE-bench / SWE-agent 合作团队|先把真实 issue 及回归条件装进可执行基准，再研究为模型设计专用编辑、查找与执行界面。后续外部审计暴露公开题目污染与测试过度指定问题。|继承独立判分的设计，用更新、更贴近本组织的留出任务评估；工具界面版本与模型同时入账。[P13](../wiki/P13.md) [P14](../wiki/P14.md) [I12](../wiki/I12.md)|
|NUS Abhik Roychoudhury 团队及 Purdue 合作者|SpecRover 推断意图并审查补丁；USEagent 比较不同任务所需动作；AutoRocq 把可形式化的证明交给 Rocq 核验。|从“更多 agent”转向“谁有资格给这个判断定案”。对需要语义检查的任务加判据，对本就有客观检查器的任务减少模型裁决。[P02](../wiki/P02.md) [P20](../wiki/P20.md) [P16](../wiki/P16.md)|
|Singapore Management University，RISE|公开基准的多 agent 轨迹与测试日志揭示不同失败源，作者发现基准本身也会产生错误。|优先采集失败时的环境和错误类型。评测平台的缺陷单独入账，允许同一补丁在修订后的评测器上重算。[P01](../wiki/P01.md)|
|Waterloo Software REBELs 及 CI 研究合作者|一项研究阅读构建系统评审，另一项借助 OpenStack 重跑历史估计是否值得再跑。共同问题是自动化规则也需要人维护，重复运算也有成本。|追踪 CI 规则谁在评审、队列为何重跑，给基础设施变更单列风险预算。[P19](../wiki/P19.md) [P03](../wiki/P03.md)|
|UT Austin、George Mason 等合作团队|FlakyGuard 研究如何选取修复所需的生产代码上下文；ReproFlake 交付可复现环境、正反日志与修复脚本。两项共享不稳定测试议题及部分作者。|把“能修”“能复现”“有人采纳”“没有复发”分别建账。引入下一种测试框架时补样本，不沿用原数据集结论。[P04](../wiki/P04.md) [P08](../wiki/P08.md)|
|北京大学 Yingfei Xiong 等、ByteDance 等合作方|AgentDiet 在两模型两基准下用运行时轨迹删减研究成本，没有把输入缩短等同于任务价值上升。|对机器保留最小上下文，对事故调查留完整事件；分别计量 token、缓存、总费用和接管价值。[P05](../wiki/P05.md)|
|南京大学软件工程研究者与华东理工研究者|两条独立研究线：前者操作规格形式和粒度，后者在 83 个公开仓库上分析 issue 协作结构与结果的关联。|可以同期开两种试验：个体任务层验证规格写法，团队层验证需求与交接链，分清两种观察单位。[P15](../wiki/P15.md) [P07](../wiki/P07.md)|
|UC San Diego 的 Haolin Li 与 Michael Coblenz；CMU 等的人机交互研究者|前者观察专业调试现场，后者调查 410 名开发者实际采纳和放弃编程助手的原因。|在上线指标之外观察接管者重建什么，以及弃用者为什么退出。把认知负担当可观察的工作，而非默认人工总能兜底。[P06](../wiki/P06.md) [P17](../wiki/P17.md)|

**论文之间不能直接相加。** 人机问卷可以发现退出原因，无法测出每项任务节省的分钟数。工业 PR 前后对照提供了真实的审查队列，仍可能混入不同任务。基准消融适合判断工具是否必要，无法替代现场采用率和上线后果。把这三类证据组成一套验证：用访谈找失败，离线消融找机制，再做有基线的现场试验。[P11](../wiki/P11.md) [P17](../wiki/P17.md) [P20](../wiki/P20.md)


## 试哪里，怎么知道该停

下列阈值是建议预注册的业务判据，均未在贵司验证。试点先过安全与可恢复性检查，再看方向和区间；样本不足时保留“不确定”。比较以任务为单位，在同一服务和故障类型内分层；同一人同时处理多个任务时不要把并行等待重复计作人时。

|优先度与负责人|试点及对照|主要结果与反证|停止或升级条件|
|---|---|---|---|
|第一，平台 CI 团队 + 两个服务 owner|回放最近约 40 个符合条件的 CI 失败。A 为既有日志/重跑；B 加确定性聚类和历史匹配；C 在 B 上加受限 agent 复现与证据包。盲审判断下一步。|首次正确定位、接管人主动分钟、错认代码故障、重跑费。按仓库和原因分层，保留无法复现项。|若 C 无法比 B 减少人工，部署 B 即可。若错误自动写入或关键证据缺失，停写并继续只读。通过后进真实影子流量。[P01](../wiki/P01.md) [P03](../wiki/P03.md) [P08](../wiki/P08.md)|
|第二，agent 平台 + 质量负责人|从人工接管记录抽样，同一模型、数据集、工具版本对旧新 harness 做配对回放；留出跨周新样本。用标注队列给覆盖不足的失败补标签。|独立验收率、严重失败数、单次合格交付成本、接管者能否解释结果。固定数据与模型，再单因素比较。|任一严重项回退就不推广；只在训练样本上获益时退回采样。新策略小流量投放后仍观察复发。[O04](../wiki/O04.md) [O05](../wiki/O05.md) [O06](../wiki/O06.md) [I16](../wiki/I16.md)|
|第三，发布工程 + 值班团队|同一历史版本变更回放跨仓依赖、生产版本与 canary 窗口。A 为当前提醒，B 在 PR 旁给版本、关键检查和影响者，C 再按可撤销策略派单。|未知组合、误放、误拦、接替耗时、等待真正授权人时间、回滚成功。刻意包含空指标与旧批准。|任何不可恢复误放都拦截扩大流量。若目录找不到 owner 或生产版本不可查，先补数据源。[D05](../wiki/D05.md) [D08](../wiki/D08.md) [O01](../wiki/O01.md) [I24](../wiki/I24.md)|
|探索，研发效能团队|在有义务维护的多团队迁移上比较“发更多 PR”和“按评审人容量发放任务”。用等待时间与进行中工作量调并发。|已验收的服务迁移数、排队 p90、每位维护者被中断次数、弃单、未部署补丁和尾部服务风险。|若增加并发只增加待审库存，降低派发速率；若瓶颈实为发布窗口，停止优化生成阶段。[I17](../wiki/I17.md) [P07](../wiki/P07.md) [P11](../wiki/P11.md)|

### 前 90 天的决策安排

**第 1–2 周**，项目负责人锁定一个有可靠回放环境、独立 owner 和高频失败的服务，对照组沿用现有 CI。记录不参加的原因，以免只纳入容易题。先抽十例让人手工组装理想证据包；如果理想证据包也改变不了接管动作，暂停 agent 封装，转查真正的等待点。[P06](../wiki/P06.md) [I09](../wiki/I09.md)

**第 3–6 周**，为历史任务做盲审，加入预先设计的坏样本：过期审批、重复事件、空遥测、同一分支的新提交、没有 owner 的服务。先测能否辨别这些错误，再比较独立验收和净投入。复核给出失败类型、具体证据和下一次应该改变的一个环节，避免多项同时改动后无法归因。[D08](../wiki/D08.md) [E10](../wiki/E10.md) [O10](../wiki/O10.md) [P01](../wiki/P01.md)

**第 7–12 周**，选择低影响任务做小流量、可撤回试点。观察期内保持原发布策略，建立主动人时、尾部等待、复发和成本的周度记录。同步复核哪些新工单是 agent 自己创建的，避免用自创需求填高吞吐。月末可选扩大、保留只读、降级到脚本或停用四种决策。若源码或产品版本跨越重大变化，先重跑相同失败集再做决定。[I17](../wiki/I17.md) [D06](../wiki/D06.md) [O07](../wiki/O07.md) [I24](../wiki/I24.md)

## 市场选择与未决问题

**现成工具可承接的部分**包括模型执行、日程触发、runner、渐进式发布、基础遥测与标注。已有企业版平台应先试其现成对应能力，按相同的任务回放对照。值得自建的候选是公司独有的验收条件、历史失败资产、审批关系，以及跨工具串起的交接体验。每一部分都可独立被现有工具替换。流程团队负责规则，服务 owner 负责验收与例外，平台团队负责执行、隔离、回放及可恢复性；组织层只消费汇总结果，个人排名不是试点交付物。[I18](../wiki/I18.md) [O01](../wiki/O01.md) [O04](../wiki/O04.md) [P12](../wiki/P12.md)

**最可能推翻这条路线的三个事实**是现有 CI 已能低成本给出同样的诊断；多数等待来自没有决策权的排队，技术证据改变不了队列；平台补齐环境和回放的维护成本大于减少的调查人时。每一种分别对应确定性基线、按责任人做的分层队列分析、含维护和失败尝试的成本账。没有这些证据前，可以决定启动试点，不能承诺年度 ROI。


## 覆盖口径、复核与复算

研究截止 2026-11-20（上海）。采用机制导向的目的抽样。先取执行、交付、组织平台各 11 个案例，再定向补充前沿编排、闭源托管与商业度量。这 50 项包含直接竞争的托管产品、开源替代及可复用的互补组件；同一厂商可有多个机制，研究型 agent 和只读的 Jules 单独说明。Cursor Automations、Stripe Minions 等额外工程实践只作为来源，不抬高样本总数。固定修订源码复核涉及 36 项；托管服务的实际运行配置仅能依赖官方说明。源码复核范围也可能只有 SDK 客户端或参考实现。产品均有版本或演进证据，未将每条演进说明当作首次发布。

论文 20 项。17 项来自 ICSE、FSE、ASE、ISSTA 研究轨；1 项为 ICSE SEIP 行业轨；另两项是 ICLR 与 NeurIPS 基准/工具论文。8 项对照读了 PDF 正文的研究设计、结果或效度讨论，其余为作者摘要、会议页及书目交叉核对。另读 METR 的现场实验正文，并单列 SPACE、人因与 SRE 等补充来源。没有穷尽四个会议的全部论文。对应作者、机构、具体章节、复核深度和限制见学术详表。[I13](../wiki/I13.md)

**如何复做。** 从三层研究协议出发，用“研究对象 + 动作 + 会议/厂商域名”定位一手线索，例如 CI recheck + ASE、coding agent + trajectory + ICSE、agent automation + dated changelog。题名在 OpenAlex/Crossref 查询后再对比会议轨道、发表或预印本日期；获取到正文则核对首页、方法段与局限。产业样本以官方代码 commit、版本页或 dated changelog、现行文档三者组合；缺其中某类则显式说明。源码重点读判定分支、默认值、输入和异常路径，选择少数能隔离的机制做正反实验。闭源产品查当前版本、账号或仓库前提，也主动查退场与事故。

**迭代留下了四项实质改动。** 第一轮发现纯开源样本无法代表采购市场，追加商业工作流、效能产品和中国团队的代表。第二轮发现 Conftest 被两组独立选中，保留两份实验记录，但从组织组计数中移除，由 OpenCost 补充资源成本视角。第三轮核对 Jules 退场、GitLab 定时功能 beta 及 Argo Rollouts 候选版，收窄相应结论；补比较对象 Antigravity。第四轮用人因、工业评审反例、METR 后续研究与 DORA 勘误审读 ROI 观点，将“生成→交付”拆为不同观察单位，并对 LangGraph 同一中断行为跨两版本复验。[M03](../wiki/M03.md) [M04](../wiki/M04.md) [M07](../wiki/M07.md) [D05](../wiki/D05.md) [I09](../wiki/I09.md) [I11](../wiki/I11.md) [E10](../wiki/E10.md)

**可复验的局部运行。** LangGraph 内存检查点的 approve/deny 与副作用放置位置在两个版本、四种条件上对照；PR-Agent 仅执行固定版本配置判定函数；OpenSandbox 仅运行空闲状态判断函数；Conftest 和 k6 用核验过的 Windows 发布包做 CLI 正反对照。合计五个不同产品机制，Conftest 有两组验证。未执行商业租户端到端流程、生产灰度、席位计费评估或内部对照试验。这些差异在研究结论与投资建议之间划出边界。

**时效与适用性。** 快照中的源代码时间、发布日、文档更新时间、抓取日并非同一个日期。发布订阅是滚动窗口，取样不表示逐版本全量审计。学术时间按发表事件或预印本标记；早期研究用于解释机制。本期优先覆盖公开原文足够的样本；没有就各厂商合同、地区可用性、私有部署和跨境数据策略做逐项选型。


## 逐项证据与复核边界

## 产品与项目

### E01 OpenHands Software Agent SDK

**平台**　Python SDK，本地会话确认策略；另提供 TypeScript、REST 界面，以下测试定位 Python。

**适用场景**　代码代理即将执行工具，同一会话里混有例行编辑、需要确认的动作，以及无法判级的动作。

**实现机制**　ConfirmRisky 把动作风险与阈值比较，等于阈值也触发。该策略的阈值默认 HIGH，未知风险由独立的 confirm_unknown 开关处理，默认询问。上游测试分别构造有、无分析器的会话，核对待执行事件与拒绝事件配对。

**人工决策**　在待确认动作上继续或拒绝。拒绝会留下带原调用标识和理由的 UserRejectObservation，后续模型可读取理由。要核对实际会话策略与分析器，不能从策略类的默认值推导所有会话都启用审批。

**组织影响**　平台可以把风险标签、阈值、人工决定和实际工具响应分开记录，以复盘哪些直接放行动作后来引发返工。

**版本与演进**　v1.63.0 的发布记录（2026-11-19 更新）列出恢复后标记来源与结果、等待模型时保存状态变化，以及恢复时移除已禁用插件的能力。它为检查恢复后的有效授权提供了具体版本锚点。

**适用边界**　风险分析器输出决定阈值的输入，策略类本身不校准误报漏报。上游测试使用模拟工具；本研究未运行 SDK 服务。

**研究推断**　“审批过”应能回答谁拒绝了哪一次工具调用、拒绝原因如何回到模型、重启后还能否追溯，而不只是一个布尔字段。

**复核实验设计**　构造低、高、未知三类无害文件操作，分别在开启/关闭分析器和重启前后运行。核对真实执行次数、拒绝事件与原调用 ID，并记录人工介入次数。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-20 · [原始来源 1](https://github.com/OpenHands/software-agent-sdk/blob/fb565cfeac21468a5101dd41497b65315c66ac3b/README.md) · [本地快照](../lanes/execution/raw/openhands/fb565cfeac21468a5101dd41497b65315c66ac3b/README.md)
- ConfirmationPolicyBase、ConfirmRisky；L43–61 核对阈值与 UNKNOWN。 · 2026-11-20 · [原始来源 2](https://github.com/OpenHands/software-agent-sdk/blob/fb565cfeac21468a5101dd41497b65315c66ac3b/openhands-sdk/openhands/sdk/security/confirmation_policy.py) · [本地快照](../lanes/execution/raw/openhands/fb565cfeac21468a5101dd41497b65315c66ac3b/openhands-sdk/openhands/sdk/security/confirmation_policy.py)
- L454–506、L656–700，模拟确认、拒绝及启用条件。 · 2026-11-20 · [原始来源 3](https://github.com/OpenHands/software-agent-sdk/blob/fb565cfeac21468a5101dd41497b65315c66ac3b/tests/sdk/conversation/local/test_confirmation_mode.py) · [本地快照](../lanes/execution/raw/openhands/fb565cfeac21468a5101dd41497b65315c66ac3b/tests/sdk/conversation/local/test_confirmation_mode.py)
- 官方 GitHub Releases Atom 内的条目 v1.63.0；date 为该条目 updated 的 UTC 日期。 · 2026-11-19 · [原始来源 4](https://github.com/OpenHands/software-agent-sdk/releases/tag/v1.63.0) · [本地快照](../lanes/execution/raw/openhands/4a1f72b4b472c11b/releases.atom)
- 论文摘要与版本历史：v1 为 2025-11-05，核对的是 2026-04-22 v2。 · 2026-04-22 · [原始来源 5](https://arxiv.org/abs/2511.03690) · [本地快照](../lanes/execution/raw/openhands/9227d5496109b868/report.html)


### E02 SWE-agent

**平台**　Python CLI、SWE-ReX 执行环境；区分 RetryAgent 与 DefaultAgent。

**适用场景**　给定仓库和 issue，一次尝试产出候选补丁后，需要决定是否值得再花一轮推理成本，以及最终保留哪个结果。

**实现机制**　RetryAgent 在一次尝试完成后提交 trajectory、模型统计与候选结果，保存本次轨迹；按配置继续或最终选取结果。ScoreRetryLoop 汇总尝试与评审成本，检查次数、接受数和开启新尝试所需的剩余预算。v1.0 起可调整多次尝试的配置、模型或参数。

**人工决策**　人预设预算、评分门槛和挑选方式，事后可用轨迹检查器抽查候选；源码中的 reviewer 分数是自动选择信号，不能代表仓库维护者已验收。

**组织影响**　适合估计“同一工单多试一次”的边际收益，用失败轨迹定位工具或上下文缺口。可将尝试编号和失败成本记到同一工单。

**版本与演进**　v1.0.0 发布记录（2025-02-13）列出可配置重试、多种配置择优、SWE-ReX 并行执行及命令行轨迹检查器，作为历史引入证据。

**适用边界**　研究样本围绕有明确问题陈述和代码环境的修复。选中候选不等于通过隐藏测试、上线成功或提升团队净产出。本次未重跑论文基准。

**研究推断**　调度预算可以发挥比新增一个模型更直接的作用，但需要独立验收器识别“多花钱挑出同一个错误”。

**复核实验设计**　对同一组有保留测试的历史 issue 随机分配单次尝试、等预算多次尝试；记录 best-of-N 与最终被选候选之间的差距，计入评审推理成本及人工挑选分钟数。

- 仓库 README 定位产品用途、平台和入口。 · 2026-07-16 · [原始来源 1](https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/README.md) · [本地快照](../lanes/execution/raw/sweagent/3ea751c087f32b16e039a2233dd6eefecef325d5/README.md)
- RetryAgent.run L390–437，每次候选与最终选取的轨迹。 · 2026-07-16 · [原始来源 2](https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/sweagent/agent/agents.py) · [本地快照](../lanes/execution/raw/sweagent/3ea751c087f32b16e039a2233dd6eefecef325d5/sweagent/agent/agents.py)
- ScoreRetryLoop L590–654，接受数和剩余预算控制。 · 2026-07-16 · [原始来源 3](https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/sweagent/agent/reviewer.py) · [本地快照](../lanes/execution/raw/sweagent/3ea751c087f32b16e039a2233dd6eefecef325d5/sweagent/agent/reviewer.py)
- 官方 GitHub Releases Atom 内的条目 v1.0.0；date 为该条目 updated 的 UTC 日期。 · 2025-02-13 · [原始来源 4](https://github.com/SWE-agent/SWE-agent/releases/tag/v1.0.0) · [本地快照](../lanes/execution/raw/sweagent/ba4b199549514a62/releases.atom)
- 论文摘要、ACI 方法和版本历史：v1 为 2024-05-06，当前为 2024-11-11 v3，未重跑论文实验。 · 2024-11-11 · [原始来源 5](https://arxiv.org/abs/2405.15793) · [本地快照](../lanes/execution/raw/sweagent/7c98d2fca05b7a49/report.html)


### E03 goose

**平台**　开源 Rust 调度器、CLI/桌面；取 scheduler/full.rs 的调度路径。

**适用场景**　维护者将重复性任务编为 recipe，例如周期性检查仓库文档漂移，要求定时执行并能暂停单个计划。

**实现机制**　调度器保存计划与已经校验的 recipe 字节，保留原目录解析相对引用，运行时结合参数和模型设置创建 Scheduled 会话，源码在该路径显式设置 GooseMode::Auto。调度器有 run_now、pause_schedule、kill_running_job 以及按计划查看会话的入口。

**人工决策**　操作者可暂停后续调度或终止当前运行，两种动作分别对应将来与现在。普通工具审查层按请求 ID 收集 deny、allow、ask，不能由交互会话存在 ask 推导定时模式也会等待人。

**组织影响**　团队能独立管理任务所有者、recipe 版本和会话记录；部署需要额外定义定时身份及扩展集合，尤其 recipe 没有显式声明扩展时。

**版本与演进**　v1.59.0 的 2026-11-10 发布记录列入 goose-agent GDK 的停止、审批及工具 hook operations。该记录说明扩展点演进，不是定时 recipe 首次上线日期。

**适用边界**　运行时会根据当前配置解析模型和扩展。冻结 recipe 文本并不冻结依赖、模型和凭证；跨实例的一次性执行保证、平台审批表现均未实测。

**研究推断**　发布一份 recipe 时还应发布可比较的执行清单，否则相同文本在两个团队中可能调用不同扩展。

**复核实验设计**　在隔离目录将只读日报安排两次，一次固定扩展、一次沿用环境配置；在运行中暂停计划并单独终止任务，核对会话状态、调用记录及是否产生第二份输出。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-20 · [原始来源 1](https://github.com/aaif-goose/goose/blob/42055e73fda21edd8f3056a5eef682d08589aef0/README.md) · [本地快照](../lanes/execution/raw/goose/42055e73fda21edd8f3056a5eef682d08589aef0/README.md)
- schedule_recipe、execute_job L845–913、pause_schedule、kill_running_job。 · 2026-11-20 · [原始来源 2](https://github.com/aaif-goose/goose/blob/42055e73fda21edd8f3056a5eef682d08589aef0/crates/goose/src/scheduler/full.rs) · [本地快照](../lanes/execution/raw/goose/42055e73fda21edd8f3056a5eef682d08589aef0/crates/goose/src/scheduler/full.rs)
- GooseToolApproval.check L31–99，按请求 ID 处理检查器决策。 · 2026-11-20 · [原始来源 3](https://github.com/aaif-goose/goose/blob/42055e73fda21edd8f3056a5eef682d08589aef0/crates/goose/src/agents/state_machine/tool_approval.rs) · [本地快照](../lanes/execution/raw/goose/42055e73fda21edd8f3056a5eef682d08589aef0/crates/goose/src/agents/state_machine/tool_approval.rs)
- 官方 GitHub Releases Atom 内的条目 v1.59.0；date 为该条目 updated 的 UTC 日期。 · 2026-11-10 · [原始来源 4](https://github.com/aaif-goose/goose/releases/tag/v1.59.0) · [本地快照](../lanes/execution/raw/goose/075e6125adcdbc9f/releases.atom)


### E04 Aider

**平台**　Git 仓库内 CLI；以下默认值为 Coder 构造器值，用户配置可覆盖。

**适用场景**　开发者让代理修改若干文件，期望编辑后自动触发语法检查或项目测试，快速决定是否返修或撤销一次更改。

**实现机制**　Coder 对实际编辑的文件运行自动 lint；auto_test 开关打开时执行已配置的测试命令。失败分别通过 confirm_ask 请求是否修复；同意才将错误作为下一轮输入。run_one 限制同一请求的反思轮数，类默认上限为 3。自动 lint 与自动测试在该构造器上的默认值分别为开和关。

**人工决策**　开发者决定是否将错误送回模型，并可查看 Git 改动。/undo 在多父提交、相关文件有未提交改动等情形会停止，避免直接覆盖人的后续工作。

**组织影响**　适合做低复杂度基线，证明额外平台开销是否换来了超过明确测试命令与有限返修的收益。

**版本与演进**　v0.86.0 的 2025-08-09 发布说明与 HISTORY 均记录缩短 /undo 中提交消息的显示，同时支持 GPT-5 等模型。此项是可读性改进，不代表该版首次拥有撤销能力。

**适用边界**　项目测试可能遗漏关键行为，运行本地命令需要合适环境。Git 撤销作用于受管代码，不能补偿外部工单或服务操作。本次未运行 Aider。

**研究推断**　有些错误可由廉价的编译器或测试给出直接反馈，无须再请一个模型扮演评审。组织产品可先把这条基线做扎实。

**复核实验设计**　在已有 lint 和单测的仓库比较只编辑、编辑加 lint、再加测试三个条件。锁定模型配置，拆分检查发现的问题、误报、同意返修率和下一次人工修改。

- 仓库 README 定位产品用途、平台和入口。 · 2026-05-22 · [原始来源 1](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/README.md) · [本地快照](../lanes/execution/raw/aider/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/README.md)
- run_one L924–944；编辑后 lint、自动测试与询问 L1599–1623。 · 2026-05-22 · [原始来源 2](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py) · [本地快照](../lanes/execution/raw/aider/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py)
- raw_cmd_undo L560–634，历史及脏文件检查。 · 2026-05-22 · [原始来源 3](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/commands.py) · [本地快照](../lanes/execution/raw/aider/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/commands.py)
- v0.86.0 的 /undo 展示变更及旧版撤销修复。 · 2026-05-22 · [原始来源 4](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/HISTORY.md) · [本地快照](../lanes/execution/raw/aider/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/HISTORY.md)
- 官方 GitHub Releases Atom 内的条目 Aider v0.86.0；date 为该条目 updated 的 UTC 日期。 · 2025-08-09 · [原始来源 5](https://github.com/Aider-AI/aider/releases/tag/v0.86.0) · [本地快照](../lanes/execution/raw/aider/6499d57b5b8b2983/releases.atom)


### E05 OpenAI Codex CLI

**平台**　开源 Rust harness；此处核对 core 源码和上游测试，厂商实践是独立证据等级。

**适用场景**　代理申请一次需授权的操作。系统面对 hook、用户、自动评审器和强制人工节点，必须知道谁有权作决定以及决定属于哪一轮。

**实现机制**　请求以工具调用及上下文构造审批载荷。拒绝类 hook 可直接否决；允许类 hook 仅在无需强制人工审批时直接生效。其余请求按配置路由到评审者；记录决策来源，自动评审与用户、hook 分别标记。迟到事件与当前轮审批的关联是已出现过的实际维护问题。

**人工决策**　强制人工检查点在允许 hook 或自动评审配置下仍保留人工决定。组织需要把哪些动作必须有人签字写入自己的策略，并验证策略确实进入当前运行。

**组织影响**　内部工程实践报告描述人负责优先级与验收标准，并将 agent 暴露的缺口回写仓库；OpenAI Cookbook 演示从真实轨迹、人的反馈和评测迭代 harness。两者是可参考的流程实例。

**版本与演进**　0.171.0 的官方记录（2026-11-20 更新）明确修复较早轮次的完成事件误取消新轮审批，并列出将自动评审缓存按策略版本隔离的改动。

**适用边界**　Rust 开源控制面、OpenAI 内部单团队经验和 Cookbook 示例是三种不同材料；均不能证明任意组织的生产改进比例。本次未调用 Codex 模型或评审服务。

**研究推断**　同一条“允许”需要绑定调用、轮次、策略版本与决策来源，才能支持租户策略变更、迟到消息以及事后责任复核。

**复核实验设计**　为只写临时文件的操作构造常规、强制人工、迟到完成和策略变更四组会话；验证每个动作匹配正确责任人、无复用旧批准，测量人工等待与返工。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-20 · [原始来源 1](https://github.com/openai/codex/blob/a0a30c40e8dbcc44af52e2df64dcce64368d4422/README.md) · [本地快照](../lanes/execution/raw/codex/a0a30c40e8dbcc44af52e2df64dcce64368d4422/README.md)
- request_approval_with_user_prompt L576–625；record_resolution 的决策来源。 · 2026-11-20 · [原始来源 2](https://github.com/openai/codex/blob/a0a30c40e8dbcc44af52e2df64dcce64368d4422/codex-rs/core/src/tools/approvals.rs) · [本地快照](../lanes/execution/raw/codex/a0a30c40e8dbcc44af52e2df64dcce64368d4422/codex-rs/core/src/tools/approvals.rs)
- required_model、approval_review_contributor 等自动评审测试案例；未执行。 · 2026-11-20 · [原始来源 3](https://github.com/openai/codex/blob/a0a30c40e8dbcc44af52e2df64dcce64368d4422/codex-rs/core/tests/suite/auto_review.rs) · [本地快照](../lanes/execution/raw/codex/a0a30c40e8dbcc44af52e2df64dcce64368d4422/codex-rs/core/tests/suite/auto_review.rs)
- 官方 GitHub Releases Atom 内的条目 0.171.0；date 为该条目 updated 的 UTC 日期。 · 2026-11-20 · [原始来源 4](https://github.com/openai/codex/releases/tag/rust-v0.171.0) · [本地快照](../lanes/execution/raw/codex/b167d4a867ff015a/releases.atom)
- 官方示例把轨迹、人的反馈、模型反馈、回归评测和 harness 变更建议串联。 · 2026-05-12 · [原始来源 5](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) · [本地快照](../lanes/execution/raw/codex/961b5ae1b640edb0/report.html)
- 官方单团队实践，来自 web 工具的页面摘录，非全文快照；只支持具体流程。 · 2026-02-11 · [原始来源 6](https://openai.com/index/harness-engineering/) · [本地快照](../lanes/execution/raw/codex/openai-harness-20260211/web-excerpt.json)


### E06 Gemini CLI

**平台**　TypeScript CLI 核心及 policy-engine.md；区分交互与 nonInteractive 模式。

**适用场景**　平台希望在开发者自定义规则之上施加企业规则，同一条命令既能在终端交互执行，也会被无人值守任务调用。

**实现机制**　规则按优先级评估，在工具身份及参数匹配后给出允许、拒绝或询问；检查器还可改变结果。引擎能分解复合 shell 命令并聚合子判断，最终 nonInteractive 模式将 ASK_USER 转成 DENY。管理员可部署系统级策略，文档也列出工作区和用户来源。

**人工决策**　交互模式下操作人可处理询问；无人值守时这个分支直接拒绝，另行排队交给谁取决于外围平台。

**组织影响**　组织可版本化规则，针对 CLI 与后台作业分别设计单元测试，并把“等人”“已拒绝”作为不同运营状态。

**版本与演进**　v0.70.0 的 2026-11-19 更新记录将 policy argsPattern 的实现替换为线性时间的 re2js。该项是匹配实现调整，不是规则引擎的首次引入。

**适用边界**　文档的 Admin tier 表格与后部示例对具体编号有出入，故只采用已交叉核对的优先级和执行语义；未执行平台权限设置。

**研究推断**　审批策略要区分判断本身和运行环境是否有人响应。没有响应端点时，“询问”很可能成为任务失败原因。

**复核实验设计**　用同一无害调用及同一规则文件在终端、无交互 worker 中各跑一次，再添加高优先级拒绝规则；分别记录最终状态、规则 ID、等待时长和人工重开所需操作。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-19 · [原始来源 1](https://github.com/google-gemini/gemini-cli/blob/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/README.md) · [本地快照](../lanes/execution/raw/gemini/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/README.md)
- PolicyEngine.check L771 之后匹配规则与附加检查，L1118–1119 非交互降级。 · 2026-11-19 · [原始来源 2](https://github.com/google-gemini/gemini-cli/blob/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/packages/core/src/policy/policy-engine.ts) · [本地快照](../lanes/execution/raw/gemini/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/packages/core/src/policy/policy-engine.ts)
- Priority system and tiers；Admin tier 数字在同页前后不一致。 · 2026-11-19 · [原始来源 3](https://github.com/google-gemini/gemini-cli/blob/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/docs/reference/policy-engine.md) · [本地快照](../lanes/execution/raw/gemini/d4cb1713fd7fc30f1c03f9ca7cbfed341c97dffd/docs/reference/policy-engine.md)
- 官方 GitHub Releases Atom 内的条目 Release v0.70.0；date 为该条目 updated 的 UTC 日期。 · 2026-11-19 · [原始来源 4](https://github.com/google-gemini/gemini-cli/releases/tag/v0.70.0) · [本地快照](../lanes/execution/raw/gemini/d4c0a4a9d41dc9b2/releases.atom)


### E07 Cline

**平台**　公开工作流文档面向 Cline 用户；实现定位到 SDK core 的 checkpoint-restore 路径。

**适用场景**　代理连续改动文件后，开发者希望比较差异，按风险选择恢复文件、撤回对话步骤或同时恢复两者。

**实现机制**　文档提供三种恢复范围。SDK core 读取检查点历史并判断 stash/commit 形式；只在带第三父提交的快照上认为未跟踪文件已被捕获。恢复前校验当前 HEAD 与快照基线，分支前进、变基或切换后会拦截可能覆盖新提交的操作。

**人工决策**　人选择具体检查点和恢复范围，发现分支已经前进时可只恢复对话或自行处理版本差异。

**组织影响**　共享环境的回退凭据应包含分支、基线提交及快照格式。恢复成功率必须按恢复对象计，代码、对话和外部系统分别对账。

**版本与演进**　SDK v0.2.0 的发布记录（2026-10-26）描述：启动一个已有在途 run 的会话会重连原运行，修复旧运行仍执行而调用方已丢失连接的问题。这是会话重连修复，与恢复代码文件的语义不同。

**适用边界**　用户文档描述 shadow Git 的工作流，SDK 路径对较旧 stash 与未跟踪文件有显式兼容限制。两者可能对应不同界面或演进阶段，本研究未用桌面端重演。

**研究推断**　恢复能力需要区分“回到某个对话”“回到某个文件版本”和“重新连接正在运行的后台任务”，三者对用户承诺不同。

**复核实验设计**　在临时 Git 仓库中分别创建未跟踪文件和后续人工提交，测试三种恢复动作；检查对话、已跟踪文件、未跟踪文件与分支头，记录被主动拦截的情况。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-19 · [原始来源 1](https://github.com/cline/cline/blob/20b042723a14412f6c1e84230b008708534d6e8c/README.md) · [本地快照](../lanes/execution/raw/cline/20b042723a14412f6c1e84230b008708534d6e8c/README.md)
- checkpointCapturedUntracked L337–355；applyCheckpointToWorktree L376–416 校验基线。 · 2026-11-19 · [原始来源 2](https://github.com/cline/cline/blob/20b042723a14412f6c1e84230b008708534d6e8c/sdk/packages/core/src/session/checkpoint-restore.ts) · [本地快照](../lanes/execution/raw/cline/20b042723a14412f6c1e84230b008708534d6e8c/sdk/packages/core/src/session/checkpoint-restore.ts)
- Compare、Restore Files、Restore Task Only 及两者同时恢复的 UI 说明。 · 2026-11-19 · [原始来源 3](https://github.com/cline/cline/blob/20b042723a14412f6c1e84230b008708534d6e8c/docs/core-workflows/checkpoints.mdx) · [本地快照](../lanes/execution/raw/cline/20b042723a14412f6c1e84230b008708534d6e8c/docs/core-workflows/checkpoints.mdx)
- 官方 GitHub Releases Atom 内的条目 SDK v0.2.0；date 为该条目 updated 的 UTC 日期。 · 2026-10-26 · [原始来源 4](https://github.com/cline/cline/releases/tag/sdk%2Fsdk%2Fv0.2.0) · [本地快照](../lanes/execution/raw/cline/207d7b4188f10b16/releases.atom)


### E08 OpenCode

**平台**　OpenCode 2.x 的 TypeScript 会话与后台任务实现。

**适用场景**　父任务委托多个子任务后继续工作，希望收到真正可区分的完成、失败、取消及仍有后台工作的回报。

**实现机制**　SubagentCompletion.deliver 检查持久化作业状态，向父会话写入含 childSessionID 的合成消息；若子代理本轮已完成但仍有后台 shell、脚本等，正文状态显示仍有工作。记录中有通知 ID 时复用它并调用 completeBackground。执行作业只在显式取消时中断子执行。

**人工决策**　人可在父会话读取带子任务身份和剩余工作的回报，适合抽查异常或调整分工；汇报消息本身不批准子代理修改。

**组织影响**　可将作业执行、消息投递、工作项验收画成三条状态线，用同一任务标识关联，以处理服务重启、迟到结果和子任务仍在运行的情形。

**版本与演进**　v2.3.0 的 2026-11-13 发布记录明确将后台子代理设为默认，父会话可继续运行，子代理空闲后汇报；这里是默认行为变化。

**适用边界**　旧记录可能没有剩余工作快照；源码选择重放记载的完成状态。单文件无法证明跨进程“一次且仅一次”投递，本次未实测作业。

**研究推断**　组织管理界面若把“子代理已发总结”当作“整个工作包完成”，可能漏掉尚未结束的构建或脚本。

**复核实验设计**　让子任务产生一项延迟完成的无害后台工作，并在回报前后分别重启父会话；核对父会话汇报、实际作业终态、重复通知数和错误结束次数。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-20 · [原始来源 1](https://github.com/anomalyco/opencode/blob/c98608c513c80558741bb7d56eb8ce14d4e58aa8/README.md) · [本地快照](../lanes/execution/raw/opencode/c98608c513c80558741bb7d56eb8ce14d4e58aa8/README.md)
- formatBody 与 deliver L39–81：正文状态、父会话、通知 ID、未完成任务。 · 2026-11-20 · [原始来源 2](https://github.com/anomalyco/opencode/blob/c98608c513c80558741bb7d56eb8ce14d4e58aa8/packages/core/src/session/subagent-completion.ts) · [本地快照](../lanes/execution/raw/opencode/c98608c513c80558741bb7d56eb8ce14d4e58aa8/packages/core/src/session/subagent-completion.ts)
- 服务终止与显式取消的差异，见 run 的 onInterrupt 路径。 · 2026-11-20 · [原始来源 3](https://github.com/anomalyco/opencode/blob/c98608c513c80558741bb7d56eb8ce14d4e58aa8/packages/core/src/session/subagent-job.ts) · [本地快照](../lanes/execution/raw/opencode/c98608c513c80558741bb7d56eb8ce14d4e58aa8/packages/core/src/session/subagent-job.ts)
- 官方 GitHub Releases Atom 内的条目 v2.3.0；date 为该条目 updated 的 UTC 日期。 · 2026-11-13 · [原始来源 4](https://github.com/anomalyco/opencode/releases/tag/v2.3.0) · [本地快照](../lanes/execution/raw/opencode/c7a3bc06b2d7b44e/releases.atom)


### E09 Claude Agent SDK for Python

**平台**　公开 Python SDK 与其 CLI 控制协议适配层；Claude Code CLI 核心不在该源码证据中。

**适用场景**　企业工单服务希望把代理的待确认操作送入自己的审查界面，并在宿主回调出错时选择明确的失败处理方式。

**实现机制**　Python Query 处理来自 CLI 的 can_use_tool 控制请求，附带上下文调用宿主回调，再发送对应 control_response。独立读循环处理取消及超时；有 hooks、SDK MCP servers 或权限回调时会保留控制输入流。公开类型支持工具执行前 defer，把待处理动作返回宿主。

**人工决策**　can_use_tool 只对进入 ask 路径的权限判断触发；如果希望在每次工具尝试上执行规则，应区分权限回调与 PreToolUse hook。宿主负责把决定绑定到正确的人和请求。

**组织影响**　平台可统一接入审批 UI 和工单，但需要自己维护值班、取消、超时和记录；可对关键 hook 设置故障阻断并检查 CLI 兼容性。

**版本与演进**　v0.2.177 的 2026-11-03 发布记录为 HookMatcher 加入 on_failure。默认 continue，显式 block 能在回调报错、返回空结果或不合法结果时阻断；旧 CLI 不支持时连接会报错。

**适用边界**　SDK 包装层与 CHANGELOG 证明公开协议和行为约定，不能通过该仓库审计闭源 CLI 的每条执行路径。本次未连接模型。

**研究推断**　接入审批界面并不等于覆盖所有动作。平台需要同时验证触发覆盖和审批服务自身不可用时采用的处理方式。

**复核实验设计**　让模拟宿主返回允许、拒绝、延迟、回调异常四类结果，交叉检查默认与显式 block；记录 CLI、SDK 和工单各自保留的请求 ID 与终态。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-19 · [原始来源 1](https://github.com/anthropics/claude-agent-sdk-python/blob/69846cdf82aef59add3b14a26b4f16d1ccee26ba/README.md) · [本地快照](../lanes/execution/raw/claude/69846cdf82aef59add3b14a26b4f16d1ccee26ba/README.md)
- L640–736，can_use_tool、上下文和响应；L1099–1106，输入管道保护。 · 2026-11-19 · [原始来源 2](https://github.com/anthropics/claude-agent-sdk-python/blob/69846cdf82aef59add3b14a26b4f16d1ccee26ba/src/claude_agent_sdk/_internal/query.py) · [本地快照](../lanes/execution/raw/claude/69846cdf82aef59add3b14a26b4f16d1ccee26ba/src/claude_agent_sdk/_internal/query.py)
- DeferredToolUse、HookMatcher.on_failure 及权限返回类型。 · 2026-11-19 · [原始来源 3](https://github.com/anthropics/claude-agent-sdk-python/blob/69846cdf82aef59add3b14a26b4f16d1ccee26ba/src/claude_agent_sdk/types.py) · [本地快照](../lanes/execution/raw/claude/69846cdf82aef59add3b14a26b4f16d1ccee26ba/src/claude_agent_sdk/types.py)
- 0.2.177 加入 on_failure；0.1.74 明确 can_use_tool 只在 ask 触发。 · 2026-11-19 · [原始来源 4](https://github.com/anthropics/claude-agent-sdk-python/blob/69846cdf82aef59add3b14a26b4f16d1ccee26ba/CHANGELOG.md) · [本地快照](../lanes/execution/raw/claude/69846cdf82aef59add3b14a26b4f16d1ccee26ba/CHANGELOG.md)
- 官方 GitHub Releases Atom 内的条目 v0.2.177；date 为该条目 updated 的 UTC 日期。 · 2026-11-03 · [原始来源 5](https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.177) · [本地快照](../lanes/execution/raw/claude/382dd658b1756c74/releases.atom)


### E10 LangGraph

**平台**　Python OSS 图运行时；静态源码观察与本机已安装版本的实测分别记录。

**适用场景**　长工作流在生成建议后暂停等审批，用户数小时后提供决定；开发者需要知道恢复时哪些逻辑会再执行。

**实现机制**　interrupt 抛出可恢复中断。启用 checkpointer 后，调用方以 Command(resume=...) 传回值；节点会从头执行，按节点内 interrupt 调用顺序匹配已有的恢复值。类型化响应可校验，裸 JSON schema 与类型适配器有不同验证语义。

**人工决策**　人能在中断处查看载荷并提交同意、拒绝或补充信息。调用方必须把人的身份、请求有效期和业务授权接入系统。

**组织影响**　适用于跨班次审查、长任务和职责分工。若中断前已经写外部系统，需用业务幂等键或事务边界保护重复写入。

**版本与演进**　1.2.24 的发布记录（2026-11-20 更新）修复 DeltaChannel 遇到 None checkpoint 等边界；此次修复不能用作 interrupt 首次上线时间。

**适用边界**　本机已安装的 LangGraph 0.2.71 和单独安装、与固定源码同版的 1.2.24 各跑四次离线实验。两版均用同进程 MemorySaver：approve 或 deny 均能恢复；放在中断前的计数由 1 变 2，放到前一已结束节点则保持 1。源码固定在 1.2.24 对应提交。未测跨进程持久存储和外部事务。

**研究推断**　审批落点是副作用设计问题。即使“等人再继续”的界面完全正确，恢复前缀仍可能重复发送通知、创建工单。

**复核实验设计**　已执行双版本、同进程、双决策、双节点布置的八次对照并保留脚本和输出；下一步用持久化存储、进程重启及幂等外部写入模拟执行，比较重复副作用与丢失恢复数。

- 仓库 README 定位产品用途、平台和入口。 · 2026-11-20 · [原始来源 1](https://github.com/langchain-ai/langgraph/blob/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/README.md) · [本地快照](../lanes/execution/raw/langgraph/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/README.md)
- interrupt L913–1053，节点重放、检查点、响应验证与中断顺序。 · 2026-11-20 · [原始来源 2](https://github.com/langchain-ai/langgraph/blob/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/libs/langgraph/langgraph/types.py) · [本地快照](../lanes/execution/raw/langgraph/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/libs/langgraph/langgraph/types.py)
- PregelLoop 对待处理写入、恢复的配置与 interrupt 的调度。 · 2026-11-20 · [原始来源 3](https://github.com/langchain-ai/langgraph/blob/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/libs/langgraph/langgraph/pregel/_loop.py) · [本地快照](../lanes/execution/raw/langgraph/58a6e1cc5b7dfc3619fc6e7e7573b040d554649b/libs/langgraph/langgraph/pregel/_loop.py)
- 官方 GitHub Releases Atom 内的条目 langgraph==1.2.24；date 为该条目 updated 的 UTC 日期。 · 2026-11-20 · [原始来源 4](https://github.com/langchain-ai/langgraph/releases/tag/1.2.24) · [本地快照](../lanes/execution/raw/langgraph/b7ba725b3b6b853d/releases.atom)


### E11 mini-SWE-agent

**平台**　Python 默认 agent 与独立环境适配器；与 SWE-agent 同团队、不同仓库及执行设计。

**适用场景**　为了判断复杂编排究竟产生多少增益，需要一个可以复核每次调用、限制成本和保留轨迹的简单基线。

**实现机制**　默认 agent 每一步查询模型，将返回动作交给 env.execute，再格式化观察结果。查询前检查累计调用、成本和经过时间；格式解析失败也要计入已发生费用，连续格式错误达到限制时退出。每轮 finally 调用 save，是否落盘由输出路径决定。

**人工决策**　实验者预设资源限制并检查轨迹；在这条默认运行路径中逐步查询看不到独立的人审节点。交互体验不能从这个类泛化到所有前端。

**组织影响**　可作为企业自动化 A/B 的对照组，把成功率增益与重试、上下文、工具预算分开，比仅对比模型总价有效。

**版本与演进**　v2.4.6 的 2026-07-23 记录显式修复“已计费但结果解析失败”未计入 cost_limit 的问题。

**适用边界**　成本上限在发出下一次请求前检查，单次调用可能使累计值超过限额。真实费用也依赖模型适配器在返回中提供成本。本次未跑仓库 benchmark。

**研究推断**　若失败尝试从成本账本消失，自动重试表面上成功率提高，实际经济性会被高估。

**复核实验设计**　使用固定响应的模型替身制造连续解析错误、正常退出和一次超预算请求，对照供应商模拟账单、轨迹、退出原因与最终超支幅度。

- 仓库 README 定位产品用途、平台和入口。 · 2026-09-03 · [原始来源 1](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md) · [本地快照](../lanes/execution/raw/mini/04d809ceab9df28f9adaed044884180159172930/README.md)
- run/query/execute_actions L88–157，异常费用、终止、观察与保存。 · 2026-09-03 · [原始来源 2](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/src/minisweagent/agents/default.py) · [本地快照](../lanes/execution/raw/mini/04d809ceab9df28f9adaed044884180159172930/src/minisweagent/agents/default.py)
- LocalEnvironment.execute 以及 _run 超时后结束进程组的实现。 · 2026-09-03 · [原始来源 3](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/src/minisweagent/environments/local.py) · [本地快照](../lanes/execution/raw/mini/04d809ceab9df28f9adaed044884180159172930/src/minisweagent/environments/local.py)
- 官方 GitHub Releases Atom 内的条目 v2.4.6；date 为该条目 updated 的 UTC 日期。 · 2026-07-23 · [原始来源 4](https://github.com/SWE-agent/mini-swe-agent/releases/tag/v2.4.6) · [本地快照](../lanes/execution/raw/mini/817fcf2059cd1f5d/releases.atom)


### D01 GitHub Actions Runner

**适用场景**　自托管 runner 接到仓库 workflow 作业；平台团队要在各仓库步骤外统一校验执行条件或收尾。

**实现机制**　Worker 先准备动作，读取宿主的 ACTIONS_RUNNER_HOOK_JOB_STARTED，将同步脚本纳入 pre-job；另读取 JOB_COMPLETED 注册 always() 的 post-job。ADR 约定脚本非零退出使作业失败。

**人工决策**　runner 管理员配置宿主脚本和退出码；开发者可从作业结果查到失败，再决定修改工作负载还是调整宿主策略。

**组织影响**　在共用 runner 池集中实施环境检查、留存审计信息；前置脚本本身的耗时和故障会影响整池。

**版本与演进**　2026-10-26 UTC，v2.338.2 的变更记录包含 Docker 29.8.0 和 Buildx 0.37.0 更新。这里记录运行环境演进，hook 的既有设计另由 ADR 与源码证明。

**适用边界**　入口在自托管 runner；动作准备早于 pre-job hook。宿主失联、强制终止时能否完整收尾未实测，不能把注册 post-hook 当作交付凭据。

**研究推断**　治理可以下沉到维护者可控制的 runner，使大量仓库复用一份规则；要单独测量宿主检查故障引起的全局阻塞。

**复核实验设计**　在隔离池令 pre-hook 对带错标签的作业返回非零；提交同一任务到有/无 hook 的池，核对本体是否执行、失败分类、正常结束与人为终止时的清理记录。

- JobExtension.cs L297–315、572–586：准备动作、加入启动钩子、注册完成钩子 · 2026-11-19 · [原始来源 1](https://github.com/actions/runner/blob/7e211dc69c347b78fc398e630e74facb11a13235/src/Runner.Worker/JobExtension.cs) · [本地快照](../lanes/delivery/raw/runner/394a839d2eca-JobExtension.cs)
- ADR 1751 L60–76：同步、退出码和管理员责任 · 2026-11-19 · [原始来源 2](https://github.com/actions/runner/blob/7e211dc69c347b78fc398e630e74facb11a13235/docs/adrs/1751-runner-job-hooks.md) · [本地快照](../lanes/delivery/raw/runner/bde72ee444dc-1751-runner-job-hooks.md)
- 发布页 变更列表 中的 Docker / Buildx 更新 · 2026-10-26 · [原始来源 3](https://github.com/actions/runner/releases/tag/v2.338.2) · [本地快照](../lanes/delivery/raw/runner/b5f68acc6324-v2.338.2.html)


### D02 Buildkite Agent

**适用场景**　自托管 worker 已经运行构建；控制端收到取消或超时，此时需把中央意图落实到具体作业进程。

**实现机制**　JobRunner 在进程启动后轮询 job state，带抖动；服务返回 canceling/canceled 或 timing_out/timed_out 时分别调用 Cancel 并传递原因。401 也触发因凭据无效而取消；短暂的普通请求失败等待下一轮。

**人工决策**　操作人员可以从控制端请求取消，runner 管理员配置检查间隔和信号。用户点击中止后，执行端仍需收到状态并处理信号。

**组织影响**　平台团队可对不同队列统一记账，区分人工中止、凭据失效、运行超时，从而定位基础设施滞后。

**版本与演进**　2026-11-19 UTC，v4.12.0 将产物上传路径纳入 signed jobs 的签名与校验，并提示先更新验签 agent，再用新版本签署 pipeline。

**适用边界**　Agent 源码可见；托管控制端的内部调度未核对。文档与源码不提供用户点击到外部副作用停止的端到端时限。

**研究推断**　作业取消应产生可测的控制延迟；签名协议升级也需要兼容性发布顺序。

**复核实验设计**　记录取消请求、runner 观测、子进程退出三个时间戳；比较不同轮询间隔、短时离线及有无外部异步子任务时的尾延迟和残留作业数。

- agent/job_runner.go L1032–1105：轮询、抖动、401、cancel 和 timeout 分支 · 2026-11-19 · [原始来源 1](https://github.com/buildkite/agent/blob/895c5a0a2b0e6289ca486b9f74a21a07bfaeb76a/agent/job_runner.go) · [本地快照](../lanes/delivery/raw/buildkite/8169ce30dc1c-job_runner.go)
- README L19–48：agent 子命令、build queue 与安装入口 · 2026-11-19 · [原始来源 2](https://github.com/buildkite/agent/blob/895c5a0a2b0e6289ca486b9f74a21a07bfaeb76a/README.md) · [本地快照](../lanes/delivery/raw/buildkite/e0451dd23140-README.md)
- v4.12.0 Security 条目以及升级验签 agent 顺序 · 2026-11-19 · [原始来源 3](https://github.com/buildkite/agent/releases/tag/v4.12.0) · [本地快照](../lanes/delivery/raw/buildkite/80c6be842a18-v4.12.0.html)


### D03 Tekton Pipelines

**适用场景**　测试或部署 PipelineRun 在并行执行中被叫停，还需要决定是否让在途任务收尾、保留清理或取证步骤。

**实现机制**　控制器从 PipelineRun 状态协调 TaskRun。CancelledRunFinally 中止正在运行的任务并继续 finally；StoppedRunFinally 允许在途任务及其重试走完，阻止新的普通任务，再调度 finally。普通 Cancelled 不调度待运行的 finally。

**人工决策**　具备相应权限的调用方选择中止语义；创建时设 Pending 可将启动推迟到条件满足，不等于自带审批身份验证。

**组织影响**　分别编码紧急刹车、温和排空和清理证明，跨团队可对齐同一运行对象及父子任务归属。

**版本与演进**　2026-10-29 UTC，v1.18.0 通过 webhook 使控制器设置的 pipeline、pipelineTask、pipelineRun 标签一经写入不可被更新者改写。

**适用边界**　需要 Kubernetes 与 Pipeline 控制器；finally 仍受总时限等条件约束。服务端 RBAC、集群故障和副作用回滚未实测。

**研究推断**　为组织提供一个取消按钮之前，需要明确它对在途动作与证据留存的承诺。

**复核实验设计**　让任务 A 处于写产物阶段、B 等待依赖、finally 归档；分别发三种取消请求，比较运行任务、重试、子任务归属和归档结果。

- pipelinerun.go L349–355、867–875：finally 超时与温和中止分支 · 2026-11-18 · [原始来源 1](https://github.com/tektoncd/pipeline/blob/94305b77d30f12e1b8e39e51b2f559fd35c55e13/pkg/reconciler/pipelinerun/pipelinerun.go) · [本地快照](../lanes/delivery/raw/tekton/69bd72212fa5-pipelinerun.go)
- pipelineruns.md L1695–1756：三类取消/停止和 Pending 时机 · 2026-11-18 · [原始来源 2](https://github.com/tektoncd/pipeline/blob/94305b77d30f12e1b8e39e51b2f559fd35c55e13/docs/pipelineruns.md) · [本地快照](../lanes/delivery/raw/tekton/f899e8136dff-pipelineruns.md)
- v1.18.0 controller-managed labels immutable via webhook，#10687 · 2026-10-29 · [原始来源 3](https://github.com/tektoncd/pipeline/releases/tag/v1.18.0) · [本地快照](../lanes/delivery/raw/tekton/cf9ac6eacd93-v1.18.0.html)


### D04 Argo CD

**适用场景**　集群对象与 Git 期望配置发生偏离，团队需区分检测差异、修正漂移，以及是否删除额外对象。

**实现机制**　controller 将目标与 live 对象配对，对额外且属于本应用的对象设置 RequiresPruning；资源忽略规则、所有权和比较错误会影响 Synced、OutOfSync 或 Unknown。automated、prune、allowEmpty、selfHeal 分别控制动作。

**人工决策**　应用维护者选择是否开启自动同步、清理、空目标和自愈；自动同步开启时直接 rollback 有限制，紧急干预需要预先定义流程。

**组织影响**　把版本库作为变更入口、把现场差异作为运行证据，平台团队可单独放宽自愈或收紧删除。

**版本与演进**　2026-11-18 UTC，v3.6.2 修正 Unknown 同步状态之后仍复用差异缓存的问题，并在 manifest-generate-paths 无变化时保留服务端差异缓存。

**适用边界**　多源应用关闭 selfHeal 仍不能保证现场修改永久保留；同步状态描述配置差异，不能证明服务正确或业务指标正常。

**研究推断**　期望状态、测不到状态、实测业务结果应分字段保存，否则会以缓存状态误报完成。

**复核实验设计**　测试命名空间制造现场漂移、额外对象及无法读取对象；分别开启 selfHeal/prune，观察状态与动作，再与业务健康检查对照。

- controller/state.go L992–1029、1058–1089：比较错误、所有权、清理标志、状态判断 · 2026-11-19 · [原始来源 1](https://github.com/argoproj/argo-cd/blob/47fd59165c522e5c16101223f9d8a86b927eb5f2/controller/state.go) · [本地快照](../lanes/delivery/raw/argocd/4011c8a8a8d2-state.go)
- auto_sync.md 的 Automatic Pruning、Self-Healing、Automated Sync Semantics 以及 L209–215 限制 · 2026-11-19 · [原始来源 2](https://github.com/argoproj/argo-cd/blob/47fd59165c522e5c16101223f9d8a86b927eb5f2/docs/user-guide/auto_sync.md) · [本地快照](../lanes/delivery/raw/argocd/31acd86aa5e7-auto_sync.md)
- v3.6.2 controller diff cache 的 #30893 / #30899 · 2026-11-18 · [原始来源 3](https://github.com/argoproj/argo-cd/releases/tag/v3.6.2) · [本地快照](../lanes/delivery/raw/argocd/242295cb7172-v3.6.2.html)


### D05 Argo Rollouts

**适用场景**　金丝雀达到特定步骤后，应根据一段指标窗口判断能否放量、是否中止，或转人工处理。

**实现机制**　AnalysisRun 记录各指标的测量和计数。控制器在判断连续成功前先检查失败、无结论和错误限额；配置 dryRun 的指标仍产生测量数据但不左右最终判定。分析可得到 Successful、Failed 或 Inconclusive 等状态。

**人工决策**　在 rollout 的分析语境中，维护者可在无结论时检查测量，再决定继续或中止；可先以 dry-run 收集新指标的行为。

**组织影响**　业务服务团队制定指标和阈值，平台复用分析流程；可拆开统计“明确退化”与“证据不足”两类等待。

**版本与演进**　2026-11-05 UTC，v1.11.0-rc1 的 Web metric provider 对空响应或非 JSON 响应也计算成功/失败表达式，改变以往直接 Successful 的行为；这是候选版本。

**适用边界**　结果强依赖采样窗口、流量、数据源和条件表达式。未运行集群或测量真实告警误报。不同终止方式有独立语义。

**研究推断**　需要把空样本和解释不清的结果带给人；把两者折叠为成功会向更多用户扩展不确定变更。

**复核实验设计**　在隔离金丝雀中注入正常指标、阈值边界、空正文、持续无数据；记录 AnalysisRun 原始测量、最终相位和人工处置，对比 RC 与旧版。

- analysis/analysis.go L104–136、398–439、620–722：测量归集、失败优先和计数阈值 · 2026-11-18 · [原始来源 1](https://github.com/argoproj/argo-rollouts/blob/458eab520fdbf360d1b34b6f6bc0f05e52ae6258/analysis/analysis.go) · [本地快照](../lanes/delivery/raw/rollouts/b9a2bcb5213c-analysis.go)
- analysis.md Failure Limits and ConsecutiveSuccessLimit、Dry-Run、Inconclusive Runs · 2026-11-18 · [原始来源 2](https://github.com/argoproj/argo-rollouts/blob/458eab520fdbf360d1b34b6f6bc0f05e52ae6258/docs/features/analysis.md) · [本地快照](../lanes/delivery/raw/rollouts/d398b6f01fad-analysis.md)
- v1.11.0-rc1 Breaking Changes 中 Web metric provider 成功/失败表达式 · 2026-11-05 · [原始来源 3](https://github.com/argoproj/argo-rollouts/releases/tag/v1.11.0-rc1) · [本地快照](../lanes/delivery/raw/rollouts/6976af9657c3-v1.11.0-rc1.html)


### D06 Renovate

**适用场景**　自动依赖更新已经产生分支，高频的小更新若逐个等待审批会积压，团队需选择可放行的更新类型。

**实现机制**　tryBranchAutomerge 要求启用 automerge 且类型为 branch，检查 automergeSchedule、分支是否已有 PR，再读取分支状态。green 才尝试 mergeAndPush；红色、非就绪、队列或分支保护产生各自结果。PR 类型走另一条路径。

**人工决策**　维护者设置 packageRules、必检项、保护分支和 merge queue；组织 preset 可继承，仓库可以覆盖规则。

**组织影响**　精细缩小无需逐项人工审查的范围，同时用队列分歧或保护规则失败解释等待。应按更新类别跟踪返工。

**版本与演进**　2026-11-19 UTC，44.253.4 在 GitLab 平台修复重新为已推送 commit 启用 automerge 的行为，显示平台侧合并状态要随新提交更新。

**适用边界**　ignoreTests 与平台检查配置会影响什么能被认作绿色。高频主分支提交也会缩小合并机会；自动成功不等于依赖升级无兼容问题。

**研究推断**　可自动批准的单位应是具有明确影响面和可复查检查集的变更类别；不要笼统授权全部低行数改动。

**复核实验设计**　同一仓库以 patch/minor/major 与检查齐全/缺失分层，先用 dry-run 分类，检查主分支再更新时的重新评估情况。

- automerge.ts L21–111：类型、时段、已有 PR、状态、dry-run、保护分支与错误处理 · 2026-11-19 · [原始来源 1](https://github.com/renovatebot/renovate/blob/c69fdddaa26c7742b7edbae5d61ab7269141642a/lib/workers/repository/update/branch/automerge.ts) · [本地快照](../lanes/delivery/raw/renovate/908500fb11cc-automerge.ts)
- automerge.md Automerge / Merge Queues / Overriding global automerge · 2026-11-19 · [原始来源 2](https://github.com/renovatebot/renovate/blob/c69fdddaa26c7742b7edbae5d61ab7269141642a/docs/usage/key-concepts/automerge.md) · [本地快照](../lanes/delivery/raw/renovate/0ae7af06669b-automerge.md)
- 44.253.4 的 platform/gitlab 修复 #47980 · 2026-11-19 · [原始来源 3](https://github.com/renovatebot/renovate/releases/tag/44.253.4) · [本地快照](../lanes/delivery/raw/renovate/2a008cb3fb54-44.253.4.html)


### D07 PR-Agent

**适用场景**　PR 大于单次上下文，部分分片可能未成功。评审者需要知道模型看过什么，哪些反馈值得再次核查。

**实现机制**　PRReviewer 合并各片推断前过滤低置信发现，以免挤占结果上限；发布判断考虑 finding 状态变化、状态阻塞或部分分片失败。部署端保留特定配置键的控制权。

**人工决策**　负责人复核 PR 反馈与未覆盖部分；v0.50.0 明确 auto-approval 路径仍禁用，配置项归宿主所有。社区项目的行为不外推至厂商商业产品。

**组织影响**　评审队列可按未覆盖或失败部分分派复核，避免把空评论计成完整检查。可收集每条建议的采纳与误报。

**版本与演进**　2026-11-07 UTC，v0.50.0 收紧仓库可改写的重试和调用次数配置，同时把 enable_auto_approval 改为宿主专有；该版本发布说明区分“增加配置约束”与“已启用自动批准”。

**适用边界**　本地调用固定 SHA 的配置判定函数，自动批准与重试次数均返回宿主专有，仓库可调整 skills.enabled 与 max_skills_tokens。未运行模型或连接 PR 平台；分片之间跨文件依赖、过滤阈值和供应商超时均可能影响覆盖与准确率。

**研究推断**　把模型覆盖情况作为交付证据的一部分交给人，独立维护“评审者是谁”和“谁有批准权”。

**复核实验设计**　固定有跨文件关联的 PR，让一片超时并重复运行；比对覆盖提示、模型发现、人工标注，以及失败片重跑后仍未发现的缺陷。

- pr_reviewer.py L920–939、1809–1834：公布状态、分片结果过滤及合并 · 2026-11-19 · [原始来源 1](https://github.com/The-PR-Agent/pr-agent/blob/b5bdfed1286513700b12b5ea5bbe6c8fa15734e6/pr_agent/commands/pr_reviewer.py) · [本地快照](../lanes/delivery/raw/pragent/ea6819c762b8-pr_reviewer.py)
- config_security.py L42–155：宿主专有键及判定 · 2026-11-19 · [原始来源 2](https://github.com/The-PR-Agent/pr-agent/blob/b5bdfed1286513700b12b5ea5bbe6c8fa15734e6/pr_agent/config_security.py) · [本地快照](../lanes/delivery/raw/pragent/61b4e7a25297-config_security.py)
- v0.50.0 Breaking changes：Host-only settings、Auto-approval、#4700 · 2026-11-07 · [原始来源 3](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.50.0) · [本地快照](../lanes/delivery/raw/pragent/efa30f4b8efe-v0.50.0.html)


### D08 Atlantis

**适用场景**　团队在 PR 里查看 Terraform/OpenTofu 计划，再由有权者执行 apply；并发和计划版本变化会影响当初审阅的内容。

**实现机制**　执行端先检查项目 apply 要求与依赖，然后获取项目/目录工作锁，加载已保存计划。在托管 plan/apply 路径中检查计划，并紧邻具体 apply 步骤再次验证。v0.49.0 为新生成的计划记录哈希。

**人工决策**　有权者检查计划后触发 apply；审批规则检查与已保存计划摘要验证是两个条件。发布说明明确 approval 自身没有与某一条 plan 记录绑定。

**组织影响**　将 PR、项目、workspace、计划摘要、审批和实际应用结果联系起来，区分“谁授权”与“授权时/应用时是什么产物”。

**版本与演进**　2026-10-25 UTC，v0.49.0 拒绝应用生成后被改动的已记录计划，要求重新 plan；审批条件在 GitHub/Gitea 以每个评审者最新 review 为准。

**适用边界**　使用定制步骤的工作流是否采用 Atlantis 托管计划需要逐项确认；默认保证仅适用于对应路径，旧版本留下的计划也不能一概视为已有哈希。

**研究推断**　高影响操作可借鉴 plan→review→apply，但应显式检查人实际看到的版本以及即将应用的摘要；重新规划也应重新评估审阅需求。

**复核实验设计**　沙盒使用无外部资源的 IaC，分别保留和刷新计划、制造并行 PR；核对被应用产物、锁持有者、最近 review 和重计划日志。

- project_command_runner.go L943–1008、1207–1256、1296–1302：要求、锁、计划加载和再次验证 · 2026-11-18 · [原始来源 1](https://github.com/runatlantis/atlantis/blob/2714f4a6dfcd75c798eec34b6dbe653a99c34a89/server/events/project_command_runner.go) · [本地快照](../lanes/delivery/raw/atlantis/0dc47b035092-project_command_runner.go)
- README 的项目说明及官方用户文档入口 · 2026-11-18 · [原始来源 2](https://github.com/runatlantis/atlantis/blob/2714f4a6dfcd75c798eec34b6dbe653a99c34a89/README.md) · [本地快照](../lanes/delivery/raw/atlantis/6d5b05623ff9-README.md)
- v0.49.0 Upgrade checklist 及 Apply/Approvals 关于计划摘要和最新 review · 2026-10-25 · [原始来源 3](https://github.com/runatlantis/atlantis/releases/tag/v0.49.0) · [本地快照](../lanes/delivery/raw/atlantis/b1ca25cc1e29-v0.49.0.html)


### D09 Conftest

**适用场景**　待合并的配置、IaC 或所有者清单发生变化，团队希望在调用外部系统前运行可重复的规则。

**实现机制**　TestRunner 按格式解析输入，加载 Rego 策略、数据、能力集与命名空间；通常按文件检查，也可合并后跨文件检查，返回结构化结果。已运行 v0.71.0 CLI，以自编生产 owner 规则得到预期退出码。

**人工决策**　领域负责人维护规则、例外和何时阻断，CI 管理者决定将退出码接成必检。团队可以把结构化的命中原因交给变更作者。

**组织影响**　让可机械验证的要求共享同一套策略；对要求 owner 的演示，生产环境有 owner / 缺失 / 开发环境缺失分别返回 0 / 1 / 0。

**版本与演进**　2026-09-30 UTC，v0.71.0 新增 CODEOWNER 文件解析器，并修复多文件时 TAP 输出产生多份计划的问题。本文的最小实验使用 JSON，未实测这个新解析器。

**适用边界**　已实测的只是 Windows 本地 CLI 的三组 JSON，不代表 CI 分支保护、真实所有权、线上漂移或团队生产率已经验证。

**研究推断**　优先把重复评审意见中语义稳定的一部分转成有版本的规则；统计规则覆盖的真实事件与误阻断。

**复核实验设计**　在历史配置变更做留出回放，比较现有人工审查与策略输出；重点复核例外、缺少上下文的通过样本、误阻断率及修复耗时。

- runner/test.go L45–122：格式解析、规则加载、命名空间、独立与组合检查 · 2026-11-19 · [原始来源 1](https://github.com/open-policy-agent/conftest/blob/31757a2c6bc2b7e370ae7dfa88b0bad7b433d9b4/runner/test.go) · [本地快照](../lanes/delivery/raw/conftest/fa210c42c7c2-test.go)
- docs/index.md 的 deny、JSON 输出、query 与上下文 · 2026-11-19 · [原始来源 2](https://github.com/open-policy-agent/conftest/blob/31757a2c6bc2b7e370ae7dfa88b0bad7b433d9b4/docs/index.md) · [本地快照](../lanes/delivery/raw/conftest/478e7caadb8c-index.md)
- v0.71.0 New Features #1404、Bug Fixes #1435 · 2026-09-30 · [原始来源 3](https://github.com/open-policy-agent/conftest/releases/tag/v0.71.0) · [本地快照](../lanes/delivery/raw/conftest/d55a96676dfb-v0.71.0.html)


### D10 Temporal（Python SDK）

**适用场景**　一个研发任务可能先执行外部 Activity，再等维护者决定；等待跨越 worker 重启或新版本上线。

**实现机制**　SDK 在激活时读取 replay 标记及历史逻辑标记，分组处理 signal、update 等事件；示例通过 workflow.wait_condition 等待 signal 改变状态，也可设超时。Replayer 能用已有 history 检查新 workflow 实现。

**人工决策**　业务实现决定谁可发 signal、何时超时、如何重试外部操作；编排层可保存决定并继续，而非一直占用一个模型请求。

**组织影响**　用持久工作流表达等待、取消、重试和升级，历史回放可成为平台变更的一项兼容性检查。

**版本与演进**　2026-11-14 UTC，1.36.1 对未记录逻辑标记 2 的工作流默认关闭 single-batch 激活，以维持旧 signal/条件等待/取消的行为；已记录标记 2 的 history 继续使用该语义。

**适用边界**　基于 Python SDK 的证据不能直接外推所有语言。重复外部副作用是否受控，取决于 Activity 和下游的幂等设计；未运行 Temporal 服务或测试历史。

**研究推断**　工作流版本升级必须尊重在途实例的事件历史。评估 harness 时应把跨版本恢复与外部副作用区分开。

**复核实验设计**　录制“发出请求→等待 signal→取消”不同先后次序的 histories，在两个 SDK 版本上回放；另对重复 Activity 注入幂等键，分别记录兼容性与外部写入次数。

- temporalio/worker/_workflow_instance.py L480–545、4264–4271：replay、逻辑标记与激活分组 · 2026-11-19 · [原始来源 1](https://github.com/temporalio/sdk-python/blob/333910697b8f7080660a30e14745b68265f55f42/temporalio/worker/_workflow_instance.py) · [本地快照](../lanes/delivery/raw/temporal/7330de10f96f-_workflow_instance.py)
- README 的 Workflow Replay、wait_condition、signal 超时示例 · 2026-11-19 · [原始来源 2](https://github.com/temporalio/sdk-python/blob/333910697b8f7080660a30e14745b68265f55f42/README.md) · [本地快照](../lanes/delivery/raw/temporal/98a2c89ea55d-README.md)
- 1.36.1 Notable Changes 对 flag 2 的兼容规则 · 2026-11-14 · [原始来源 3](https://github.com/temporalio/sdk-python/releases/tag/1.36.1) · [本地快照](../lanes/delivery/raw/temporal/fd30f046623d-1.36.1.html)


### D11 Jenkins Pipeline Input Step

**适用场景**　生产发布抵达 Jenkins Pipeline 的 input 步骤时，需要指定值班组或人员确认，或由有权人员中止。

**实现机制**　InputStepExecution 在 POST 端点做 preSubmissionCheck，检查是否已经处理、是否可提交；未指定 submitter 用 Job.BUILD 权限，指定时按用户/组匹配并保留管理员特例。submitterParameter 可记录提交者，abort 向流水线传播中断。

**人工决策**　配置者设定可提交人员或组；经授权的账号确认、填写参数或拒绝。管理员特例需进入组织自己的职责分离检查。

**组织影响**　平台用同一输入步骤表达例外升级；能统计等待时长、决策者与处理结果，为减少无价值等待提供样本。

**版本与演进**　2026-07-02 UTC，560.v56198a_642157 为 Pipeline Graph View 复用 input 对话框增加资源文件，使另一界面复用交互。此项属于呈现与集成变更。

**适用边界**　该插件不自动判断审批者当时看到哪个 commit 或产物，也不能仅凭一次确认断言双人分权成立；构建参数另需绑定具体交付内容。

**研究推断**　审批事件至少应能关联可执行产物与决策者。等待点可以复用 Jenkins，证据绑定仍须在上层实现。

**复核实验设计**　用普通构建者、指定组成员和管理员分别提交或拒绝同一输入，记录结果、提交者字段及重复提交响应；更新构建版本后检查旧批准能否被复用。

- InputStepExecution.java L284–311、336–346、372–396：批准/拒绝、处理状态、人员与组 · 2026-11-09 · [原始来源 1](https://github.com/jenkinsci/pipeline-input-step-plugin/blob/0c9db265274122f4ff54056c7d5977f266ef75db/src/main/java/org/jenkinsci/plugins/workflow/support/steps/input/InputStepExecution.java) · [本地快照](../lanes/delivery/raw/jenkins/c2863f36c0b2-InputStepExecution.java)
- README L23–39：submitter 与 submitterParameter · 2026-11-09 · [原始来源 2](https://github.com/jenkinsci/pipeline-input-step-plugin/blob/0c9db265274122f4ff54056c7d5977f266ef75db/README.md) · [本地快照](../lanes/delivery/raw/jenkins/8c9b7338ca6d-README.md)
- 560.v56198a_642157 的 Pipeline Graph View 对话框 #258 · 2026-07-02 · [原始来源 3](https://github.com/jenkinsci/pipeline-input-step-plugin/releases/tag/560.v56198a_642157) · [本地快照](../lanes/delivery/raw/jenkins/b89a96a9b16d-560.v56198a_642157.html)


### O01 Backstage Software Catalog

**适用场景**　跨仓库变更或运行失败需要找受影响组件和维护组。目录后端持续摄取实体描述，前端展示实体及其关系。

**实现机制**　处理器解析 Component 的 owner、dependsOn、dependencyOf 等字段，生成双向关系；来源实体先处理再拼接，处理中的实体与读者看到的最终实体有时间差。

**人工决策**　团队维护服务描述和 owner，平台维护实体处理器。将目录用来查候选负责人，审批身份仍由执行系统验证。

**组织影响**　把工作对象从仓库文件提升为服务、团队和依赖，对跨团队任务可先路由再派工。

**版本与演进**　2026-11-17 v1.57.0 将若干前端插件 API 稳定为 1.0；此为门户扩展接口稳定化，不能据此为早已存在的目录关系定首发日期。

**适用边界**　静态声明会过时，目录出现 owner 不证明该人员当班或有生产权限。未部署。

**研究推断**　建立可查询且允许纠错的责任关系，比把所有仓库知识复制到 agent 上下文更适合分配跨团队例外。

**复核实验设计**　抽 30 个真实服务，让目录推荐负责人，与轮值表及历史处理人交叉核验；记录无 owner、过期和多归属冲突。

- 来源进入目录、processing 与 stitching 的异步边界，生命期与 orphan 说明。 · 2026-11-19 · [原始来源 1](https://github.com/backstage/backstage/blob/184acad411be8cfbac126c3a2885cb4740109176/docs/features/software-catalog/life-of-an-entity.md) · [本地快照](../lanes/organization/raw/backstage/184acad411be8cfbac126c3a2885cb4740109176/docs/features/software-catalog/life-of-an-entity.md)
- BuiltinKindsEntityProcessor.ts 第 114–198 行，实体引用归一化、正反关系与 Component 字段发射。 · 2026-11-19 · [原始来源 2](https://github.com/backstage/backstage/blob/184acad411be8cfbac126c3a2885cb4740109176/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) · [本地快照](../lanes/organization/raw/backstage/184acad411be8cfbac126c3a2885cb4740109176/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts)
- 2026-11-17 v1.57.0 将若干前端插件 API 稳定为 1.0；此为门户扩展接口稳定化，不能据此为早已存在的目录关系定首发日期。 · 2026-11-17 · [原始来源 3](https://github.com/backstage/backstage/releases/tag/v1.57.0) · [本地快照](../lanes/organization/raw/backstage/release-v1.57.0.html)


### O02 Apache DevLake

**适用场景**　组织同时用多个 AI 工具，希望知道哪一段交付时间变化，及不同工具指标能否比较。

**实现机制**　Go 计算器取项目映射内已合并 PR，用首提交、首个非作者评论、合并与成功生产部署分段计算。部署先按 SHA 直连，再从前后成功部署的 commit diff 回查；无映射时部署阶段为空。

**人工决策**　数据负责人定义项目/生产环境映射并复核遗漏。平台负责人解释等待时间，试点团队决定是否调整评审容量。

**组织影响**　PostgreSQL 多 AI 看板直接承认不同来源返回的行数与操作不同；Kiro 不提供建议采纳事件，接受率留空。

**版本与演进**　2026-11-02 v1.0.3-beta19 为 PostgreSQL 增补 Cursor/Multi-AI 面板并将 Claude Code 纳入多 AI 对比，修复无上次成功部署时重复计算；属于 beta。

**适用边界**　合并样本排除被放弃的补丁；未映射生产数据会漏阶段。面板不能从活跃量推断真实因果提效。未部署。

**研究推断**　组织应先给每个工具的事件分母和缺失值签字，再让领导看工具对比。空值替成零会误导采购。

**复核实验设计**　给同一组 PR 逐个核对首评、上线 SHA、弃用原因和漏链，报告覆盖率及按失败/弃用分层的周期。

- change_lead_time_calculator.go 第 82–85、118–165、250–334 行，PR 纳入、时间段、成功生产部署映射与缺失。 · 2026-11-19 · [原始来源 1](https://github.com/apache/devlake/blob/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/backend/plugins/dora/tasks/change_lead_time_calculator.go) · [本地快照](../lanes/organization/raw/devlake/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/backend/plugins/dora/tasks/change_lead_time_calculator.go)
- 多 AI 看板的 Claude Code: Tool Actions、Returned Lines & Acceptance Availability 与 Acceptance Rate Availability 面板。 · 2026-11-19 · [原始来源 2](https://github.com/apache/devlake/blob/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/grafana/dashboards/postgresql/multi-ai-comparison.json) · [本地快照](../lanes/organization/raw/devlake/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/grafana/dashboards/postgresql/multi-ai-comparison.json)
- calculate_change_lead_time_test.go 的项目映射和端到端 fixture，作为官方测试规范阅读，未执行。 · 2026-11-19 · [原始来源 3](https://github.com/apache/devlake/blob/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/backend/plugins/dora/e2e/calculate_change_lead_time_test.go) · [本地快照](../lanes/organization/raw/devlake/652d7da9323fd4447d3c2d3705f482ff5a9f54d8/backend/plugins/dora/e2e/calculate_change_lead_time_test.go)
- 2026-11-02 v1.0.3-beta19 为 PostgreSQL 增补 Cursor/Multi-AI 面板并将 Claude Code 纳入多 AI 对比，修复无上次成功部署时重复计算；属于 beta。 · 2026-11-02 · [原始来源 4](https://github.com/apache/devlake/releases/tag/v1.0.3-beta19) · [本地快照](../lanes/organization/raw/devlake/release-v1.0.3-beta19.html)


### O03 OpenTelemetry Collector

**适用场景**　多个 runner、评测器和部署平台输出不同信号，需要让事件到达观察后台并判断证据是否缺失。

**实现机制**　服务按配置建 receiver、processor、exporter 与 connector 的有向图，拒绝成环并从下游先启动。发送队列可选持久化；队列满或存储异常导致入队失败时，数据无法进入导出重试。

**人工决策**　平台团队选择队列容量、溢出处理和留存，观测系统独立告知采集失败，业务负责人定义缺证时能否继续。

**组织影响**　统一传输可降低接入成本；任务标识、审批语义、可靠台账仍需在业务层定义。

**版本与演进**　2026-11-06 v0.165.0 启动时检查 batch processor 与 exporterhelper 重复 batching；发布说明写明检查不穿越 connector 或隐藏实现的 exporter wrapper。

**适用边界**　入队失败计数与导出重试是不同故障。持久化队列不会保存 Auth 扩展设置的上下文。未部署。

**研究推断**　当信号没送达时，应把本次任务标为证据不全，避免在无记录状态下自动晋级。

**复核实验设计**　用合成任务让接收端保持可用但让导出端断开，逐渐塞满队列；对账发出数、入队失败数、后端可见数，比较溢出策略。

- exporterhelper/README.md 第 12–37、95–106 行，入队失败、重试、持久化的条件。 · 2026-11-19 · [原始来源 1](https://github.com/open-telemetry/opentelemetry-collector/blob/0c7a74cd0a4ab1c70834c91b67942eaaa9065825/exporter/exporterhelper/README.md) · [本地快照](../lanes/organization/raw/otel/0c7a74cd0a4ab1c70834c91b67942eaaa9065825/exporter/exporterhelper/README.md)
- service/internal/graph/graph.go 第 78–133、300–332、438–505 行，构图、双批次告警和组件启停次序。 · 2026-11-19 · [原始来源 2](https://github.com/open-telemetry/opentelemetry-collector/blob/0c7a74cd0a4ab1c70834c91b67942eaaa9065825/service/internal/graph/graph.go) · [本地快照](../lanes/organization/raw/otel/0c7a74cd0a4ab1c70834c91b67942eaaa9065825/service/internal/graph/graph.go)
- 2026-11-06 v0.165.0 启动时检查 batch processor 与 exporterhelper 重复 batching；发布说明写明检查不穿越 connector 或隐藏实现的 exporter wrapper。 · 2026-11-06 · [原始来源 3](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.165.0) · [本地快照](../lanes/organization/raw/otel/release-v0.165.0.html)


### O04 Langfuse Annotation Queues

**适用场景**　大量线上 trace/observation 难以逐项阅读，把选中的条目交给项目标注者形成可追查的判断。

**实现机制**　队列可分配给用户；完成接口校验项目权限，仅更新项目内 PENDING 项，记录完成时间和 annotatorUserId，之后写审计事件。

**人工决策**　标注人检查选中条目并评分；主管维护入队标准、分歧仲裁和复核比例。完成标记可作为反馈输入。

**组织影响**　给人一个有限、可统计的队列，能量化积压、复核时延和意见分歧，而非要求人阅读全量 agent 日志。

**版本与演进**　2026-11-19 v4.83.0 支持在单条标注视图中跳转条目并对队列排序，同版增加单 key 开支限额。

**适用边界**　该完成接口没有验证交付物是否可发布；审计写入在更新之后。部署版本、权限与抽样偏差均影响实际效果，未部署。

**研究推断**　例外处理要保留是谁对哪条运行记录给了什么判断；关闭队列不能代替修复或上线授权。

**复核实验设计**　盲抽成功与失败各 20 条，由两人独立标注，对比一致率、每条耗时和处理后回归用例转化率。

- annotation-queues.yml，项目对外队列、条目和分配接口契约。 · 2026-11-19 · [原始来源 1](https://github.com/langfuse/langfuse/blob/41c0fe3e485aaf3f6c6f107042ca09fff5242268/fern/apis/server/definition/annotation-queues.yml) · [本地快照](../lanes/organization/raw/langfuse/41c0fe3e485aaf3f6c6f107042ca09fff5242268/fern/apis/server/definition/annotation-queues.yml)
- annotationQueueItemsRouter.ts 第 423–475 行，PENDING 条件、权限、完成者和后续审计。 · 2026-11-19 · [原始来源 2](https://github.com/langfuse/langfuse/blob/41c0fe3e485aaf3f6c6f107042ca09fff5242268/web/src/features/annotation-queues/server/annotationQueueItemsRouter.ts) · [本地快照](../lanes/organization/raw/langfuse/41c0fe3e485aaf3f6c6f107042ca09fff5242268/web/src/features/annotation-queues/server/annotationQueueItemsRouter.ts)
- annotationQueueAssignmentsRouter.ts 第 69 行起，批量创建分配、跳过重复和成员查询。 · 2026-11-19 · [原始来源 3](https://github.com/langfuse/langfuse/blob/41c0fe3e485aaf3f6c6f107042ca09fff5242268/web/src/features/annotation-queues/server/annotationQueueAssignmentsRouter.ts) · [本地快照](../lanes/organization/raw/langfuse/41c0fe3e485aaf3f6c6f107042ca09fff5242268/web/src/features/annotation-queues/server/annotationQueueAssignmentsRouter.ts)
- 2026-11-19 v4.83.0 支持在单条标注视图中跳转条目并对队列排序，同版增加单 key 开支限额。 · 2026-11-19 · [原始来源 4](https://github.com/langfuse/langfuse/releases/tag/v4.83.0) · [本地快照](../lanes/organization/raw/langfuse/release-v4.83.0.html)


### O05 Arize Phoenix Experiments

**适用场景**　修改 agent 的工具选择或策略后，要检查相同输入上输出和中间动作是否发生退化。

**实现机制**　Python 客户端把实验绑定到数据集版本，按样本×重复次数展开任务；可在 run 完成后基于 trace spans 评估调用了哪一个工具。dry_run 可取小样本。

**人工决策**　领域专家写预期动作、检查评价用 rubric 和样本覆盖，研发人员比较实验后决定是否晋级。

**组织影响**　组织能把线上失败改写成带预期动作的固定样本，多版本在相同基线上回放。

**版本与演进**　2026-11-20 arize-phoenix v21.3.0 新增通过 CLI 赋予数据集标签，并调整 trace 查询性能；属于数据维护和查询增强。

**适用边界**　官方演示是模拟工具选择；trace 中观察到工具调用不证明结果正确。没有运行 Phoenix 服务。

**研究推断**　把实际路径与可接受路径都记录下来。只判断最终答案会漏掉越过人工检查的调用。

**复核实验设计**　对同一数据集固定三个版本，每种情况重复五次，分别统计最终结果和关键调用序列；人工仲裁替代路径。

- 官方 experiment_trace_evaluator.py 描述使用 OpenTelemetry spans 与预期工具比对的完整示例。 · 2026-11-20 · [原始来源 1](https://github.com/Arize-ai/phoenix/blob/33d17e2455307384a0a29bed33be56de266d216e/packages/phoenix-client/examples/experiments/experiment_trace_evaluator.py) · [本地快照](../lanes/organization/raw/phoenix/33d17e2455307384a0a29bed33be56de266d216e/packages/phoenix-client/examples/experiments/experiment_trace_evaluator.py)
- 客户端 experiments/__init__.py 第 781–882、916–1005 行，版本、dry run、重复项、实际与预期运行数。 · 2026-11-20 · [原始来源 2](https://github.com/Arize-ai/phoenix/blob/33d17e2455307384a0a29bed33be56de266d216e/packages/phoenix-client/src/phoenix/client/resources/experiments/__init__.py) · [本地快照](../lanes/organization/raw/phoenix/33d17e2455307384a0a29bed33be56de266d216e/packages/phoenix-client/src/phoenix/client/resources/experiments/__init__.py)
- 2026-11-20 arize-phoenix v21.3.0 新增通过 CLI 赋予数据集标签，并调整 trace 查询性能；属于数据维护和查询增强。 · 2026-11-20 · [原始来源 3](https://github.com/Arize-ai/phoenix/releases/tag/arize-phoenix-v21.3.0) · [本地快照](../lanes/organization/raw/phoenix/release-arize-phoenix-v21.3.0.html)


### O06 Promptfoo

**适用场景**　模型、提示或 harness 更新时，需要让批量样本的测试结果形成流水线可读的门槛。

**实现机制**　断言可产生通过状态、得分和命名指标，按权重聚合；零权重指标可用于观测。数值型测试总阈值覆盖普通单条断言状态，非有限数值另走错误分支。

**人工决策**　业务方明确哪些错误不得由总分抵消，评测负责人维护权重、阈值和裁决样本，检查边缘行为。

**组织影响**　给跨模型回归设置一致的分数口径，也允许先观测再转为硬阻断。

**版本与演进**　2026-11-18 0.126.0 限制 derivedMetrics 字符串公式的语法与长度，部分表达式会在跑用例前失败。

**适用边界**　总分达标可能掩盖局部缺陷；模型判分还受样本和模型版本影响。未运行此工具。

**研究推断**　用外置独立门禁处理不可补偿的硬约束，让软评分显示质量与成本权衡。

**复核实验设计**　固定 3 项断言，故意让高权重项通过、关键低权重项失败，比较总阈值和单项硬门的产出差异。

- expected-outputs/index.md 的断言、聚合和阈值配置语义。 · 2026-11-20 · [原始来源 1](https://github.com/promptfoo/promptfoo/blob/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/site/docs/configuration/expected-outputs/index.md) · [本地快照](../lanes/organization/raw/promptfoo/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/site/docs/configuration/expected-outputs/index.md)
- assertionsResult.ts 第 250–329、407–444 行，权重、零权重指标与数值型阈值及错误处理。 · 2026-11-20 · [原始来源 2](https://github.com/promptfoo/promptfoo/blob/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/src/assertions/assertionsResult.ts) · [本地快照](../lanes/organization/raw/promptfoo/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/src/assertions/assertionsResult.ts)
- derivedMetricFormula.ts 的词法/语法解析和表达式约束。 · 2026-11-20 · [原始来源 3](https://github.com/promptfoo/promptfoo/blob/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/src/evaluator/derivedMetricFormula.ts) · [本地快照](../lanes/organization/raw/promptfoo/a0ab170dd9c2cfe419a482d073ae9cf0848a7114/src/evaluator/derivedMetricFormula.ts)
- 2026-11-18 0.126.0 限制 derivedMetrics 字符串公式的语法与长度，部分表达式会在跑用例前失败。 · 2026-11-18 · [原始来源 4](https://github.com/promptfoo/promptfoo/releases/tag/0.126.0) · [本地快照](../lanes/organization/raw/promptfoo/release-0.126.0.html)


### O07 OpenFeature flagd

**适用场景**　只希望一部分仓库或团队使用新版审批策略，且同一实验对象重复请求应分到同一组。

**实现机制**　fractional evaluator 对显式分桶输入编码，缺省使用 flagKey 和 targetingKey，对确定性 CBOR 求 Murmur3 哈希并映射到加权区间。缺省分桶键为空会报错。

**人工决策**　产品和服务负责人选择分桶单位、比例及退出条件。调用端必须定义求值异常时的安全默认值。

**组织影响**　同一仓库或团队可成为稳定的暴露单元，让分阶段发布和对照组更易复现。

**版本与演进**　2026-11-17 flagd v0.19.0 将端口参数限定为有效数字 uint16，属于破坏性配置校验变更，非分桶功能首发。

**适用边界**　工具仅执行分配规则；分组键选择、跨团队干扰和发布效果判断归试验设计负责。未部署。

**研究推断**　把开关作用对象从个人请求改成团队或仓库，匹配协作流程真正的影响范围。

**复核实验设计**　固定 100 个仓库 ID 运行两轮，比较相同配置的分组一致性；改变 key 和比例测迁移人数，并测试缺键错误路径。

- 官方 fractional-operation 参考说明的参数、权重和分桶对象。 · 2026-11-17 · [原始来源 1](https://github.com/open-feature/flagd/blob/11037220611eab982261d2348b13147b4450b562/docs/reference/custom-operations/fractional-operation.md) · [本地快照](../lanes/organization/raw/flagd/11037220611eab982261d2348b13147b4450b562/docs/reference/custom-operations/fractional-operation.md)
- fractional.go 第 51–63、138–181、230–280 行，编码、缺键错误与哈希分桶逻辑。 · 2026-11-17 · [原始来源 2](https://github.com/open-feature/flagd/blob/11037220611eab982261d2348b13147b4450b562/core/pkg/evaluator/fractional.go) · [本地快照](../lanes/organization/raw/flagd/11037220611eab982261d2348b13147b4450b562/core/pkg/evaluator/fractional.go)
- 2026-11-17 flagd v0.19.0 将端口参数限定为有效数字 uint16，属于破坏性配置校验变更，非分桶功能首发。 · 2026-11-17 · [原始来源 3](https://github.com/open-feature/flagd/releases/tag/flagd%2Fv0.19.0) · [本地快照](../lanes/organization/raw/flagd/release-flagd-v0.19.0.html)


### O08 OpenFGA

**适用场景**　规划器想对某项目或工单执行动作，执行器需要在动作发生时查主体是否具备特定关系。

**实现机制**　服务端 Check 把模型、用户—关系—对象 tuple、请求上下文、contextual tuples 及一致性选项交给授权解析器；实现有可选缓存/读取限制和对部分非终止错误的后备 checker。

**人工决策**　资源负责人维护授权模型与关系，业务执行器必须把每个受保护动作接到授权查询并处理错误。

**组织影响**　可为多个执行器共用一套项目和服务关系，适合将 agent 的委托权限同资源归属连接。

**版本与演进**　2026-09-20 v1.21.0 把 Dynamic Conditions 作为实验特性发布。Atom 显示 09-28 更新，个别发布页确认发布时间为 09-20。

**适用边界**　权限允许只表明主体可以做动作，不证明这次变更已得到具体业务批准。缓存与撤销延迟要单测。未部署。

**研究推断**　将有权操作与此次运行获准操作分别记录，并给审批约束绑定运行标识及有效期。

**复核实验设计**　用同一任务在撤销前后、不同一致性选项和重试后各发 Check，记录结果和时间；同时验证业务端确实拒绝失败结果。

- 官方 Check 设计文档说明如何处理关系与查询。 · 2026-11-16 · [原始来源 1](https://github.com/openfga/openfga/blob/798149843737e264e64b8660baadb946528c02f0/docs/check/README.md) · [本地快照](../lanes/organization/raw/openfga/798149843737e264e64b8660baadb946528c02f0/docs/check/README.md)
- pkg/server/commands/check.go 第 182–219、259–266、324–340 行，请求传递、解析与回退的边界。 · 2026-11-16 · [原始来源 2](https://github.com/openfga/openfga/blob/798149843737e264e64b8660baadb946528c02f0/pkg/server/commands/check.go) · [本地快照](../lanes/organization/raw/openfga/798149843737e264e64b8660baadb946528c02f0/pkg/server/commands/check.go)
- 2026-09-20 v1.21.0 把 Dynamic Conditions 作为实验特性发布。Atom 显示 09-28 更新，个别发布页确认发布时间为 09-20。 · 2026-09-20 · [原始来源 3](https://github.com/openfga/openfga/releases/tag/v1.21.0) · [本地快照](../lanes/organization/raw/openfga/release-v1.21.0.html)


### O09 Prometheus Alertmanager

**适用场景**　一个上游故障令几十次自动执行同时失败，值班人员需要看到能行动的一条根因告警。

**实现机制**　标签按路由树递归匹配，子路由的 continue 决定是否继续匹配兄弟节点。抑制规则要求源/目标规则匹配且指定标签相等，并处理同时匹配源目标的自抑制情况。

**人工决策**　值班人员配置接收者、分组、静默和抑制范围，复核关键告警被静默的时长及原因。

**组织影响**　把批量失败汇总到负责该服务的队伍，减少重复打断，同时保留根因与下游告警关系。

**版本与演进**　2026-09-17 v0.34.1 修复部分抑制场景下告警被错误解除静默的问题，涉及 #5542、#5449、#5559。

**适用边界**　发送少不等于事故少。范围过宽、标签错误会降低可见性；工具本身不回滚部署。未部署。

**研究推断**　把值班中断数与未送达关键事件同时记账，单纯追求压低告警总数可能掩盖失败。

**复核实验设计**　模拟同租户根因、三个派生失败和另一个租户同时失败，检查后者仍通知；恢复根因后验证持续失败能再次通知。

- docs/alertmanager.md，去重、分组、路由、静默和抑制。 · 2026-11-19 · [原始来源 1](https://github.com/prometheus/alertmanager/blob/eb31108b02fcd9d8d277172f6f6e91856a3d0441/docs/alertmanager.md) · [本地快照](../lanes/organization/raw/alertmanager/eb31108b02fcd9d8d277172f6f6e91856a3d0441/docs/alertmanager.md)
- inhibit.go 第 190–233、295 行后，匹配条件、equal 标签和双侧匹配。 · 2026-11-19 · [原始来源 2](https://github.com/prometheus/alertmanager/blob/eb31108b02fcd9d8d277172f6f6e91856a3d0441/inhibit/inhibit.go) · [本地快照](../lanes/organization/raw/alertmanager/eb31108b02fcd9d8d277172f6f6e91856a3d0441/inhibit/inhibit.go)
- dispatch/route.go 第 148–177 行，路由递归、continue 与父级回退。 · 2026-11-19 · [原始来源 3](https://github.com/prometheus/alertmanager/blob/eb31108b02fcd9d8d277172f6f6e91856a3d0441/dispatch/route.go) · [本地快照](../lanes/organization/raw/alertmanager/eb31108b02fcd9d8d277172f6f6e91856a3d0441/dispatch/route.go)
- 2026-09-17 v0.34.1 修复部分抑制场景下告警被错误解除静默的问题，涉及 #5542、#5449、#5559。 · 2026-09-17 · [原始来源 4](https://github.com/prometheus/alertmanager/releases/tag/v0.34.1) · [本地快照](../lanes/organization/raw/alertmanager/release-v0.34.1.html)


### O10 Grafana k6

**适用场景**　在自动交付链中验证性能/SLO 门槛，失败时发出可以被流水线消费的退出码。

**实现机制**　Go 阈值引擎对指标聚合值应用比较运算；没有聚合样本时该轮会跳过并返回通过。abortOnFail 和延迟参数控制何时提前中止。

**人工决策**　服务 owner 设定业务指标、足够样本量和中止条件。异常先核对测试流量是否到达目标，再对服务作判断。

**组织影响**　为多团队提供可重用的性能验收程序，机器可以自动阻断失败的候选版本。

**版本与演进**　2026-11-12 v2.4.0 新增实验性运行层级 tracing；browser_data_received 改用编码传输大小，官方要求复核既有阈值。

**适用边界**　本机仅验证 Windows CLI 合成 Rate，无网络请求；没有测真实服务延迟、生产负载或端到端交付。

**研究推断**　每个质量门要同时检查可测性与结果，尤其要把样本不足和指标达标分开。

**复核实验设计**　已实测 v2.4.0 同一阈值 rate>=0.75、同为四次迭代，4/4 成功时退出 0，1/4 成功时退出 99。原始命令、输入与输出见本地 runtime/k6.json。

- 官方 examples/thresholds.js 的阈值写法。 · 2026-11-18 · [原始来源 1](https://github.com/grafana/k6/blob/0110662a25cdb14690d7ba5454d6b6e718d8f9d5/examples/thresholds.js) · [本地快照](../lanes/organization/raw/k6/0110662a25cdb14690d7ba5454d6b6e718d8f9d5/examples/thresholds.js)
- metrics/thresholds.go 第 40–82、145–168、170–214 行，缺样本路径、比较和延迟中止。 · 2026-11-18 · [原始来源 2](https://github.com/grafana/k6/blob/0110662a25cdb14690d7ba5454d6b6e718d8f9d5/metrics/thresholds.go) · [本地快照](../lanes/organization/raw/k6/0110662a25cdb14690d7ba5454d6b6e718d8f9d5/metrics/thresholds.go)
- 2026-11-12 v2.4.0 新增实验性运行层级 tracing；browser_data_received 改用编码传输大小，官方要求复核既有阈值。 · 2026-11-12 · [原始来源 3](https://github.com/grafana/k6/releases/tag/v2.4.0) · [本地快照](../lanes/organization/raw/k6/release-v2.4.0.html)
- 本地 Windows 实验记录，含 CLI 输入、标准输出、标准错误、退出码以及官方压缩包 SHA-256。 · 2026-11-20 · [原始来源 4](https://github.com/grafana/k6/releases/download/v2.4.0/k6-v2.4.0-windows-amd64.zip) · [本地快照](../lanes/organization/runtime/k6.json)


### O11 OpenCost

**适用场景**　自动运行产生大量测试与后台任务，需要按命名空间/标签归集资源成本，识别空闲容量和无法归属的用量。

**实现机制**　Allocation 按 CPU、GPU、RAM、存储与网络等成本算总额，AggregateBy 依据属性、过滤器和 idle/shared 分摊选项重组；无有效归属值可被标成 __unallocated__。

**人工决策**　FinOps 与平台负责人约定共享成本、空闲成本如何分摊，并决定哪些失败或闲置任务需要降配或暂停。

**组织影响**　将执行平台消耗映射到业务团队，再与工作单号、模型账单和最终采纳结果外部拼接。

**版本与演进**　2026-10-13 pricing/public v1.0.9 标签为价格模块增加 GBP、EUR、JPY。此为定价子模块变化；主服务版本另计。

**适用边界**　Kubernetes 分摊不能自动得到 SaaS 模型 token 账单、人的审阅时间或交付价值。缺失标签会改写团队分母。未部署。

**研究推断**　每次尝试成本和每次被验收交付成本必须分别报告，未归集成本单列，避免让失败重试变成无主开销。

**复核实验设计**　同一工作流重复运行五次，只验收其中一次。比对共享成本分摊前后的每次尝试成本、每次验收成本和未归集成本。

- README.md 描述 Kubernetes 成本分配、可观测和 OpenCost 规范。 · 2026-11-19 · [原始来源 1](https://github.com/opencost/opencost/blob/266407979a7fb3065322f0f089e287e7ad62f76b/README.md) · [本地快照](../lanes/organization/raw/opencost/266407979a7fb3065322f0f089e287e7ad62f76b/README.md)
- core/pkg/opencost/allocation.go 第 925–995、1531–1563、1623、1790、1945 行，成本组件、分摊和未分配项。 · 2026-11-19 · [原始来源 2](https://github.com/opencost/opencost/blob/266407979a7fb3065322f0f089e287e7ad62f76b/core/pkg/opencost/allocation.go) · [本地快照](../lanes/organization/raw/opencost/266407979a7fb3065322f0f089e287e7ad62f76b/core/pkg/opencost/allocation.go)
- pkg/costmodel/allocation.go，计算资源分配随时间窗聚合的入口。 · 2026-11-19 · [原始来源 3](https://github.com/opencost/opencost/blob/266407979a7fb3065322f0f089e287e7ad62f76b/pkg/costmodel/allocation.go) · [本地快照](../lanes/organization/raw/opencost/266407979a7fb3065322f0f089e287e7ad62f76b/pkg/costmodel/allocation.go)
- 2026-10-13 pricing/public v1.0.9 标签为价格模块增加 GBP、EUR、JPY。此为定价子模块变化；主服务版本另计。 · 2026-10-13 · [原始来源 4](https://github.com/opencost/opencost/releases/tag/modules%2Fpricing%2Fpublic%2Fv1.0.9) · [本地快照](../lanes/organization/raw/opencost/release-modules-pricing-public-v1.0.9.html)


### F01 OpenAI Symphony

**平台**　语言无关 SPEC 与 Elixir 参考实现；仓库样例展示团队工作流。

**适用场景**　问题管理系统持续出现可以并行处理的维护任务。工程师希望移动工单状态就能派工，也能在事项被取消或返工时收回或恢复执行。

**实现机制**　orchestrator 在每次派发前先与 tracker 对账，区分 running、blocked、terminal，按可用并发槽派发；重试带 token，陈旧定时器不会接管新尝试。规范把正常结束后的继续检查与失败指数退避分开。每事项有独立工作目录，仓库内 WORKFLOW.md 保存提示与运行配置。

**人工决策**　样例在 PR 附着并验证后移入 Human Review；人同意后进入 Merging，要求修改则回 Rework。发起新运行、修改 tracker 和产品责任验收是不同动作；人可通过 tracker 状态收回正在处理的工作。

**组织影响**　工单成为团队可见的排队、认领和交接单位，运行日志与 PR 通过 issue ID 关联。人主要处理需求不明确、指标冲突和最终接受，而不是每次在聊天中重新分派。

**版本与演进**　2026-04-27 官方经验报告公开这套工单驱动规范；v0.0.3 的 2026-09-15 发布记录列出凭证别名清理及 GitLab API 认证变更。不能据此将单团队产出外推为普遍收益。

**适用边界**　SPEC 允许不同信任和沙箱策略；独立工作目录并非进程级隔离。人审状态属于样例约定，组织必须决定哪些仓库保护能强制执行。静态阅读，无真实 tracker 租户实验。

**研究推断**　把任务分配的状态机交给调度器，把任务内部可变步骤留给代理，用明确的交付状态界定机器和人的责任。

**复核实验设计**　比较同类维护单的手工启动与 tracker 调度；主动制造重复轮询、工单转终态和旧重试到达，观察重复 PR 数、遗留 worker 数、等待验收分钟数和真正关闭的工单数。

- SPEC 核对调度边界、并发、重复尝试与独立工作目录。 · 2026-09-15 · [原始来源 1](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md) · [本地快照](../lanes/frontier/raw/symphony/c6638056502ecd2e/SPEC.md)
- maybe_dispatch、reconcile_issue_state、handle_info retry token。 · 2026-09-15 · [原始来源 2](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/orchestrator.ex) · [本地快照](../lanes/frontier/raw/symphony/ffa6fd2ca66f775b/orchestrator.ex)
- 样例的 Human Review、Merging 与 Rework 约定。 · 2026-09-15 · [原始来源 3](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/WORKFLOW.md) · [本地快照](../lanes/frontier/raw/symphony/7c465f8a44c6698d/WORKFLOW.md)
- v0.0.3 的认证与发行更新；Atom 条目 updated UTC 日期。 · 2026-09-15 · [原始来源 4](https://github.com/openai/symphony/releases/tag/v0.0.3) · [本地快照](../lanes/frontier/raw/symphony/85b0986012457a2c/releases.atom)
- 厂商内部实践与公开规范的网页摘录；非完整页面。 · 2026-04-27 · [原始来源 5](https://openai.com/index/open-source-codex-orchestration-symphony/) · [本地快照](../lanes/frontier/raw/symphony/report-20260427/web-excerpt.json)


### F02 GitHub Agentic Workflows（gh-aw）

**平台**　GitHub Actions、github.com；公开编译及 handler 实现。

**适用场景**　仓库维护者要自动分类 issue、更新文档或分析 CI，但希望预审自动化能写哪些仓库对象，并沿用已经部署的 Actions 运行器与权限制度。

**实现机制**　仓库中的 Markdown 描述任务，CLI 生成标准 Actions YAML。默认只读代理提出结构化 safe outputs，独立处理层根据受信配置和操作类型路由到 handler。源码按类型取授权配置、校验目标、识别 staged 状态与批次摘要。handler 的实际写权限可以与代理读取上下文的权限分离。

**人工决策**　工作流作者或维护者先审可用输出和目标；staged 允许预览。并非每种写入都天然需要真人确认，合并或部署仍要接入仓库规则或业务审批。

**组织影响**　可沿用 runner group 与组织级策略，把同一机器人能够提议的动作做成多个团队可复用的有限目录。应将提议数、拒绝数、真正写入数拆开计量。

**版本与演进**　官方 2026-02-13 技术预览已有只读默认与 safe outputs；2026-10-28 GA 说明增加自托管 ARC/Docker-in-Docker 支持和预算预测等。以前已经具备的机制不能算作 GA 首发。

**适用边界**　历史 changeset 主张 staged 空权限；2026-10-14 的后续 ADR 指出有些 handler 预览前仍须读取私有对象，否则 403，建议分配最小只读。ADR 状态为 Proposed，不能仅凭提案断定所有编译版本的权限矩阵。未运行 GitHub 租户工作流。

**研究推断**　最小权限不总等于零权限。应将读取验证、预览、实际提交分别建模，使审批端能看到将写入的准确对象。

**复核实验设计**　选私有测试仓的标签变更，比较只读 staged、授权写入及不满足过滤条件三种运行。核对实际 GitHub 权限、预览是否与最终动作一致、以及触发前后资源变化。

- process_safe_outputs 调用独立 manager 并避免将 handler stdout/stderr 打包。 · 2026-11-19 · [原始来源 1](https://github.com/github/gh-aw/blob/32398b3f20e9dd5ce206a0183611b45a62ad9267/actions/setup/js/process_safe_outputs.cjs) · [本地快照](../lanes/frontier/raw/ghaw/05a1b17671d7b2c2/process_safe_outputs.cjs)
- 2026-10-14 Proposed ADR，对照 staged 权限和私有仓库过滤器。 · 2026-11-19 · [原始来源 2](https://github.com/github/gh-aw/blob/32398b3f20e9dd5ce206a0183611b45a62ad9267/docs/adr/68724-infer-read-permissions-for-staged-safe-output-handlers.md) · [本地快照](../lanes/frontier/raw/ghaw/a9289183a6eb3b41/68724-infer-read-permissions-for-staged-safe-output-handlers.md)
- 早期 changeset 对 staged 不配置写权限的预期。 · 2026-11-19 · [原始来源 3](https://github.com/github/gh-aw/blob/32398b3f20e9dd5ce206a0183611b45a62ad9267/.changeset/patch-skip-write-permissions-staged-safe-outputs.md) · [本地快照](../lanes/frontier/raw/ghaw/e0bdd71d1c678b10/patch-skip-write-permissions-staged-safe-outputs.md)
- 2026-10-28 正式 GA，默认权限、运行器和预算预测。 · 2026-10-28 · [原始来源 4](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/) · [本地快照](../lanes/frontier/raw/ghaw/5880fcffa12f6e79/page.html)
- 2026-02-13 技术预览说明，追溯只读及 safe outputs。 · 2026-02-13 · [原始来源 5](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/) · [本地快照](../lanes/frontier/raw/ghaw/e8c7c38a862ffaa0/page.html)
- safe_output_handler_manager 的 effectiveAuthorization、授权规则选择、batchDigest、stagedFor 与按类型 dispatch。 · 2026-11-19 · [原始来源 6](https://github.com/github/gh-aw/blob/32398b3f20e9dd5ce206a0183611b45a62ad9267/actions/setup/js/safe_output_handler_manager.cjs) · [本地快照](../lanes/frontier/raw/ghaw/965a3aa3dfdfeba6/safe_output_handler_manager.cjs)


### F03 Tessl

**平台**　Tessl Registry、CLI、托管评测；本次核对公开文档与发布页，未读取后端源码。

**适用场景**　多个团队共享技能文件。维护者需要知道哪个版本确实能改变代理的输出，以及更换模型后规则是否仍生效。

**实现机制**　以 plugin root 关联 skill 和 evals，用相同任务分别运行无 skill、有 skill 两种条件，按场景标准评分；也能声明其他 variants。文档区分内容 review 与实际任务 eval，并支持用已有仓库历史工作构造测试。Web changelog 进一步记录跨代理的技能激活观测。

**人工决策**　作者编写或审查验收标准、选择历史任务及对照模型，并检查低分案例、无激活案例；查看原始轨迹比接受一个汇总倍率更能解释失败。

**组织影响**　团队可将共享规范作为可版本化依赖管理，并把“没读规范”和“读了仍失败”分开治理。跨团队迁移前需要用接收方的仓库样本再评估。

**版本与演进**　2026-02-17 公告发布 task evals，并把 repo evals 记为当时 beta；2026-10-30 周更记录 Codex、Cursor、Tessl 的评测也能报告实际加载的技能，此前只记录 Claude Code。两项证据适用时间不同。

**适用边界**　厂商文档给出评测流程，未获得托管后台源码，也未复跑其注册表上的分数。历史任务泄漏、评分器偏好和同一场景随机性都可能影响差值。

**研究推断**　技能被安装、被读取、行为改变、最终交付改善是四个不同问题。只看下载量或单次通过率，会隐藏错误的优化目标。

**复核实验设计**　选取未进入技能编写材料的历史维护项，固定模型版本、多次重复两种配置，分别记录加载、行为达标、独立测试通过和总成本，再换仓库检查可迁移性。

- Prove a skill works using evaluation；baseline、variant、plugin 根路径和场景。 · [原始来源 1](https://docs.tessl.io/improving-your-skills/evaluate-skill-quality-using-scenarios) · [本地快照](../lanes/frontier/raw/tessl/d4f59b4b0ed976c7/page.html)
- 2026-10-30 周更中 Skill activation for more agents；区分加载与完成。 · [原始来源 2](https://docs.tessl.io/changelog-web) · [本地快照](../lanes/frontier/raw/tessl/97b16a8986accb80/page.html)
- 2026-02-17 Task Evals 发布说明及当时 repo evals 的阶段。 · 2026-02-17 · [原始来源 3](https://tessl.io/blog/introducing-task-evals-measure-whether-your-skills-actually-work) · [本地快照](../lanes/frontier/raw/tessl/70663727a3deff21/page.html)


### F04 Claude Code Scheduled tasks（原 Routines）

**平台**　Claude Code 云会话，也可按组织路由到自托管环境。源码核对范围止于公开文档；本例与 E09 SDK 是不同产品层。

**适用场景**　在成员电脑关机后，仍需按日程处理积压工单，或在上游 SDK 的 PR 合并后提交下游语言版本的对应修改。

**实现机制**　将提示、环境、仓库、连接器与触发器保存到任务；日程、GitHub 事件或 API 请求启动会话。保存过的提示是任务指令，触发本身不代表当次高影响动作获得人授权。当前文档说明在 Anthropic 云新建会话时优先使用 auto mode；连续阻止达到阈值后可暂停等待人。

**人工决策**　创建者选择触发条件、最小连接器与执行身份；组织管理员能关停能力。文档明确任务属于个人账号，经其 GitHub、Slack 等连接器做的事体现该账号身份，故需业务侧管理离职和交接。

**组织影响**　将原来靠人盯仓库事件的维护变成可重复执行的服务。对组织产品，任务归属、谁承担配额、能否接管及凭据轮换，比可选多少 cron 表达式更关键。

**版本与演进**　2026-04-14 以 Routines 名称发布。现行官方文档改称 Scheduled tasks，并解释旧名称为何仍留在 URL 和部分界面；无一手证据确定改名首日。

**适用边界**　适用权限取决于托管方式、连接器和分支保护。个人拥有的任务不等于团队共享服务账号；公开文档不能证明某组织内的实际策略。未登录或触发任务。

**研究推断**　组织级自动化中，“系统能定时运行”与“人员变化后仍有明确责任人”需要分别选型和验收。

**复核实验设计**　在两个授权测试账号的非生产项目里分别创建同一只读任务，记录事件来源、产物作者和配额账单归属，再停用管理员开关或撤销一个连接器，验证队列和故障提示。

- 现行 Scheduled tasks 文档，核对旧名、触发、个人归属、权限与暂停。 · [原始来源 1](https://code.claude.com/docs/en/routines.md) · [本地快照](../lanes/frontier/raw/routines/9377bc3e62c3bed0/page.md)
- 2026-04-14 产品发布页，核对历史命名和发行时间。 · 2026-04-14 · [原始来源 2](https://claude.com/resources/articles/introducing-routines-in-claude-code) · [本地快照](../lanes/frontier/raw/routines/9c2422bf3dc711f9/page.html)


### F05 OpenSandbox

**平台**　原 alibaba/OpenSandbox 地址现指向 opensandbox-group/OpenSandbox；本例核对 Fast Sandbox 自动休眠及 Linux/容器相关部署文档。

**适用场景**　大量代理在工具调用、人工审批或外部依赖期间闲置。平台希望释放容量，同时避免把短暂缺失的活动遥测解释成工作已结束。

**实现机制**　根据 ingress 流量在 Redis 记录活动时间，sweeper 逐项检查是否到达空闲门槛，再执行暂停。源码明确，活动记录缺失时先返回 UNKNOWN 并申请写 tombstone；后续观测越过门槛才可判 idle。下一次请求可唤醒环境，其等待预算耗尽会返回 503 和 Retry-After，恢复仍可能继续。

**人工决策**　平台管理员启用 server 与 ingress 侧开关，工作负载还要选择声明 idlePolicy；业务侧决定出现超时是等待恢复、重试还是升级给人。

**组织影响**　组织可把等待人审的计算成本与恢复延迟分别量化。通过网关的流量和实际任务进展需分别观测，否则后台纯计算任务可能完全不适用这种策略。

**版本与演进**　1.3.0-rc.2 的 2026-11-19 发布记录修复 Docker 续期与过期删除竞争、Kubernetes 过期删除旧对象的竞争，也修复已正常退出的 BatchSandbox 状态；该版本是候选版，不能写为稳定版全面可用。

**适用边界**　文档仅覆盖全栈 v1.2.0+ 的 Fast Sandbox 后端和经过 ingress 的工作负载，默认关闭。本次运行固定源码中的纯判断函数，未部署 Redis、网关、Docker、Kubernetes 或云集群。

**研究推断**　超时、空闲、已被删除和恢复中是不同状态。元数据过期时保留“不确定”，往往比静默终止工作更符合研发任务的代价结构。

**复核实验设计**　已用固定提交的 evaluate_idle 运行六个本地用例，近期活动、过期活动、无记录、新旧 tombstone、近期活动覆盖旧 tombstone 均符合预期。下一步在专用集群注入遥测延迟，比较误休眠率、恢复 p95、计算费用及重试风暴。

- OpenSandbox 仓库用途、平台及后端。 · 2026-11-19 · [原始来源 1](https://github.com/opensandbox-group/OpenSandbox/blob/b71264afc2a32048b7d7a1fe7b876c8a07a03493/README.md) · [本地快照](../lanes/frontier/raw/sandbox/39535d8f0c100407/README.md)
- evaluate_idle 所有条件分支与未知状态的 tombstone 意义。 · 2026-11-19 · [原始来源 2](https://github.com/opensandbox-group/OpenSandbox/blob/b71264afc2a32048b7d7a1fe7b876c8a07a03493/server/opensandbox_server/integrations/idle_pause/decision.py) · [本地快照](../lanes/frontier/raw/sandbox/4a9d6938393164f6/decision.py)
- v1.2.0+、Fast Sandbox、网关流量和 Redis 前置条件、唤醒超时。 · 2026-11-19 · [原始来源 3](https://github.com/opensandbox-group/OpenSandbox/blob/b71264afc2a32048b7d7a1fe7b876c8a07a03493/docs/guides/auto-pause-wake.md) · [本地快照](../lanes/frontier/raw/sandbox/75d07beab3dfd353/auto-pause-wake.md)
- 1.3.0-rc.2 发布记录，续期与删除竞争及正常退出的状态问题。 · 2026-11-19 · [原始来源 4](https://github.com/opensandbox-group/OpenSandbox/releases/tag/release-1.3.0-rc.2) · [本地快照](../lanes/frontier/raw/sandbox/4adc4ff2609bd9ba/releases.atom)


### M01 Factory Droid / Missions

**适用场景**　迁移或跨模块改造超出单次会话；需要先把目标分成 feature 与 milestone，并指定何时检查。

**实现机制**　团队与 orchestrator 明确范围、依赖、技能和里程碑；每个 milestone 末安排 validation workers。文档给出的资源估算按每个里程碑在首轮通过时执行两次验证计算；发现问题后可生成新的修复任务。CLI 的 Mission Control 展示进度。

**人工决策**　先批准计划；执行过程中可暂停 orchestrator、解释阻塞、改方向。验证频率由里程碑划分决定，QA 验证可在设置中关闭。

**组织影响**　团队可以把一键启动服务、对应用输入、持久日志等作为仓库准备工作，帮助其他人复用验收方式。产品文档没有承诺增加 worker 就能缩短总工期。

**版本与演进**　2026-08-29，CLI v0.208.0 / Desktop v0.165.0 修复 Mission 被中断、暂停或恢复后里程碑验证仍应执行的行为。

**适用边界**　公开技术文档和版本记录已核对；未接入产品，未检查托管调度实现。验证者与实现者共享错误假设时仍可能一起放过问题。

**研究推断**　最能区分编排质量的问题是恢复后还欠哪些检查。审批内容应能说明验收标准何时执行，以及更改标准需谁重新确认。

**复核实验设计**　喂入同一小迁移，在验证前暂停并恢复；比较任务状态、验证记录、追加修复和最终可重放证据，独立验收者另测隐藏用例。

- Planning & Validation：Validation、Development scripting for QA、成本估算 · [原始来源 1](https://docs.factory.com/missions/planning.md) · [本地快照](../lanes/managed/raw/M01/c7104501e177-plan.md)
- Running in the CLI：Intervening and redirecting，计划批准后的监控与暂停 · [原始来源 2](https://docs.factory.com/missions/running-cli.md) · [本地快照](../lanes/managed/raw/M01/0950e865198d-run.md)
- CLI v0.208.0 / Desktop v0.165.0 的 Mission milestone validation 修复 · 2026-08-29 · [原始来源 3](https://docs.factory.com/changelog/release-notes.md) · [本地快照](../lanes/managed/raw/M01/ddfd27ffa817-log.md)


### M02 Cognition Devin / Devin Bots

**适用场景**　团队想持续维护某个产品目标，例如减少一类回归；任务顺序需要根据上一轮结果持续决定。

**实现机制**　Bot 保存自己的会话、记忆、工具与权限，为子任务启动 Devin sessions，跟踪结果并决定下一个动作。Needs you 汇集 PR、权限请求与待决策项；Bot 的访问资源与能向 Bot 发消息的人分开配置。

**人工决策**　新 Bot 默认私有；分享 Bot 也分享请求其使用既有授权资源的能力。管理员可查看/撤销 grant；若只需传播做法，应分享 template。Mark done 清理个人侧栏的语义与停止工作不同。

**组织影响**　团队能为长期结果指定负责人，用一个异常队列处理分散会话的决定；持久授权使“谁能调用 Bot”和“Bot 能访问什么”都成为组织治理对象。

**版本与演进**　2026-11-17，Cognition 发布 Devin Bots，将持续目标委托给可以并行发起多个 Devin 会话的 Bot；11-16 的 Cloud 更新还区分个人 Mark done 与关闭会话。

**适用边界**　2026-11-17 上线，属于早期产品。内部案例是厂商自述，未取得独立对照、真实组织采纳数据、托管引擎源码或授权环境运行证据。

**研究推断**　收件箱应计量每项决定的到达、等待、打断次数与结局；仅记录 Bot 完成的子任务数可能掩盖等待人处理的关键瓶颈。

**复核实验设计**　在无生产连接的试用组织给 Bot 一项带停止条件的持续维护任务，对比共享模板与共享 Bot；核对新任务、权限请求、撤权后访问及人工决策时长。

- What needs you、权限请求与 Bot 默认行为 · [原始来源 1](https://docs.devin.ai/work-with-devin/bots.md) · [本地快照](../lanes/managed/raw/M02/9823c2514a10-bot.md)
- Who can use、What it can access、Resources 和 revoke；模板与共享 Bot 的差别 · [原始来源 2](https://docs.devin.ai/work-with-devin/bots/access-and-security.md) · [本地快照](../lanes/managed/raw/M02/8afd7d4069f9-access.md)
- Introducing Devin Bots：持续目标、多 Devin 会话、内部自述案例 · 2026-11-17 · [原始来源 3](https://devin.ai/blog/introducing-devin-bots) · [本地快照](../lanes/managed/raw/M02/817040293119-launch.html)
- November 16：Subscribers and Mark done，个人完成与后台会话状态的区别 · 2026-11-16 · [原始来源 4](https://docs.devin.ai/release-notes/2026.md) · [本地快照](../lanes/managed/raw/M02/1ad66dfe2675-log.md)


### M03 Google Jules（已只读）

**适用场景**　历史上将 GitHub 仓库例行维护设为定期任务，或启动单个异步任务，侧重用计划、活动记录和 PR 监督工作。

**实现机制**　历史任务先克隆仓库、初始化虚拟机并安装依赖，再给出步骤和假设；人可以反馈后批准。历史计划文档还明确离开页面后计时器可能自动批准。曾支持定时启动任务、产生 PR；退场时可导出提示、计划、活动、补丁和配置。

**人工决策**　计划反馈与手动批准曾提供干预窗口，但离开后的自动批准不满足必须显式同意的控制要求。当前优先回收配置与任务证据，已有代码分支和 PR 留在 GitHub。

**组织影响**　这是选择平台时必须考虑的数据可携带性案例。团队的长期资产包括判定依据、排程与历史，不仅是最终的代码。

**版本与演进**　2026-10-29 发布退场公告，列明 11-11 后转为只读、计划于 12-31 结束；另一处文档对编辑排程仍写需删除重建，而 2026-01-26 的更新已允许编辑、暂停与恢复。

**适用边界**　截至 2026-11-20，官方时间表已进入只读阶段，不能列为可启动新任务的在售选项。退场公告提及 Antigravity 并给出辅助导出方式，未承诺将原会话状态无损导入新平台。未登录服务确认租户状态。

**研究推断**　用时间有界的历史证据解释产品演进；合同或试点应明确停服时可导出哪些交付证据，迁移后能恢复哪些语义。

**复核实验设计**　利用用户自愿提供的脱敏导出样本查验计划、记录、补丁、定时任务是否可索引及关联；新方案独立验证只读和迁移流程。

- Jules Turndown，以及 Update Scheduled Tasks 的时间线 · 2026-10-29 · [原始来源 1](https://jules.google/docs/changelog/) · [本地快照](../lanes/managed/raw/M03/e9e029192f03-log.html)
- Scheduled Tasks 文档 Creating / Managing；与 2026-01-26 发布记录并列复核 · [原始来源 2](https://jules.google/docs/scheduled-tasks/) · [本地快照](../lanes/managed/raw/M03/b69a91392d86-schedule.html)
- Reviewing the plan：虚拟机设置、审批以及离开后计时自动批准 · [原始来源 3](https://jules.google/docs/review-plan/) · [本地快照](../lanes/managed/raw/M03/cd1ebdf4ae39-plan.html)


### M04 GitLab Duo Agent Platform

**适用场景**　团队要将 issue、CI 与 merge request 连起来：浏览器事件或计划发起任务，后台执行，再将阻塞或需要决定的会话集中给人。

**实现机制**　Foundational flows 与团队自定义 flows 分开。GitLab UI 中 Developer Flow 由 runner 运行并创建/更新 MR；CLI 在本机执行；IDE 的 Software Development Flow 拟计划并暂存改动。Sessions 的 Needs a decision 汇集待回应会话。19.6 的定时自动化使用有限服务账号并记录运行历史。

**人工决策**　顶级 group 与项目控制启用条件，具权用户配置服务账号、触发器和流；负责人在合适界面审阅 MR 或确认操作。由 Web Chat 发起独立后台流时，不能沿用 Chat 工具审批的语义。

**组织影响**　直接利用团队原有 issue、runner、CI 和 MR 对象传递任务标识，结合每个自动化的运行量、成功率、失败原因和会话详情判断是否需要人工接管。

**版本与演进**　2026-07-16，19.2 将 Custom Flows 发布为 GA；2026-11-19，19.6 的 scheduled automations 进入 beta，并在 Automations 界面整合定时/事件触发、运行历史和会话详情。

**适用边界**　Custom Flows GA 与 19.6 scheduled automations beta 的成熟度不同。定时执行仅适用于启用的 AI Catalog 自定义 flow 或 Developer Flow，其他 foundational flows、外部 agents、用配置文件定义的 flows 不适用。有公开 GitLab 组件，本案例证据为文档与发行记录，未复核其服务端实现或部署。

**研究推断**　同一个品牌内部可以同时存在交互式与无人值守的运行合同。平台应将执行位置、运行主体和审核策略附着在一次 run 上。

**复核实验设计**　在试验项目触发同一修复意图的 Web、CLI 和 IDE 路径，再用有资格的 flow 配置定时执行；核对运行身份、审批归属、会话 ID 和重复触发。

- Choose a flow for coding tasks 对比 UI、Chat、CLI、IDE 的执行与审批 · [原始来源 1](https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/) · [本地快照](../lanes/managed/raw/M04/7016977f820c-flow.html)
- Needs a decision 和 Cancel a running session · [原始来源 2](https://docs.gitlab.com/user/duo_agent_platform/sessions/) · [本地快照](../lanes/managed/raw/M04/f4d1cf0be24d-sessions.html)
- GitLab 19.2：Custom Flows 与 CLI 一般可用 · 2026-07-16 · [原始来源 3](https://about.gitlab.com/press/releases/2026-07-16-gitlab-19-2-brings-governed-agentic-automation/) · [本地快照](../lanes/managed/raw/M04/e39520fcd960-log.html)
- GitLab 19.6：scheduled automations 为 beta、运行记录、独立 service account · 2026-11-19 · [原始来源 4](https://about.gitlab.com/blog/gitlab-scheduled-automations/) · [本地快照](../lanes/managed/raw/M04/ea7d44f02877-new.html)
- Scheduled automation prerequisites：获准账号角色、启用条件和不支持的 flow · [原始来源 5](https://docs.gitlab.com/user/duo_agent_platform/automations/) · [本地快照](../lanes/managed/raw/M04/35fba77af685-automations.html)


### M05 CodeRabbit

**适用场景**　组织希望在 PR 上一致执行评审规范，部分如变更是否越出工作项范围难以用纯规则表达。

**实现机制**　内置与自然语言自定义检查支持不同配置方式。V2 可通过 pre_merge_checks 表达部分内置检查；V3 无此 YAML 节点，禁用若干内置检查，仓库可在 .coderabbit/pre-merge-checks/ 设置自定义定义。适用版本可向 GitHub 发布 Check Run。

**人工决策**　管理员选择策略和告警/错误等级。要成为合并必检，需要在 GitHub branch protection 或 ruleset 中自行将真实检查标识设为 required；修改规则 ID 或目录作用域会影响检查身份。

**组织影响**　可以从 warning 阶段收集争议和例外，再决定是否把具体检查升级为必检；需要指定归属，避免自然语言策略扩张后无人维护。

**版本与演进**　2026-03-11 公布内置与自然语言自定义 pre-merge checks、warning/error 和配置方式。当前文档另列 V3 迁移语义，发布日期不作为 V3 推出的证据。

**适用边界**　商业评审服务内部推理和误报率未实测。配置 V2 与 V3 的语义有别；路径不匹配可标 skipped，未载入定义时可能不报告检查。仅有“发布 Check Run”不能证明违反规则时一定挡住 merge。

**研究推断**　要分别测量建议是否合理、平台是否收到状态、分支规则是否强制。三处中任一处缺失，都可能出现“看见红灯仍能合并”。

**复核实验设计**　准备匹配、不匹配路径、跳过评审三类 PR；把一条可客观核对的检查从 warning 升为 required，比较报告、规则 ID、是否可合并和所有者处置。

- V2 与 V3 差别、Require a check before merge、真实检查身份和 skipped · [原始来源 1](https://docs.coderabbit.ai/pr-reviews/pre-merge-checks) · [本地快照](../lanes/managed/raw/M05/a7b31f4e4336-checks.html)
- How Custom Checks Work、重跑与已失败检查、链接仓库上下文 · [原始来源 2](https://docs.coderabbit.ai/pr-reviews/custom-checks) · [本地快照](../lanes/managed/raw/M05/6b07d8148b3f-custom.html)
- 发布说明 Pre-merge checks 的检查类型、运行时机与 warning/error · 2026-03-11 · [原始来源 3](https://www.coderabbit.ai/blog/pre-merge-checks-built-in-and-custom-pr-enforced) · [本地快照](../lanes/managed/raw/M05/afbf6ba2f98d-log.html)


### M06 Graphite Merge Queue

**适用场景**　多个团队同时推送有依赖的 PR；单个分支检查已绿，仍要确认最终组合能通过 CI 并依正确顺序合并。

**实现机制**　以 stack 为队列单位；支持同一 stack 内快进并行测试、多个 stack 的推测性并行 CI、以及成批测试。批失败时可缩小子集定位问题 stack 并剔除；前序失败时随后推测的组合需要重跑。

**人工决策**　管理员配置 GitHub 条件和队列优化、并行度与批策略，团队查看排队和失败状态；平台停摆时需由负责人选择暂停、等待恢复或启动受控替代流程。

**组织影响**　适合把 PR 生成吞吐与整合能力分开观测。可按仓库计量排队时间、重跑成本、合并失败率与批失败后定位成本。

**版本与演进**　2025-12-19 Cursor 公告确认整合关系，未将未来集成计划当作已实现功能。另据官方状态页，2026-10-30 一次 PR 无法合并事件持续 15 小时 20 分钟并已恢复；这是事故记录。

**适用边界**　官网仍展示产品与试用入口，Cursor 于 2025-12-19 宣布收购协议并表示产品独立运营。没有检查托管队列源码或租户功能。易抖动 CI 会放大下游重跑；单次故障不能推断普遍可用性。

**研究推断**　组织级收益取决于下游队列与测试稳定性；多 agent 生成更多 PR 时，应事先衡量推测 CI 增量成本和外部平台故障的等待损失。

**复核实验设计**　用历史有依赖的 PR 到达序列仿真串行、并行与批处理；在隔离环境复现普通测试失败，统计 CI 重跑、队列尾延迟，再演练供应商不可用时的待办回收。

- 产品官网的 GitHub 接入、试用和 Merge queue 入口 · [原始来源 1](https://graphite.com/) · [本地快照](../lanes/managed/raw/M06/42b8a45ab893-home.html)
- Parallel CI、batch merge failures、flaky tests 的代价 · [原始来源 2](https://graphite.com/docs/merge-queue-optimizations.md) · [本地快照](../lanes/managed/raw/M06/38c58b70d54e-queue.md)
- Set Up The Graphite Merge Queue 的仓库配置与接入 · [原始来源 3](https://graphite.com/docs/set-up-merge-queue.md) · [本地快照](../lanes/managed/raw/M06/d8e492d39210-setup.md)
- Notice history，Oct 30 PRs are unable to be merged，持续时间与已恢复 · 2026-10-30 · [原始来源 4](https://status.graphite.com/history/1) · [本地快照](../lanes/managed/raw/M06/cf9072b271f4-status.html)
- Cursor 公司公告 Graphite is joining Cursor，协议和保留独立产品声明 · 2025-12-19 · [原始来源 5](https://cursor.com/blog/graphite) · [本地快照](../lanes/managed/raw/M06/f54a2bd014b0-log.html)


### M07 Google Antigravity

**适用场景**　多项开发工作并行，负责人需要在关键检查点查看计划、diff 或浏览器录屏，并针对具体产物反馈。

**实现机制**　Google I/O 公布的 2.0 桌面应用整合多 agent、动态子 agent 和后台定时任务；当前 Artifacts 文档列出计划、diff、架构图与录屏，在 App 与 CLI 提供不同的查阅入口，可在计划上内联评论。

**人工决策**　在需要先计划的任务选择适当的 review policy；Always Ask 会停下来等待批准。按当前文档，显式 /plan 默认仍等待批准，即使设置 Always Proceed，除非提示明确要求计划后继续。

**组织影响**　通过共享验收产物给负责人减少逐工具调用盯守的需要；针对 UI 任务可将录屏与测试断言、变更版本一起留档。这里的跨团队共享流程是研究建议。

**版本与演进**　2026-05-19，Google I/O 宣布 Antigravity 2.0 独立桌面应用及 CLI，列出并行 agents 和定时任务；2026-10 的 Jules 公告将 Antigravity 列为开发方向去处之一。

**适用边界**　官方仍提供产品文档。未核对专有 harness 源码或运行实测，录屏不能覆盖未执行的 UI 路径。Jules 公告举例使用其 CLI 辅助导出，但没有证明两个产品的调度、批准或记忆可直接兼容。

**研究推断**　用少数可检查产物管理并发工作，同时保留上游需求和下游验收；在迁移场景中尤其要复核显式批准、默认继续与等待超时的差异。

**复核实验设计**　测试同一含页面交互的任务，通过 App 与 CLI 各自产出计划、diff、录屏；按默认与显式 /plan 做对照，记录停止点及验收者能否复核对应 commit。

- Artifact review policy：Always Ask、Always Proceed、显式 /plan 及继续条件 · [原始来源 1](https://antigravity.google/docs/artifact-review) · [本地快照](../lanes/managed/raw/M07/724c49bcbf16-review.html)
- Reviewing artifacts across surfaces：计划、代码差异、浏览器录屏与 CLI 提醒 · [原始来源 2](https://antigravity.google/docs/artifacts) · [本地快照](../lanes/managed/raw/M07/37585ed838d5-artifacts.html)
- Google I/O 2026：Antigravity 2.0 / CLI、dynamic subagents、scheduled tasks · 2026-05-19 · [原始来源 3](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/) · [本地快照](../lanes/managed/raw/M07/ad6f8cabff92-log.html)


### B01 DX AI Measurement Framework

**适用场景**　在续购、扩大发放或停止 AI 工具时，负责人需要同时衡量使用、影响、成本，并找出交付瓶颈。

**实现机制**　框架将每名开发者每周自报节省时间等直接信号，与 PR 吞吐、感知交付速度、开发体验等纵向数据联合使用。Q3 报告按 AI 代码占比分组，并报告复杂度加权的每人每周 PR 吞吐。

**人工决策**　研发负责人维持团队口径、注明哪些是估计，并向开发者说明用途；开发者提供工具难以捕捉的返工和理解成本。

**组织影响**　在 2026 Q3 自报 500 多家公司样本中，AI 代码占比 20%–40% 档首次评审中位等待 40 分钟，80% 以上档为 82 分钟。分组比较提示可检查评审产能。

**版本与演进**　Q3 报告覆盖 2026 年 7–9 月的评审对照，吞吐曲线覆盖 2025 年 10 月至 2026 年 9 月。这是研究观测窗口，框架首发日未核实。

**适用边界**　厂商样本和分组是观察性材料，不能推出 AI 造成等待增加。Q2 落地页分别使用 teams 和 organizations 称呼样本；未得到原始行数据或各档样本量。商业后台未实测。

**研究推断**　扩大许可前先回答额外产出是否真的到达用户；把审阅等待、交付质量、人时与成本列入同一试点决策。

**复核实验设计**　按团队分阶段启用，预设交付结果和人工返工指标，记录所有符合资格团队及无响应调查者。若净验收无改善且人工服务时间上升，暂停扩容复盘。

- 官方框架 PDF 第 2–5 页，用量、影响、成本，直接和间接口径，以及个人绩效使用边界。 · [原始来源 1](https://getdx.com/uploads/ai-measurement-framework.pdf) · [本地快照](../lanes/market/raw/B01/01-20261120.pdf)
- Q2 季报摘要，500+ teams 与 500+ organizations 两种描述，样本口径须保留不确定性。 · [原始来源 2](https://getdx.com/report/state-of-ai-impact-in-engineering-q2-report/) · [本地快照](../lanes/market/raw/B01/02-20261120.html)
- 2026 Q3 研究，首评等待比较的分组、500+ companies、7–9 月窗口及四季加权吞吐趋势。 · [原始来源 3](https://getdx.com/report/state-of-ai-impact-in-engineering-q3-report/) · [本地快照](../lanes/market/raw/B01/03-20261120.html)


### B02 LinearB AI Analytics

**适用场景**　组织既有作者使用 AI 辅助，也有机器人直接开 PR；管理者要区分交付变慢发生在等待接单还是实际评审。

**实现机制**　LinearB 可先按开发者当天 AI 活跃和阈值标记当天提交，显式 AI Git 元数据可直接标记，再按 PR 中已标记提交占比给 PR 分类。pickup 始于非草稿 PR 开启，止于首个非作者动作；无评论的批准或合并可作为终点。

**人工决策**　主管配置分类阈值，抽查有元数据的结果和模糊归因，评审团队处理等待阶段异常。阈值只控制标签，对开发工作流不执行阻断。

**组织影响**　能分开计量编码、接单、评审、部署，并将自动创建 PR 与人员辅写场景分别观察；无评论批准/合并时 review time 记为 0。

**版本与演进**　分类阈值帮助页元数据记录 2026-03-16 发布、10-04 修订；2026 基准报告列出 AI 与手动 PR 的不同采纳率。修订日期不能当作阈值功能首发。

**适用边界**　开发者日级活跃会被映射到当天其他提交，工作强度、项目难度与归因相关；厂商报告公开摘要缺乏逐行数据。商业后台及分类器未实测。

**研究推断**　看到 review time 下降应同时查看 pickup、无评论样本和弃用率，其下降可能只来自排队位置或统计定义变化。

**复核实验设计**　对 50 个 PR 手工标出纯人工、辅写、全自动、弃用。调整阈值看标签稳定性，再按相似任务比较首评等待、合并率和有效交付率。

- 分类阈值帮助页，逐提交与 PR 分层、显式元数据优先和阈值只影响标签。该日期为页面修订日。 · 2026-10-04 · [原始来源 1](https://linearb.helpdocs.io/article/wyb2trfd6o-configuring-ai-classification-thresholds) · [本地快照](../lanes/market/raw/B02/01-20261120.html)
- Cycle Time Calculation，四阶段起止、作者评论以及零 review time 的分支；日期为元数据修订日。 · 2026-03-16 · [原始来源 2](https://linearb.helpdocs.io/article/0vif1ihmgc-how-is-cycle-time-calculated) · [本地快照](../lanes/market/raw/B02/02-20261120.html)
- 2026 年基准报告公开摘要给出 AI PR 与手工 PR 的接单等待、合并接受率等厂商观测。 · [原始来源 3](https://linearb.io/resources/software-engineering-benchmarks-report) · [本地快照](../lanes/market/raw/B02/03-20261120.html)


### B03 GitHub Copilot usage metrics

**适用场景**　企业管理员按组织检查 Copilot 分配、使用深度和席位覆盖，并希望把仪表板与导出对齐。

**实现机制**　仪表板/API 共用部分字段。补全接受率分子为接受动作数，分母为生成动作数；日记录统计当日活跃，adoption phase 使用滚动 28 天群体，累加每日人数会重复计算。

**人工决策**　管理员选择组织与时窗，核对 IDE 遥测开关、数据延迟和席位信息；团队另行核验发布后的价值。

**组织影响**　前后端数据来自工具生产者，接入成本低；适合回答某团队用到什么能力、哪些人群还需要支持。

**版本与演进**　2026-02-27 使用度量正式 GA；07-22 新增面向企业管理员/组织所有者的 impact dashboard，把 28 天采用阶段分类做成视图。两次事件口径不同。

**适用边界**　IDE 遥测关闭会令细分活动缺失，但服务端仍可能把用户计入活跃人口。采纳事件不是发布、客户验收或缺陷回归。未查询私有租户。

**研究推断**　用量作为覆盖率与干预入口，再按工单连接交付结果；不能把每个被接受的建议视作被采纳的工作项。

**复核实验设计**　固定一日和同一组织，把日活、滚动覆盖、生成、接受四列分别对账。抽样关联上线工单及回滚，给无法映射事件单独分母。

- 指标口径对账文档的日期/人口范围、缺失 IDE 遥测、28 天与每日人数及补全采纳公式。 · [原始来源 1](https://docs.github.com/en/copilot/reference/copilot-usage-metrics/reconciling-usage-metrics) · [本地快照](../lanes/market/raw/B03/01-20261120.html)
- 官方变更记录，使用仪表板与相关 API 正式 GA 的范围。 · 2026-02-27 · [原始来源 2](https://github.blog/changelog/2026-02-27-copilot-metrics-is-now-generally-available/) · [本地快照](../lanes/market/raw/B03/02-20261120.html)
- 官方变更记录，impact dashboard 与基于滚动 28 天使用的 adoption phase。 · 2026-07-22 · [原始来源 3](https://github.blog/changelog/2026-07-22-new-copilot-usage-metrics-impact-dashboard/) · [本地快照](../lanes/market/raw/B03/03-20261120.html)


### B04 Harness AI Engineering Insights / AI DLC Agent

**适用场景**　组织同时采购多种 AI 助手，希望把本地会话、耗费和合入情况连到团队交付与工单。

**实现机制**　工作站常驻代理关联终端工具遥测与 Git 活动。AI committed code 用已归因 AI 提交行数除以全部提交行；另有已提交 AI 行/生成 AI 行。PR 含一个归因提交即可归入 agent，工单可通过关联 PR 归因，工单去重。

**人工决策**　管理员部署代理、配置团队和允许采集的字段；PR 与工单归因结果需由团队按实际任务抽查。

**组织影响**　可把成本、session、提交、PR 和完成工单放在同一处，按工作类型和时间查看所用样本数及分位数。

**版本与演进**　归档时 Insights 页面标 Beta，内页显示 2026-11-12 修订；终端代理安装页 11-02 修订。均为文档更新，未核实首次可用日期。

**适用边界**　官方说明的采用率分母是已导入且安装代理的开发者。采集矩阵显示部分助手无能力覆盖，不能将未覆盖数据填零。探索性生成、共享提交、拆分任务都可能扭曲不同采纳分母。未登录实测。

**研究推断**　生成行、提交行、含 AI 的 PR、最终工单的分母各异。以成本/验收任务作投资决策前要验证首次归因和跨工具冲突。

**复核实验设计**　取重写提交、一个工单多 PR、多人协作、纯探索任务各五例，对账归因和去重。剔除无法观测的工具，给其单独报告覆盖缺口。

- AI Engineering Insights （Beta） 的 Adoption / Impact、PR 归因和 Work Items Delivered 定义，日期为文档修订。 · 2026-11-12 · [原始来源 1](https://developer.harness.io/docs/software-engineering-insights/harness-sei/insights/ai-engineering/) · [本地快照](../lanes/market/raw/B04/01-20261120.html)
- AI DLC Agent （Beta） 入口页，展示产品阶段与安装/数据安全子页。 · 2026-11-02 · [原始来源 2](https://developer.harness.io/ai-dlc-insights/use-ai-dlc-insights/setup/agent) · [本地快照](../lanes/market/raw/B04/02-20261120.html)
- 终端代理技术说明，支持工具矩阵、采集数据、Git 钩子与默认不采集 prompt/response；日期为文档修订。 · 2026-11-02 · [原始来源 3](https://developer.harness.io/ai-dlc-insights/use-ai-dlc-insights/setup/agent/index) · [本地快照](../lanes/market/raw/B04/03-20261120.html)


### B05 阿里云云效 Insight（效能洞察）

**适用场景**　组织想知道需求进开发、测试与上线的等待位置，以及自动生成大量变更后是否改善交付响应。

**实现机制**　Insight 汇集 Projex、Codeup 等系统。需求交付分布每个点表示一个已上线需求，按交付日与耗时展示；累积流图反映不同状态在制品与交付速率。代码报表仅统计已开启洞察报表的代码库。

**人工决策**　团队维护工作项状态、项目与库范围，并在复盘中调整批次、测试或上线节奏，负责人核对遗漏的仓库。

**组织影响**　本地研发体系已有项目、迭代、代码到流水线的总账，便于新增自动化实验前先建立历史对照，也可为跨团队共享约定统一事件定义。

**版本与演进**　效能洞察概览页面 2025-04-27 更新，度量方法 2025-06-04 更新，代码库报表范围说明 2026-06-02 更新。以上都是文档日期。

**适用边界**　已上线需求排除了中途撤销和尚未结束的工作项，关闭采集的仓库不会出现在代码报表。所审材料没有证明 AI 提交归因能力。未登录租户或读取闭源实现。

**研究推断**　国内落地无需先更换研发平台。用既有需求、代码进入、测试和上线时间轴承接 agent 事件，先解决漏链再比较产出。

**复核实验设计**　选同一项目的同类需求，按月同时列入已交付、未完成、撤销三组。先校对默认报表覆盖，再按试点/参照团队比较在制品、需求龄期和发布节奏。

- 产品概览，覆盖 Projex、Codeup 等，项目、代码与流水线报表和高级版范围；页面最后更新日。 · 2025-04-27 · [原始来源 1](https://help.aliyun.com/zh/yunxiao/user-guide/what-is-performance-insights) · [本地快照](../lanes/market/raw/B05/01-20261120.html)
- 研发效能度量方法，已交付需求分布、在制品累积流图、批次与等待示例；页面最后更新日。 · 2025-06-04 · [原始来源 2](https://help.aliyun.com/zh/yunxiao/use-cases/how-do-we-measure-r-d-effectiveness) · [本地快照](../lanes/market/raw/B05/02-20261120.html)
- 如何查看代码库提交情况，开启洞察报表的代码库范围及个人/仓库视图；页面最后更新日。 · 2026-06-02 · [原始来源 3](https://help.aliyun.com/zh/yunxiao/user-guide/how-do-i-view-code-base-commits) · [本地快照](../lanes/market/raw/B05/03-20261120.html)


## 论文

### P01 Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents in Real-World GitHub Scenarios

**论文与轨道**　ICSE 2026 Research · 正文定点复核

**作者**　Zhi Chen、Wei Ma、Lingxiao Jiang

**作者结果**　新加坡管理大学 RISE 的研究者将 8 个 agent 在 SWE-bench Verified 500 道题上的 3,977 条求解轨迹与 3,931 份测试日志拆开读。执行期的 Python 错误与较低解决率、较多推理开销相关，并发现 3 个得到维护者确认的评测平台错误。

**对研发平台的启示**　失败分类应单列环境、工具、评测器和补丁。保存原始失败与重放记录后，才决定是改镜像、改 harness 还是修代码。

**适用边界**　500 道公开 Python 项目题，错误与失败有关联；不能据此把一次 OSError 判为一定无法修复。

**复核位置**　正文 PDF pp.2–4、9–11；Study Design、Discussion · [论文入口](https://doi.org/10.1145/3744916.3773140)

- 书目或作者摘要；按完整题名匹配 · 2026-04-12 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3ABeyond+Final+Code++A+Process-Oriented+Error+Analysis+of+Software+Development+Agents+in+Real-World+GitHub+Scenarios&per_page=5) · [本地快照](../raw/2026-11-20/P01-oa.json)
- 正文 PDF pp.2–4、9–11；Study Design、Discussion · 2026-04-12 · [原始来源 2](https://arxiv.org/pdf/2503.12374) · [本地快照](../raw/2026-11-20/P01-body.pdf)


### P02 SpecRover: Code Intent Extraction via LLMs

**论文与轨道**　ICSE 2025 Research · 正文定点复核

**作者**　Haifeng Ruan、Yuntong Zhang、Abhik Roychoudhury

**作者结果**　SpecRover 通过迭代搜索提炼代码意图，结合复现测试、解释及独立角色审查候选补丁。作者在完整 SWE-bench 上报告 19.3% 解题率，Lite 上为 31%。隐藏验收测试不参与生成。

**对研发平台的启示**　把症状、预期行为和验证方法分别提供给审查人；对照时保留一套生成器看不到的用例。

**适用边界**　审查角色可能继承错误的意图；历史基准成绩只说明该论文设置下的解题能力。

**复核位置**　正文 PDF pp.2、5–6；补丁校验与对照 · [论文入口](https://doi.org/10.1109/icse55347.2025.00080)

- 书目或作者摘要；按完整题名匹配 · 2025-04-26 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3ASpecRover++Code+Intent+Extraction+via+LLMs&per_page=5) · [本地快照](../raw/2026-11-20/P02-oa.json)
- 正文 PDF pp.2、5–6；补丁校验与对照 · 2025-04-26 · [原始来源 2](https://arxiv.org/pdf/2408.02232) · [本地快照](../raw/2026-11-20/P02-body.pdf)


### P03 Rechecking Recheck Requests in Continuous Integration: An Empirical Study of OpenStack

**论文与轨道**　ASE 2025 Research · 摘要及书目

**作者**　Yelizaveta Brus、Rungroj Maipradit、Earl T. Barr、Shane McIntosh

**作者结果**　作者回顾 OpenStack 314,947 次 CI recheck，用任务、机器人及用户的历史行为预测重跑是否转绿，AUROC 为 0.736。论文的累计时间节约来自回放估计。

**对研发平台的启示**　可在新环境以影子模式判断是否重跑，并分别记录错过真失败、浪费算力和开发者等待。

**适用边界**　只观察人已选择重跑的样本；预测转绿不说明根因消失，也不能把总历时换算为实际节省的人年。

**复核位置**　会议页 Abstract L181–183 · [论文入口](https://doi.org/10.1109/ase63991.2025.00121)

- 书目或作者摘要；按完整题名匹配 · 2025-11-16 · [原始来源 1](https://api.crossref.org/works?query.bibliographic=Rechecking+Recheck+Requests+in+Continuous+Integration%3A+An+Empirical+Study+of+OpenStack&rows=4) · [本地快照](../raw/2026-11-20/P03-crossref.json)
- 会议或出版页的浏览器文本摘录 · [原始来源 2](https://conf.researchr.org/details/ase-2025/ase-2025-papers/55/Rechecking-Recheck-Requests-in-Continuous-Integration-An-Empirical-Study-of-OpenStac) · [本地快照](../raw/web/P03-view.txt)


### P04 FlakyGuard: Automatically Fixing Flaky Tests at Industry Scale

**论文与轨道**　ASE 2025 Research · 摘要及书目

**作者**　Chengpeng Li、Farnaz Behrang、August Shi、Peng Liu

**作者结果**　FlakyGuard 选择性遍历代码图，补入不稳定测试相关上下文。作者报告修复可复现样本中的 47.6%，并报告 51.8% 的修复被开发者接受。

**对研发平台的启示**　应分列原始失败、成功复现、产出修复、维护者采纳和后续复发五个分母。

**适用边界**　无法复现的失败在第一个成功率分母之外；现有摘要不足以证明长期降低复发率。

**复核位置**　作者摘要；工业样本及接受口径 · [论文入口](https://doi.org/10.1109/ase63991.2025.00179)

- 书目或作者摘要；按完整题名匹配 · 2025-11-16 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AFlakyGuard++Automatically+Fixing+Flaky+Tests+at+Industry+Scale&per_page=5) · [本地快照](../raw/2026-11-20/P04-oa.json)


### P05 Reducing Cost of LLM Agents with Trajectory Reduction

**论文与轨道**　FSE 2026 Research · 摘要及书目

**作者**　Yuan-an Xiao、Pengfei Gao、Chao Peng、Yingfei Xiong

**作者结果**　AgentDiet 删减轨迹中的无用、重复和过期上下文。在被测组合中输入 token 降低 39.9%–59.7%，作者报告任务表现维持。

**对研发平台的启示**　把供模型消费的压缩轨迹和能供第三方复核的完整事件分开，测每次正确验收的总成本。

**适用边界**　模型、计费缓存和任务分布变化会改变收益；论文数字不能外推成企业账单降幅。

**复核位置**　作者摘要；两种模型、两个基准 · [论文入口](https://doi.org/10.1145/3797084)

- 书目或作者摘要；按完整题名匹配 · 2026-06-30 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AReducing+Cost+of+LLM+Agents+with+Trajectory+Reduction&per_page=5) · [本地快照](../raw/2026-11-20/P05-oa.json)


### P06 A Grounded Theory of Debugging in Professional Software Engineering Practice

**论文与轨道**　FSE 2026 Research · 正文定点复核

**作者**　Haolin Li、Michael J. Coblenz

**作者结果**　UC San Diego 观察 7 名专业开发者及 5 名直播开发者处理自身代码库中的 17 个调试任务。开发者通过导航、执行、前向与反向追踪来更新对系统的解释。

**对研发平台的启示**　交接应给出已排除的原因、反例和下一次能区分假设的观察；仅给最终摘要会迫使接管者重建推理。

**适用边界**　能展示代码且能安排观察的样本有选择性；部分记录覆盖不到调试起点或终点，未测这种交接界面的提效值。

**复核位置**　正文 PDF pp.3–5；招募与质性研究边界 · [论文入口](https://doi.org/10.1145/3797077)

- 书目或作者摘要；按完整题名匹配 · 2026-06-30 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AA+Grounded+Theory+of+Debugging+in+Professional+Software+Engineering+Practice&per_page=5) · [本地快照](../raw/2026-11-20/P06-oa.json)
- 正文 PDF pp.3–5；招募与质性研究边界 · 2026-06-30 · [原始来源 2](https://arxiv.org/pdf/2602.11435) · [本地快照](../raw/2026-11-20/P06-body.pdf)


### P07 Unpacking AI Agent Participation in Issue-Centered Collaboration in Open-Source Software Development

**论文与轨道**　ISSTA 2026 Research · 摘要及书目

**作者**　Kaiwen Zhi、Guisheng Fan、Wentao Chen

**作者结果**　华东理工相关研究以 issue 事件序列区分人和 agent 协作。agent 相关协作复杂性与产出和新增缺陷有统计关联，解决效率的关系依赖上下文。

**对研发平台的启示**　同一平台应按服务、任务类型和团队拆开观察；用 issue 到生产的事件链核对异常变化。

**适用边界**　观察性开源仓库数据，不能解释选用 agent 的团队为什么本来就不同，缺陷也取决于被记录程度。

**复核位置**　作者摘要；83 仓库 project–month 面板 · [论文入口](https://doi.org/10.1145/3832206)

- 书目或作者摘要；按完整题名匹配 · 2026-10-01 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AUnpacking+AI+Agent+Participation+in+Issue-Centered+Collaboration+in+Open-Source+Software+Development&per_page=5) · [本地快照](../raw/2026-11-20/P07-oa.json)


### P08 A Dataset of Reproducible Flaky-Test Failures

**论文与轨道**　ISSTA 2026 Research · 正文定点复核

**作者**　S. Rafi、Mahbub-Ul-Hoque Sumon、Md Erfan、Maruf Morshed Khan、August Shi、Wing Lam

**作者结果**　ReproFlake 汇集 1,115 个可复现的不稳定测试，按四类整理，提供环境、通过与失败日志、修复及验证脚本。

**对研发平台的启示**　保存一红一绿、环境版本和验证修复的脚本，构造团队自己的困难例回放集。

**适用边界**　入库条件要求成功复现；Java/Maven 环境影响范围。一次修复成功不足以证明以后不再不稳定。

**复核位置**　正文 PDF pp.2–3、16；构造与效度讨论 · [论文入口](https://doi.org/10.1145/3832216)

- 书目或作者摘要；按完整题名匹配 · 2026-10-01 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AA+Dataset+of+Reproducible+Flaky-Test+Failures&per_page=5) · [本地快照](../raw/2026-11-20/P08-oa.json)
- 正文 PDF pp.2–3、16；构造与效度讨论 · 2026-10-01 · [原始来源 2](https://arxiv.org/pdf/2605.21677) · [本地快照](../raw/2026-11-20/P08-body.pdf)


### P09 Programming by Chat: A Large-Scale Behavioral Analysis of 11,579 Real-World AI-Assisted IDE Sessions

**论文与轨道**　ASE 2026 Research · 摘要及书目

**作者**　Ningzhi Tang、Chaoran Chen、Zihan Fang、Gelei Xu、Maria Dhakal、Yiyu Shi、Collin McMillan、Yu Huang、Toby Jia-Jun Li

**作者结果**　作者读了 899 位开发者在 1,300 个仓库公开提交的 11,579 段 IDE 会话、74,998 条开发者消息。可以观察到逐步明确需求、委派诊断与验证、把计划写成持久材料等行为。

**对研发平台的启示**　第一次派工只要求列出确定条件和待裁决项；容许任务中途修订规格并作废旧验收。

**适用边界**　会把聊天提交到公开仓库的人并不代表企业全体；消息频度与任务质量是不同结果。

**复核位置**　会议页 Abstract L200–202 · [论文入口](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/47/Programming-by-Chat-A-Large-Scale-Behavioral-Analysis-of-11-579-Real-World-AI-Assist)

- 会议或出版页的浏览器文本摘录 · [原始来源 1](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/47/Programming-by-Chat-A-Large-Scale-Behavioral-Analysis-of-11-579-Real-World-AI-Assist) · [本地快照](../raw/web/P09-view.txt)


### P10 Generation of Web Apps with Agentic IDEs: An Empirical Assessment

**论文与轨道**　ASE 2026 Research · 正文定点复核

**作者**　Manuel Marceca、Maria Teresa Rossi、Leonardo Mariani

**作者结果**　研究让 Copilot、Cursor、Windsurf 从头实现五种全栈应用。常见 CRUD 等模式比引入异步任务队列的架构产生更少错误。

**对研发平台的启示**　分流时按系统间假设、状态一致性与可验证程度分层，避免只按改动行数。

**适用边界**　五个从零搭建的应用，检查清单的定义与标注影响错误计数；无法代表旧系统维护。

**复核位置**　正文 PDF pp.3、9；三种 IDE、构念效度 · [论文入口](https://doi.org/10.1145/3832783.3837506)

- 书目或作者摘要；按完整题名匹配 · 2026-10-07 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AGeneration+of+Web+Apps+with+Agentic+IDEs++An+Empirical+Assessment&per_page=5) · [本地快照](../raw/2026-11-20/P10-oa.json)
- 正文 PDF pp.3、9；三种 IDE、构念效度 · 2026-10-07 · [原始来源 2](https://arxiv.org/pdf/2608.20903) · [本地快照](../raw/2026-11-20/P10-body.pdf)


### P11 Automated Code Review in Practice

**论文与轨道**　ICSE 2025 SEIP · 摘要及书目

**作者**　Umut Cihan、Vahid Haratian、Arda İçöz、Mert Kaan Gül、Ömercan Devran、Emircan Furkan Bayendur、Baykal Mehmet Uçar、Eray Tüzün

**作者结果**　10 个项目可以使用基于 Qodo PR Agent 的评审工具；深入分析的 3 个项目共 4,335 个 PR，其中 1,568 个获自动评审。73.8% 的自动评论标记已解决，但总体平均关闭时间由 5 小时 52 分增至 8 小时 20 分，项目趋势不一。

**对研发平台的启示**　评审产品需同时度量有效修复、无用建议和等待，对所有符合条件的 PR 保留分母。

**适用边界**　前后比较包含团队和任务组成变化。关闭评论不能证明修复了真实缺陷，也不能断言工具造成变慢。

**复核位置**　作者摘要；ICSE SEIP 行业轨，三项目 PR 与调查 · [论文入口](https://doi.org/10.1109/icse-seip66354.2025.00043)

- 书目或作者摘要；按完整题名匹配 · 2025-04-27 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AAutomated+Code+Review+In+Practice&per_page=5) · [本地快照](../raw/2026-11-20/P11-oa.json)


### P12 Expectations, outcomes, and challenges of modern code review

**论文与轨道**　ICSE 2013 research · 摘要及书目

**作者**　Alberto Bacchelli、Christian Bird

**作者结果**　访谈、观察、问卷及评论分类表明，评审除发现缺陷外，还传递知识、建立团队认知、提出替代实现；理解变更目的贯穿其中。

**对研发平台的启示**　将维护者边读边学习、需要业务裁决的评审与可机械验证的检查分开计价。

**适用边界**　2013 年工具和流程与当今 agent 不同，适合解释评审工作内容。

**复核位置**　作者摘要；微软多团队现场研究 · [论文入口](https://doi.org/10.1109/icse.2013.6606617)

- 书目或作者摘要；按完整题名匹配 · 2013-05-01 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AExpectations++outcomes++and+challenges+of+modern+code+review&per_page=5) · [本地快照](../raw/2026-11-20/P12-oa.json)


### P13 SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

**论文与轨道**　ICLR 2024 · 摘要及书目

**作者**　Jimenez, Carlos E.、Yang, John、Alexander Wettig、Shunyu Yao、Kexin Pei、Ofir Press、Karthik Narasimhan

**作者结果**　Princeton 等研究者用 12 个 Python 仓库、2,294 对 issue 与修复建立 SWE-bench，把跨文件变更接到可重复测试。

**对研发平台的启示**　可以借用其任务包和独立测试思想做内部盲测，按时间隔离数据并轮换留出集。

**适用边界**　覆盖的是已出现修复的公开 issue；上线授权、业务澄清、需求定夺和跨团队协调不在判分中。

**复核位置**　原论文作者摘要；初版 arXiv 2023，ICLR 2024 · [论文入口](https://doi.org/10.48550/arxiv.2310.06770)

- 书目或作者摘要；按完整题名匹配 · 2023-10-10 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3ASWE-bench++Can+Language+Models+Resolve+Real-World+GitHub+Issues+&per_page=5) · [本地快照](../raw/2026-11-20/P13-oa.json)


### P14 SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

**论文与轨道**　NeurIPS 2024 · 摘要及书目

**作者**　John Yang、Carlos E. Jimenez、Alexander Wettig、Kilian Lieret、Shunyu Yao、Karthik Narasimhan、Ofir Press

**作者结果**　SWE-agent 为模型设计查找、编辑和执行工具界面，在 SWE-bench 与 HumanEvalFix 上测试单次成功。它让“固定模型、替换工具界面”的对照变得可操作。

**对研发平台的启示**　先单独比较错误反馈与可见状态，再决定是否升级推理模型。

**适用边界**　论文模型与任务是历史配置，两种测试都不观察生产发布。

**复核位置**　NeurIPS 2024 正式论文摘要页 · [论文入口](https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html)

- 会议或出版页的浏览器文本摘录 · [原始来源 1](https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) · [本地快照](../raw/web/P14-view.txt)


### P15 From Vibe to Spec: An Empirical Study to Demystify Specifications in Code Generation

**论文与轨道**　ASE 2026 Research · 摘要及书目

**作者**　Ruirui He、Hanqing Lu、Lezhi Ma、Kai Ye、Qiong Wu、Shangqing Liu、Lei Bu、Xuandong Li

**作者结果**　南京大学研究者构造五个中等规模项目，操作规格形式和输入粒度。细结构伪代码有利于稳定生成，模块级输入在这些项目上取得较好的质量、稳定性和 token 平衡。

**对研发平台的启示**　试验时同时计入维护规格的人时，并用不参与编写规格的人做盲审。

**适用边界**　项目为数百至千余行的规模，研究不足以回答大型遗留系统的规格维护成本。

**复核位置**　会议页 Abstract L200–206 · [论文入口](https://doi.org/10.1145/3832783.3837515)

- 书目或作者摘要；按完整题名匹配 · 2026-10-07 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AFrom+Vibe+to+Spec++An+Empirical+Study+to+Demystify+Specifications+in+Code+Generation&per_page=5) · [本地快照](../raw/2026-11-20/P15-oa.json)
- 会议或出版页的浏览器文本摘录 · [原始来源 2](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/219/From-Vibe-to-Spec-An-Empirical-Study-to-Demystify-Specifications-in-Code-Generation) · [本地快照](../raw/web/P15-view.txt)


### P16 Agentic Verification of Software Systems

**论文与轨道**　FSE 2026 Research · 正文定点复核

**作者**　Haoxin Tu、Huan Zhao、Yahui Song、Mehtab Zafar、Ruijie Meng、Abhik Roychoudhury

**作者结果**　NUS 的 AutoRocq 与 Rocq 交互，读取目标与错误、搜索证明，最终由检查器验证推导；在所选 Linux 内核案例上验证 12 个引理，论文报告基线为 2–10 个。

**对研发平台的启示**　把少量代价高且语义明确的约束交给独立检查器，区分“命题写对”和“命题得到证明”。

**适用边界**　已形式化的性质和可负担的证明搜索构成前提；不能借此担保业务意图或整个软件无缺陷。

**复核位置**　正文 PDF pp.3、17；AutoRocq 与效度讨论 · [论文入口](https://doi.org/10.1145/3808164)

- 书目或作者摘要；按完整题名匹配 · 2026-06-30 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AAgentic+Verification+of+Software+Systems&per_page=5) · [本地快照](../raw/2026-11-20/P16-oa.json)
- 正文 PDF pp.3、17；AutoRocq 与效度讨论 · 2026-06-30 · [原始来源 2](https://arxiv.org/pdf/2511.17330) · [本地快照](../raw/2026-11-20/P16-body.pdf)


### P17 A Large-Scale Survey on the Usability of AI Programming Assistants: Successes and Challenges

**论文与轨道**　ICSE 2024 Research · 摘要及书目

**作者**　Jenny T. Liang、Chenyang Yang、Brad A. Myers

**作者结果**　CMU 等研究者问卷覆盖 410 名开发者。减少按键和回忆语法是动机，难以控制输出及功能、非功能需求偏离是不用工具的原因。

**对研发平台的启示**　试点退出原因和拒用者也要入样，调查可控感时与任务实耗配对。

**适用边界**　问卷为自报，面向较早的编程辅助实践；不能给自动派工定量预测。

**复核位置**　会议页 Abstract L353–356 · [论文入口](https://doi.org/10.1145/3597503.3608128)

- 书目或作者摘要；按完整题名匹配 · 2024-2-6 · [原始来源 1](https://api.crossref.org/works?query.bibliographic=A+Large-Scale+Survey+on+the+Usability+of+AI+Programming+Assistants%3A+Successes+and+Challenges&rows=4) · [本地快照](../raw/2026-11-20/P17-crossref.json)
- 会议或出版页的浏览器文本摘录 · [原始来源 2](https://conf.researchr.org/details/icse-2024/icse-2024-research-track/3/A-Large-Scale-Survey-on-the-Usability-of-AI-Programming-Assistants-Successes-and-Cha) · [本地快照](../raw/web/P17-view.txt)


### P18 LinkAnchor: An Autonomous LLM-Based Agent for Issue-to-Commit Link Recovery

**论文与轨道**　FSE 2026 Research · 摘要及书目

**作者**　Arshia Akhavan、Alireza Hoseinpour、Abbas Heydarnoori、Hamid Bagheri、Mehdi Keshani

**作者结果**　LinkAnchor 懒加载上下文，沿提交图追回解决 issue 的提交链，避免只对孤立的 issue/commit 对打分。

**对研发平台的启示**　组织测量先给自动关联附可信度；原因链未能核实的发布可计作未知，支持后来人工修订。

**适用边界**　六项目的检索命中与部署归因有距离；一个 issue 可能有回滚、重做和多团队贡献。

**复核位置**　作者摘要；六个开源项目的关联恢复 · [论文入口](https://doi.org/10.1145/3808191)

- 书目或作者摘要；按完整题名匹配 · 2026-6-30 · [原始来源 1](https://api.crossref.org/works?query.bibliographic=LinkAnchor%3A+An+Autonomous+LLM-Based+Agent+for+Issue-to-Commit+Link+Recovery&rows=4) · [本地快照](../raw/2026-11-20/P18-crossref.json)


### P19 Code Review of Build System Specifications: Prevalence, Purposes, Patterns, and Perceptions

**论文与轨道**　ICSE 2023 Research · 正文定点复核

**作者**　Mahtab Nejati、Mahmoud Alfadel、Shane McIntosh

**作者结果**　Waterloo Software REBELs 在 Qt、Eclipse 分析 502,931 个变更集，并定性分析 500 个、访谈 9 人。构建规格变更在评审中受到的讨论比生产和测试代码少。

**对研发平台的启示**　修改 harness、CI 规则或验证器时设独立 owner；规则改动的影响半径可能比业务改动更大。

**适用边界**　讨论少不是缺陷率高；两个大项目、构建技术及人工编码限制泛化。

**复核位置**　正文 PDF pp.10–11；双项目与人工编码限制 · [论文入口](https://doi.org/10.1109/icse48619.2023.00108)

- 书目或作者摘要；按完整题名匹配 · 2023-05-01 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3ACode+Review+of+Build+System+Specifications++Prevalence++Purposes++Patterns++and+Perceptions&per_page=5) · [本地快照](../raw/2026-11-20/P19-oa.json)
- 正文 PDF pp.10–11；双项目与人工编码限制 · 2023-05-01 · [原始来源 2](https://rebels.cs.uwaterloo.ca/papers/icse2023_nejati.pdf) · [本地快照](../raw/2026-11-20/P19-body.pdf)


### P20 Unified Software Engineering Agent as AI Software Engineer

**论文与轨道**　ICSE 2026 Research · 正文定点复核

**作者**　Leonhard Applis、Yuntong Zhang、Shanchao Liang、Nan Jiang、Lin Tan、Abhik Roychoudhury

**作者结果**　USEagent 将测试、修复等动作放入统一调度。1,271 道混合任务，消融中移除 ExecuteTests 后，取样 REPOCOD 的成功率从 8.7% 降到 0%，同一表的 SWE-Ver 指标保持 49.6%。

**对研发平台的启示**　按任务类型做动作消融。同一种执行工具在某类任务中无可见增量，在另一类任务中可能决定结果。

**适用边界**　同一消融实验的模型与任务子集有限，测试覆盖率只是部分任务的代理指标。

**复核位置**　正文 PDF pp.7、9、11；表 4 消融 · [论文入口](https://doi.org/10.1145/3744916.3773202)

- 书目或作者摘要；按完整题名匹配 · 2026-04-12 · [原始来源 1](https://api.openalex.org/works?filter=title.search%3AUnified+Software+Engineering+agent+as+AI+Software+Engineer&per_page=5) · [本地快照](../raw/2026-11-20/P20-oa.json)
- 正文 PDF pp.7、9、11；表 4 消融 · 2026-04-12 · [原始来源 2](https://arxiv.org/pdf/2506.14683) · [本地快照](../raw/2026-11-20/P20-body.pdf)


## 工程现场与对照

### I01 OpenAI 的 agent-first 仓库

**复核位置**　每个 worktree 的可观测性与仓库约束

**一手材料**　团队把应用按工作树独立启动，给 agent 提供浏览器、指标与日志；维护者把架构约束编成能反复执行的检查。这让开发者可以指定某次冷启动或用户路径的目标。

**证据边界**　为特定内部项目有意重建基础设施；文中的时间倍数是团队估计，没有同期对照。

- 每个 worktree 的可观测性与仓库约束 · [原始来源 1](https://openai.com/index/harness-engineering/) · [本地快照](../raw/2026-11-20/I01.html)


### I02 Stripe Minions

**复核位置**　Blueprints、Linting and CI；原文行 49–85

**一手材料**　蓝图混合确定性步骤和由模型决定的步骤。跑 lint、push 是确定性节点；CI 失败才把证据发回修复节点，第二轮 CI 后交回人。合并前有人工审查。

**证据边界**　厂商给出的每周超过 1,300 个已合并 PR 是量，不是每个 PR 的成本、价值或事故率。QA devbox 和既有测试平台是前提。

- Blueprints、Linting and CI；原文行 49–85 · [原始来源 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) · [本地快照](../raw/web/I02-view.txt)


### I03 Anthropic 跨会话长任务

**复核位置**　初始化、进度文件、功能列表

**一手材料**　初始化 agent 建立环境和工作清单，后续会话增量工作，读进度文件与 Git 状态再继续。每个会话能重新找到验收目标。

**证据边界**　适用于可拆分和持久化的工作；错误验收清单同样会跨会话延续。

- 初始化、进度文件、功能列表 · [原始来源 1](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [本地快照](../raw/2026-11-20/I03.html)


### I04 Cursor Automations

**复核位置**　2026-03-05 发布说明

**一手材料**　日程、Slack、Linear、GitHub、PagerDuty 或 webhook 等事件可在云沙箱启动任务，使用配置的 MCP、模型与记忆工具。

**证据边界**　厂商说明触发与执行方式，未提供治理成本或审查节省的有对照实测。

- 2026-03-05 发布说明 · [原始来源 1](https://cursor.com/changelog/03-05-26) · [本地快照](../raw/2026-11-20/I04.html)


### I05 Cursor Automations 多仓扩展

**复核位置**　2026-05-20 版本 3.5

**一手材料**　增设 Agents Window 管理入口，一次自动化可附多个仓库，也可不附代码仓库。跨仓和从工具事件起步成为明确的配置选项。

**证据边界**　可读写多个仓库不等于跨仓原子提交、连带回滚或一致的发布验收。

- 2026-05-20 版本 3.5 · [原始来源 1](https://cursor.com/changelog/05-20-26) · [本地快照](../raw/2026-11-20/I05.html)


### I06 GitHub Copilot cloud agent 自动化

**复核位置**　自动化配置、仓库与套餐条件

**一手材料**　可用日程、仓库事件或 API 从仓库 Agents 页触发；可产生 issue 标签或 PR。该文限定在启用功能且满足计划条件的 private/internal 仓库，列出管理员与托管账户限制。

**证据边界**　适用性取决于仓库、账户和策略；此产品与 GitHub Agentic Workflows 是不同机制。

- 自动化配置、仓库与套餐条件 · [原始来源 1](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-automations) · [本地快照](../raw/2026-11-20/I06.html)


### I07 GitHub 云端代理的责任边界

**复核位置**　PR 审批和 workflow 执行

**一手材料**　文档区分提出变更、运行 workflow、批准和合并。云代理不能批准或合并自己的 PR；默认路径中的特定 workflow 需要有写权限的人确认，部分行为可配置。

**证据边界**　触发人、自动化所有者和 app 身份不同，不能假定每份结果对应相同的审批规则。

- PR 审批和 workflow 执行 · [原始来源 1](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations) · [本地快照](../raw/2026-11-20/I07.html)


### I08 METR 随机任务试验

**复核位置**　PDF pp.1–2、6–8

**一手材料**　16 位熟悉所维护项目的开源开发者做 246 个任务，任务被随机分配允许或禁止当时的 AI 工具。允许 AI 的实现用时估计增加 19%，作者给出的区间为 2%–39%。

**证据边界**　研究覆盖 2025 年初的工具与熟悉仓库的开发者，不能把结论外推为 2026 年企业 agent 的效果。

- PDF pp.1–2、6–8 · [原始来源 1](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf) · [本地快照](../raw/2026-11-20/I08.pdf)


### I09 METR 修订实验设计

**复核位置**　2026-02-24；选择与计时

**一手材料**　后续招募遇到不愿放弃 AI 的人不参试、部分任务不提交、报酬变化及并行工作工时难归属。作者判断新数据对当前效果大小的指示很弱。

**证据边界**　需要同时保存拒绝和未纳入的任务，区分墙钟、主动人时及多任务重叠。

- 2026-02-24；选择与计时 · [原始来源 1](https://metr.org/blog/2026-02-24-uplift-update/) · [本地快照](../raw/2026-11-20/I09.html)


### I10 DORA 2025

**复核位置**　报告概览与 AI Capabilities Model

**一手材料**　报告将 AI 看作组织已有能力与弱点的放大因素，强调平台、工作方式和组织条件。

**证据边界**　群体研究和作者综合解释适合提出分层变量；不能据此预测单企业节省金额。

- 报告概览与 AI Capabilities Model · [原始来源 1](https://dora.dev/research/2025/dora-report/) · [本地快照](../raw/2026-11-20/I10.html)


### I11 DORA 2025 勘误

**复核位置**　v.2025.2，报告 p.71

**一手材料**　勘误把一处 stability 改为 instability，两者对绩效与风险补偿的解读相反。

**证据边界**　引用图表和报告要记版本，提速与失稳应分开跟踪。

- v.2025.2，报告 p.71 · [原始来源 1](https://dora.dev/research/2025/errata/) · [本地快照](../raw/2026-11-20/I11.html)


### I12 OpenAI 对 SWE-bench Verified 的审计

**复核位置**　不合理测试与污染分析

**一手材料**　评测作者区分测试额外要求、公开材料泄漏等误差来源；部分题要求 issue 未明说的专有名字，向模型提供评测反馈还可能暴露答案。

**证据边界**　厂商审计本身有采样与检测限制；对某个分数的质疑不能代表所有任务都失效。

- 不合理测试与污染分析 · [原始来源 1](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) · [本地快照](../raw/2026-11-20/I12.html)


### I13 CCF 软件工程/系统软件/程序设计语言目录

**复核位置**　国际会议 A 类表

**一手材料**　本期所用分类把 FSE、ASE、ICSE、ISSTA 列在 A 类。期刊、行业轨、workshop 和其他领域会议在本报告分开标注。

**证据边界**　目录只核定系列与类别，论文发表轨道需另查。

- 国际会议 A 类表 · [原始来源 1](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/) · [本地快照](../raw/2026-11-20/I13.html)


### I14 Anthropic 分离生成与评估

**复核位置**　2026-03-24；实验与迭代

**一手材料**　工程实验先给视觉设计明确评价维度，再让评估 agent 通过浏览器操作、截图并反馈给生成器。作者还观察到仅改评价标准的描述也能改变生成结果。

**证据边界**　生成器与评估器同时改动会混淆归因，审美偏好也需要目标用户校准。

- 2026-03-24；实验与迭代 · [原始来源 1](https://www.anthropic.com/engineering/harness-design-long-running-apps) · [本地快照](../raw/2026-11-20/I14.html)


### I15 Devin Playbooks

**复核位置**　组织及 Enterprise Playbooks、编写建议

**一手材料**　可把重复任务说明存于组织库、跨会话使用。官方建议并行运行实例暴露歧义，针对需要人工帮助的位置修订 playbook。

**证据边界**　重用提示与强制执行规则不同，重要前置条件还要有独立检查。

- 组织及 Enterprise Playbooks、编写建议 · [原始来源 1](https://docs.devin.ai/product-guides/creating-playbooks) · [本地快照](../raw/2026-11-20/I15.html)


### I16 OpenAI Performance Factory

**复核位置**　2026-11-18；Regression Workflow、评测

**一手材料**　性能告警开工单，agent 诊断并写入同一任务、提出供工程师审查的修复；部署后另一个 agent 核对指标是否回基线。团队另行评估诊断能力和人能否读懂摘要。

**证据边界**　厂商现场报告；依赖组织已有的追踪、指标、剖析与发布数据。未取得该团队原始数据。

- 2026-11-18；Regression Workflow、评测 · [原始来源 1](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/) · [本地快照](../raw/2026-11-20/I16.html)


### I17 OpenAI Symphony

**复核位置**　2026-04-27；任务状态机

**一手材料**　Linear 工单成为控制对象，每个活跃任务对应工作区，系统持续轮询、处理停滞和新任务；一次工单可以产生多个 PR，也可以只交付调查。

**证据边界**　一些团队 landed PR 增长只是其观察量，不能解释团队净产出变化。

- 2026-04-27；任务状态机 · [原始来源 1](https://openai.com/index/open-source-codex-orchestration-symphony/) · [本地快照](../raw/web/I17-view.txt)


### I18 GitHub Agentic Workflows

**复核位置**　2026-10-28 GA 发布记录

**一手材料**　将 Markdown 工作流编译成 Actions YAML，复用 runner 与已有策略；默认只读，后续允许写入的操作经 safe outputs 处理。

**证据边界**　GA 是该功能的发布状态，个别客户的效率数字不能作为所有客户基线。

- 2026-10-28 GA 发布记录 · [原始来源 1](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/) · [本地快照](../raw/web/I18-view.txt)


### I21 METR 评估 Anthropic 内部 AI 研发

**复核位置**　2026-11-05；研究访问范围与删节披露

**一手材料**　METR 获得内部指标和访谈，判断 Anthropic 在明确任务上的模型能力进展较历史阶段可能显著加快，约为历史速率的两倍；对幅度和归因均保留较大不确定性。

**证据边界**　AI 研发组织的能力进展率与普通产品团队的工单用时是不同结果。作者称最有信息量的证据多数被删节，外部无法完整复核。

- 2026-11-05；研究访问范围与删节披露 · [原始来源 1](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) · [本地快照](../raw/web/I21-view.txt)


### I22 Endsley 与 Kiris 的人工接管研究

**复核位置**　Human Factors 1995，作者摘要

**一手材料**　在导航专家系统实验中，较低的态势感知伴随自动化失败后较差的决策响应。

**证据边界**　跨领域人因证据，只能作为研发现场的待验证假设，不能声称已有软件团队接管延时的同幅度测量。

- Human Factors 1995，作者摘要 · [原始来源 1](https://journals.sagepub.com/doi/10.1518/001872095779064555) · [本地快照](../raw/web/discovery-human.txt)


### I23 SPACE 开发者生产率框架

**复核位置**　Microsoft Research，2021

**一手材料**　以满意度与福祉、绩效、活动、沟通协作、效率与流动等维度观察开发工作，反对用单项活动计数统一衡量生产力。

**证据边界**　是测量框架，不能给 agent 使用规定一个跨公司的收益阈值。

- Microsoft Research，2021 · [原始来源 1](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/) · [本地快照](../raw/web/I23-view.txt)


### I24 Google SRE 金丝雀实践

**复核位置**　Canarying Releases；control、canary 与判断

**一手材料**　将待发布版本暴露给有限流量，在限定时间窗内与并行对照比较，决定是否扩大流量。

**证据边界**　对照可比性、流量构成和波动会左右判断；单纯通过预发布测试不能替代生产信号。

- Canarying Releases；control、canary 与判断 · [原始来源 1](https://sre.google/workbook/canarying-releases/) · [本地快照](../raw/web/I24-view.txt)

