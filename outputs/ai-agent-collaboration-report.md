# AI Agent 办公软件：从单体执行到组织与跨组织协作

研究基线：2026-11-16（Asia/Shanghai）  
研究对象：Tencent WorkBuddy、千问办公、ChatGPT Work/Codex、Claude/Claude Code；参照 Microsoft 365 Copilot Agents、Gemini Enterprise/Agent Platform、Notion Agent/Custom Agents。  
方法：Karpathy LLM Wiki 式证据库；官方资料优先；事实、推断和建议分层。

## 一、执行摘要

AI Agent 办公产品正在经历一次比“聊天→执行”更重要的转型：从服务单个用户的 Agent，转向参与团队工作、持有组织身份、持续运行、共享上下文并受组织治理的数字协作者。

本轮研究得到六个核心结论：

1. **多 Agent 不等于团队协作。** WorkBuddy 的专家团队、Codex/Claude Code 的 subagents 或 agent teams 主要解决任务并行与专业分工；只有当多人能共同定义目标、查看状态、编辑产物、分配责任和治理 Agent 时，产品才进入组织协作。
2. **共享空间正在成为新的产品内核。** 千问办公的协作空间、ChatGPT Teams/Space、Notion workspace、Slack/Teams/Claude Tag 等表明，Agent 的主入口会从“个人聊天框”转向项目空间、频道、任务和文档。
3. **最关键的技术对象是身份与委托，不是模型。** 组织必须知道 Agent 代表谁、使用谁的凭据、访问什么、能否再委托、谁承担成本和责任。Team service account、用户委托、Agent-owned identity 不能混成一个“已授权”。
4. **产物应脱离对话成为组织资产。** 统一文件、资料空间、Space 页面/Slides、Notion pages、repo/PR 都将 Agent 输出变成可版本化、共享、评论和审计的对象。
5. **当前成熟能力主要局限在单租户内部。** 核心样本公开资料足以证明跨部门或同 workspace 协作，但不足以证明完整跨企业 Agent federation。把 Slack/Teams 外部频道、A2A 或 MCP 直接等同为跨组织安全协作，会高估产品成熟度。
6. **跨组织的机会在“信任与责任层”。** A2A、MCP、OAuth/OIDC、Agent Identity/Agent Auth 正提供通信和授权基础；真正缺少的是可理解的双边授权、目的限制、最小数据披露、双边审计、撤销、保留、结算与争议处理产品。

## 二、市场与产品形态

### 2.1 Tencent WorkBuddy：从超级个体到 AI 专家团队

