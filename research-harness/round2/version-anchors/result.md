# 十项采购判断的历史锚点

35 项采购比较中，有些证据能支持明确的发布日，有些只能定位一个受支持的版本或网页说明。本轮选出需要补强的 10 项，逐项核对厂商原文的日期、适用对象与变更含义。它们是额外的历史锚点；有完整窗口分母的 6 条产品线另见[逐版本审计](../evolution/result.md)。原始公告与本地摘要记录在[来源清单](sources.json)，没有把页面的最后更新时间当作功能首发。

|产品与时点|能定位到的变更|对采购或设计的影响|
|---|---|---|
|Moderne，2026-05-19|厂商发布 Changelog，按 changeset 对同次改动关联的多个仓统一展示，区分已可处理和仍阻塞的变更，并提供 API/MCP 查询。文章中还有未来时的 agent 推理轨迹计划。|跨仓状态已是可采购的能力。问能否看到“做了什么”和“为什么做”时，要求供应商在当前租户分别演示。[厂商公告](https://moderne.ai/blog/moderne-changelog-multi-repository-change-intelligence)|
|阿里云云效，2026-08-01 生效|架构调整公告区分此前代码评审场景的免费能力、全模块 AI 助手开始计费以及推荐站点调整。|可用入口、工作区站点和计费对象都会改变迁移成本。不能把旧代码评审为免费推广为全平台长期免费。[生效公告](https://help.aliyun.com/zh/yunxiao/product-overview/alibaba-cloud-devops-ai-assistant-upgrade-and-site-architecture-adjustment)|
|SonarQube Server，2025.5 版本说明|在 2025.6 的历史汇总页，2025.5 小节说明因工具升级出现的部分问题可进入 sandbox，暂不影响质量门禁，留待项目成员处置。页面另提示 2025.6 当前不再获补丁。|升级检测器可改变“失败”工作量；采购验收需演示新增问题是否硬阻断、谁消化例外和过渡期后如何处理。[按版本记录](https://docs.sonarsource.com/sonarqube-server/2025.6/server-update-and-maintenance/release-notes)|
|Mergify，2026-11-12|允许用户在 PR 仍等待检查和批准时先勾选排队，到条件满足才入队。勾选后推送新提交会取消该请求。|“表达排队意向”和“批准当前 head”应存为不同事件，尤其需要把换版后的旧意向作废。[发布原文](https://docs.mergify.com/changelog/2026-11-12-queue-a-pull-request-before-its-ready/)|
|LaunchDarkly，2025-05-14|Guarded rollouts 增强在开跑前验证 flag 与 metric 是否正常发出，并可自定义持续时间。|观测缺失和没有回归表现不同。应单独演示遥测中断时流量是否继续，及其与部署回滚的边界。[公告](https://launchdarkly.com/changelog/guarded-rollouts-improvements/)|
|Spacelift，Self-hosted v5.1.1 说明|官方给出由已弃用的 initialization/task policies 迁移至 approval policy 的条件，后者对 run 和 task 统一表达，并增加 review 状态和人工决定。这个版本化页面没有足够证据确定机制首次上线日。|旧策略和新策略同时存在时，应核验拒绝和通过的优先级以及人能取消哪个动作。[版本化迁移指南](https://docs.spacelift.io/self-hosted/v5.1.1/concepts/policy/deprecated/migrate-to-approval-policy)|
|Snyk Open Source，2026-02-04 Early Access|Breakability Analysis 给建议的依赖升级 PR 标出兼容性风险；当时须显式打开预览，公告还说明了数据处理条件。|风险评分是安排验证与 review 的信息，不能代替消费者的测试或授予合并权。[预览公告](https://updates.snyk.io/merge-with-confidence-introducing-breakability-analysis-for-pull-requests/)|
|Rootly，2026-11-12|在 Microsoft Teams 引入调查、追问、呼叫值班者及接班摘要；若干操作需在聊天界面确认。|入口变化不修订所有自动调查的连接器权限；对有写权限的 Private Agent 与原生调查分开核对。[Teams 公告](https://rootly.com/changelog/investigate-page-and-catch-up-without-leaving-microsoft-teams)|
|Datadog，2025-12-02|厂商宣布 Bits AI SRE 一般可用。当前指向 Bits Investigation 的文档与当时的发布名称分别记录。减少 MTTR 的数字若来自个别客户，需回到其基线。|核价和选型先确认调查结果的交付方式、集成、是否有恢复证据，不能将调查 GA 解释成可自动恢复一切告警。[一般可用公告](https://www.datadoghq.com/newsroom/press-releases/datadog-launches-bits-ai-sre-agent-to-resolve-incidents-faster/)|
|Sentry，2026-04-28|Seer Agent 面向问答与调试的发布文给出 open beta 阶段，并区别若干接入界面。Issue Fix API 的 stopping point 是另一可具体查证的能力。|将对话入口和后台工作对象分开询价和验收，为异步任务保存可重查的运行 ID；不能从当时的 beta 公告倒推出今天所有 API 的发布阶段。[产品公告](https://blog.sentry.io/introducing-seer-agent/)|

实际筛查中，云效总目录本身只是导航，追到调整公告才获得生效日期。Sentry 页面靠前的一个 article 节点是其他文章推荐，重新定位到主标题所在正文，才获得 Seer 的 beta 状态。LaunchDarkly 支持站原页本地抓取失败，保留失败并改用厂商有日期的改进公告。
