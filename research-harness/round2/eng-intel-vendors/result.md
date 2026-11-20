# 三种组织研发效能平台的采购对照

DX、Jellyfish、LinearB 都能让工程负责人看到团队层面的变化，但能回答的问题不同。DX 可把具体软件实体上失败的检查变成有负责人的改进任务。Jellyfish 把投入、代理身份和开发者体验放在一起，适合追问“问题集中在哪个团队、该投谁”。LinearB 可以用工作协议把等待评审的具体 PR 送回团队。本组的购买对象是组织级度量与改进系统，单列 3 家；与执行研发任务的 35 个产品、模型或代理评估品类分开统计。同一个厂商可以同时提供几种工作。[DX Initiatives](https://docs.getdx.com/scorecards/initiatives/) · [Jellyfish AI Impact](https://jellyfish.co/blog/new-in-ai-impact-agent-developer-insights-executive-reporting/) · [LinearB 工作协议](https://linearb.io/blog/team-working-agreements)

|采购问题|DX|Jellyfish|LinearB|
|---|---|---|---|
|团队变化以什么为单位？|合并的人类 PR / 按在组天数折算的开发者；另有独立的问卷回应人数|月度公司分布、团队、工具、agent 身份；单项指标的 PR、行、费用分母不同|开发者 UTC 人日、commit、PR、分支阶段与调查对象|
|谁有办法干预？|Scorecard 管理员发起 initiative，owner 跟踪失败实体，团队可收到提醒|负责人以团队体验与遥测决定是否投入工程师；公开自用案例把行动落实到测试自动化工作|负责人按约定给长时间无人评审的 PR 发 Slack/Teams 提醒；调查可单独追问|
|需要采购现场核对什么？|哪些输入在多租户或客户云里；未链接账号、换组、小样本抑制如何处理|代理提交者与人工开 PR 能否拆分；分段是否保护匿名；行动能否回连工程事项|更改归因阈值后历史看板是否变；提醒是否送对团队、已接受评审后是否停止|

## DX：把团队反馈转成有主的改进工作

**归属与部署。** 2025-09-18 Atlassian 公告说已签订收购协议。Atlassian FY26 年报 Note 7 写明在 **2025-11-10 收购了 DX 的 100% 股权**。Software Collection 页面当前列入 DX。交付方式仍须逐条看 DX 部署说明：多租户 SaaS 的第一方 DX 数据在共享基础设施上，GitHub、Jira 等第三方导入数据使用专用基础设施；DX Dedicated 是厂商运营的单租户；DX Managed 则在客户拥有的云账户内由 DX 负责部署、升级、监控和值班。总览和 Managed 页写 AWS/GCP，但后者的 GCP 具体操作说明仍标 coming soon，本文只确认文档列举的方案，现场需查所需云区和实际开通状态。[签约公告](https://www.atlassian.com/blog/announcements/atlassian-acquires-dx) · [Atlassian FY26 年报](https://s206.q4cdn.com/270053503/files/doc_financials/2026/ar/Atlassian-FY26-Annual-Report.pdf) · [交付选项](https://docs.getdx.com/deployment-options/) · [DX Managed](https://docs.getdx.com/managed/)

**采集与分母。** DX 的 PR throughput 是指定期间合并的 PR 数除以贡献工程师数，排除 bot 开的 PR。作为开发者必须已合并过至少一个 PR，且未被明确标为非开发者；SCM 身份需关联。进出团队或组织时按实际在组日数摊分分母。问卷中的“工作是否经常编程”、管理员设置或属性导入都可能改变人员归类。厂商 Q3 2026 研究另用加权 PR/人/周的 TrueThroughput，样本来自 500 多家公司，图表覆盖 2025-10 至 2026-09。该加权研究指标与仪表盘普通 PR throughput 用不同定义。[指标定义与团队变动示例](https://docs.getdx.com/reports/pr-throughput/) · [Q3 研究](https://getdx.com/report/state-of-ai-impact-in-engineering-q3-report/)

**反馈和交接。** Snapshot 按周期向选定职能发问卷、提醒未答者，团队按分数与文字反馈讨论摩擦点。API 分别返回合格群体数与答题人数，小群体可按账户最小答题门槛隐藏结果；官方说明支持具名评论，不能把小群体抑制解释为所有文字都匿名。Scorecard 管理员可针对一项或多项检查建 initiative，将失败实体转为任务，填写 owner、截止日期，按实体归属向团队发送可选 Slack 提醒。调查低分如何转成可计算的检查，需要团队设计；没有证据表明单次低分会自动改仓或触发该机制。[Snapshots](https://docs.getdx.com/snapshots/overview/) · [分组返回值](https://docs.getdx.com/webapi/methods/snapshots.driverscores.breakdown/) · [具名评论](https://docs.getdx.com/knowledgebase/why-are-comments-non-anonymous/) · [行动对象](https://docs.getdx.com/scorecards/initiatives/)

**可证伪演示。** 提供一位月中换组开发者、一条 bot PR 和一个未链接 SCM 账号，要求导出两个团队各自的分子、折算分母及未归类记录。再选一条实际失败的实体检查，指定 owner，到期前后追踪提醒，检查修复后能否关联回原任务。验收记录应能区分数据缺失、团队归属改变和检查真正修复。

## Jellyfish：同一个 PR 在采用率和成本表里可能有不同归属

**研究与版本。** 2025-06-18 厂商发表滚动研究，说明以其 AI Impact 数据分析 2024-07 至 2025-06 的逾 200 万个 PR。2025-11-18 发布的更新增加 Autonomous Agent Insights、将开发者体验预设问卷整合进 AI Impact，并推出管理层报告工作流。聚合样本反映其客户和所接工具的数据，缺乏随机分配条件；客户参与、自选工具和业务结构均可能影响差异。[公开研究](https://jellyfish.co/blog/ai-impact-data-june-2025/) · [功能更新](https://jellyfish.co/blog/new-in-ai-impact-agent-developer-insights-executive-reporting/)

**采集与分母。** 趋势页的 Autonomous Agent Activity 以 PR 开启者为 agent 或 PR 包含 agent 身份所提交的 commit 为参与信号；同页讨论的是已合并 PR 中的参与占比。Software Factory PRs 更窄，按公司每月已合并 PR 中由 factory agent 身份开启的比例衡量，并对公司分布取分位数。人开 PR、代理贡献 commit 的情况会让两个指标分离。AI Code Percentage 又以已合并 PR 的新增代码行做分母；Cost per PR 将工程薪酬加已定价的 AI 使用成本除以**由人开启且合并**的 PR 数，按公司计算。不能用这一成本去乘“所有合并 PR 数”反推总成本。聊天中的帮助若未留下可识别身份，无法仅靠该 PR 身份规则证明用了代理。[现行指标逐项定义](https://jellyfish.co/ai-engineering-trends/)

**反馈和交接。** 自用案例披露了一个可追查的行动链。测试自动化体验首次得分 26/100，工程负责人安排一名工程师投入两周，该工程师先询问同事的具体阻碍；2024 上半年再次调查，得分为 58/100。其问卷案例允许按团队或角色筛选匿名答卷，没有在该案例公布保证匿名的最小切片、同一批受访人比例或严格对照。产品提供线索，工程负责人决定投人，二次主观得分无法单独推算节省工时或确认质量提高。[调查与干预原例](https://jellyfish.co/blog/how-jellyfish-used-its-own-devex-tool-to-double-engineer-satisfaction-with-test-automation/) · [DevEx 产品页](https://jellyfish.co/platform/devex/)

**可证伪演示。** 同时导入人工开 PR/代理 commit、代理开 PR/人工 review、全程人工但通过聊天问答三种交付；要求按公司月、仓库与代理身份解释归类，并对照 PR 总数、厂商特定 factory 开启数及人工开启数。再选调查低分的一个团队，要求说明谁能看到小团队切片、如何记录负责人和复测日期，以及行动记录能否回连真实任务。未核实的是客户租户里的 RBAC、最小样本阈值和从评分直接创建任务的能力。

## LinearB：AI 归因的变化可能只来自阈值

**版本与反馈。** 2025-09-08 厂商宣布 MCP server、AI Insights 和 DevEx surveys。2026-10-21 公告将自定义选项、开放文本和 Slack 调查分发说明为当日可用，适用对象是已连接 Slack 的客户。可发给全组织、团队或指定个人，通过个人链接免登录作答，可仅提醒未答者；同一公告让 Teams 客户联系 CSM 核实。它证明系统能够追踪谁未完成，没有说明每条答案对所有管理者具名可见，隐私界面需实演。[初始公布](https://linearb.io/blog/introducing-the-next-chapter-AI-productivity) · [2026-10-21 调查更新](https://linearb.io/blog/surveys-enhancements)

**采集与分母。** 官方归因指南先逐开发者、逐 UTC 日计算 AI 接受行数 / 当日提交行数；达到默认 25% 时，该开发者当日的所有 commit 会标为 AI 辅助。第二层用 PR 内被标记 commit 的占比和可配置阈值给 PR 贴标。文档以 10% 举例，此处不把它写成系统默认。这不是逐行的代码来源鉴定；改阈值在代码未变时也能改变标签。Cycle Time 另用四个阶段：编码、等待首次评审、评审、部署；草稿先算编码，等待从提交评审到第一条非作者评论，无评论时可用批准或合并；启用 Jira 起算后，编码起点可变为事项进入 In Progress。必须保留数据源配置及所选时段，才知道跨队差异可能来自哪一步。[归因原文](https://linearb.helpdocs.io/article/wyb2trfd6o-configuring-ai-classification-thresholds) · [周期计算原文](https://linearb.helpdocs.io/article/0vif1ihmgc-how-is-cycle-time-calculated)

**干预与边界。** 厂商工作协议示例用 WorkerB 在 Slack/MS Teams 提醒团队有 PR 等待处理。它将工作队列里的对象交给团队；只凭通知无法确认谁接单、评审质量或延迟为何改变。个体对选定调查的回应与 PR 元数据应分开核验。采购现场可让团队先看到规律、约定响应窗口，再查看提醒和接单记录。[工作协议案例](https://linearb.io/blog/team-working-agreements)

**可证伪演示。** 提交同一开发者 UTC 当天的两条 commit，只有一条实际使用辅助工具，将接收/提交行数设置为 25/100；保持 PR 和提交不动，把 commit 阈值从 25% 调到 26%。核对标签、历史重新计算范围、导出结果和数据缺失分组。另给一条长时间无人评审的草稿，转为 ready 后让作者先留言，再让评审人留言，检查何时起算和何时停止提醒。本轮没有验证重算时延、审批者身份或 WorkerB 的当前授权和套餐。

## 把同一份输入交给三套规则

公开规则能够离线重放。设 30 日窗口，A、B 全月在组，C 在组 15 日；三人都已关联 SCM 并有合并历史。六个 PR 中五个已合并：两个由 A 于同一天人工提交，一个由 B 人工提交，一个全由代理完成，一个由 C 开启、包含代理 commit。第六个仍开着。A 当天共提交 100 行、AI 接受 25 行。假设用于排除 bot 的身份已正确映射。下表是按公开规则实现的**合成算例**，并非三个 SaaS 账户的运行结果。[固定输入](fixture.json) · [规则脚本](fixture.py) · [逐项结果](fixture-results.json)

|对同一输入提出的问题|结果|改变哪个条件能使它变化|
|---|---|---|
|DX 已合并的人类 PR / 开发者月|4/(1＋1＋0.5)＝**1.6**|C 入组日改到月初，分母变 3|
|Jellyfish，合并 PR 中有可识别代理参与|2/5＝**40%**|C 开的混合 PR 也算参与；若只认开启者，结果是 1/5|
|LinearB，两层阈值，无可识别机器人提交者的 PR 子集|PR 阈值固定为示例的 10%；人日阈值 25% 时 **2/3**，26% 时 **0/3**|两个均由 A 当天提交的 PR 连带翻转；另两个含机器人身份，单列为待演示分支|

同一组合成记录中，DX 算出每开发者月 1.6 个由人员开启且合并的 PR（4 / 2.5），Jellyfish 在 5 个已合并 PR 中识别出 2 个有代理参与。LinearB 的简化重放在 3 个无可识别机器人提交者的 PR 中，改变人日阈值可把达标数从 2 变成 0。第一个数衡量吞吐，后两个各按不同证据给 PR 分类。采购时要求供应商逐条导出分类、缺失和排除项，再判断负责人能否从一个异常值追到具体任务。

## 原件与复算

截至 2026-11-20。优先使用原厂申报、帮助文档、带日期的产品公告及厂商直接发布的研究，产品营销、客户/厂商自述和本研究算例分别标出。没有登录企业租户，未采集员工个人数据。部分 LinearB HelpDocs 当前抓取返回 403，但同一研究早先归档了相同 URL 的完整原厂原件；两份快照标题和 SHA-256 已再次核对。财务事实以年报 Note 7 为准。合成 fixture 从本目录运行 `python fixture.py`；运行 `python verify.py` 校验指标原文定位、证据与输入。复算只证明规则演示的内在一致性。[原始来源](sources.json) · [复用快照与定位](reused.json) · [采购演示的证据索引](claim-checks.json)