WorkBuddy 公开产品结构覆盖个人 Agent、云端助理和多 Agent 项目空间。官方产品页称多个 Agent 可在项目空间并行工作，专家、Skill 和连接器可沉淀复用；腾讯官方文章描述一个团队负责人自动拆解任务，多位专家并行并共享信息，最后整合为一份文件，而非多份零散笔记。[WorkBuddy 产品页](https://cloud.tencent.com/product/workbuddy)、[腾讯官方文章](https://www.tencent.com/zh-cn/your-new-ai-colleague-brought-a-few-friends/)

其优点是“专业角色 + 执行 + 可验收交付”，对普通职场用户比 CLI 友好。但当前公开证据更强地支持“一个人调用 AI 团队”和“组织内复用能力”，对多人共同任务、细粒度产物权限、Agent owner/lifecycle 及跨企业协作的说明较弱。因此，产品设计者不应只复制“100 个专家”，更应补上 Agent 成为组织资产后的治理模型。

### 2.2 千问办公 2.0：把数字员工放进协作空间

千问办公是本轮最直接面向 Team Agent 的样本。官方将协作空间、数字员工小Q、空间记忆、待办、定时任务、资料空间、人机共创和端云一体连接起来。协作空间可关联钉钉群聊、听记、表格和文档，成员用原生 IM 交办；空间记忆可查看、纠正和停用；自动任务可由事件或计划触发，纯云端任务可在电脑关闭后运行。[千问办公 2.0](https://docs.qwenwork.cn/podcasts/qwenwork-2-team-agent)、[协作空间](https://docs.qwenwork.cn/web/collaboration)

它最值得借鉴的是将协作问题拆成三条链：

- 信息链：讨论与资料进入共同上下文，接手者不从零解释。
- 行动链：Agent、待办、看板、定时/事件触发维持推进。
- 成果链：资料空间保存和复用产物，人和 AI 在同一成果上继续修改。

边界同样明确：协作空间按企业组织使用，成员从当前企业中选择；群聊关联需要审批，申请并不等于取得读取权限；企业管理员权限和开放平台 API 权限是不同控制面。[隐私与安全](https://docs.qwenwork.cn/getting-started/privacy-security)、[管理员角色](https://docs.qwenwork.cn/enterprise-ultimate/organization/admin-roles)

### 2.3 ChatGPT Work / Codex：多表面协作系统

OpenAI 的路径不是一个独立办公套件，而是组合：Work 完成长任务；Teams/Team Tasks 组织团队自动化；Space 承载页面、幻灯片和共享内容；Slack/Teams surface 将 Agent 放进沟通场所；Codex 提供代码执行、云环境和 subagent workflows。[Working with agents](https://learn.chatgpt.com/docs/working-with-agents)

最重要的产品机制是执行身份分层。Team Tasks 在云端用团队服务账号和已配置连接运行；Slack 中请求 Codex Cloud 时，surface 服务账号用于查找环境，任务仍以请求用户身份运行。[Teams and Team Tasks](https://learn.chatgpt.com/docs/enterprise/teams)、[@ChatGPT in Slack and Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams)

这套架构揭示了组织 Agent 的两种权限语义：

- `acts as me`：严格继承当前用户权限，适合个人敏感操作。
- `acts for the team`：使用团队服务账号，适合持续自动化，但可能让用户间接使用自己没有的源系统权限。

管理员还需分别治理 Work Cloud、Work Local、Codex Local、Codex Cloud、workspace RBAC、plugins/apps、shared connections 和 source-system ACL；官方明确这些不是统一的一个控制层。[Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq)

### 2.4 Claude / Claude Code：repo-native 与 channel-native

Claude Code 的组织能力建立在软件工程协作底座上：共享 `.claude/settings.json` 随代码库分发，个人 local 设置留在本机，组织 managed settings 施加最高优先级政策。多 Agent 用于任务内部并行；Claude Tag 则进入 Slack channel，成为一个可以被多人 @、共享上下文和接续对话的 Claude。[Claude Code settings](https://code.claude.com/docs/en/settings)、[Claude Tag](https://www.anthropic.com/news/introducing-claude-tag)

它说明团队 Agent 未必需要新建一套办公 UI：代码仓库、PR、CI 和 Slack channel 已经提供版本、review、责任与通知。但 repo-native 的治理假设不能直接搬到非技术办公：普通文档、CRM 操作和对外沟通缺少 Git 的变更审查与回滚语义，需要产品补上审批、版本和副作用控制。

### 2.5 平台参照

- **Microsoft 365 Copilot Agents** 把 Agent 当作可分享、可共同拥有、可上架和可治理的租户应用；Agent inventory、组织目录、admin policy、Purview audit/eDiscovery 是组织规模化的参照。[Admin guide](https://learn.microsoft.com/microsoft-365/copilot/agent-essentials/m365-agents-admin-guide)
- **Gemini Enterprise/Agent Platform** 将 Agent Identity、Registry、Gateway、IAM、policy enforcement 和 traces 放入平台层；这是跨系统/跨 Agent 技术治理的强参照。[Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/agents)
- **Notion** 明确区分按用户权限行动的 Notion Agent 和拥有自身权限、触发器、owner、预算及活动日志的 Custom Agent。该分型非常适合作为产品信息架构基线。[Notion Agent](https://www.notion.com/help/notion-agent)、[Custom Agents permissions](https://www.notion.com/help/custom-agents-sharing-and-permissions)

## 三、横向产品设计框架

### 3.1 先确定产品的“协作单元”

单体 Agent 的协作单元是 conversation；组织 Agent 的协作单元应是 workspace/case/project，内部至少包含目标、成员、任务、上下文来源、Agent roster、产物、决策与审批。否则用户只能“共享聊天链接”，无法交接真实工作。

### 3.2 角色设计

必须显式区分 requester、task owner、reviewer/approver、agent owner、data owner、workspace admin/security 和 external collaborator。一个人可兼任多个角色，但系统不能假设创建者永远是 owner 或审批者。

### 3.3 Agent 分型

| 类型 | 权限来源 | 典型使用 | 生命周期 |
|---|---|---|---|
| Personal Agent | 当前用户委托 | 私人整理、草拟、个人工作流 | 随用户/会话 |
| Team Agent | 组织服务身份或受控共享连接 | 团队例会、项目跟踪、业务自动化 | owner + 预算 + 版本 + 下架 |
| External Agent | 外部组织的联邦身份 | 客户/供应商协作、跨企业任务 | 双边 grant + 合同 + 可撤销 |

### 3.4 上下文与记忆

组织记忆不能是不可见的向量库。每条关键记忆应有来源、适用空间、可见人群、更新时间、置信度、事实/推断类型和过期时间，并允许查看、纠正、停用。原内容删除或权限收回时，系统要明确摘要/副本是否仍保留。

### 3.5 产物与共同编辑

Agent 结果应默认进入可版本化 Artifact，而不是停在 transcript。Artifact 要有独立 ACL、草稿/审核/发布状态、来源与修改历史。外部分享要区分引用原对象、复制内容和通过 Agent service 间接访问三种语义。

### 3.6 主动性与可控性

主动 Agent 需要可见规则、运行记录、失败原因、下一次运行时间、暂停、立即运行、重跑和 kill switch。高风险动作采用“Agent 先准备，人再判断”；无需把每个读取动作都弹窗，也不能让定时任务自动取得更高权限。

## 四、跨组织协作：真正未被解决的部分

跨部门通常共享一个 IdP、法务主体和管理员；跨企业则进入不同信任域。产品至少要表达：对方是谁、Agent 由谁签发、代表谁、要求什么能力、要看哪些数据、会把结果带到哪里、谁付费、保留多久、谁负责。

### 4.1 推荐对象模型

- Trust Relationship：双方组织与 Agent issuer 的信任关系。
- Collaboration Contract：目的、数据类别、允许动作、地域、保留、二次使用、责任和退出。
- External Agent Grant：授权给具体 Agent/版本/能力，限定资源、期限、最大动作和预算。
- Shared Case：双方可对账的 task ID、状态、产物摘要、审批和事件。
- Disclosure Event：内容从一域复制/摘要到另一域的显式事件。
- Incident/Revocation：吊销身份、冻结任务、保全证据和通知对方的流程。

### 4.2 标准分工

A2A 用于 Agent 发现、任务消息和异步协作；MCP 用于 Agent/应用访问工具与数据；OAuth/OIDC/Agent Auth 处理身份与委托。它们不解决业务合同和最终责任。[A2A](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)、[MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)、[OpenID AAuth](https://openid.net/wg/aauth/charter/)

### 4.3 推荐渐进路线

先做受控 external guest，再做 bilateral federation，最后才开放动态 Agent 网络。第一阶段让一个组织托管空间并限制 guest；第二阶段引入双方 Agent identity、结构化 grant 和双边审计；第三阶段才允许 Agent 动态发现和协商能力。这样能先验证业务责任与用户体验，再承担开放网络的安全复杂度。

## 五、技术架构重点

### 5.1 身份与授权

至少保存 human principal、tenant、agent identity、runtime/workload identity、acting credential 五类身份。每次工具调用记录完整授权链。子 Agent 或外部 Agent 使用 token exchange 获得更窄、短期、限定 audience/purpose 的凭据，禁止传递上游宽权限 token。

### 5.2 Durable workflow

长任务状态必须在模型上下文之外持久化。工作流引擎管理状态、依赖、审批、checkpoint、重试、幂等和补偿；模型负责生成计划和处理非结构化信息。对发送消息、修改 CRM、付款、删除等副作用动作设置幂等键和二次确认。

### 5.3 Context broker

检索请求携带 user/agent/tenant/purpose/classification；按源系统 ACL 过滤并保留 provenance。向量索引不能只靠 metadata filter 做租户隔离，底层对象存储、缓存、队列、trace 和 billing 都要贯穿 tenant_id。

### 5.4 Agent gateway

所有 Agent→Tool、Agent→Agent 调用经过统一 Gateway：认证、PDP、schema validation、DLP、内容检测、限流、预算和 trace。MCP/A2A adapter 只是接入层，Gateway 才是组织策略执行点。

### 5.5 运行时

本地、托管云、自托管 runner 各有不同文件、网络、凭据和数据驻留边界。任务创建时就应绑定 execution profile；不要在运行中无提示迁移。凭据通过 secrets broker 按任务短期下发，环境销毁后失效。

### 5.6 可观测与审计

端到端 trace 至少关联 `task → agent/version → delegation → tool/resource → policy decision → approval → artifact → cost/outcome`。日志内容级别需可配，避免为了审计永久保存全部敏感 prompt；可以使用摘要、哈希、分类标签和有限保留期。

## 六、安全与治理重点

最高风险不是模型“答错”，而是错误在共享权限和自动化下被放大：

- Confused deputy：低权限用户利用团队 Agent 的高权限连接获取信息或执行动作。
- Delegation escalation：下游 Agent 得到比上游任务更宽的权限。
- Prompt injection：外部文档/网页把数据带出或改变工具调用。
- Memory poisoning：错误或恶意内容进入团队长期记忆。
- Orphan agent：owner 离职后 Agent、凭据、定时任务和预算仍存活。
- Duplicate side effects：重试造成重复发送、重复修改、重复交易。
- Supply-chain drift：Skill/MCP/插件更新后权限和行为发生变化。

对应控制包括最小权限、逐跳授权、来源/指令隔离、可治理记忆、owner transfer、幂等/补偿、版本固定/签名/变更审批，以及按 Agent/团队/任务的预算和异常告警。

## 七、建议路线图

### Phase 1：组织内可信协作

建立 space、任务、Artifact、可见记忆、Personal/Team Agent 分型、acting identity、owner、预算、运行记录和审批。优先打磨一个高频闭环，例如项目周报与风险跟进，而不是先堆专家数量。

### Phase 2：治理与持续自动化

加入 Agent catalog、版本/发布、事件触发、durable workflow、连接器治理、成本/质量评估、orphan 处理、本地/云/自托管策略。

### Phase 3：跨组织受控协作

从 guest space 开始，加入 collaboration contract、external grant、最小披露、双边 trace；之后接 A2A/Agent Auth。将“外部 Agent 可访问什么”和“外部组织的人可看到什么”分成两套权限。

## 八、待验证事项

1. WorkBuddy 企业版 Agent owner、细粒度 RBAC、运行日志、凭据和外部成员模型。
2. 千问协作空间的空间管理员/普通成员/数字员工在每类数据源上的实际权限矩阵，以及跨组织钉钉群的处理。
3. ChatGPT Teams/Team Tasks、Slack/Teams surface 对外部频道参与者的实际行为和历史产物可见性。
4. Claude Tag 在 Slack Connect、外部成员、频道记忆和离职/撤销场景中的边界。
5. Microsoft/Google/Notion 跨 tenant/workspace 的 Agent 分享和审计责任。
6. A2A + Agent Auth 在多跳委托、权限传播、撤销和双边 trace 对账上的运行时实验。

这些事项需要真实企业账号/沙箱实验；本轮未实测，不应从文档机制直接推出可靠性或安全保证。
