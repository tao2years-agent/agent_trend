# AI Agent 组织协作知识库

<!-- second-edition -->
**2026-11-20 决策版**　[深度分析](../research-harness/outputs/deep-report-v2.html) · [四页决策稿](../research-harness/outputs/insights-decision.html) · [分享 PDF](../research-harness/outputs/insights-decision.pdf) · [复核 Wiki](../research-harness/round2/index.md)。下方早期交付与当时覆盖数保留供追溯。
<!-- /second-edition -->

- [组织级研发自动化、人工接管与效能度量专题（2026-11-20）](../research-harness/wiki/index.md)

- [企业研发的组织级上下文与团队记忆专题（2026-11-18）](../org-context/wiki/index.md)

> 查询从本页进入；基线日期：2026-11-16。`官方事实`、`研究推断`、`规划建议`在各页分别标注。

## 执行摘要

AI 办公产品的竞争焦点已经从“模型能否完成任务”迁移到“工作是否能在多人、多个 Agent、多个系统和多个责任主体之间连续流转”。真正的组织协作产品需要同时管理六种对象：人、Agent、任务、上下文、产物和权限。只提供多 Agent 并行，仍然只是更强的单人生产力工具。

当前主流产品的成熟区主要是**单租户组织内协作**：共享空间、共享连接、团队 Agent、任务自动化、资产目录和审计。公开证据尚不足以说明任何核心产品已经完整解决两个独立企业之间的 Agent 联邦协作。跨组织能力目前更接近“基础设施正在形成”：A2A 解决 Agent 发现/任务通信，MCP 解决工具与数据接入，OpenID Agent Auth 与 NIST 工作聚焦跨信任域身份和委托；但业务合同、数据使用边界、责任归属、撤销与争议处理仍需产品层实现。

## 产品页

- [Tencent WorkBuddy](products/workbuddy.md)
- [千问办公 2.0](products/qwenwork.md)
- [ChatGPT Work / Codex](products/openai-work-codex.md)
- [Claude / Claude Code](products/claude-code.md)
- [横向参照：Microsoft、Google、Notion](products/platform-comparators.md)

## 机制与设计页

- [从单体 Agent 到组织协作：成熟度模型](topics/maturity-model.md)
- [协作内核：共享上下文、任务与产物](topics/collaboration-kernel.md)
- [Agent 身份、委托与权限](topics/identity-delegation.md)
- [跨组织协作：信任域、协议与责任](topics/cross-organization.md)
- [治理、安全、审计与成本](topics/governance-security.md)
- [技术参考架构](topics/technical-architecture.md)
- [产品设计清单与路线图](topics/product-design.md)

## 研究状态

- [来源与覆盖](../state/coverage.md)
- [未决问题](../state/open-questions.md)
- [当前 checkpoint](../state/checkpoint.md)
