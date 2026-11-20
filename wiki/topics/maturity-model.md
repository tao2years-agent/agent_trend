# 从单体 Agent 到组织协作：成熟度模型

## 五级模型

| 层级 | 协作对象 | 典型能力 | 常见误判 |
|---|---|---|---|
| L0 单体助手 | 一个人 + 一个会话 | 问答、生成、局部工具调用 | 能生成文件就叫“办公平台” |
| L1 个人执行 Agent | 一个人 + 长任务 | 规划、工具、云端/本地执行、可验收交付 | 自动执行就叫“团队协作” |
| L2 多 Agent 工作组 | 一个人 + 多 Agent | 分工、并行、汇总、内部通信 | AI 团队等于多人团队 |
| L3 团队协作 Agent | 多人 + Agent + 共享资产 | 空间、角色、共享上下文、待办、共创、运行记录 | 同租户协作等于跨组织 |
| L4 组织治理平台 | 多团队 + Agent portfolio | Agent 目录、owner、RBAC、预算、版本、审计、下架 | 有 admin console 就已解决运行时授权 |
| L5 跨组织 Agent 网络 | 多信任域的人与 Agent | 联邦身份、能力发现、委托链、双边政策、可对账审计 | 支持 A2A/MCP 就天然安全合规 |

## 核心判断

WorkBuddy 的公开能力覆盖 L1–L3 并开始进入 L4；千问办公 2.0 重点落在 L3/L4；ChatGPT Work/Codex 是多个 L2–L4 表面的组合；Claude Code 从 repo-native L2/L4 向 Slack multiplayer L3 扩展；Microsoft、Google、Notion 在 Agent 资产治理上提供了更成熟的 L4 参照。

没有足够官方证据把任何核心样本直接判为完整 L5。A2A、MCP、Agent Identity 和 Agent Auth 是 L5 的必要基础，却不包含商业责任、数据用途限制和争议处理的完整产品语义。
