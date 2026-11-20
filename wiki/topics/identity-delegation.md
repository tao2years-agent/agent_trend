# Agent 身份、委托与权限

## 需要区分的五种主体

| 主体 | 作用 | 不应被谁替代 |
|---|---|---|
| Human principal | 发起、批准、承担业务责任 | Agent 身份 |
| Organization/Tenant | 定义信任域、政策和数据归属 | 一个群或一个项目名称 |
| Agent identity | 标识哪个 Agent/版本在行动 | 创建者账号 |
| Runtime/workload identity | 标识哪次运行、哪台沙箱在请求资源 | 长期 Agent identity |
| Connection/credential identity | 对外系统实际看到的账号 | “用户要求我做”这段文字 |

## 两种合法权限模型

1. **用户委托型**：Agent 以调用用户的权限执行，适合个人助手和敏感操作。令牌应短期、降权、限定 audience、tool、resource、purpose 和最大影响。
2. **Agent 自有权限型**：团队 Agent 使用服务账号/共享连接，适合无人值守和跨成员流程。必须有 owner、审批、访问清单、额度、轮换、撤销和持续审计。

混合模型最常见：服务账号读取团队数据，某个用户批准写操作，实际写入以该用户或受控 workload identity 执行。ChatGPT Team Tasks、Notion Custom Agents 和 Gemini Agent Identity 都证明不能用一种权限语义覆盖全部场景。[研究推断]

## 技术要求

- 身份与能力声明可验证，避免仅相信自然语言 Agent Card。
- 每次工具调用携带可审计的授权链：issuer → organization → human/agent → runtime → action。
- 令牌 exchange 时逐跳缩小权限，禁止把宽权限 bearer token 原样传给子 Agent。
- Agent 间调用由 Gateway/PDP 再授权，而不是把上游“已批准”当通行证。
- 高风险动作支持 step-up authentication、双人审批、时间窗和金额/数据量阈值。
- 离职/转岗触发 Agent owner 转移、凭据撤销和未完成任务处理。

## 标准位置

MCP 的 HTTP 授权用于 client 代表资源所有者访问 server；企业托管授权扩展让组织通过 IdP 集中控制 MCP server 访问。A2A 处理 Agent 发现与任务通信。OpenID AAuth 正在解决 Agent 如何证明自己、代表谁、如何跨信任域取得授权。它们互补而非互相替代。
