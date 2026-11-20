# 跨组织协作：信任域、协议与责任

## 先定义“跨组织”

下列场景风险不同，产品不能都叫“外部协作”：

1. 同一企业不同部门：一个 IdP/租户，政策相对统一。
2. 外部 guest：一方租户承载空间，外部人获得受限席位。
3. 共享渠道：Slack Connect/Teams 等宿主提供跨企业对话，但 Agent 归属可能仍在单方。
4. Agent-to-Agent federation：双方 Agent 在各自组织运行，通过协议委托任务。
5. 多方业务网络：客户、供应商、平台、审计方共同参与，存在合同、结算和监管责任。

核心样本公开资料大多停留在 1，少量可能借宿主平台触达 2/3，但本轮未核实完整 4/5。

## 跨组织产品需要新增的对象

- `Trust relationship`：双方组织、信任期限、允许的 agent issuer 与协议版本。
- `Collaboration contract`：目的、数据类别、允许动作、留存、地域、二次使用、责任和退出。
- `External agent grant`：对具体 Agent/版本/能力的授权，而非对整个厂商域名放行。
- `Shared case/task`：双方都能对账的任务 ID、状态、产物摘要和决策记录。
- `Disclosure policy`：哪些上下文可发送、哪些只能在本域计算后返回结论。
- `Revocation/incident`：即时吊销、任务冻结、证据保全和双边通知。

## 协议只覆盖一部分

- A2A：能力发现、消息/任务交换、异步状态与 Agent 协作接口。
- MCP：Agent/应用到工具和数据源的标准入口。
- OAuth/OIDC/Agent Auth：身份、委托、token exchange 和跨域授权。
- 业务产品层：目的限制、审批、数据最小化、责任、计费、争议、用户体验。

因此“支持 A2A”只能证明能通信，不能证明对方 Agent 值得信任、任务有权执行、结果可以共享或法律责任已经明确。[研究推断]

## 推荐的默认交互

外部 Agent 首次请求时展示：对方组织与 Agent issuer、所求能力、拟访问的数据类别、预期输出、最长运行时间、成本承担方、写操作范围和保留策略。用户批准的是一个结构化 grant，不是一句“允许这个 Agent 帮忙”。

跨域工作优先采用“数据留在本域，返回最小结果/证明”的模式。需要复制内容时，把复制行为本身作为可审批、可撤销（若技术允许）、可审计的 disclosure event。

## 证据

- [Linux Foundation A2A announcement](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [MCP Enterprise-Managed Authorization](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/extensions/auth/enterprise-managed-authorization.mdx)
- [OpenID Agent Auth WG](https://openid.net/wg/aauth/charter/)
- [NIST agent identity design tenets](https://www.nist.gov/blogs/cybersecurity-insights/design-tenets-agent-identity-management-systems)
