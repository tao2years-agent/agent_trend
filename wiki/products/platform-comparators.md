# 横向参照：Microsoft、Google、Notion

## Microsoft 365 Copilot Agents：Agent 是租户应用资产

Microsoft 的强项是分发与合规：Agent 可有多个 owner，可分享给指定用户或整个组织，可提交组织目录；管理员管理 inventory、访问、共享、发布、部署、阻止，并借助 Purview 做审计/eDiscovery。它提示产品设计者：Agent 不只是会话或 Prompt，而应有 owner、版本、目录状态和下架流程。[官方事实 + 规划启示]

## Gemini Enterprise：Agent Identity + Gateway

Gemini Enterprise/Agent Platform 提供最清晰的技术治理参考：独立的 Agent Identity（SPIFFE 形式）、Agent Registry、Gateway、IAM、策略执行、日志/指标/trace，以及用户委托工具访问。其 Agent Designer 还揭示一个关键风险：共享 Agent 时，使用者可能通过 Agent 查询关联数据，即使没有底层数据的直接权限。[官方事实]

这个设计并非必然错误，但产品必须明确选择：Agent 是“按调用者权限裁剪”，还是“以自身权限提供受控服务”。两者应在 UI、审计和风险分级上完全不同。[研究推断]

## Notion：个人代理与团队代理分型

Notion Agent 按当前用户权限行动；Custom Agent 则像独立团队成员，拥有自己的资源权限、触发器、owner、预算和活动记录。Custom Agent 甚至可以跨内部权限边界向使用者返回信息，这是被设计出来的能力，而非偶然副作用。[官方事实]

这给出一个非常值得复用的产品模型：

- `Personal agent`：用户的延伸，权限随用户，离职即失效。
- `Team agent`：组织拥有的服务主体，权限独立，需 owner、资金来源、生命周期和管理员兜底。
- `External agent`：另一个信任域拥有的主体，必须经过联邦、合同和双边审计；当前主流办公产品仍缺成熟开箱方案。[规划建议]

## 证据

- [Microsoft Agents admin guide](https://learn.microsoft.com/microsoft-365/copilot/agent-essentials/m365-agents-admin-guide)
- [Microsoft Agent sharing](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/copilot-studio-lite-share-manage-agent?view=o365-worldwide)
- [Google Agent Designer](https://support.google.com/g/answer/16540723?hl=en)
- [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/agents)
- [Notion Agent](https://www.notion.com/help/notion-agent)
- [Notion Custom Agents permissions](https://www.notion.com/help/custom-agents-sharing-and-permissions)
