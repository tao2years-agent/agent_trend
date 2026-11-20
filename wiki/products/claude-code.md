# Claude / Claude Code

## 判断

Claude Code 的组织化路径以代码仓库为协作底座：团队把 `.claude/settings.json`、指令、插件和 Hook 随仓库共享，组织再用 managed settings 施加更高优先级的政策。Agent teams/子 Agent 主要解决同一任务内的并行工作；Claude Tag 则把 Agent 作为共享成员放进 Slack channel，让频道参与者看到任务并接续对话。[官方事实]

## 两种协作范式

1. **repo-native**：代码、版本控制、review 和 CI 天然提供共享对象与变更历史。Agent 参与的是已有软件工程协作系统。
2. **channel-native**：Claude Tag 在获准频道内与所有人互动、积累相关上下文、在 thread 中交付结果；官方称其为 multiplayer。

这两种范式比传统单体 CLI 更团队化，但“多 Agent 会互相通信”与“多人/多组织共同治理这些 Agent”仍是两件事。[研究推断]

## 治理

- 项目级共享设置可进版本库，但个人 local 设置留在本机。
- 组织 managed settings 可覆盖用户/项目设置，用于安全与合规。
- Team/Enterprise 提供席位、用量、审计/Compliance API 等管理能力。
- 本地、云端、自托管 runner 的设置与执行边界不同，应分别评估。

## 跨组织判断

Claude Tag 的公开页面证明了同一 Slack channel 中的多人共享 Agent；Claude Code 证明了同 repo 团队设置和多会话编排。本轮没有官方证据证明跨两个独立 Anthropic 组织的共享所有权、联邦授权或跨域审计。若底层 Slack channel 含外部成员，也需单独核实 Claude 的可见性、数据处理和管理员责任。

## 证据

- [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag)
- [Settings files and precedence](https://code.claude.com/docs/en/settings)
- [Claude Code and new admin controls for business plans](https://www.anthropic.com/news/claude-code-on-team-and-enterprise)
