# Repository Checkpoint

## 2026-11-20 · GitHub 可复用发布

- 当前主研究已经迁移到 [`research-harness/round2/`](../research-harness/round2/index.md)；其 [`checkpoint`](../research-harness/round2/state/checkpoint.md) 和 [`coverage`](../research-harness/round2/state/coverage.md) 是继续该主线的权威状态。
- 根级 [`INDEX.md`](../INDEX.md)、[`AGENTS.md`](../AGENTS.md) 与 [`DEVELOPMENT.md`](../DEVELOPMENT.md) 提供跨环境导航、证据规则和构建入口。
- 仓库准备发布到 `tao2years-agent/agent_trend`；二进制原始证据和渲染产物使用 Git LFS，文本证据保留标准 Git diff。
- 下方 2026-11-16 内容是最早的 AI Agent 组织协作基线，保留用于历史追踪，不代表当前主研究的覆盖状态。

## 2026-11-16 · 初始基线

更新时间：2026-11-16。

## 已完成

- 建立 Karpathy LLM Wiki 式目录、研究协议与来源台账。
- 定位并核对 28 个官方/标准组织来源。
- 完成 7 类产品横向矩阵、5 个产品页、7 个机制/设计页。
- 完成产品与技术深度报告。
- 建立抓取脚本、HTML 生成与 lint 工作流。
- 离线 HTML 已在真实 Chrome 中验证桌面/390×844 移动视口、目录筛选、移动目录展开与控制台日志；均通过。

## 当前限制

- 本机脚本无法通过代理访问外网；raw 中为不可变失败 metadata，尚无完整页面快照。
- 未登录产品进行运行时实验；所有产品行为基于官方材料，不声称实测。
- 跨组织能力大多为“未找到证据”，不能解读成确认不支持。

## 下一步

1. 在可联网环境运行 `python scripts/fetch_sources.py --refresh-date <date>`（脚本后续可扩展参数）补齐 raw。
2. 用企业试用账号设计权限/外部成员/自动任务/撤销实验矩阵。
3. 补充定价、地域、部署和数据保留对比；这些信息变化快，需单独时间戳。
4. 建立 A2A + Agent Auth 的跨域最小原型，验证委托链和 trace 对账。
