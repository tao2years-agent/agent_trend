# 三类工作值得分别投资

上一轮把 CI 失败诊断列为第一。另读 Airbnb、Google、Spotify 的工程一线报告后，更稳妥的选择方法是先找组织里**有期限、有总清单、有独立判据**的工作。如果下一季度要迁走一个弃用 API，跨仓迁移通常具备这三项条件；偶发 CI 失败则可能只有最后一项。若团队没有成规模的迁移，故障分诊仍可优先。这里给出选题条件，公开材料无法替某家企业判定其主要瓶颈。

## 跨仓迁移：把长尾交给谁

- **Airbnb 提供了停止自动重试的实证。** 在约 3,500 个 Enzyme 测试文件的迁移中，流水线就绪后，首次批跑四小时约完成 75%。团队抽样看失败、调整提示与脚本、再扫全量，随后又循环四天达到 97%。部分长尾文件已重试 50–100 次，最后约 3% 交给人，另花一周收尾。六周工程投入及 API 成本与事前人工工期估计比较，并非随机对照。平台应该提供按失败原因分群、同类批修和显式放弃重试的入口。上升的自动完成率并不自动证明最后一轮仍划算。[Airbnb 原文](https://airbnb.tech/infrastructure/accelerating-large-scale-test-migration-with-llms/)
- **Google 的 80% 与 50% 有不同分母。** 在文中同一个迁移工作流，已落地变更中 80% 的代码修改由 AI 编写；工程师估计总时间少用约 50%。前者观察代码来源，后者是执行人的估计。人仍识别需改的文件，审阅候选，按所有权拆成多个 change list。编译与用例是候选筛选条件，若连测试也改了，旧行为是否保留需要另外证明。产品选型应观察未生成、生成但未合、已合但未部署的服务。[Google Research](https://research.google/blog/accelerating-code-migrations-with-ai/)
- **Spotify 说明有些规模来自 agent 之前。** 2023 年已有 BOM 与 Fleet Management，可先为多个仓库建临时分支跑 CI，逐批按服务重要性允许自动合并，合并后监控失败部署。团队报告当时 96% 的生产后端服务使用 Java BOM。2025 年 Honk 给迁移补入模型和独立评估：验证器之后的 judge 报告约否决四分之一会话，其中约一半能纠正；工程团队同时写明还没有为 judge 建立专门评测。因此“能拒绝”和“拒得对”仍需分开。已有成熟批量变更能力的组织应直接测试模型对剩余难例的边际增量。[既有批量平台](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring) · [Honk 反馈循环](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)

**何时买哪一层。** 对稳定 API 映射优先测 OpenRewrite 的确定性 recipe 和多轮无多余改动；需要先掌握跨仓阻塞面，可使用 Moderne 的 migration dry-run 配编译验证；每仓存在上下文差异，再测 Sourcegraph Agentic Batch Changes 的计划、单仓 canary 与分段发布。三者承接的职责不同。强基线里仍有多少工作、其中多少需要业务解释，决定是否值得再加 agent。针对只提供单仓 PR 的产品，应要求现场演示同一迁移中依赖阻塞、移出范围和 owner 换人三种情况。[OpenRewrite](https://docs.openrewrite.org/authoring-recipes/recipe-conventions-and-best-practices) · [Moderne](https://docs.moderne.io/hands-on-learning/spring-boot-migration/module-1-migration-assessment/) · [Sourcegraph](https://sourcegraph.com/docs/agentic-batch-changes)

## 上线前的人工监督：谁决定打扰工程师

Meta 的 Catching JiTTests 夜间用闲置算力处理前一天风险较高的 diff。它生成可能揭示问题的测试，组合模型判分与确定性误报过滤，然后才决定是否联系工程师。人可以管理判定标准并复查汇总结果。2026-10-29 团队披露，有 589 名工程师回应，占触达的 64%，另报告 60% 真阳性。两个数字分别涉及人和发现，不能直接相乘计算所有 diff 的检出率。高风险 diff 优先、未触达及未响应三处选择都会影响样本。文中半年捕获 74 个严重隐私问题及事故变化属于其部署现场的报告。[Meta 工程原文](https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/)

可以试的产品增量是**维护负责人的注意力预算**：每周只投递少量可复现的高价值发现，同时在被过滤和无人响应的项目中随机抽查一小部分，估计漏报；给每次有效纠正记录可复用的验收。与全量投递对照，观察每个真实修复的人工分钟、严重漏报和被打扰次数。这个设计要能区分“没有人回应”和“确认误报”，否则阈值会越来越偏向最愿意回应的人。企业没有可信的严重性标注、维护者已处于评审积压时，先做影子评判。

## 生产事故：诊断、动作与恢复分开计分

微软研究页面收录的 2026 预印本把一次微服务故障拆为定位服务、选择允许动作及作用对象、检验恢复。所测较强 RAG 方法对根因服务的准确率为 91.4%–99.7%，符合标注恢复方案的比例仅 36.8%–60.3%。即使根因服务和故障类型均对，恢复动作仍可能无效。它是带允许动作空间和标注方案的简化实验，不能把该比例当成真实生产恢复率。IBM 的 ITBench 另以初版 94 个跨领域场景评估端到端动作，作者报告其测试配置在 SRE 场景仅解决 13.8%。两个实验任务、模型和分母不同，不相减作性能差。[恢复研究](https://www.microsoft.com/en-us/research/publication/can-llms-really-recover-microservice-failures-a-recovery-aware-evaluation-of-diagnosis-to-action-reasoning/) · [ITBench](https://research.ibm.com/publications/itbench-evaluating-ai-agents-across-diverse-real-world-it-automation-tasks)

商业产品对应不同层次。Datadog Bits 在证据不足时可将调查标为 inconclusive。AWS DevOps Agent 接收人在调查期间的消息，但文档明确它在推理步骤之间读取队列，不能将发消息等同于立刻打断在途工具调用。组织对接时应分别记录接收人工指令、停止新动作、确认在途副作用、观测服务恢复四个时点。[Datadog 调查](https://docs.datadoghq.com/bits_ai/bits_investigation/investigate_issues/) · [AWS 调查与交互](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

**试点顺序。** 先让产品只读重放已结案的事件，在隐藏最终结论的条件下记录证据质量、得出结论的时间与合理放弃。其次让值班工程师判断候选恢复动作、目标资源和观测窗；跨越权限域的动作交给责任方。最后才在低影响、可撤销的故障演练里测试动作。已有 ChatOps 或告警框架时，独立比较“转发日志”“证据归纳”“建议动作”和“执行后验证”的边际收益。
