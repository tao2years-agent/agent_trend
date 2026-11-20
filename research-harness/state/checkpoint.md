# 2026-11-20 研究检查点

<!-- second-edition -->
**2026-11-20 决策版**　[深度分析](../outputs/deep-report-v2.html) · [四页决策稿](../outputs/insights-decision.html) · [分享 PDF](../outputs/insights-decision.pdf) · [复核 Wiki](../round2/index.md)。下方早期交付与当时覆盖数保留供追溯。
<!-- /second-edition -->

[深度分析](../outputs/deep-report.html) · [离线分享](../outputs/insights.html) · [分享 PDF](../outputs/insights.pdf) · [竞品矩阵](../outputs/product-matrix.csv) · [专题 Wiki](../wiki/index.md)

本期完成 50 个产品/项目/组件、20 项学术工作及 22 条工程与对照材料的判读。50 项中 36 项核对固定修订实现。5 个不同项目有局部实验，商业端到端与内部团队效果实验均未执行。源表含 236 个引用指针。具体计数与完整性校验以 [coverage.json](coverage.json)、[audit.json](audit.json) 及 [reader-check.json](reader-check.json) 为准。

## 接着研究什么

1. 先取得同一服务同期合格任务全集、失败日志、服务 owner 与上线时间。当前资料没有内部样本，尚不能判断本企业最大的等待点。
2. 用历史数据分别测纯规则基线、人工整理的理想证据包、受限 agent。若人工理想证据包都不能改变下一步，换选题。
3. 同一提交在托管执行、权限继承、审批过期和中断恢复上的实际结果仍需企业沙箱账号。采购判断还需所在地区、支持套餐及调用成本。
4. 源码复核未逐版本遍历。后续先更新高影响差异：Jules 计划退场、GitLab 定时自动化、Argo Rollouts 候选版本、新版 LangGraph 和 OpenSandbox。新状态保存新版本证据。
5. METR 后续数据的选择偏差、受删节的 AI 研发案例、开源公开会话代表性和跨团队评审等候效应保留为未决项，不用补猜数字。
