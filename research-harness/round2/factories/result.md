# 四家公司怎样把后台 agent 接进真实研发

内部工程系统常先在一个组织里解决已有工具的连接、排队和验收问题。它们对自建还是采购很有参考价值，每周 PR 数等自报运营量仍不能换算成净节约。下面四家按谁承担环境、工具、审核和失败后的责任比较。它们不计入 35 个主采购对象。[快照清单](sources.json) · [渲染后的官方正文](rendered-sources.json)

|团队与现场|从触发到验收，人在何处|迁移到另一组织前要验证什么|
|---|---|---|
|Stripe Minions，2026-02 两篇工程报告|典型任务可从 Slack 发起，进入预热的隔离 devbox。blueprint 让 LLM 节点处理实现、修 CI 等不确定步骤，由确定性节点跑 lint、推分支。第一次完整 CI 失败可由自动修复或 agent 再试，第二轮后交给工程师。第一篇报告每周超过 1,000 个完全由 minion 产码且被合并的 PR，第二篇报告超过 1,300 个，均有人审。|先测重试预算何时交给人，能否让人接着已产生的环境和证据做事。公开材料没有给出所有尝试、相同工作量的人时、每项 PR 的下游影响；两个周规模不足以估计生产率趋势。[Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) · [Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)|
|Ramp Inspect；Ramp Sheets 维护|Inspect 为每次会话给出完整开发沙箱、多用户接入和可视预览。Sheets 团队在 PR 合并时生成监控，告警后先分诊：真问题起修复，噪声调整监控，已有修复 PR 则让后续运行停下。团队报告首周发现 40 个真实问题，也记录重复报警和阈值失准；合并保留工程师评审。|修改监控阈值会改变系统将来能看到的异常。试点应从原始流保留独立抽样，分开记录重复报警、真修复和错删检测。一个修复链接能帮助普通去重，不能充当并发写入的事务保证。[Inspect](https://engineering.ramp.com/post/why-we-built-our-background-agent) · [Sheets 现场](https://labs.ramp.com/research/ramp-sheets-self-maintaining/)|
|OpenAI 内部仓库的 harness engineering 与 Symphony|前者把工程约束写入仓库并机械检查，验收能包括改前/改后应用演示和自动后台清理。后者让 issue tracker 驱动工作区与并发运行。公开规范可查看调度、重试、reconciliation 与状态；文章在特定团队报告 landed PR 增幅，未提供按等价工作计算的组织对照。|先看已有 issue 状态谁有权修改、负责人退出后工作区如何回收、代码外的验收去哪里查。可复用规范验证编排，成本和效果必须用本团队的工作清单验算。[团队工程实践](https://openai.com/index/harness-engineering/) · [Symphony 说明](https://openai.com/index/open-source-codex-orchestration-symphony/) · [公开规范](https://github.com/openai/symphony/blob/main/SPEC.md)|
|StrongDM Software Factory，2026-02 公开实践|团队描述以外部 scenarios 表达端到端用户故事，使用外部依赖的行为替身（Digital Twin Universe）重复验证，并以组织规则移除逐行人工代码审查。人仍决定目标、场景与什么结果可接受。|对替身和真实服务定期做契约核对，保留未参与调优的场景，检查裁判误放。组织自述没有独立证明替身覆盖线上故障或人工监督成本归零。对需要指定审批人或真实目标回执的变更，仍从采购约束倒推设计。[现场叙述](https://factory.strongdm.ai/) · [技术与场景](https://factory.strongdm.ai/techniques)|

**裁判一致意味着什么。** 2026-11-17 的 Ramp 评测从曾合并的 Inspect 会话中取题，比对候选补丁和真实补丁。最初的评审把发现差异、判断差异是否重要混在一起；后来共享差异清单，分开判断并讨论分歧。72 个任务、360 次对比中，两位模型评审的一致数从 195 到 275，再到 337（54.2%、76.4%、93.6%）。原 PR 的工程师在小规模核验上与接近 90% 的任务判定一致，文章没有在该段给出这部分样本分母。两位模型达成共识与两者都正确是不同指标。适合借走的是“先给出证据、再判断重要性”及抽查分歧/一致样本；只从已经合并的会话取样会漏掉无人接手和失败放弃的任务。[Ramp 评测原文](https://builders.ramp.com/post/building-llm-judges-to-judge-llms) · [固定源登记](additional-sources.json)

**四种实现的共同前提。** 团队已经有一批可重复的工作、可创建的环境和能验收的人。可卖的产品机会取决于能替客户接下哪项现有劳动。若客户已有 CI、评审队列和独立测试团队，最先需要的可能只是找出一批共同失败并交回同一负责人。本文比较现场的公开叙述与规范，没有访问内部系统。OpenAI 两份文章通过公开网页工具核读，本地直接 HTTP 返回 403，另存 GitHub 固定版规范。
