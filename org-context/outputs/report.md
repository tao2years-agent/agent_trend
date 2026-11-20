# 面向企业软件研发的组织级上下文与团队记忆
## 一页决策摘要

**下周先拿十余个真实变更做一个判断：把维护者当时知道、仓内又不容易发现的一条验证要求，在开发者准备提交时递给他，他会不会多跑一个真正必要的检查？** 给每例设三个条件：原样 CLI、现有 CI/affected 提示、维护者挑好证据后在同一时刻递送。只有第三组改变动作并改善验收，才值得花钱自动提炼和检索。如果第三组也无增益，优先补测试或 CI。这里是试点建议，尚无企业内效果数据。

**以前想窄了两处。** 一是把共同理解想成共同拥有一份文档。在 34 次真实评审中，评审者需要先理解变更的目的和情境；在另一项 11 人工作现场观察中，开发者会向 Agent 问技术问题，却仍向同事寻求组织判断和共识。“谁有权确认这个例外”即使无法写成知识，也可以路由。二是把长期记住放在实时核验前面。库作者想知道下游如何使用、下游想知道升级会破坏什么；到发布现场，能改变动作的证据是**哪个消费版本已部署、这对版本是否验证过**。这类问题已有成熟的工程查询。[A06](https://arxiv.org/abs/2507.09637) [A14](https://arxiv.org/abs/2610.33588) [A12](https://doi.org/10.1145/2501585.2501586) [D14](https://docs.pact.io/pact_broker/can_i_deploy)

**近期投三条窄路。** 首选提交前补关键验证，第二是阻塞时找对确认人，第三是跨仓改接口时给出带版本的消费者证据。它们各有清晰动作：跑一项检查、得到一次有效裁决、推迟或拆分一次不兼容变更。第一条可以只用 Git 和 CI，第二条不用先建库，第三条严重度较高但受部署清单制约。团队索引、全量频道接入和全仓自动说明暂缓。产品团队应把“收到证据后改了哪一步”设为立项证据。

**最接近题目的负面证据来自两种上限实验。** SWE Context Bench 的 v1 在 99 个有关联的后续任务上，已知正确关联的摘要组解决率 34.34%，无经验组 26.26%，自由选摘要组 22.22%。v3 扩到 51 仓、376 个关联任务；在扩展集的 Codex 组合上，已知正确摘要的解决率从 22.60% 升至 23.94%，平均耗时从 349.41 秒变为 362.39 秒。不同模型和指标上的收益并不同步。[V04](https://arxiv.org/html/2602.08316v3) VibeMemBench 特意挑了参考求解器能从经验受益的任务，仍有 12 个系统/求解器组合中的 11 个未超过关闭记忆的基线。两项都是作者离线实验。它们支持先测“挑对后有没有用”，再测“能否挑对”，不能预测公司的收益。[A04](https://arxiv.org/abs/2602.08316) [A15](https://arxiv.org/abs/2609.23570)

**最接近落地的正面证据证明了可部署性。** SAP 部分团队的快照中，900 条贡献产生 1,144 条经策展的记忆，作者明确尚未测出下游编码效果。GitHub 在 2026-10-28 将 Copilot Memory 推到付费计划 GA，同日以预览方式推出 Dreaming，可对纳入版本控制的技能或指令提 PR。共享记忆已经进入现有产品；内部差异化更可能来自企业独有的验证证据、版本边界和裁决关系。后半句是研究推断。[A05](https://arxiv.org/abs/2608.00122) [D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/)

**投资闸口。** 十一月追踪首次正确定位、验证覆盖、维护者净耗时与返工。先证实人选证据有增量，再做选择器；自动选择只增加阅读与 token 时收缩成显式查询；现有测试、负责人目录或契约能低成本解决时就复用。任何扩大可见范围都单独验收。研究截止为 2026-11-18（上海），没有采集贵司私有材料。

## 从决策现场反推信息需求

下表是根据现场研究与产品机制构造的工作情境。第一列的动作可以观察和打点，例子用于设计试验，具体故障并非贵司实录。真实观察的范围和样本见论文表。

| 工作节点与协作尺度 | 此刻的人、问题与失败例 | 信息流、现有解法及剩余缺口 | 递送时刻与可观察后果 |
|---|---|---|---|
| 需求澄清，业务与模块组 | 新人把“撤回”实现成删除；客服语境要求保留交易轨迹 | 验收样例由业务方解释，测试夹具与领域符号由模块组确认；找不到时问业务方 | 在提方案时给一对正反例；看第一次定位和方案是否更改。只在启动时发词表容易略过。[A03](https://arxiv.org/abs/2602.05892) [A09](https://doi.org/10.1109/icse.2007.45) |
| 理解旧实现，同仓异人 | 开发者重提弃案，不清楚是架构禁令还是旧部署的临时限制 | 原 PR/ADR 能证明当时的理由，现环境决定理由是否仍成立，例外需有权人裁决 | 提议替代实现时并列两份证据；可直接复议，少走一次反复评审。[A06](https://arxiv.org/abs/2507.09637) [A53](https://www.sciencedirect.com/science/article/pii/S0950584916301707) |
| 改到同一接口，多人并行 | 两个PR各自测试通过，一个改序列化、另一个改变调用前提 | 开着的PR和分支是短期信号；先用平台通知；尚未推送的工作只可由本人选择共享 | 重叠升级为语义冲突才提示，合并即过期；统计需要协调与误报警各多少。[A47](https://doi.org/10.1023/A:1021271517844) [A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) |
| 编辑和验证，同仓多人 | 维护者知道旧租户必须跑迁移回放，新人只跑单元测试 | 先找测试和CI声明；缺的是业务边界与本次diff的对应，owner可补签 | 提交前展示缺口及命令；记录多跑了什么、结果、评审还要求什么。[A06](https://arxiv.org/abs/2507.09637) [A29](https://arxiv.org/abs/1810.05286) |
| 评审，熟人或跨组 | 评审者不清楚变更目标，花时间重建需求 | 对照需求原文、作者解释、现有断言；自动评论多会挤掉人问问题的机会 | 首次打开diff时给意图与未决项，作者有权补充，评审可拒绝；测往返和漏错。[A06](https://arxiv.org/abs/2507.09637) [A42](https://www.cabird.com/pubs/bacchelli2013eoc.pdf) |
| 发布，跨仓／平台依赖 | 主干已迁移但线上消费方尚未升级；把“仓里没有”当“线上没有” | 锁文件、部署清单、契约矩阵各回答不同问题；无可见消费者不等于无任何消费者 | 在移除字段或放行前提供版本对，阻塞时指向掌握部署状态的人。[A12](https://doi.org/10.1145/2501585.2501586) [D14](https://docs.pact.io/pact_broker/can_i_deploy) |
| 排障，跨环境、值班交班 | 上一班验证的是灰度，下一班用结论跳过生产检查 | 时间线、镜像、区域、已排除假设与原日志；普通复盘只在事后写 | 交接前保存失败重现实验，进入新环境自动标记需复核；统计重复探索和误排除。[A11](https://doi.org/10.1145/1753326.1753342) [A30](https://arxiv.org/abs/1703.01897) |
| 中断与接手，个人到团队 | 开发者回来找到最后的文件，却忘了下一处要查的符号 | IDE导航、CLI日志、任务指针和意图；只在同任务内短期保留 | 恢复时返回关键代码位置。跨人还要补“为何查它”和授权。[A11](https://doi.org/10.1145/1753326.1753342) |
| 上手与维护者交接，团队 | 新人不知找谁；最近提交者已调组 | 目录给正式owner，近期评审给经验线索，值班表给可联系的人；交接人确认继任 | 第一次确有阻塞时再路由；追踪专家净负担及一次有效答复。[A09](https://doi.org/10.1109/icse.2007.45) [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| 规范下发，组织到项目 | 集团要求留审计轨迹，分支有批准过的例外 | 组织发布者定义强制边界；项目可记录例外和到期日，执行交给测试或策略引擎 | 在相关操作前解释失败门禁；不能靠提示词承诺服从。[D13](https://coder.com/changelog/project-level-memory-for-coder-agents-in-239) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| Desktop、IM与云端切换 | 桌面选中一份工单仅供本次讨论，云Agent以服务身份运行，输出将去多人频道 | 显式附加标出处和期限；云端重取当前授权；频道受众含访客，可能比私聊广 | 在从私有界面切换到频道时重算输出许可；不确定时私返，用户明确选可分享材料。[D03](https://www.anthropic.com/news/introducing-claude-tag) [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) |

**一个可复核的工作流。** 假设支付库要去掉旧枚举值。需求单由产品负责人说明“新请求禁止旧值”，维护者能确认读路径仍需兼容；代码搜索会命中过时样例；某消费服务的生产镜像仍反序列化旧值。CLI解释需求时给验收正反例，编辑时给消费方固定修订，发布时查询部署矩阵。若最后组合未知，请服务负责人验证。把三种证据合成一句“已迁移”，会把可逆的代码改动变成难以回滚的协议切换。业务释义、代码事实、部署事实和批准在此分别由四方负责。[A12](https://doi.org/10.1145/2501585.2501586) [G04](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) [D14](https://docs.pact.io/pact_broker/can_i_deploy)

## 从题面之外发现的机会

以下均为研究者推断，给出发现路径和可否证的动作；没有把来源论文或产品说成已经验证这些设计。

- **先排查为何搜不到，再重新搜索（O11）。** Glean允许管理员分开诊断索引状态与指定用户的访问；Rovo在权限同步失鲜时隐藏来源。研发Agent可据可公开的状态决定稍后重试还是请有权人确认。若只显示“没有命中”，用户会继续无效换词。[D12](https://docs.glean.com/administration/search/access-verification) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/)
- **让旧决定随前提一起复议（O05）。** 架构知识综述说明记录理由有独立成本；企业检索基准把冲突设成独立题类。把历史否决绑到可检查的版本/成本条件，有变化时发起复议；成败看是否避免沿用已失效的禁令。[A53](https://www.sciencedirect.com/science/article/pii/S0950584916301707) [A08](https://arxiv.org/abs/2605.05253)
- **仅在第二次需求出现时请求贡献（O10）。** Answer Garden把未解问题路由给专家，答案可复用；SAP部署说明采集与策展会有大量无产出记录。按复发触发策展有机会让获益者和贡献者看到同一笔节省。代价是罕见但高风险知识需要单独通道。[A45](https://doi.org/10.1145/91478.91485) [A05](https://arxiv.org/abs/2608.00122) [A48](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/01/groupware-and-social-dynamics.pdf)
- **用代码位置和试验轨迹恢复被打断的思路（O09）。** CHI实验中自动线索提高任务成功率，记录的恢复首动作耗时并未显著改善。界面可以只重开当时的位置供人继续判断，短期、本地、到期删除。[A11](https://doi.org/10.1145/1753326.1753342)
- **显示没有被测试过的版本对（O14）。** Pact用已部署的消费方和提供方版本查验证矩阵。CLI可把未知组合送回发布人的下一步，缺口本身就是证据；有可靠的同等流水线提示时应直接链接它。[D14](https://docs.pact.io/pact_broker/can_i_deploy) [G06](https://github.com/pact-foundation/pact_broker/blob/6298abd2d4394e0255c944a9fbbc451402d766a6/lib/pact_broker/matrix/parse_query.rb)
- **只向真正使用过旧规则的地方传播撤销（O15）。** Copilot把停用与删除分开，Rovo明示访问同步延迟。推断为每次注入保留派生来源和版本，支持在下次消费时阻止旧副本。验证撤销后最后一次使用时间，同时核算追踪成本。[D18](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli/) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/)
- **先与同环境的历史失败比对，再决定是否改代码（O16）。** 生产测试选择依赖历史信号。可把已知环境故障和新代码差异分开显示，避免一次误归因让人改掉正确代码；最终由现有测试确认。[A29](https://arxiv.org/abs/1810.05286) [D15](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/)


## 产业演进与可复用的机制

**时间窗口。** 产业近十二个月按 2025-11-18 至 2026-11-18，最近三个月按 2026-08-18 至 2026-11-18。以下仅计有正式发布页的事件。附录中无发布日期的能力仅作截面比较。文档的最后修改、Git 提交时间和新功能上线各自记录。

| 发布日期 | 性质、状态及新增量 | 对内部产品意味着什么 |
|---|---|---|
| 2025-12-19 | Copilot Memory 向部分 Pro/Pro+ 用户早期开放。[D20](https://github.blog/changelog/2025-12-19-copilot-memory-early-access-for-pro-and-pro/) | 个人订阅早期可用不能外推为企业默认开通。 |
| 2026-01-15 | 仓库记忆进入公开预览；使用前对当前代码校验，仓库所有者可删除。[D17](https://github.blog/changelog/2026-01-15-agentic-memory-for-github-copilot-is-in-public-preview/) | “从哪来、还能不能用、谁能删”是同一生命周期的三次检查。 |
| 2026-04-02 | Rovo Dev 可在 Jira 内从工作项启动后台编码流程，返回供审查的 PR。[D21](https://www.atlassian.com/blog/announcements/rovo-dev-in-jira) | 工单原生入口可以省去手工搬运需求。需求仍有歧义时，挪动入口不能替人补足验收条件。 |
| 2026-05-26 | 新增仓级停用及更清楚的个人/仓库作用域提示；停用后已有事实保留。[D18](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli/) | 禁止读取、禁止新增、物理删除，应有不同验收用例。 |
| 2026-06-22 | Cursor 3.9 的 Team Marketplaces 增加从 GitLab、Bitbucket 或 Azure DevOps 导入插件仓的支持。[D22](https://cursor.com/changelog/customize) | 分发可复用资产已有渠道；分发量不说明某项技能被选中或改善了变更。 |
| 2026-06-23 | Claude Tag 在 Slack 向 Team/Enterprise 推出 beta；共享线程、身份和可访问频道由管理员配置。[D03](https://www.anthropic.com/news/introducing-claude-tag) | 同一频道接续工作降低重复说明成本，也改变回复受众。厂商内部使用量不证明净收益。 |
| 2026-08-13 | Claude Tag 的主动发言从单消息判断扩展到频道上下文、记忆和指令。**早于最近三个月起点五天**。[D16](https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room) | 负例“何时应保持沉默”值得进入主动提示评测。 |
| **2026-10-28** | **近三个月**。GitHub Copilot Memory 在付费计划 GA；Dreaming 为 public preview，可提议改已检入的技能/指令，并提供跨仓搜索入口。[D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/) | 已有持久化、后台整理和审查工作流。发布文中93%遵循偏好、42%工作流效率改善只来自被审阅且已用记忆的CLI会话；公开分母与随机对照不足。 |
| **2026-11-03** | **近三个月**。Coder 2.39 发布项目聊天共享记忆、指令与技能，以及可按组限制、带审计的组织技能和指令。[D13](https://coder.com/changelog/project-level-memory-for-coder-agents-in-239) | 平台团队能治理发布范围；本页没有对照实验说明开发者实际减少多少返工。 |

在两种已核验的近期增量中，GitHub 把**从历史工作提议变更**推到已有 PR 审查现场，Coder 把**谁能下发与共享**推到已有项目容器。两者解决的产品问题不同。季内没有可靠发布页的厂商不参与“无新增”判断。

### 重点方向如何贯穿运行时

| 方向 | 采集、提炼与校验 | 存储、选择、注入与精确回取 | 刷新、撤回、裁决与成本 |
|---|---|---|---|
| 验证缺口 | 读取当前diff、测试配置、CI结果及曾导致返工的授权评审；确定性解析命令/路径，模型只提匹配理由，维护者认可例外 | 存规则适用模块、环境、命令引用与来源SHA；提交事件按路径和依赖筛，先重用affected。显示“已跑/待跑”，点击获取原断言或作业；运行由用户或现有自动化发起 | 配置或调用图变更使关联待复核，过期条目静默退出；可忽略本次或提修订。主要成本是误报和维护者复核，服务端CI判定优先。[A29](https://arxiv.org/abs/1810.05286) [G05](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) |
| 专家与裁决 | 从目录、基准分支CODEOWNERS、工单裁决、值班表分别取证；确定性匹配角色，模型组织问题，owner确认谁有权答 | 最少存责任关系和有效期，实时查询在岗；阻塞者主动请求才展示“负责/近期处理过/可代理”及出处；给人草稿，不自动群发 | 转岗从目录撤销，申诉交团队管理员。重复问题若已可由测试回答则停止路由；量化专家收到的请求分钟与转派。[A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| 跨仓兼容 | 从服务目录、契约发布、部署记录、依赖引用获得版本边；静态发现待确认，契约执行提供实证，负责人确认例外 | 存版本对与验证ID，按目标环境、发行版本和调用方筛选；编辑时展示潜在影响，发布时查询实时矩阵。回取固定提交或指定作业，IAM随查询重验 | 新部署覆盖当前组合，旧组合保留历史时间；不明标未证。平台维护标识映射，消费方负责契约；目录缺项可能带来最高误判成本。[A12](https://doi.org/10.1145/2501585.2501586) [G04](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) [D14](https://docs.pact.io/pact_broker/can_i_deploy) |
| 旧决定与经验 | 原PR作者写清目的、反例、证据，模型把会话提为候选；只有授权维护者能升格项目约定 | 以问题、条件、证据ID、失效条件和作者为最小单位。索引词法/符号先行，必要时语义再排；在出现相同选择时给当前前提和原话入口。拒绝只剩总结的二次生成 | 相似任务再次出现才请求策展；原文删、前提变即停推，保留已撤回标识。可改、忽略或举报，评审后按稳定ID更新派生物。[A05](https://arxiv.org/abs/2608.00122) [A04](https://arxiv.org/abs/2602.08316) |
| 接力与排障 | 采集最后验证命令、返回码、工作树、未决假设；由交班者选交接项。模型写摘要，宿主保存原证据引用 | 任务私有短存；接手人从任务或工单进入，验证SHA、依赖、环境后才允许复用。长上下文压缩后用不可变blob、日志范围与哈希重新获取原材料 | 已合并/关闭即清理短期包。长寿经验另需可复现条件和复用证据；可复用来源只在其授权范围展示。跨设备追原日志和重建环境都有延迟。[A11](https://doi.org/10.1145/1753326.1753342) [A15](https://arxiv.org/abs/2609.23570) |
| 频道与权限 | 采集连接器授权及输出目的地，私聊材料保持来源标签。模型可做归纳；权限判断、成员变更和目的地检查由宿主执行 | 缓存键含租户、读取身份、来源版本、目的地与授权版本；检索前过滤，回取时再授权，发布前逐条验证派生物的可披露范围 | 频道出现访客或ACL不同步时暂停共享，退回私有响应；连接器管理员处理同步，作者有权撤回，缓存和任务快照也要失效。[D03](https://www.anthropic.com/news/introducing-claude-tag) [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) |

**三项判定独立执行。** 例如生产 A 服务的回退命令对当前问题可能相关，提问人能在值班群读到它，但当前任务在预发 B 环境。顺序可以先按租户和代理身份削减候选，再核对提交范围、模块、依赖与环境，最后比较语义；输出时按目的地重新检查。记录来源事实发生时间、被系统观察时间和适用区间，避免把新补录的旧故障当刚发生的故障。私人约定仅随其作者，共识前讨论带“待裁决”，发布约定需责任人和生效范围。跨两个模块的例外以条件交集表达，不把组织层的普通建议自动提升为硬门禁。

**七个消费入口的取舍（设计建议）。** 稳定且每题必用的短指令可作常驻前缀；重复请求或许能复用前缀缓存，但频繁编辑会破坏命中，具体以宿主账单计。按路径触发适合模块规约，有目录移动、通配符过宽和先编辑后触发的问题。模型主动发现只常驻索引，可能完全不点；工具检索适合跨仓或版本问题，多一次调用就有一次网络往返。Desktop显式附加适合人已选好的材料，可跳过召回，但需标明仅本次。提交、评审、部署事件适合成本较高而时点明确的检查，过早会刷屏。无人云任务需固定输入快照、执行身份和回调目的地；失去权限时将任务标为待确认。每次记录发现→读取→采纳三次时间戳、调用数、缓存读写/未缓存输入、输出与端到端耗时；不同厂商字段先保留原值再归一化。[D02](https://code.claude.com/docs/en/memory) [D05](https://cursor.com/docs/rules) [D07](https://docs.devin.ai/product-guides/knowledge) [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) [A03](https://arxiv.org/abs/2602.05892)

**区分这些机制，可以直接查五处证据。**

1. 分层文件只能证明存储组织。Gemini CLI 的JIT函数明确接收目标路径和已加载集合；Qwen Code的层级发现会组合内容，而Cursor规则中的文件引用还需工具读取。要证明“在这次编辑前注入”，得同时有触发事件、命中文档哈希、提交给模型的内容记录及宿主版本。[G01](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/utils/memoryDiscovery.ts) [G02](https://github.com/QwenLM/qwen-code/blob/a0ee2c0e75e11d18bb5e1821180147d9ad2167b6/packages/core/src/memory/memoryDiscovery.ts) [D05](https://cursor.com/docs/rules)
2. 在 Gemini CLI 可沿真正的读取路径继续追：read-file.ts 第216行把本次目标交给发现器；命中时分别追加到字符串或多模态工具结果的 llmContent。memoryContextManager.ts 第148行调用子目录发现函数。我们在 Bun 中直接执行固定提交的原版 jit-context.ts，注入受控管理器：验证目标和信任根传递、文本追加、空结果、多模态追加、管理器异常和缺失六种断言。测试通过。此实验仅覆盖适配函数；没有运行完整 CLI、文件发现与模型推理。[J02](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/read-file.ts) [J03](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/context/memoryContextManager.ts) [J01](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/jit-context.ts) [J05](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/jit-context.test.ts)
3. 部署库可以统计贡献和链接；开发者是否读到、是否因此改跑用例，则要到任务事件里找。SAP快照的1,144条不能作为采用率分母；GitHub公布的已用记忆会话也不能充当所有任务的基线。[A05](https://arxiv.org/abs/2608.00122) [D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/)
4. Slack检索是以具体身份执行，Tag还有频道/身份范围。面向频道的摘要能推断源文敏感内容；删除链接不足以解决。应分别检验私有读取、私有输出、共享输出和听众扩大后的旧缓存。[D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) [D03](https://www.anthropic.com/news/introducing-claude-tag) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/)
5. 接力摘要包含“这次做到哪”；可复用经验还要有将来如何匹配、何时不成立、谁能确认、哪个检查能重做。SWE Context Bench 的自由选摘要落后于无经验，就是未来任务选错对象的反例。[A04](https://arxiv.org/abs/2602.08316) [A11](https://doi.org/10.1145/1753326.1753342)

### 要不要让 Agent 做

**能把答案写成断言时，先做断言。** 类型/契约能拒绝接口形态错误；CI可强制跑关键验证；组织审批可交分支保护；目录能回答“谁负责”。这些机制确定、可复查，而且对不用 Agent 的人也生效。CodeAgent 的增量须落在缺口：在提交前早一步给命令、在跨仓时解释未验证组合、在没有唯一答案时帮人找到裁决者。给已强制检查再写一条常驻提醒，容易徒增 token。[D14](https://docs.pact.io/pact_broker/can_i_deploy) [G05](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) [A01](https://arxiv.org/abs/2602.11988)

**持久化要讲清付账的人。** 责任人稳定、多人重复用、仓内无法推回、失效可检测的例外适合入仓；谁正在改、哪个版本在线、当前能否发布适合即时查询；未成共识的判断存任务或线程并设到期日；个人试错一般留个人。对贡献者可预填证据与范围，返回“这条后来避免了哪次追问”，并提供一次撤回所有派生引用的入口。每月维护总分钟数若高于被避免的追问及返工分钟数，即使召回率很高也应停止扩张。[A45](https://doi.org/10.1145/91478.91485) [A48](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/01/groupware-and-social-dynamics.pdf) [A05](https://arxiv.org/abs/2608.00122)


## 哪些证据足以影响立项

**仓库里已有多少可用文档，会改变初始化的价值。** Gloaguen 等人的 v1 用 138 个已有人工说明的任务加 SWE-bench Lite 作对照。其 2026-09-29 的 v3 把重点表述为：文件里的具体要求大体能被遵循，但仓库概览通常没有加速找到相关文件。作者还有一个很重要的反事实：先生成概览，再人为移除仓内其他文档、示例和 docs 内容，此时生成文件平均带来约 2.7% 的改善（按作者措辞）。这说明应把“有无重复信息”作为变量。它没有证明在原本就缺乏文档的企业仓也能生成同样好的概览，因为实验生成时那些材料仍在。[A01](https://arxiv.org/abs/2602.11988) [V01](https://arxiv.org/html/2602.11988v3)

**快和对可以往不同方向走。** Lulla 等人的 124 个 PR 配对实验以耗时、输出 token 为主；三仓双 Agent 消融用隐藏测试判正确。后者有 288 次可判结果，但只有 17 个独立任务，且两个仓的按需资料比常驻大得多。把重复运行数当任务数，或把 Corpus 大小的差异算成加载方式的增益，都会让选择看似更有把握。内部试点应使用同字节内容、相同工具和调用上限，把正确率和人审时间同时留在结果表。[A61](https://arxiv.org/abs/2601.20404) [A02](https://arxiv.org/abs/2607.27250)

**给对信息和造出检索器是两笔投资。** SWE Context Bench 的 v1 在同一相关任务集合上给出了直给、自由选择、完整轨迹与摘要的对照；v3 的样本扩展到 1,100 个基础任务、376 个关联任务。VibeMemBench 更进一步，先筛出“某个求解器已能从历史获益”的目标，其他系统仍常拿不到净增益。前者说明选择器会消耗收益，后者说明即便题目有意偏向记忆有用，也不足以证明端到端产品有效。ContextBench 提供文件、代码块和行的金标，适合找丢失在哪一环。金标可用来裁判，不能交给生成器。[A03](https://arxiv.org/abs/2602.05892) [A04](https://arxiv.org/abs/2602.08316) [V04](https://arxiv.org/html/2602.08316v3) [A15](https://arxiv.org/abs/2609.23570)

**组织记忆的另一半在人与权责。** Ko 等人亲眼看到开发者因唯一知情者不在而切换任务；Haenni 等人的上下游受访者有方向相反的信息需求。Codebook 原型能把符号连到人、变更、讨论，受访者却希望不同团队使用不同排序。这说明统一“专家分”容易将熟悉度冒充责任边界。再结合 CSCW 的专业知识推荐、共同理解和贡献负担研究，O03应同时显示查询依据、角色和替代联系人；专家一句“我了解当年情况但没有批准权”本身就是高质量结果。[A09](https://doi.org/10.1109/icse.2007.45) [A12](https://doi.org/10.1145/2501585.2501586) [A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) [A50](https://www.cs.cmu.edu/~illah/CLASSDOCS/Clark91.pdf) [A48](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/01/groupware-and-social-dynamics.pdf)

**观察和部署比问卷多提供一层证据，仍需要结果对照。** SAP 的系统表明贡献→门控→入库→MCP 查询在部分团队能运转；其信任分没有按任务结果校准。CHI 中断恢复实验支持在任务切回时展示代码线索，但没有证明换人交接能复制收益。METR 的随机研究则发现有经验开发者的感知节省与实测耗时方向相反。以企业内“返工/维护者人时”作主结果，会比拿点赞或条目增长作代用指标更接近产品决策。[A05](https://arxiv.org/abs/2608.00122) [A11](https://doi.org/10.1145/1753326.1753342) [A07](https://arxiv.org/abs/2507.09089)

**先保留廉价基线。** EnterpriseRAG-Bench 的合成公司有冲突、近重复和缺答案题，其特定实现中词法检索在部分题型胜过向量。它不含贵司的身份边界、口头协商或真实维护成本。跨仓试点应先以 Git/Sourcegraph 的词法和符号检索、Backstage 目录或 Pact 矩阵作对照。若“人工选对证据”也不改变行动，换嵌入模型的优先级就很低。[A08](https://arxiv.org/abs/2605.05253) [D09](https://sourcegraph.com/docs/code-search/working/search-contexts) [G04](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) [D14](https://docs.pact.io/pact_broker/can_i_deploy)

**专家名单和落实责任是两种干预。** Meta 的一项现场 A/B 针对只分配给团队的评审，从排名前三的人中随机明确指派一人，TimeInReview 下降 11.6%，每个 diff 上评审者投入时间的护栏指标未发现显著变化。另一项平衡负载的试验结果混合。这给 O03 提供了比“专家推荐看上去准确”更近的证据。内部先用人确认的指派做试验，同时看等待与专家负担；不能把评审的降幅外推到跨组业务裁决。[A67](https://arxiv.org/abs/2312.17169)

### 阅读范围与证据标签

论文表中“正文复核”指检查与判断有关的方法、结果和局限章节；对部分 PDF 使用分页摘录，不等于逐字通读或独立复现。其余论文只登记书目/摘要和用途，不支持新的定量断言。未标为有对照的现场观察、部署自报和产品公开行为均不作因果解释。论文首次公开以可核的 arXiv v1 为准；仅有会议/期刊信息的记录标出版时间，更早作者稿未知。近三年内的修订不重计新论文。A04 v1 的比较数字仅用于该版实验，v3规模和新表另列；A01 v1 的 AGENTbench 在 v3 称 CTXbench。[A01](https://arxiv.org/abs/2602.11988) [V01](https://arxiv.org/html/2602.11988v3) [A04](https://arxiv.org/abs/2602.08316) [V04](https://arxiv.org/html/2602.08316v3)


## 产品取舍与十一月实验

### 排序与争议

| 投入位置 | 依次选择 | 为什么这样排；何时调整 |
|---|---|---|
| 近期CLI | **① O01 提交前补关键验证**，**② O03 阻塞时找能确认的人**，**③ O02 改接口前定位真实消费者** | ①频繁、紧贴已有动作，Git/CI可取且可盲评。②无需先沉淀，减少等待有直接价值，但问错人会转嫁成本。③单次后果更重，部署信息却常不齐；有成熟契约的团队可把它提到首位。 |
| 中长期差异化 | **① O05 随前提变化复议旧决定**，**② O15 按引用传播规则撤销**，**③ O12 按共享目的地裁切证据** | ①利用内部特有决策史；若作者不写前提，图谱也补不出来。②跨多个消费端后价值上升，依赖宿主记录派生关系。③对跨端团队重要，但要能处理外部成员和撤权；在仅本地单人CLI阶段只做必要边界。 |
| Demo容易高估 | **① O13 自动生成全仓说明**，**② O07 显示所有人的编辑动态**，**③ O04 为所有任务自动写长交接摘要** | ①生成成功与被采用相距最远，成本会跟着每次会话走。②信息新鲜但许多重叠无需沟通；注意力成本由同事承担。③若没有跨人/跨天恢复，摘要很快失效。三者都有窄场景，需以真实任务频率决定保留范围。 |

**一个反直觉的结论。** 即使能证明历史里有正确经验，也可能不值得建自动记忆产品。选择错误的代价包括执行更多检查、引入错误约束和维护者复核。能以更低成本消除同一失误的 CI 或契约应当胜出。会改变判断的证据是：在未经“经验有用”筛选的连续内部任务中，系统选取的经验持续接近人工直给的收益；收益延伸到第二位开发者，扣除策展和错用成本仍为正。[A04](https://arxiv.org/abs/2602.08316) [A15](https://arxiv.org/abs/2609.23570) [A01](https://arxiv.org/abs/2602.11988)

**对原候选的回评。** 团队知识库适合“反复出现、仓内找不到且可裁决”的小类问题，先以 O10 检验供需。频道记忆适合跨人未决讨论的短期延续，先做 O12 目的地检查，私聊观察不得直接升级组织规范。路径规则对已知模块验证和例外很有用，但业务词跨模块时容易失配。任务接力优先 O04 的可复跑证据包，拿 O09 的本地恢复线索作低成本对照。项目初始化 Skill 在 O01 证实有材料可沉淀时可作为作者工具；独立优先级低于 O01、O03、O02。[D03](https://www.anthropic.com/news/introducing-claude-tag) [D05](https://cursor.com/docs/rules) [A11](https://doi.org/10.1145/1753326.1753342) [A01](https://arxiv.org/abs/2602.11988)

### 实验共用的观察与隔离方法

以下规模、阈值和人日均是**试点设计假设**，不代表公司已有基线。第一天抽近期连续任务按场景标记适用率，再选择对应难度的实验样本；两者分别报告，避免用富集样本推算全员ROI。基线收集最近一次实际命令、等待专家和评审返工的分布，若无可靠日志，当场记录5次普通流程再启动对照。按任务、熟悉度及模块分层配对，分开报告人和无人Agent，固定模型、预算、工具权限、机器、依赖与缓存状态。一人不重复看到同题答案；同题离线多次运行按任务聚类，报告任务差值、负例与不确定范围，小样本不宣称统计定论。

| 漏斗 | 可核验记录 | 常见错算 |
|---|---|---|
| ①信息存在 | owner事先登记可用来源、当时版本、谁可读；另列无答案任务 | 把后来写的复盘算进覆盖 |
| ②召回命中 | 对当时有权看的来源，记录候选ID、排名、版本以及该场景的必要证据 | 用关键词或文件命中代替段落正确 |
| ③实际读到 | 宿主确认正文或证据片段已送入模型输入；人端分开记录展开和能否复述，不以曝光代替理解 | 文件存在、工具返回句柄、UI展示标题 |
| ④实际采用 | 预先定义可观测动作：换文件、增跑用例、转交正确owner、申请验证或延后发布；用trace/录屏和当事人简短核对 | Agent说“已采纳”但命令与基线相同 |
| ⑤最终完成 | 独立盲评验收、最终测试、完成时间、返工轮次；同时计维护者时间、错误拒答/披露、过期误用 | 生成PR、测试全绿或用户点赞单独记成功 |

每次诊断分解为“没材料／没选对／送达太晚／看了没改动作／改动作却没改善结果”。记录任务开始到首次正确定位、关键验证分子/分母、发起追问次数和回答者分钟数、误报数、端到端 P50/逐例长尾、工具调用、模型/宿主版本、cached input、cache write（若有）、uncached input、output。缺字段标“不可观测”；不把 cached token 重计入未缓存成本。正确定位由盲评者按预先定义的可接受文件/符号集合判定，可补录不同但正确的路线。

**防止未来信息泄漏。** 为每题设截止时刻 T 和各仓 base SHA；只交付由该提交导出的源码树或仅含祖先的隔离仓，不能直接把含未来对象、远程分支和remotes的完整克隆交给 Agent。连接器只返回截至 T 已存在且当时可见的版本；不能回放历史权限时用人工脱敏快照。CI历史、文档编辑史、训练示例、上下游部署、记忆索引、提示词与缓存均按 T 切片，每臂清空派生缓存或显式控制热缓存。最终修复、合入后的PR评论、新增隐藏测试和金标由独立裁判隔离。由红队式数据复核员抽查输入包，直接搜索最终提交号、答案独有字符串和后发工单；命中则作废并重建。预训练污染无法完全排除，优先用私有、前瞻任务。没有跨仓历史快照的案例不用于因果比较。

### E1　单仓多人，验证提示能否少一次评审返工

- **假设与人群。** 同仓不同作者反复漏掉同类业务验证，现有CI没有在提交前告诉他们应该加哪一个检查。选一仓、2位维护者、4–6位开发者。先看连续20项变更，区分没有问题、已有门禁和确实漏验；回放约12道有代表性的任务，含无需额外测试的负例。
- **最小实现与对照。** 1–2工程人日，另计维护者标注。只需基准源码、CI定义、历史日志和维护者能指认的证据。CLI提交前显示一条提示。A原样工具；B同一时点给现有CI/affected链接；C在B基础上人工选一条带证据的必要检查。另记录若把同一规则写入CI，谁受益、需多少维护时间。
- **埋点与判定。** 逐题保存实际命令、运行结果、未跑原因、盲评必要检查覆盖和返工分钟；不因多跑一百项就多得分。试点信号是在至少3个不同任务**相较B**新增必要动作，并减少后续请求或发现真实问题，且误报的额外时间小于挽回的时间。C无优势就停止自动检索；若单条确定性规则能覆盖全部有效例，转做CI。若C有优势，再用最简单的路径匹配替代人工选取并重测。[G05](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) [A29](https://arxiv.org/abs/1810.05286) [A06](https://arxiv.org/abs/2507.09637)

### E2　跨仓接口，真实部署版本能否改变迁移顺序

- **假设与人群。** 平台owner和两个消费组对影响范围的误判来自版本与环境缺失。选一生产者、两个消费者、各一名有权限维护者，准备6–10个字段/端点迁移案例，包含静态匹配但未部署、已部署但主干已迁移、查不到契约三类。
- **最小实现与对照。** 2–4工程人日，需只读部署清单、Git修订和现有Pact或一张人工验证表；不用构建全组织图。A按仓搜索+直接问人，B调用现有契约/服务目录，C把B的同一结果在删接口前送入CLI并链接原始版本。三组均允许询问团队；人工记录金标只给裁判。
- **埋点与判定。** 比较实际迁移计划、首次找到有效消费者用时、确证/未知/误报、追问分钟和是否放行不兼容版本。试点信号是至少两项决策被正确改序或补验且对假阳性仍按原计划；任何把未知标为可发布的结果都停止推送确定结论。若大多数案例查不到部署版本，先治理标识；若B与C一样快，保留平台查询入口。[A12](https://doi.org/10.1145/2501585.2501586) [D14](https://docs.pact.io/pact_broker/can_i_deploy) [D09](https://sourcegraph.com/docs/code-search/working/search-contexts)

### E3　零知识库，给阻塞问题找一位有资格确认的人

- **假设与人群。** 一部分等待来自找错角色，缩短首个有效答复时间不需要保存答复正文。两个组各选一位轮值负责人，征集约12个自然发生的问题，分别标注知识咨询和需要授权的例外。维持原沟通渠道。
- **最小实现与对照。** 0.5–1工程人日；当前CODEOWNERS、目录和值班表足够。A原样问人，B按CODEOWNERS，C再按“了解/负责/有权批准”区分并给一个问题草稿；开发者自行决定是否联系。槽位轮换或按难度配对，同一问题不发给三个人。
- **埋点与判定。** 记录转派、响应时区、首个有效确认、最终是否采用、专家净耗时及被打扰者数；仅存任务ID、角色及时间。试点信号是重复可见的转派减少且总等待和专家负担同向下降。若目录本身过时或同一人过载，改轮值与目录流程；若复发问题占比很低，关闭事后沉淀。[A09](https://doi.org/10.1109/icse.2007.45) [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

### E4　初始化 Skill，有效的是内容、加载时点，还是都没有

- **假设与人群。** 一个陌生仓库中，维护者能指出少数代码/CI推导不出的例外；只有在相关任务里递给第二位开发者才有增量。选两个不同规范成熟度的仓、各2名维护者、4–6名非原作者。约12–16个任务，包含例外生效、同路径无关、分支不适用、文档过期四类。
- **最小实现与对照。** 2–3工程人日。Skill只读扫描，生成可审阅的短索引与最多3条候选，维护者可全部拒绝。先比较 A 原仓、B 默认自动生成的说明、C 人工核准例外（三者统一投递时点）；再仅用C的完全同字节内容，对比常驻、按路径、显式查询。冻结源码，独立记录构建提示词预算和日后每会话成本。检查第二人及新进程的实际输入；插入过期、删除、改名、嵌套路径等负例。
- **埋点与判定。** 记录不同作者能否读到同一有效版本、每条建议阅读/采用/拒绝、首定位、隐藏验收、维护者写审时间及四类token。试点继续条件是至少两个独立作者在不同题中复用独有约束并改善验收，扣除维护成本后仍有收益。若只有验证例外有效，缩成O01的策展Skill；若人工直给也无效，停止初始化投资。若人工有效但正常CLI没加载，修宿主再测，不能算内容失败。[A01](https://arxiv.org/abs/2602.11988) [A02](https://arxiv.org/abs/2607.27250) [A61](https://arxiv.org/abs/2601.20404)

### 初始化 Skill 的产品边界

| 能完全在 Skill 内试的部分 | 取决于 CLI、连接器或平台的部分 |
|---|---|
| 发现仓库现有README、测试、路径规范，列重复或互相矛盾的候选；询问维护者“上次让新人返工的是哪条”；输出可审diff、证据锚点、适用条件与删除建议。借Git评审和版本史落盘。 | 哪一轮、哪条路径实际触发；不同身份或云任务是否可读；提交给模型多少字节；同文件去重、截断、压缩后的原文定位、缓存命中、错误传播和撤权。文件被提交不承诺下一会话读取。 |
| 在命令里主动打开指定证据、生成带SHA的引用；人工更新或删除候选。可先用已有Git权限与PR审查。 | 自动跨分支/跨仓匹配，实时部署或并行变更发现，区分读者与输出受众，组织强制政策和正式门禁、审计和撤销派生缓存。 |

**问题面有边界。** 适合低频变动、能由项目owner裁决、同仓多人复用的知识，尤其是无法从代码推回的验证例外；缺少贵司真实任务分布，无法诚实给覆盖百分比。用“连续任务中确有非显然且仍有效的共享事实数 / 连续任务总数”估覆盖上限，再乘实际送达率与改变动作率，逐项报告分母。首次安装者觉得写得好、用文件里刚写过的问答测试、用新主干回放旧任务、让作者自己证明有用、只看减少输入token，这五种做法都可能伪验证。若需要的主要是实时部署或权威裁决，转O02/O03比加长Wiki合算。

**时间安排（建议）。** 11月19–20日确定T、冻结基线、完成盲标和数据可用性检查；11月23–27日并行运行E1、E2、E3，E4独立在另一批任务执行；11月30日对负例、净成本与权限异常逐题复盘。中期用4–8周在第二个团队前瞻复验，才扩到轻量选择器和证据版本管理。长期只有在跨范围复用已被证明且撤销可测时再做组织级索引、频道协作与云端投递。首周的最便宜淘汰器是E1的人选证据对照；一个方向失败，不妨碍其他实验独立成立。


## 检索台账、证据等级与待解问题

**执行口径。** 2026-11-18，Asia/Shanghai。插件目录未返回指定的 Deep Research 连接器，本研究由当前会话直接检索、下载、比对和编译。研究范围是企业研发决策中可改变动作的信息流。先查综述及真实研发工作，再查相邻行业机制、当期产品、基准和反例，最后评价题面中的候选。没有进入公司私有仓、聊天或真实企业账号。输出是一份定向证据综述；公开来源、英语资料和能获得全文的工作有选择偏差。

**语料与筛选。** 入口包括出版方、作者实验室、会议程序、arXiv、Crossref、GitHub API、厂商指南和正式发布记录。以“谁缺什么、何时行动、能观察什么结果”为纳入条件；目录只在有具体所有权语义时纳入，搜索只在有版本、权限或实时交付机制时纳入。经典文献用于构造人与团队问题，近三年文献用于检查代理行为、检索质量和真实部署。不将论文续版、翻译、厂商营销转述或相同产品的多个客户端重复计数。检索结果混入的理财新闻、百科、论坛体验、泛办公平台、没有研发工作流的通用多Agent榜单，以及仅复述论文的镜像均未作为核心证据。出处冲突不消除原记录。

**引用追踪，实际核对的边。** 由评审和架构知识综述确立“知识转移/理由”两组检索词；沿 A12 §2 的后向引用核对 A09、A10、A41，发现同仓与生态上下游需求的差异。沿 A03 §2 回查 SWE-bench、SWE-PolyBench、SWE-bench Pro 的题源；沿 A02 引言的明确引用从 A01、A61 向前追到同一双 Agent 消融，再检查 A01 最新版以避免过度解读早期数据。该路径是有记录的引文链，未声称遍历所有引用者。ASE/ISSTA补齐测试选择，TSE补齐维护中信息觅食，TOSEM补齐评审者负载，CSCW/CHI补齐贡献激励、共同理解与中断；不能据会议名推断部署效果。[A12](https://doi.org/10.1145/2501585.2501586) [A03](https://arxiv.org/abs/2602.05892) [A02](https://arxiv.org/abs/2607.27250) [A54](https://conf.researchr.org/details/ase-2024/ase-2024-research/125/Hybrid-Regression-Test-Selection-by-Integrating-File-and-Method-Dependences) [A55](https://conf.researchr.org/details/issta-2020/issta-2020-papers/14/Dependent-Test-Aware-Regression-Testing-Techniques) [A56](https://doi.org/10.1109/TSE.2006.116) [A67](https://arxiv.org/abs/2312.17169)

**保留了会改变解读的差异。** ①初始化文件的效率、正确率与有无已有文档分别记录。②允许分享、可以读取、可以公开发言分别验证。③官方当前文档的更新时间未知时写“未核”，不从抓取时间构造首发。④“发布/预览”“厂商自用或选定会话”“独立任务对照”“本研究实测”分列。⑤闭源实现以公开描述为上限；开源代码按固定提交解释；单测只阅读，未执行。⑥模型摘要、编码机密和我方研究推断都不具有组织裁决效力。

**已执行的本地运行验证。** Git 2.47.1.windows.1，两次合成提交。检出旧提交后，给定后续对象ID仍能读出后续答案；从旧提交导出的tar中只包含旧版rule.txt，没有Git对象。两项断言均通过。这个反例支持实验隔离设计，并未测量Agent品质、连接器权限或真实用户收益。HTML渲染验证单独记入研究状态。

**待解问题和证据缺口。**

1. 贵司连续任务中，有多少确实被“仓内推不出的信息”阻塞？按成熟度、任职时长、产品线、任务类型分母统计，避免只收失败故事。
2. 知道验证要求后，已有门禁是否已经以足够低的代价兜底？分别核算提前发现与事后修复的净时间。
3. 权限变化何时传到派生摘要、模型输入、日志和共享回复？公开文档不足以证明贵司多连接器组合的传播上界。用合成身份和受众矩阵验证。
4. 小组策展能否持续一个季度、原owner离开后谁接手？当前部署快照无法给出长期净收益、专家负载、公平性或失效清理的人力曲线。
5. 路径触发、冷/热缓存、压缩后回取是否在自家CLI和云宿主表现一致？本研究没有运行竞品端到端，也没有内部基线。
6. 当“未找到调用者”只是来源覆盖不全时，怎样既不泄露隐藏仓存在，又能表达不确定性？需平台团队和安全团队共同验收；静态分析也无法穷尽动态消费者。

**维护方式。** 每次刷新先新建日期目录保存原始字节及哈希，或保存带查询参数的浏览摘录；失败不冒充原始网页。再以稳定ID合并证据，更新裁决与阅读卡，重新生成报告及离线版。原始材料存于本地，外发报告应自行决定是否附证据包；本研究未发布或上传。


**本轮覆盖。** 论文候选 67，核准 62，其中正文复核 17，其余索引 45。产业表 21 行，GitHub CODEOWNERS 与 Copilot 合并按同一平台计为 20 个产品或项目。固定提交源码复核 7 个项目。机会 16 个，实验 4 个。Gemini CLI 的 JIT 适配函数已在受控条件下执行；竞品端到端运行 0，内部用户实验 0。

## 产业机制对照表

| 产品 / 项目 | 使用现场和行为 | 选择与边界 | 对内部产品的判断、来源 |
| --- | --- | --- | --- |
| Codex | CLI在项目目录发现指令，以预算拼接；评审可固定一份指令快照。 | 固定版本的发现器按候选目录取文件并受剩余字节数限制；刷新管理器串行更新。集成测试包含同一轮工具之后更新全局指令的场景。 | 实验要记实际内容哈希、被截断字节和载入事件；只记文件存在解释不了行为。 [D01](https://developers.openai.com/codex/guides/agents-md) [C01](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/src/agents_md.rs) [C02](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/src/agents_md_manager.rs) [C03](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/tests/suite/agents_md_refresh.rs) |
| Claude Code | 进入项目与从会话目录深入读取文件是不同事件。 | 子目录CLAUDE.md可随读取加载，终端显示Loaded路径；路径限定的规则也受按需加载预算约束。指令冲突仍可能出现。 | CLI应支持显示“何时因何加载”；把人可看懂的目录树当载入证明会误判。 [D02](https://code.claude.com/docs/en/memory) |
| Claude Tag | Slack频道中多人可接续同一线程，管理员配置Agent身份、来源和工具；DM可用个人连接。 | 初版描述有身份和频道范围；2026-08-13增强主动介入的上下文。可达渠道、发言判断和分享许可是三件事。 | 适合观察等待确认的线程。插件读取个人连接后向频道复述，需要另审目的地可见性。 [D03](https://www.anthropic.com/news/introducing-claude-tag) [D16](https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room) |
| GitHub Copilot | 从仓库记忆预览演进到付费计划GA；Dreaming预览可为受版本控制的指令和Skill提PR。 | 一月记录使用前对照当前代码；五月加入仓库停用开关，停用保留旧记录，个人偏好独立。 | 提议→人审与直接写入可变记忆两条生命周期；已有GitHub场景宜测试挂接现有能力。 [D20](https://github.blog/changelog/2025-12-19-copilot-memory-early-access-for-pro-and-pro/) [D17](https://github.blog/changelog/2026-01-15-agentic-memory-for-github-copilot-is-in-public-preview/) [D18](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli/) [D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/) |
| Cursor | IDE、CLI、Cloud Agents可按规则选择上下文，规则中的文件引用可让Agent另行读取。 | 项目.mdc的globs、description、alwaysApply控制选择；已引用的文件内容未必已内联。团队规则可用glob。 | 目录、规则体和第二跳文件分别埋点；没有读第二跳时给用户显式附加入口。 [D05](https://cursor.com/docs/rules) |
| Qoder | Repo Wiki生成项目说明，可导出到.qoder/repowiki。 | 代码变化可提示局部更新，Git目录手改后可Sync。文档描述启用与增量更新选项。 | 可复用可读的入口和增量更新交互；这份文档未给编辑决策中被采纳的频率。 [D06](https://docs.qoder.com/user-guide/repo-wiki) |
| Devin | 云端会话从组织共享Knowledge中选条目；支持按文件夹启停。 | trigger帮助检索，选中后读取整条，建议按单一工作流拆小。 | 把“目录用来管理”与“运行时逐条检索”分别验证；任务结束时提供停用过期条目的入口。 [D07](https://docs.devin.ai/product-guides/knowledge) |
| OpenHands | SDK区分仓库说明、知识与任务技能。 | 设计文档中KeywordTrigger匹配用户消息，TaskTrigger还能带用户输入；关键词命中与语义适用度有差距。 | 可廉价复现触发，需专门测同义表达、负例及仅在代码中出现的符号。 [D08](https://github.com/OpenHands/docs/blob/main/sdk/arch/skill.mdx) |
| Gemini CLI | 在已信任根下针对目标路径发现子目录上下文。 | loadJitSubdirectoryMemory选择包含目标的最深信任根，向上查找，以Git根或信任根为界并按文件身份去重；测试覆盖根外跳过。 | read-file会将命中内容追加到本次工具结果；受控试验只执行适配函数。不同工具、模型是否采用仍需分别测。 [G01](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/utils/memoryDiscovery.ts) [J02](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/read-file.ts) [J01](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/jit-context.ts) |
| Qwen Code | 分层指令可组合进会话；另有项目本地QWEN.local.md。 | 当前源码在启用隐式发现、可信目录且找到项目根时才加入本地文件；规范身份去重；有符号链接与不可信目录测试。 | 同一仓库中个人补充与共享规范可相异；排查两位同事行为差异时应显示来源。 [G02](https://github.com/QwenLM/qwen-code/blob/a0ee2c0e75e11d18bb5e1821180147d9ad2167b6/packages/core/src/memory/memoryDiscovery.ts) |
| aider | 在聊天预算内生成仓库符号地图。 | 以定义、引用构图，加权PageRank后按预算选内容；当前谈话中的文件/名称可影响排序。 | 对陌生仓定位的廉价基线；符号相关性不能回答弃案原因。 [G03](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py) |
| Backstage | 组件、API、组等目录实体产出所有权和依赖关系。 | 处理器从spec.owner、consumesApis、providesApis等发出有向边及其逆边。标注遗漏会让图不完整。 | 接现有服务目录查询责任人；owner元数据不等于上线批准或实时在岗。 [G04](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) |
| Nx | 开发者根据diff找affected项目。 | filterAffected先定位触及项目，再反向遍历依赖图；测试含项目配置删除时全部受影响及可关闭回退。 | 在已建模的monorepo优先运行原命令。图外动态调用和未声明依赖另找证据。 [G05](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) |
| Pact Broker | 发布前查询特定消费方、提供方版本及目标环境的验证记录。 | 矩阵查询解析器接收环境、分支、版本；官方例子要求记录部署版本。单有契约文件不足以回答“能否发到生产”。 | 把缺验证的组合和命令带回CLI；正式门禁仍由流水线执行，缺结果不能当通过。 [G06](https://github.com/pact-foundation/pact_broker/blob/6298abd2d4394e0255c944a9fbbc451402d766a6/lib/pact_broker/matrix/parse_query.rb) [D14](https://docs.pact.io/pact_broker/can_i_deploy) |
| Sourcegraph | Search Contexts可把一组仓和修订版本作为检索边界。 | 固定修订减少跨版本误读；搜到代码代表指定集合中存在静态匹配，未证明已部署。 | 跨仓实验可先保存现成查询，对照任务基准SHA。 [D09](https://sourcegraph.com/docs/code-search/working/search-contexts) |
| Slack | Real-time Search API在用户交互时查询消息和文件。 | 应用范围与用户授权共同约束；访问私有会话或从Slack外查询需要用户令牌。 | 支持“不落库，问时查”；查询主体的结果还需按输出线程的受众裁切。 [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) |
| Atlassian Rovo | 连接器将权限同步到搜索、聊天与Agent消费面。 | 官方文档说明同步超出连接器新鲜度窗口会隐藏该来源；Salesforce例外，按查询验权。 | 撤权滞后是可测失败条件；可以降级为请用户打开原文。 [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) |
| Glean | 管理员可用Document lookup区分文档是否已索引、指定同事能否访问。 | 内容抓取、群组身份、权限同步可能分别延迟。访问诊断不能授予新权限。 | 给服务台一个“为什么我看不到”的诊断入口，避免Agent为缺失内容编理由。 [D12](https://docs.glean.com/administration/search/access-verification) |
| Coder | 2.39支持以项目组织聊天，项目共享记忆、指令和技能。 | 管理员发布组织级指令与技能，可限定组并记录修改审计。 | 组织下发、项目共享会话各自有作者与撤销路径；未见任务质量对照。 [D13](https://coder.com/changelog/project-level-memory-for-coder-agents-in-239) |
| Meta Predictive Test Selection | 代码提交触发预测测试选择，服务于持续集成。 | 用历史执行和变更预测哪些测试会失败，并监控漏选；部署报告属于特定测试基础设施。 | 已有稳定选择器时优先调用，只有补到遗漏的业务验证才形成Agent增量。 [D15](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/) [A29](https://arxiv.org/abs/1810.05286) |
| GitHub CODEOWNERS | PR按基准分支上的路径规则请求评审。 | 受保护分支可配置必须通过代码所有者审批；修改频率和所有权是两种数据。 | 先给当前路径的正式负责人，再列熟悉该问题的人，分别注明依据。 [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |

## 学术证据详表

| 论文与正文定位 | 方法、样本与基线 | 作者结果 | 局限与迁移边界 |
| --- | --- | --- | --- |
| [A09](https://doi.org/10.1109/icse.2007.45) Information Needs in Collocated Software Development Teams · ICSE 2007 §3–6 [正文](https://www.microsoft.com/en-us/research/uploads/prod/2007/05/icse07_ko.pdf) [本地证据](../raw/web/field-measure.txt) | 现场观察微软17名开发者、约25小时，按分钟标记活动和提问；无干预组。 | 知道同事正在做什么、某行为为何发生，常要靠具体的人；人不在会搁置任务。 | 单公司、短时同地观察。内部应记录阻塞分钟及绕行，不能沿用其发生率。 |
| [A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) Codebook: Discovering and Exploiting Relationships in Software Repositories · §3–5；Hoozizat、Deep Intellisense [正文](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) [本地证据](../raw/web/field-measure.txt) | 代码符号、工作项、变更和人建图；Hoozizat访谈14名工程人员，另一原型结合5名开发与测试人员参与设计。 | 点击符号可追到修改与讨论；不同团队希望不同排序。9/14强烈认可Hoozizat。 | 原型接受度和演示；没有减少等待的对照。贡献者、当前专家和授权人应分开呈现。 |
| [A11](https://doi.org/10.1145/1753326.1753342) Evaluating cues for resuming interrupted programming tasks · CHI 2010 pp.1、6–9 [正文](https://chrisparnin.me/pdf/cues-chi09.pdf) [本地证据](../raw/sources/2026-11-18/F11.pdf) | 371人问卷；实验中14名受试者，用笔记、符号树或按时序的代码片段恢复任务。 | 两种自动提示的任务成功率约为仅用笔记的两倍；恢复首动作耗时差异不显著。 | 短时实验且样本小；换人接手需要补意图与权限。不能将成功率倍数换算为提速倍数。 |
| [A12](https://doi.org/10.1145/2501585.2501586) Categorizing developer information needs in software ecosystems · §3、4.1、4.2、5 [正文](https://scg.unibe.ch/archive/papers/Haen13a-EcosystemInformationNeeds.pdf) [本地证据](../raw/sources/2026-11-18/F12.pdf) | 14份便利样本答复，上下游角色分问，开放和轴心编码，无基线。 | 上游想知道谁怎样使用库，下游用邮件列表、仓库动态、示例和教程判断改动影响。 | 活跃生态开发者的描述。可迁移到依赖图补充真实调用与部署，无法证明自动通知有效。 |
| [A01](https://arxiv.org/abs/2602.11988) Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? · §3–5、表1–2、图3 [正文](https://arxiv.org/html/2602.11988v1) [本地证据](../raw/sources/2026-11-18/F01.html) | AGENTbench 从12个有人工文件的Python仓抽138题，另有SWE-bench Lite 300题；无文件、工具默认生成、已有人工文件。 | 生成文件在8个设置中5个降低解决率；表2中生成组相对无文件成本平均增加20%与23%（两个基准）。人工文件在作者总体概括中有小幅收益。 | 只在有文件的数据上有人工臂；测试覆盖有限，领域约束未必进入金标。先查成本增加是否换来上线必要验证。 |
| [A61](https://arxiv.org/abs/2601.20404) On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents · §III–V；配对设计与未来工作 [正文](https://arxiv.org/html/2601.20404v1) [本地证据](../raw/sources/2026-11-18/F16.html) | 10仓124个PR，有/无该提交时已有的AGENTS.md；计时、输出token。 | 中位耗时下降28.64%，输出token下降16.58%。 | 未按补丁正确性和维护质量独立评分。与A01指标不同，不能用其数字预测内部节省。 |
| [A02](https://arxiv.org/abs/2607.27250) Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories · §3.1–3.3、4、限制 [正文](https://arxiv.org/html/2607.27250v1) [本地证据](../raw/sources/2026-11-18/F02.html) | 3仓17题，两种Agent，无/常驻/选择三组各重复3次；288次有隐藏测试结果。 | 未测出正确率差异，作者等效界约10或15个百分点；错误多为实现与接线。 | 任务数小，两个仓的按需语料比常驻大约10倍和18倍，题目难度筛选偏向一款Agent。不能解读为策略严格等价。 |
| [A03](https://arxiv.org/abs/2602.05892) ContextBench: A Benchmark for Context Retrieval in Coding Agents · §2–4；文件/块/行级指标 [正文](https://arxiv.org/html/2602.05892v1) [本地证据](../raw/sources/2026-11-18/F03.html) | 66仓8语言1,136题，半自动生成并由专家复核金标；比较5种Agent、4个模型。 | 探索到与实际使用的代码存在落差；召回偏高而精度不足，更复杂宿主没有稳定领先。 | 金标预知最终补丁，只能作裁判；可能漏掉另一条正确思路。内部再加动作和开发者评价。 |
| [A04](https://arxiv.org/abs/2602.08316) SWE Context Bench: A Benchmark for Context Learning in Coding · §2.3、3；Resolved 与成本表 [正文](https://arxiv.org/html/2602.08316v1) [本地证据](../raw/sources/2026-11-18/F04.html) | 300个基础任务外接99个关联任务，5组比较无经验、自由选/已知正确关联×轨迹/摘要。 | 无经验26.26%解决，已知正确摘要34.34%，自由选摘要22.22%；自由选完整轨迹26.26%。 | 这是构造的有关联序列，真实待办的重复比例未知。优先测可用知识上限，再测选择损失。 |
| [A15](https://arxiv.org/abs/2609.23570) VibeMemBench: Evaluating Memory Systems for Coding Agents on Real Repository Coding Tasks · 目标筛选、held-out solver、系统比较 [正文](https://arxiv.org/html/2609.23570v1) [本地证据](../raw/sources/2026-11-18/F15.html) | 90仓111个目标、3,634条历史轨迹；预选出参考求解器受益的目标，再用5个留出求解器测试。 | 直接给已验证记录时4个求解器提高1.1–4.5个百分点；12种系统/求解器配对中11种未超过关记忆基线。 | 富集可受益任务，不能估普通任务收益。人工直给与系统检索必须同测。 |
| [A05](https://arxiv.org/abs/2608.00122) Shared Organizational Memory for Enterprise Coding Agents: System Design and Deployment Snapshot · §3–6、表2；2026-07-22快照 [正文](https://arxiv.org/html/2608.00122v1) [本地证据](../raw/sources/2026-11-18/F05.html) | SAP部分内部团队贡献后经同意、策展、门控、MCP检索；真实部署计数，另测56个合成门控样例。 | 900条提交中483条产出至少一条记忆，合计1,144条。已有部署、引用与链接；尚未验证下游任务增益。 | 不能把46.3%无产出全归因为重复。未校准的信任分不能替代权限或组织批准。 |
| [A06](https://arxiv.org/abs/2507.09637) Code Review as Decision-Making -- Building a Cognitive Model from the Questions Asked During Code Review · 方法、结果、参与者与讨论 [正文](https://arxiv.org/html/2507.09637v1) [本地证据](../raw/sources/2026-11-18/F06.html) | 同一办公环境10名开发者34次真实评审，出声思考、访谈，对问题序列做主题及时间分析。 | 评审者会从识别情境走向形成预期和判断，现场有人回到Jira查意图。 | 同一组织且研究者在场，无法由问题频率推算缺陷率。值得试给评审者证据入口，保留其判断。 |
| [A07](https://arxiv.org/abs/2507.09089) Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity · 主结果、附录D与随机化说明 [正文](https://arxiv.org/html/2507.09089v1) [本地证据](../raw/sources/2026-11-18/F07.html) | 16位有经验开源维护者246项真实任务，任务随机允许或禁止当时AI；AI组136项。 | 回归调整后的完成时间增加19%；事后自估节省20%。 | 2025年初工具和熟悉的仓，比较的是整体工具可用性。只能支持用实测工时校正问卷。 |
| [A08](https://arxiv.org/abs/2605.05253) EnterpriseRAG-Bench: A RAG Benchmark for Company Internal Knowledge · §3–7、分题型表 [正文](https://arxiv.org/html/2605.05253v1) [本地证据](../raw/sources/2026-11-18/F08.html) | 合成企业约51.2万文档、9类来源、500题；比较BM25、向量与Bash Agent的答案和召回。 | 在20道冲突题该实现的BM25正确率90%，向量60%；20道完整性题两者均40%。 | 人造公司和出题机制；不能推断BM25在企业普遍领先。检索起步要保留便宜词法基线。 |
| [A13](https://arxiv.org/abs/2602.20478) Codified Context: Infrastructure for AI Agents in a Complex Codebase · 方法、表3、4个观察案例 [正文](https://arxiv.org/html/2602.20478v1) [本地证据](../raw/sources/2026-11-18/F13.html) | 单复杂项目的283次开发会话，对分层说明、专门Agent和按需规范做案例回顾。 | 展示规范复用和维护轨迹，为“哪些知识可写”提供示例。 | 同一项目自述，无独立对照或新增团队冷启动。不能据此承诺团队采用。 |
| [A14](https://arxiv.org/abs/2610.33588) Developers as Managers of AI Agents: A Workplace Shadowing Study · 观察设计、Finding 2、总结 [正文](https://arxiv.org/html/2610.33588v1) [本地证据](../raw/sources/2026-11-18/F14.html) | 跟随11位职业开发者工作约15小时，编码255条提示，并做4.6小时访谈；无干预组。 | 平均33.4%观察时间用于构思提示或检查回复；受访者仍向同事寻求组织背景与权威判断。 | 观察时段短、参与者自选。支持测人检查和求确认耗时，不能推算替代人数。 |
| [A67](https://arxiv.org/abs/2312.17169) Improving Code Reviewer Recommendation: Accuracy, Latency, Workload, and Bystanders · v2 三个现场A/B、TimeInReview结果表；另见TOSEM DOI 10.1145/3736405 [正文](https://arxiv.org/html/2312.17169v2) [本地证据](../raw/sources/2026-11-18/F67.html) | Meta分别以约8.2万diff、2.8万作者、1.25万作者评估推荐准确度/延迟、负载平衡、团队评审落实到个人。 | 第三实验针对仅分配给组的评审，从前三位候选中随机指派一人，评审等待相关指标TimeInReview下降11.6%；负载平衡实验结果混合。 | 只适用于该组织的特定评审状态；直接给审批人、推荐顾问和自动联系有不同组织后果。内部试验同时计被打扰者净耗时。 |

**版本复核。** 上表 A01、A03、A04、A07、A08、A61 的定量引文取所链接的正文版本。A01 v3 使用 CTXbench 名称，A04 v3 扩大实验，详见主体。补查了 A07 v2、A08 v2、A61 v2 的主要结论。A03 较新版正文未取得，保留 v1 数字。[V01](https://arxiv.org/html/2602.11988v3) [V04](https://arxiv.org/html/2602.08316v3) [V07](https://arxiv.org/html/2507.09089v2) [V08](https://arxiv.org/html/2605.05253v2) [V61](https://arxiv.org/html/2601.20404v2)

## 产品机会清单

以下为设计建议；举例均为拟议交互。每项的证据等级针对其问题或机制，并非对产品收益的评级。

### O01　改完代码，提醒还少跑哪项检查

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 单仓作者准备提交 |
| 现状与缺口 | 照README跑快测；模块的兼容用例只在资深评审脑中 |
| 交互与机制 | 先读diff和CI定义；只在仍缺关键检查时显示“旧格式迁移尚无验证，打开用例或运行命令” |
| 复用资产／关键依赖 | 测试路径、CI记录、评审批注 ／ Nx等工具之外确有独有信号 |
| 失败代价 | 提示过多拖慢提交，漏选导致返工 |
| 最低成本验证 | 维护者预标10项必要验证，盲评有无提示后的命令 |
| 证据强度 | 现场需求与工程替代强，Agent增量待测。[A06](https://arxiv.org/abs/2507.09637) [A29](https://arxiv.org/abs/1810.05286) [G05](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) |

### O02　删除接口前列出仍在使用旧版本的调用方

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 平台作者准备改公共API |
| 现状与缺口 | grep当前主干或群发；静态使用者和线上版本混在一起 |
| 交互与机制 | 按部署版本查契约和调用点，显示“结算服务生产v2.4尚无此组合验证”，可打开证据 |
| 复用资产／关键依赖 | 服务目录、锁文件、契约矩阵 ／ 部署清单覆盖长尾消费者 |
| 失败代价 | 误报打断别组；漏报破坏兼容 |
| 最低成本验证 | 两团队选两接口，对比grep与带版本表清单 |
| 证据强度 | 真实上下游需求、可执行替代强。[A12](https://doi.org/10.1145/2501585.2501586) [D14](https://docs.pact.io/pact_broker/can_i_deploy) [G04](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) |

### O03　把未决问题交给能拍板的人

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 工程师因例外政策受阻 |
| 现状与缺口 | 问最近提交者；熟悉实现者未必有权豁免 |
| 交互与机制 | 先查问题类型、owner与值班，草拟“能否在本分支保留旧字段？”；人确认后才发 |
| 复用资产／关键依赖 | 目录、CODEOWNERS、工单决策者 ／ 专家负载、代理与授权映射 |
| 失败代价 | 错人、打扰、暴露客户名 |
| 最低成本验证 | 人工路由与CODEOWNERS对比，测首次有效答复时间 |
| 证据强度 | 现场研究较强，路由效果待测。[A09](https://doi.org/10.1109/icse.2007.45) [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |

### O04　下次接手时直接回到上次未验证的那一步

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 同人隔天/同事接力/云任务失败 |
| 现状与缺口 | 翻长对话重跑；上轮最后动作不等于下一步 |
| 交互与机制 | 附SHA、失败命令与未决假设，接手者点“复跑”；SHA变化标示差异 |
| 复用资产／关键依赖 | 命令退出码、工作树、任务ID ／ 可复现环境与新接手人权限 |
| 失败代价 | 复跑副作用、误以为已验证 |
| 最低成本验证 | 对同一冻结任务比较普通摘要与证据指针 |
| 证据强度 | 同人实验较强，换人推断。[A11](https://doi.org/10.1145/1753326.1753342) [A14](https://arxiv.org/abs/2610.33588) |

### O05　遇到旧决策时提示当年的前提是否还成立

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 维护者重新引入曾被否决的设计 |
| 现状与缺口 | 搜旧PR读结论；看不到作决定时的依赖条件 |
| 交互与机制 | 显示“当年因数据库版本回退，新集群版本已不同”，请原owner复议，不代替批准 |
| 复用资产／关键依赖 | ADR、历史PR、当前清单 ／ 能验证的前提、原作者离任 |
| 失败代价 | 过期否决束缚新设计 |
| 最低成本验证 | 给5对“理由相同/前提已变”案例测是否盲从 |
| 证据强度 | 设计推断。[A53](https://www.sciencedirect.com/science/article/pii/S0950584916301707) [A08](https://arxiv.org/abs/2605.05253) |

### O06　把需求里的业务词定位到一个可运行的例子

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 新人与跨组开发者解释需求 |
| 现状与缺口 | 搜同名类；同词在结算与客服含义不同 |
| 交互与机制 | 选中工单“结清”，返回本产品测试夹具、输入输出与符号；业务方标记哪种含义 |
| 复用资产／关键依赖 | 验收样例、测试名称、领域术语 ／ 术语分歧裁决与样例维护 |
| 失败代价 | 改对名字却改错行为 |
| 最低成本验证 | 10个歧义词，对比全文搜索后的首次正确定位 |
| 证据强度 | 检索研究与部署观察支持问题。[A03](https://arxiv.org/abs/2602.05892) [A05](https://arxiv.org/abs/2608.00122) [A39](https://doi.org/10.1145/2786805.2786855) |

### O07　在变更真正重叠时给双方一次提示

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 多人并行编辑或准备rebase |
| 现状与缺口 | 看PR列表；并发意图未提交 |
| 交互与机制 | 结合开启的PR、符号和契约变化，标明观察时间，允许静音到下次相关变更 |
| 复用资产／关键依赖 | PR事件、diff、工作项 ／ 草稿可见性与误报过滤 |
| 失败代价 | 通知疲劳与工作泄露 |
| 最低成本验证 | 回放已公开PR，用时间切片盲标需协调的重叠 |
| 证据强度 | CSCW理论与原型，收益推断。[A47](https://doi.org/10.1023/A:1021271517844) [A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) |

### O08　告诉评审者本次还缺哪一项决定依据

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 评审者首次看陌生diff |
| 现状与缺口 | 翻Jira、催作者补背景；最不确定的是预期变化 |
| 交互与机制 | 在评审面显示需求意图、已验证行为与一个未回答的问题，允许选择“信息已足” |
| 复用资产／关键依赖 | 工单、diff、测试结果 ／ 学习不同评审者的证据缺口 |
| 失败代价 | 锚定判断、错过替代解释 |
| 最低成本验证 | 并排盲评普通PR说明与问题卡，看追问轮次和漏错 |
| 证据强度 | 真实评审过程强，产品效果未知。[A06](https://arxiv.org/abs/2507.09637) [A42](https://www.cabird.com/pubs/bacchelli2013eoc.pdf) |

### O09　恢复被中断工作时重开当时看的代码片段

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 开发者被叫去排障后回原任务 |
| 现状与缺口 | 靠最后一个标签页或个人便签 |
| 交互与机制 | 按时间列最近3个代码位置和实验；一键回到当时符号，路径变更则回旧提交 |
| 复用资产／关键依赖 | IDE导航、CLI读取与git对象 ／ 用户是否允许采集足迹 |
| 失败代价 | 产生监控感，记录私密材料 |
| 最低成本验证 | 随机交叉对比普通便签与本地时序线索 |
| 证据强度 | 实验较强，跨设备推断。[A11](https://doi.org/10.1145/1753326.1753342) |

### O10　完成一次专家答疑后，先检查有没有第二个人需要

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 专家回答重复提问 |
| 现状与缺口 | 答完就散或强制写Wiki；贡献成本由回答者独担 |
| 交互与机制 | 同类问题第二次出现，邀请回答者确认一条可复用问答；无人复用则到期 |
| 复用资产／关键依赖 | 两次提问、原答、同意记录 ／ 近义问题合并与贡献者激励 |
| 失败代价 | 权宜答复固化成约定 |
| 最低成本验证 | 人工收集一周重复提问，追踪第二次是否少打扰专家 |
| 证据强度 | 组织系统与企业部署支持机制，净收益待测。[A45](https://doi.org/10.1145/91478.91485) [A46](https://web.eecs.umich.edu/~ackerm/pub/94b12/cscw94.html) [A05](https://arxiv.org/abs/2608.00122) |

### O11　找不到证据时说明缺在索引、权限还是版本

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 新成员查“为什么我查不到” |
| 现状与缺口 | 换关键词或让同事截图 |
| 交互与机制 | 在允许范围内显示“当前可查询源未同步”，有权管理员可诊断；对普通人隐藏受限资源存在性 |
| 复用资产／关键依赖 | 索引水位、授权检查、源状态 ／ 不能借诊断泄露存在性 |
| 失败代价 | 错误授意跨权复制或误判知识不存在 |
| 最低成本验证 | 合成四个缺失原因、两类身份测排错时间与泄露 |
| 证据强度 | 已有产品机制，研发结果为推断。[D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) [D12](https://docs.glean.com/administration/search/access-verification) [A08](https://arxiv.org/abs/2605.05253) |

### O12　把共享频道回复收缩成所有收件人均可看的证据

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 开发者把个人排查转到公共线程 |
| 现状与缺口 | 复制粘贴或请Agent总结；读取者和受众范围不同 |
| 交互与机制 | 频道只显示获准发布的摘要，个人侧有受限引用；受众不明时留在个人界面 |
| 复用资产／关键依赖 | DLP标签、频道成员属性、连接器权限 ／ 受众变化、访客、嵌套引用和引用派生物 |
| 失败代价 | 不可逆泄露 |
| 最低成本验证 | 用虚构文档和角色矩阵评测允许/拒绝；观察是否仍能推进 |
| 证据强度 | 平台边界实证，输出策略为建议。[D03](https://www.anthropic.com/news/introducing-claude-tag) [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) |

### O13　初始化时只提议仓库无法自行说明的几条约定

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 维护者带新人，或团队首次安装CLI |
| 现状与缺口 | 生成全仓介绍；与README和CI重复 |
| 交互与机制 | 对比仓内已有证据，只提交“例外条件＋验证命令＋owner”草案；支持整项忽略 |
| 复用资产／关键依赖 | Skill、Git PR、模板 ／ 维护者愿意审且有独有知识 |
| 失败代价 | 常驻成本、过期、前缀拥挤 |
| 最低成本验证 | 等内容比较人工小条目、自动生成、原样仓库 |
| 证据强度 | 直接实证互有分歧。[A01](https://arxiv.org/abs/2602.11988) [A02](https://arxiv.org/abs/2607.27250) [A61](https://arxiv.org/abs/2601.20404) |

### O14　准备发布时列出尚无验证结果的版本组合

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 发布经理和无人值守云任务 |
| 现状与缺口 | 靠绿灯或读群记录；不知道绿灯覆盖了哪个环境 |
| 交互与机制 | 从Pact/CI取部署矩阵，列出unknown和可执行补证步骤；沿用现有门禁 |
| 复用资产／关键依赖 | 部署流水号、消费方契约、作业链接 ／ 版本与环境标识对齐 |
| 失败代价 | 把未知当兼容而放行 |
| 最低成本验证 | 用旧发布记录遮住一个结果，看是否正确暂停 |
| 证据强度 | 成熟工程实践；CLI只应补发现与解释。[D14](https://docs.pact.io/pact_broker/can_i_deploy) [G06](https://github.com/pact-foundation/pact_broker/blob/6298abd2d4394e0255c944a9fbbc451402d766a6/lib/pact_broker/matrix/parse_query.rb) |

### O15　规范失效时通知受影响的使用处

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 规范维护者改规则或撤销知识 |
| 现状与缺口 | 全员公告；旧副本仍在提示词里 |
| 交互与机制 | 按引用ID找仍使用旧版的项目与缓存，展示可重算差异；仅在下次相关操作提示 |
| 复用资产／关键依赖 | 版本、来源ID、调用日志 ／ 派生摘要追踪与撤销传播 |
| 失败代价 | 一次错误扩散至多团队 |
| 最低成本验证 | 撤回一条合成规则，记录最后一次被使用时刻 |
| 证据强度 | 治理机制可借鉴，跨端效果推断。[D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/) [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) [A05](https://arxiv.org/abs/2608.00122) |

### O16　把同一次失败分成旧环境故障与本次代码回归

| 维度 | 判断 |
| --- | --- |
| 触发者与时机 | 作者看到CI失败准备改代码 |
| 现状与缺口 | 重跑或按错误字符串搜索；相似日志可能来自另一镜像 |
| 交互与机制 | 并列同SHA/环境/依赖的历史结果，缺匹配给复现场景；用户选择重跑或修补 |
| 复用资产／关键依赖 | CI运行ID、镜像摘要、测试历史 ／ 环境指纹与噪声代表性 |
| 失败代价 | 掩盖真实回归 |
| 最低成本验证 | 盲测旧故障，比较错误修改次数，CI保留原判 |
| 证据强度 | 部署案例支持信号，分类效果待验证。[A29](https://arxiv.org/abs/1810.05286) [D15](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/) |

## 论文索引与筛查决策

| ID、论文及一手入口 | 时间口径 | 深度与研究用途 | 证据快照 |
| --- | --- | --- | --- |
| [A01](https://arxiv.org/abs/2602.11988) Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? | 2026-02-12 · arXiv v1 | 正文复核。初始化文件的负例，区分模型生成和人写要求 | [本地证据](../raw/sources/2026-11-18/A01.html) |
| [A02](https://arxiv.org/abs/2607.27250) Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories | 2026-07-28 · arXiv v1 | 正文复核。常驻、选择与无文件消融，检查推断精度 | [本地证据](../raw/sources/2026-11-18/A02.html) |
| [A03](https://arxiv.org/abs/2602.05892) ContextBench: A Benchmark for Context Retrieval in Coding Agents | 2026-02-05 · arXiv v1 | 正文复核。定位与最终任务成功分开计量 | [本地证据](../raw/sources/2026-11-18/A03.html) |
| [A04](https://arxiv.org/abs/2602.08316) SWE Context Bench: A Benchmark for Context Learning in Coding | 2026-02-09 · arXiv v1 | 正文复核。经验选择与摘要价值，需要错误经验对照 | [本地证据](../raw/sources/2026-11-18/A04.html) |
| [A05](https://arxiv.org/abs/2608.00122) Shared Organizational Memory for Enterprise Coding Agents: System Design and Deployment Snapshot | 2026-07-31 · arXiv v1 | 正文复核。组织部署的写入、策展和采纳漏斗 | [本地证据](../raw/sources/2026-11-18/A05.html) |
| [A06](https://arxiv.org/abs/2507.09637) Code Review as Decision-Making -- Building a Cognitive Model from the Questions Asked During Code Review | 2025-07-13 · arXiv v1 | 正文复核。评审者先问哪些问题、还缺哪些证据 | [本地证据](../raw/sources/2026-11-18/A06.html) |
| [A07](https://arxiv.org/abs/2507.09089) Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | 2025-07-12 · arXiv v1 | 正文复核。熟悉项目的维护者、主观与客观时间差 | [本地证据](../raw/sources/2026-11-18/A07.html) |
| [A08](https://arxiv.org/abs/2605.05253) EnterpriseRAG-Bench: A RAG Benchmark for Company Internal Knowledge | 2026-05-05 · arXiv v1 | 正文复核。企业跨工具检索，候选证据与问答分数的边界 | [本地证据](../raw/sources/2026-11-18/A08.html) |
| [A09](https://doi.org/10.1109/icse.2007.45) Information Needs in Collocated Software Development Teams | 2007-05 · 出版，首公开未核 | 正文复核。同事成为唯一信息源时如何阻塞任务 | [本地证据](../raw/sources/2026-11-18/A09.json) |
| [A10](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/codebook-cameraready.pdf) Codebook: Discovering and Exploiting Relationships in Software Repositories | 2010 · 出版，首公开未核 | 正文复核。跨工具关系与普通文本搜索 | [本地证据](../raw/web/field-measure.txt) |
| [A11](https://doi.org/10.1145/1753326.1753342) Evaluating cues for resuming interrupted programming tasks | 2010-04-10 · 出版，首公开未核 | 正文复核。恢复线索与自写笔记 | [本地证据](../raw/sources/2026-11-18/A11.json) |
| [A12](https://doi.org/10.1145/2501585.2501586) Categorizing developer information needs in software ecosystems | 2013-08-19 · 出版，首公开未核 | 正文复核。库维护者如何知晓下游 | [本地证据](../raw/sources/2026-11-18/A12.json) |
| [A13](https://arxiv.org/abs/2602.20478) Codified Context: Infrastructure for AI Agents in a Complex Codebase | 2026-02-24 · arXiv v1 | 正文复核。单项目长期文档维护案例 | [本地证据](../raw/sources/2026-11-18/A13.html) |
| [A14](https://arxiv.org/abs/2610.33588) Developers as Managers of AI Agents: A Workplace Shadowing Study | 2026-10-24 · arXiv v1 | 正文复核。真实工作现场观察，委派和监督 | [本地证据](../raw/sources/2026-11-18/A14.html) |
| [A15](https://arxiv.org/abs/2609.23570) VibeMemBench: Evaluating Memory Systems for Coding Agents on Real Repository Coding Tasks | 2026-09-20 · arXiv v1 | 正文复核。跨会话记忆的仓库任务评测 | [本地证据](../raw/sources/2026-11-18/A15.html) |
| [A16](https://arxiv.org/abs/2607.24882) Agent Retrieval Bench: Evaluating Repository Context Retrieval for Coding Agents | 2026-07-27 · arXiv v1 | 书目/摘要索引。代码检索评价与耗时成本 | [本地证据](../raw/sources/2026-11-18/A16.html) |
| [A17](https://arxiv.org/abs/2606.11864) CORE-Bench: A Comprehensive Benchmark for Code Retrieval in the Era of Agentic Coding | 2026-06-10 · arXiv v1 | 书目/摘要索引。代码检索基准与代理搜索 | [本地证据](../raw/sources/2026-11-18/A17.html) |
| [A18](https://arxiv.org/abs/2510.04905) Retrieval-Augmented Code Generation: A Survey with Focus on Repository-Level Approaches | 2025-10-06 · arXiv v1 | 书目/摘要索引。仓库级检索综述与后向追踪起点 | [本地证据](../raw/sources/2026-11-18/A18.html) |
| [A19](https://arxiv.org/abs/2507.23361) SWE-Exp: Experience-Driven Software Issue Resolution | 2025-07-31 · arXiv v1 | 书目/摘要索引。经验驱动的历史修复复用 | [本地证据](../raw/sources/2026-11-18/A19.html) |
| [A20](https://arxiv.org/abs/2507.00014) SWE-Bench-CL: Continual Learning for Coding Agents | 2025-06-13 · arXiv v1 | 书目/摘要索引。持续学习任务序列 | [本地证据](../raw/sources/2026-11-18/A20.html) |
| [A21](https://arxiv.org/abs/2601.22129) SWE-Replay: Efficient Test-Time Scaling for Software Engineering Agents | 2026-01-29 · arXiv v1 | 书目/摘要索引。执行轨迹重用和推理预算 | [本地证据](../raw/sources/2026-11-18/A21.html) |
| [A22](https://arxiv.org/abs/2509.16941) SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? | 2025-09-21 · arXiv v1 | 书目/摘要索引。长程任务基线 | [本地证据](../raw/sources/2026-11-18/A22.html) |
| [A23](https://arxiv.org/abs/2504.08703) SWE-PolyBench: A multi-language benchmark for repository level evaluation of coding agents | 2025-04-11 · arXiv v1 | 书目/摘要索引。跨语言任务及定位范围 | [本地证据](../raw/sources/2026-11-18/A23.html) |
| [A24](https://arxiv.org/abs/2609.08149) SWE-Bench Pro Verified: A Reliable Benchmark for Software Engineering Agents | 2026-09-08 · arXiv v1 | 书目/摘要索引。测试可靠性与基准校正 | [本地证据](../raw/sources/2026-11-18/A24.html) |
| [A25](https://arxiv.org/abs/2610.27911) MMEnterprise-Bench: Evaluating Enterprise Agents over Evolving Multimodal Records | 2026-10-20 · arXiv v1 | 书目/摘要索引。随时间变化的企业记录 | [本地证据](../raw/sources/2026-11-18/A25.html) |
| [A26](https://arxiv.org/abs/2608.11584) EnterpriseRAG: Benchmarking LLM Instruction Adherence and Robustness under Non-Ideal Enterprise Retrieval | 2026-08-12 · arXiv v1 | 书目/摘要索引。不理想检索条件下的指令遵循 | [本地证据](../raw/sources/2026-11-18/A26.html) |
| [A27](https://arxiv.org/abs/2609.25563) AkasicMEM: Governed Enterprise Memory for Agents | 2026-09-22 · arXiv v1 | 书目/摘要索引。企业记忆治理机制，机制提案 | [本地证据](../raw/sources/2026-11-18/A27.html) |
| [A28](https://arxiv.org/abs/2607.09493) Shared Selective Persistent Memory for Agentic LLM Systems | 2026-07-10 · arXiv v1 | 书目/摘要索引。多主体的选择性持久化 | [本地证据](../raw/sources/2026-11-18/A28.html) |
| [A29](https://arxiv.org/abs/1810.05286) Predictive Test Selection | 2018-10-11 · arXiv v1 | 书目/摘要索引。测试选择的生产对照和现成替代 | [本地证据](../raw/sources/2026-11-18/A29.html) |
| [A30](https://arxiv.org/abs/1703.01897) Software Engineers' Information Seeking Behavior in Change Impact Analysis - An Interview Study | 2017-03-06 · arXiv v1 | 书目/摘要索引。变更影响分析中的人工信息搜寻 | [本地证据](../raw/sources/2026-11-18/A30.html) |
| [A31](https://arxiv.org/abs/2310.06770) SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | 2023-10-10 · arXiv v1 | 书目/摘要索引。单仓 issue 到补丁、隐藏验证 | [本地证据](../raw/sources/2026-11-18/A31.html) |
| [A32](https://arxiv.org/abs/2405.15793) SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | 2024-05-06 · arXiv v1 | 书目/摘要索引。代理与计算机接口对行为的影响 | [本地证据](../raw/sources/2026-11-18/A32.html) |
| [A33](https://arxiv.org/abs/2410.10813) LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory | 2024-10-14 · arXiv v1 | 书目/摘要索引。更新、遗忘与拒答维度 | [本地证据](../raw/sources/2026-11-18/A33.html) |
| [A34](https://arxiv.org/abs/2402.17753) Evaluating Very Long-Term Conversational Memory of LLM Agents | 2024-02-27 · arXiv v1 | 书目/摘要索引。长时对话记忆边界 | [本地证据](../raw/sources/2026-11-18/A34.html) |
| [A35](https://arxiv.org/abs/2307.03172) Lost in the Middle: How Language Models Use Long Contexts | 2023-07-06 · arXiv v1 | 书目/摘要索引。长上下文中证据位置的影响 | [本地证据](../raw/sources/2026-11-18/A35.html) |
| [A36](https://arxiv.org/abs/2303.12570) RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation | 2023-03-22 · arXiv v1 | 书目/摘要索引。迭代检索与仓库级生成 | [本地证据](../raw/sources/2026-11-18/A36.html) |
| [A37](https://arxiv.org/abs/2310.11248) CrossCodeEval: A Diverse and Multilingual Benchmark for Cross-File Code Completion | 2023-10-17 · arXiv v1 | 书目/摘要索引。跨文件补全，测试词法与上下文 | [本地证据](../raw/sources/2026-11-18/A37.html) |
| [A38](https://arxiv.org/abs/2306.03091) RepoBench: Benchmarking Repository-Level Code Auto-Completion Systems | 2023-06-05 · arXiv v1 | 书目/摘要索引。检索和补全拆分测量 | [本地证据](../raw/sources/2026-11-18/A38.html) |
| [A39](https://doi.org/10.1145/2786805.2786855) How developers search for code: a case study | 2015-08-30 · 出版，首公开未核 | 书目/摘要索引。代码搜索的真实行为 | [本地证据](../raw/sources/2026-11-18/A39.json) |
| [A40](https://cs.gmu.edu/~tlatoza/papers/plateau2010.pdf) Hard-to-Answer Questions about Code | 2010 · 出版，首公开未核 | 书目/摘要索引。难以回答的可达性与理由 | [本地证据](../raw/web/se.txt) |
| [A41](https://doi.org/10.1145/1181775.1181779) Questions programmers ask during software evolution tasks | 2006-11-05 · 出版，首公开未核 | 书目/摘要索引。定位之后的关系理解 | [本地证据](../raw/sources/2026-11-18/A41.json) |
| [A42](https://www.cabird.com/pubs/bacchelli2013eoc.pdf) Expectations, Outcomes, and Challenges of Modern Code Review | 2013 · 出版，首公开未核 | 书目/摘要索引。评审中的知识转移与理解 | [本地证据](../raw/web/A42.txt) |
| [A43](https://research.google/pubs/modern-code-review-a-case-study-at-google/) Modern Code Review: A Case Study at Google | 2018 · 出版，首公开未核 | 书目/摘要索引。评审部署与规模迁移边界 | [本地证据](../raw/web/A43.txt) |
| [A44](https://web.eecs.umich.edu/~ackerm/pub/00b30/cscw00.er.pdf) Expertise Recommender: A Flexible Recommendation System and Architecture | 2000 · 出版，首公开未核 | 书目/摘要索引。领域专家发现 | [本地证据](../raw/web/A44.txt) |
| [A45](https://doi.org/10.1145/91478.91485) Answer Garden: a tool for growing organizational memory | 1990-03 · 出版，首公开未核 | 书目/摘要索引。未解答问题转交专家后再沉淀 | [本地证据](../raw/sources/2026-11-18/A45.json) |
| [A46](https://web.eecs.umich.edu/~ackerm/pub/94b12/cscw94.html) Augmenting Organizational Memory: A Field Study of Answer Garden | 1994 · 出版，首公开未核 | 书目/摘要索引。组织中的贡献与维护 | [本地证据](../raw/web/cscw.txt) |
| [A47](https://doi.org/10.1023/A:1021271517844) A Descriptive Framework of Workspace Awareness for Real-Time Groupware | 2002 · 出版，首公开未核 | 书目/摘要索引。协作现场的谁、在哪、做什么 | [本地证据](../raw/web/A47.txt) |
| [A48](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/01/groupware-and-social-dynamics.pdf) Groupware and Social Dynamics: Eight Challenges for Developers | 1994 · 出版，首公开未核 | 书目/摘要索引。贡献者与获益者的激励差 | [本地证据](../raw/web/A48.txt) |
| [A49](https://journals.aom.org/doi/10.5465/amr.1991.4278992) Organizational Memory | 1991 · 出版，首公开未核 | 书目/摘要索引。组织信息留存的多个载体 | [本地证据](../raw/web/A49.txt) |
| [A50](https://www.cs.cmu.edu/~illah/CLASSDOCS/Clark91.pdf) Grounding in Communication | 1991 · 出版，首公开未核 | 书目/摘要索引。协作双方对理解的确认 | [本地证据](../raw/web/cscw2.txt) |
| [A52](https://www.sciencedirect.com/science/article/pii/S0164121221000480) A systematic literature review and taxonomy of modern code review | 2021 · 出版，首公开未核 | 书目/摘要索引。综述入口、证据分类 | [本地证据](../raw/web/review-archive.txt) |
| [A53](https://www.sciencedirect.com/science/article/pii/S0950584916301707) Software architecture knowledge management approaches and their support for knowledge management activities: A systematic literature review | 2016-12 · 出版，首公开未核 | 书目/摘要索引。决策持久化成本与活动覆盖 | [本地证据](../raw/web/review-archive.txt) |
| [A54](https://conf.researchr.org/details/ase-2024/ase-2024-research/125/Hybrid-Regression-Test-Selection-by-Integrating-File-and-Method-Dependences) Hybrid Regression Test Selection by Integrating File and Method Dependences | 2024 · 出版，首公开未核 | 书目/摘要索引。ASE 变更验证粒度 | [本地证据](../raw/web/venue.txt) |
| [A55](https://conf.researchr.org/details/issta-2020/issta-2020-papers/14/Dependent-Test-Aware-Regression-Testing-Techniques) Dependent-Test-Aware Regression Testing Techniques | 2020 · 出版，首公开未核 | 书目/摘要索引。ISSTA 有顺序依赖时选择测试的风险 | [本地证据](../raw/web/venue.txt) |
| [A56](https://doi.org/10.1109/TSE.2006.116) An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks | 2006 · 出版，首公开未核 | 书目/摘要索引。TSE 维护工作的搜寻链 | [本地证据](../raw/web/c3.txt) |
| [A61](https://arxiv.org/abs/2601.20404) On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents | 2026-01-28 · arXiv v1 | 正文复核。初始化文件效率的配对对照，前向追踪至双代理消融 | [本地证据](../raw/sources/2026-11-18/A61.html) |
| [A62](https://arxiv.org/abs/2610.31715) What Open-Source Projects Tell Their Coding Agents: A Census of AGENTS.md and CLAUDE.md | 2026-10-22 · arXiv v1 | 书目/摘要索引。仓库指令普查，采用与效果分开 | [本地证据](../raw/sources/2026-11-18/A62.html) |
| [A63](https://arxiv.org/abs/2607.02606) ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance | 2026-07-01 · arXiv v1 | 书目/摘要索引。多问题维护的跨任务状态 | [本地证据](../raw/sources/2026-11-18/A63.html) |
| [A64](https://arxiv.org/abs/2608.16801) When Agents Coordinate: Measuring Coordination in Multi-Agent AI Coding | 2026-08-17 · arXiv v1 | 书目/摘要索引。多代理协调的可观测性 | [本地证据](../raw/sources/2026-11-18/A64.html) |
| [A65](https://arxiv.org/abs/2510.01353) MEMTRACK: Evaluating Long-Term Memory and State Tracking in Multi-Platform Dynamic Agent Environments | 2025-10-01 · arXiv v1 | 书目/摘要索引。跨平台动态状态追踪 | [本地证据](../raw/sources/2026-11-18/A65.html) |
| [A66](https://arxiv.org/abs/2511.08301) Smarter Together: Creating Agentic Communities of Practice through Shared Experiential Learning | 2025-11-11 · arXiv v1 | 书目/摘要索引。共享经验及实践共同体 | [本地证据](../raw/sources/2026-11-18/A66.html) |
| [A67](https://arxiv.org/abs/2312.17169) Improving Code Reviewer Recommendation: Accuracy, Latency, Workload, and Bystanders | 2023-12-28 · arXiv v1 | 正文复核。推荐评审者时考虑延迟、负载及旁观者 | [本地证据](../raw/web/quarter-full.txt) |

**未纳入计数。** A51 Searching, skimming, and exploring: patterns of information seeking in the debugging process（书目未可靠核对）；A57 Interruptions and Recovery: Leveraging Dynamic Code History for Task Resumption（书目未可靠核对）；A58 To Copilot and Beyond: 22 AI Systems Developers Want Built（书目未可靠核对）；A59 An empirical study of architectural decision networks and their evolution through developer discussions（书目未可靠核对）；A60 Categorizing the content of GitHub README files（书目未可靠核对）。

## 来源、固定提交与检索明细

### 开源实现与测试定位

| 证据 | 仓库 | 提交时间（UTC） | 固定提交文件 | 本地 |
| --- | --- | --- | --- | --- |
| G01 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [packages/core/src/utils/memoryDiscovery.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/utils/memoryDiscovery.ts) | [本地证据](../raw/git/gemini-cli/2026-11-18/memoryDiscovery.ts) |
| G01 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [packages/core/src/utils/memoryDiscovery.test.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/utils/memoryDiscovery.test.ts) | [本地证据](../raw/git/gemini-cli/2026-11-18/memoryDiscovery.test.ts) |
| G02 | QwenLM/qwen-code | 2026-11-18T02:58:57Z | [packages/core/src/memory/memoryDiscovery.ts](https://github.com/QwenLM/qwen-code/blob/a0ee2c0e75e11d18bb5e1821180147d9ad2167b6/packages/core/src/memory/memoryDiscovery.ts) | [本地证据](../raw/git/qwen-code/2026-11-18/memoryDiscovery.ts) |
| G02 | QwenLM/qwen-code | 2026-11-18T02:58:57Z | [packages/core/src/memory/memoryDiscovery.test.ts](https://github.com/QwenLM/qwen-code/blob/a0ee2c0e75e11d18bb5e1821180147d9ad2167b6/packages/core/src/memory/memoryDiscovery.test.ts) | [本地证据](../raw/git/qwen-code/2026-11-18/memoryDiscovery.test.ts) |
| G03 | Aider-AI/aider | 2026-05-22T14:02:20Z | [aider/repomap.py](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/repomap.py) | [本地证据](../raw/git/aider/2026-11-18/repomap.py) |
| G03 | Aider-AI/aider | 2026-05-22T14:02:20Z | [tests/basic/test_repomap.py](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_repomap.py) | [本地证据](../raw/git/aider/2026-11-18/test_repomap.py) |
| G04 | backstage/backstage | 2026-11-17T21:29:33Z | [plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.ts) | [本地证据](../raw/git/backstage/2026-11-18/BuiltinKindsEntityProcessor.ts) |
| G04 | backstage/backstage | 2026-11-17T21:29:33Z | [plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.test.ts](https://github.com/backstage/backstage/blob/bc2ee5019905ba2985e7a9315397d30d8c4eef53/plugins/catalog-backend/src/processors/BuiltinKindsEntityProcessor.test.ts) | [本地证据](../raw/git/backstage/2026-11-18/BuiltinKindsEntityProcessor.test.ts) |
| G05 | nrwl/nx | 2026-11-17T23:15:03Z | [packages/nx/src/project-graph/affected/affected-project-graph.ts](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.ts) | [本地证据](../raw/git/nx/2026-11-18/affected-project-graph.ts) |
| G05 | nrwl/nx | 2026-11-17T23:15:03Z | [packages/nx/src/project-graph/affected/affected-project-graph.spec.ts](https://github.com/nrwl/nx/blob/cd0630bb20d53022aab01a450284b5ecf9ac3454/packages/nx/src/project-graph/affected/affected-project-graph.spec.ts) | [本地证据](../raw/git/nx/2026-11-18/affected-project-graph.spec.ts) |
| G06 | pact-foundation/pact_broker | 2026-11-15T00:57:07Z | [lib/pact_broker/matrix/parse_query.rb](https://github.com/pact-foundation/pact_broker/blob/6298abd2d4394e0255c944a9fbbc451402d766a6/lib/pact_broker/matrix/parse_query.rb) | [本地证据](../raw/git/pact_broker/2026-11-18/parse_query.rb) |
| C01 | openai/codex | 2026-11-18T02:56:01Z | [agents_md.rs](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/src/agents_md.rs) | [本地证据](../raw/sources/2026-11-18/C01.rs) |
| C02 | openai/codex | 2026-11-18T02:56:01Z | [agents_md_manager.rs](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/src/agents_md_manager.rs) | [本地证据](../raw/sources/2026-11-18/C02.rs) |
| C03 | openai/codex | 2026-11-18T02:56:01Z | [agents_md_refresh.rs](https://github.com/openai/codex/blob/f09fb197f517acb3052ae3976a7fc3b5a5a8897d/codex-rs/core/tests/suite/agents_md_refresh.rs) | [本地证据](../raw/sources/2026-11-18/C03.rs) |
| J01 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [jit-context.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/jit-context.ts) | [本地证据](../raw/sources/2026-11-18/J01.ts) |
| J02 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [read-file.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/read-file.ts) | [本地证据](../raw/sources/2026-11-18/J02.ts) |
| J03 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [memoryContextManager.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/context/memoryContextManager.ts) | [本地证据](../raw/sources/2026-11-18/J03.ts) |
| J05 | google-gemini/gemini-cli | 2026-11-18T00:38:51Z | [jit-context.test.ts](https://github.com/google-gemini/gemini-cli/blob/4f343cabc7b59ab990d7411e920094108524abff/packages/core/src/tools/jit-context.test.ts) | [本地证据](../raw/sources/2026-11-18/J05.ts) |

### 产品来源的时间口径

| 官方来源 | 发布/增强日期 | 页面更新元数据 | 快照 |
| --- | --- | --- | --- |
| [D01](https://developers.openai.com/codex/guides/agents-md) Codex | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/web/prod.txt) |
| [D02](https://code.claude.com/docs/en/memory) Claude Code | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D02.html) |
| [D03](https://www.anthropic.com/news/introducing-claude-tag) Claude Tag | 2026-06-23 beta | 2026-09-29 | [本地证据](../raw/sources/2026-11-18/D03.html) |
| [D04](https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work/) GitHub Copilot | 2026-10-28 GA/预览 | 2026-10-28 | [本地证据](../raw/sources/2026-11-18/D04.html) |
| [D05](https://cursor.com/docs/rules) Cursor | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D05.html) |
| [D06](https://docs.qoder.com/user-guide/repo-wiki) Qoder | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D06.html) |
| [D07](https://docs.devin.ai/product-guides/knowledge) Devin | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D07.html) |
| [D08](https://github.com/OpenHands/docs/blob/main/sdk/arch/skill.mdx) OpenHands | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D08.html) |
| [D09](https://sourcegraph.com/docs/code-search/working/search-contexts) Sourcegraph | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D09.html) |
| [D10](https://docs.slack.dev/apis/web-api/real-time-search-api/) Slack | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D10.html) |
| [D11](https://support.atlassian.com/organization-administration/docs/how-connector-permissions-are-kept-in-sync/) Rovo | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D11.html) |
| [D12](https://docs.glean.com/administration/search/access-verification) Glean | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D12.html) |
| [D13](https://coder.com/changelog/project-level-memory-for-coder-agents-in-239) Coder | 2026-11-03 版本2.39 | 未核 | [本地证据](../raw/sources/2026-11-18/D13.html) |
| [D14](https://docs.pact.io/pact_broker/can_i_deploy) Pact Broker | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D14.html) |
| [D15](https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/) Meta PTS | 2018-11-21 部署文章 | 2020-03-24 | [本地证据](../raw/sources/2026-11-18/D15.html) |
| [D16](https://claude.com/resources/articles/claude-tag-now-reads-even-more-of-the-room) Claude Tag update | 2026-08-13 增强 | 未核 | [本地证据](../raw/sources/2026-11-18/D16.html) |
| [D17](https://github.blog/changelog/2026-01-15-agentic-memory-for-github-copilot-is-in-public-preview/) Copilot preview | 2026-01-15 公开预览 | 2026-01-15 | [本地证据](../raw/sources/2026-11-18/D17.html) |
| [D18](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli/) Copilot controls | 2026-05-26 控制增强 | 2026-05-26 | [本地证据](../raw/sources/2026-11-18/D18.html) |
| [D19](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) GitHub CODEOWNERS | 仅当前文档，首发未核 | 未核 | [本地证据](../raw/sources/2026-11-18/D19.html) |
| [D20](https://github.blog/changelog/2025-12-19-copilot-memory-early-access-for-pro-and-pro/) Copilot early access | 2025-12-19 早期开放 | 2025-12-19 | [本地证据](../raw/sources/2026-11-18/D20.html) |
| [D21](https://www.atlassian.com/blog/announcements/rovo-dev-in-jira) Rovo Dev in Jira | 2026-04-02 工作项入口 | 2026-04-29 | [本地证据](../raw/sources/2026-11-18/D21.html) |
| [D22](https://cursor.com/changelog/customize) Cursor 3.9 | 2026-06-22 3.9增强 | 未核 | [本地证据](../raw/sources/2026-11-18/D22.html) |

### 检索式与未筛选返回

下列均在2026-11-18执行。多库检索通过网页索引、出版方及作者站点完成；网站返回的相对时间不作为发布日期。书目逐题检索另见 papers.tsv 和 Crossref 原始响应。

| 批次 | 关键词与时间限制 | 检索摘录 |
| --- | --- | --- |
| A42 | Expectations Outcomes and Challenges of Modern Code Review Bacchelli Bird Microsoft | [本地证据](../raw/web/A42.txt) |
| A43 | Modern Code Review A Case Study at Google Sadowski research google | [本地证据](../raw/web/A43.txt) |
| A44 | Expertise Recommender A Flexible Recommendation System and Architecture McDonald Ackerman author pdf | [本地证据](../raw/web/A44.txt) |
| A47 | A descriptive framework of workspace awareness for real-time groupware Gutwin Greenberg doi | [本地证据](../raw/web/A47.txt) |
| A48 | Grudin Groupware and social dynamics eight challenges for developers microsoft research | [本地证据](../raw/web/A48.txt) |
| A49 | Organizational Memory Walsh Ungson 1991 DOI | [本地证据](../raw/web/A49.txt) |
| A51 | Lawrance debugging information foraging scent programmers debugging scholarly paper ACM | [本地证据](../raw/web/A51.txt) |
| A60 | site:dl.acm.org TOSEM architectural design decisions architecture knowledge developers empirical study decision rationale | [本地证据](../raw/web/A60.txt) |
| A67 | site:dl.acm.org "ACM Transactions on Software Engineering and Methodology" repository-level coding agents context benchmark retrieval | [本地证据](../raw/web/A67.txt) |
| adj | software engineering flaky tests prediction test selection Facebook predictive test selection Google TAP test failures change impact developer deployment contracts case study | [本地证据](../raw/web/adj.txt) |
| aug | after:2026-08-17 before:2026-11-19 coding agent shared memory organizational knowledge Claude Tag team rules Cursor Devin Copilot changelog team context | [本地证据](../raw/web/aug.txt) |
| bench | agent memory evaluation software engineering experiential learning SWE-Exp SWE-agent trajectories memory SWE-Replay SWE-bench-CL continual learning software engineering agents arxiv benchmarks memory coding 2026 | [本地证据](../raw/web/bench.txt) |
| c1 | Codebook Discovering Exploiting Relationships software repositories Categorizing Developer Information Needs Software Ecosystems Haenni doi | [本地证据](../raw/web/c1.txt) |
| c2 | site:dl.acm.org expertise recommender flexible architecture Answer Garden grounding in communication workspace awareness groupware Grudin | [本地证据](../raw/web/c2.txt) |
| c3 | TSE A study how developers seek relate collect relevant information software maintenance TOSEM architectural knowledge documentation decisions | [本地证据](../raw/web/c3.txt) |
| claude | site:code.claude.com/docs/en/memory paths rules when reads files subdirectories startup | [本地证据](../raw/web/claude.txt) |
| codex | site:developers.openai.com codex AGENTS.md discovery instructions | [本地证据](../raw/web/codex.txt) |
| codquarter | site:atlassian.com/blog after:2026-08-17 before:2026-11-19 Rovo Dev always-on engineering context work item agent software team knowledge | [本地证据](../raw/web/codquarter.txt) |
| cscw | CSCW expertise recommender McDonald Ackerman organizational memory Answer Garden groupware Grudin disparity work benefit grounding communication Clark Brennan workspace awareness Gutwin Greenberg transactive memory Lewis organizations memory Walsh Ungson | [本地证据](../raw/web/cscw.txt) |
| cscw2 | "Expertise Recommender" McDonald Ackerman CHI CSCW 2000 doi / "groupware and social dynamics" Grudin work benefit DOI / "grounding in communication" Clark Brennan Stanford grounding effort | [本地证据](../raw/web/cscw2.txt) |
| ctx | site:arxiv.org shared memory coding agents team knowledge maintenance longitudinal organizational coding agents benchmark shared memory enterprise | [本地证据](../raw/web/ctx.txt) |
| cursorquarter | site:cursor.com/changelog after:2026-08-17 before:2026-11-19 knowledge shared team rules learned skills context organization changelog | [本地证据](../raw/web/cursorquarter.txt) |
| delta | after:2026-08-17 before:2026-11-19 site:claude.com "Claude Tag" memory channels October November updates agent identity | [本地证据](../raw/web/delta.txt) |
| deploy | site:arxiv.org enterprise coding agents shared memory context team deployment knowledge coding agents real developers organizational context enterprise Slack memory SWE-CI | [本地证据](../raw/web/deploy.txt) |
| devin-follow | Devin "Knowledge" "trigger" knowledge notes site:docs.devin.ai OR site:cognition.ai | [本地证据](../raw/web/devin-follow.txt) |
| devin | site:docs.devin.ai knowledge triggers suggestions Devin knowledge playbooks | [本地证据](../raw/web/devin.txt) |
| devquarter | site:cognition.ai/blog OR site:docs.devin.ai/release-notes after:2026-08-17 before:2026-11-19 Devin knowledge organization context knowledge sharing | [本地证据](../raw/web/devquarter.txt) |
| forward | "Evaluating AGENTS.md" context files repository instructions replication field study effect 2026 beyond AGENTS.md Agent READMEs measuring efficacy | [本地证据](../raw/web/forward.txt) |
| gcc | site:arxiv.org "AGENTS.md" Lulla efficiency coding agents | [本地证据](../raw/web/gcc.txt) |
| glean | site:docs.glean.com permissions indexing stale permissions identity source search results | [本地证据](../raw/web/glean.txt) |
| pact | site:docs.pact.io can-i-deploy matrix deployed environment unknown verification | [本地证据](../raw/web/pact.txt) |
| paper1 | coding agents context files evaluating AGENTS.md repository level context files agent skills benchmark contextbench swe smith swe context 2026 arxiv | [本地证据](../raw/web/paper1.txt) |
| paper2 | organizational memory enterprise search benchmark permissions temporal questions enterprise benchmark CRMArena WorkArena LongMemEval LoCoMo BEAM benchmark enterprise RAG | [本地证据](../raw/web/paper2.txt) |
| paper3 | site:arxiv.org software engineering agents repository context realistic issue benchmarks SWE-bench Live SWE PolyBench multi repository cross repositories benchmark SWE-QA Pro | [本地证据](../raw/web/paper3.txt) |
| paper4 | developer information needs expertise recommender coordination requirements workspace awareness Palantir Deep Intellisense Codebook Microsoft field study code search at Google | [本地证据](../raw/web/paper4.txt) |
| ports | site:conf.researchr.org TOSEM developer documentation information needs knowledge software developers code review 2024 2025 | [本地证据](../raw/web/ports.txt) |
| qoder | site:docs.qoder.com Repo Wiki update knowledge base index | [本地证据](../raw/web/qoder.txt) |
| recent | after:2026-08-17 before:2026-11-19 site:github.blog/changelog copilot memory repository instructions organization knowledge coding agent | [本地证据](../raw/web/recent.txt) |
| review-archive | "A systematic literature review and taxonomy of modern code review" primary studies 2021 / "Software architecture knowledge management approaches and their support" 2017 studies approaches abstract | [本地证据](../raw/web/review-archive.txt) |
| review | software engineering agents context repository code retrieval survey 2025 2026 code language model repository level benchmark CrossCodeEval RepoBench RepoCoder Repoformer CoCoMIC RepoHyper DraCo GraphCoder | [本地证据](../raw/web/review.txt) |
| reviewer | "Improving Code Reviewer Recommendation" workload bystanders author software engineering 2025 2026 workload latency top-k comparison | [本地证据](../raw/web/reviewer.txt) |
| rovo | site:support.atlassian.com rovo permissions search connector synced permissions | [本地证据](../raw/web/rovo.txt) |
| se | developer information foraging software debugging Lawrance Piorkowski questions developers ask Sillito LaToza hard to answer questions information needs code review Bacchelli Sadowski Google code search developers | [本地证据](../raw/web/se.txt) |
| sec | temporal retrieval contradictions LongMemEval LoCoMo time knowledge editing dated questions benchmark retrieval FreshQA TimeQA ACL temporal knowledge benchmark timestamps | [本地证据](../raw/web/sec.txt) |
| tag | Claude Tag shared team knowledge Anthropic Claude Tag launch date | [本地证据](../raw/web/tag.txt) |
| tagup | site:claude.com "Claude Tag now reads even more" date what new integrations | [本地证据](../raw/web/tagup.txt) |
| tech1 | Cursor rules always apply auto attached agent requested Devin knowledge triggers Qoder repowiki rules official docs | [本地证据](../raw/web/tech1.txt) |
| tech2 | Sourcegraph search contexts revisions repository Backstage catalog owner Pact Broker can-i-deploy Nx affected official docs | [本地证据](../raw/web/tech2.txt) |
| tech3 | Slack enterprise search API AI apps permission search context shared channel Glean permission aware search Atlassian Rovo permissions docs | [本地证据](../raw/web/tech3.txt) |
| tech4 | OpenHands repository microagents keyword triggers official documentation Qoder Repo Wiki generation update Qwen Code GEMINI.md JIT Gemini CLI hierarchical context | [本地证据](../raw/web/tech4.txt) |
| tosem | software developer expertise recommendation code reviewer recommendation "TOSEM" authors systematic literature review code review TOSEM code reviewers / software development agent context instructions "ACM Transactions on Software Engineering and Methodology" retrieval augmented code generation repository level survey | [本地证据](../raw/web/tosem.txt) |
| venue | site:conf.researchr.org ISSTA test selection regression testing Ekstazi STARTS change impact test selection ASE TOSEM TSE program comprehension developer tasks empirical information | [本地证据](../raw/web/venue.txt) |