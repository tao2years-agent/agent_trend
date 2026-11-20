# 八个正式研究轨的检索、误命中与盲点

冻结日期为 2026-11-20。ICSE、FSE、ASE、ISSTA 的 2025 和 2026 年主研究轨共列出 1,738 个不同题名和 1,738 个不同 event UUID，585 条在接受表中提供了可直接提取的 DOI 链接且无重复。预设的五组题名检索式命中 142 篇。首轮已选论文中有 14 篇确实位于此框，题名检索找回 8 篇，漏掉 6 篇。这是对已知小样本的诊断。

## 每个来源贡献了多少候选

|官方接受目录|收录题名|命中|未命中|Q1 编排|Q2 交付|Q3 监督|Q4 组织|Q5 评测|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|[ICSE-2025](https://conf.researchr.org/track/icse-2025/icse-2025-research-track)|245|10|235|1|3|2|0|4|
|[ICSE-2026](https://conf.researchr.org/track/icse-2026/icse-2026-research-track)|321|32|289|17|4|7|3|2|
|[FSE-2025](https://conf.researchr.org/track/fse-2025/fse-2025-research-papers)|135|5|130|1|0|1|0|3|
|[FSE-2026](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers)|211|15|196|5|1|3|2|4|
|[ASE-2025](https://conf.researchr.org/track/ase-2025/ase-2025-papers)|246|19|227|5|5|2|3|6|
|[ASE-2026](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)|263|32|231|22|4|3|3|2|
|[ISSTA-2025](https://conf.researchr.org/track/issta-2025/issta-2025-papers)|107|3|104|0|0|1|0|2|
|[ISSTA-2026](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers)|210|26|184|12|4|5|1|5|

同一题名能命中多组；来源命中数按唯一题名计。[全部题名及命中原因](frame.tsv) · [逐条筛选状态](screening.tsv) · [分层复核计数](coverage.tsv) · [所有命中的摘要判定](../venue-review/review.tsv)。

## 为何不用会议名称检索出版库来定义分母

八个输入都是各自主研究轨网页的 Accepted Papers 表；时段、主题 session 和混合日程未进入分母。FSE 两年正式规则都写明研究轨论文发表于 PACMSE 的相应 FSE 期，再获邀在会议报告。ISSTA 2025 公告将发表转到 PACMSE，2026 延续该方式；两年均可能接受 Research、Experience 和 Replicability 三种类型。ASE 两届的发布轨名为 Research Papers，征稿明确包含 Technical Research Papers 和 Experience Papers。ICSE 的 Research Track 独立于 SEIP、Journal First 等。该表没有统一子型字段；13 个 ISSTA 题名以括号明确自报 Experience Paper 或 Replicability Study，按题名标记保存。其余 1,725 项记 unknown，描述性副标题不作为正式子型。只使用这些界面可以稳定定义八个轨目录，不能宣称覆盖所有挂名该会议或同期发表的软件工程研究。

正文卷期、会上报告年份和预印本首次公开年份可以不同。本轮以研究轨的会议年归属，原始 HTML 和 SHA-256 见 [来源清单](manifest.json)。会议小标题、奖项或制品标签没有作为题名的一部分。未在研究轨接受表抓到 DOI 的行仍有 UUID 和来源 HTML，可以通过官网详情表单按 UUID 定位。

## 随机抽核与错误来源

每届分别按 SHA-256(event UUID) 升序从命中、未命中两层各取 2 篇，固定 32 篇。命中层的 16 篇有 14 篇直接相关、2 篇相邻。未命中层的 16 篇有 7 篇直接相关、7 篇相邻、2 篇离题。另补 5 个目的抽取，不参与抽样统计；入选 6 个代表案例中 Testora 已在抽样内。每篇记录准确英文题名、作者摘要、来源快照与中文裁定。[32+5 条原文定位与判定](sample-review.tsv)

直接漏检涵盖用 PR 意图识别行为回归（Testora）、贡献者离开后 PR 流量的准实验、用变更前后成对执行发现意外语义变化（ChangeGuard）、发布说明生成（VerLog）、完整车辆 API 测试流程、基于代码知识的运行故障归因（COCA），以及告警分诊。共同原因是论文用具体操作或领域名词表述工作，没有采用预置词形。命中后仍出现反例，例如路径规划中的 multi-agent、代码检索中的 modality collaboration、区块链事务中的 rollback，以及跨语言训练中的 knowledge transfer。它们分别与软件执行代理、团队协作、发布回滚、工程师知识交接同形异义。

全部 142 篇命中再以官网作者摘要逐条审查：89 篇直接相关、43 篇相邻、10 篇离题。抽样在每届和每个命中层中等额，不是按总体规模等概率抽取；抽样和目的补充都不宜外推整体真实召回率。单次分析者裁定也可能误判相邻与直接相关的边界。

## 既有论文被漏掉的具体原因

20 篇中的 P11 为 ICSE SEIP，P12、P17、P19 为较早届次，P13、P14 属于其他会议；这 6 项不在本框。框内未命中的 P02、P15 由 intent/spec 描述约束，P05 与 P18 使用 LLM agent 而非预列的 agent 组合，P06 从职业开发者的调试实践建构理论，P09 以 chat 和 IDE sessions 描述行为。追加检索可预置 intent/specification、LLM agents、development sessions、developer turnover、debugging practice、release notes 和 behavioral regressions，再在另一年或另一会议盲测。此次保留 v1 的六次已知漏检；事后补词不可写成对原结果的改善。[逐篇匹配](prior-recall.tsv)

## 六个此前缺少的机制

### F01 · 变更意图作回归判据

Testora: Using Natural Language Intent to Detect Behavioral Regressions。PR 到达后从修改处生成测试，运行前后两个版本。仅在行为不同的时候，用 PR 标题、描述与提交消息判断差异是否符合意图。

热门 Python 项目中发现 19 个回归和 11 个顺带修复旧错误的 PR。作者报给开发者的 13 项回归中 10 项获确认、8 项已修，均不能用 19 当已上报分母。 同一批 PR 影子双跑，盲评纯行为差异告警与意图过滤告警；统计每百 PR 漏报、确认缺陷和复核分钟。意图描述本身含糊时应当保留不确定并交人工。

Q2 漏掉 behavioral regressions，Q5 漏掉自然语言意图这种预言。 [作者摘要](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/10/Testora-Using-Natural-Language-Intent-to-Detect-Behavioral-Regressions)

### F02 · 何时值得多加一位审查者

The Cost vs the Benefit of Adding an Extra Code Reviewer to Mitigate Developer Turnover through Reviewer Recommenders。先识别文件知识集中或无人承接的 PR，只在存在离职风险的变更上建议增补审查者，允许管理者调节预算。

历史模拟中，激进策略在全量 PR 中平均 16.6% 加人，风险指标下降 82%；FarAwareRec 在 1.9% 加人，风险文件下降 42%。额外审查覆盖率和风险下降的分母不同。 真实试验预登记每周额外 review 分钟和二线人员能否独立回滚；若知识测试无改善或排队延迟超阈值，即使风险代理指标下降也收紧策略。

既有 P12 描述审查目标，未回答给哪些 PR 增加人的席位。 [作者摘要](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/28/The-Cost-vs-the-Benefit-of-Adding-an-Extra-Code-Reviewer-to-Mitigate-Developer-Turnov)

### F03 · 人如何解决自动验收判据不一致

TerzoN: Human-in-the-Loop Software Testing with a Composite Oracle。TerzoN 在一个视图呈现隐式、属性和输入输出示例三种判据；参与者能够审视相互抵触的判断并描述缺陷。

作者用 fast-check 作对照，14 位专业工程师参加随机人类实验。使用 TerzoN 的组诱发缺陷数相对多 72%，准确描述的缺陷超过两倍，测试速度相对快 16%。 对一个真实服务分配同难度任务，记录可复现的真缺陷与人工解释时间；观察者盲评，保留测试时长和任务难度的绝对值。小样本人因试验不足以推断组织 ROI。

补充 P16 的形式验证，从单一机器裁决扩展为多个判据和冲突处置。 [作者摘要](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/30/TerzoN-Human-in-the-Loop-Software-Testing-with-a-Composite-Oracle)

### F04 · 把值班手册编译成可审阅的执行图

StepFly: Agentic Troubleshooting Guide Automation for Incident Diagnosis。先由 SRE 借助 TSG Mentor 改善指引，再离线从手册抽取 DAG 和查询准备插件，在线阶段仅在依赖满足时调度，独立节点可并行。

前期研究 92 份真实手册；后续评估在 GPT-4.1 上约 94% 成功。对于可并行手册，执行时间下降 32.9% 至 70.4%。92 是前期手册数，摘要没有给该成功率的精确分母。 选低风险只读手册回放，对比人手执行和图调度的步骤遗漏、误停与人工接管时间；模拟过期依赖，检验治理者能否阻断旧图。

将以 issue 修复为中心的执行样本扩展到 SRE 手册维护、离线编译和实时诊断。 [作者摘要](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/76/StepFly-Agentic-Troubleshooting-Guide-Automation-for-Incident-Diagnosis)

### F05 · 版本化 agent 配置与质量成本分层

A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption。RAMP 从仓库可审阅配置建立四层累积量表，区分行为规则、具名 agent 和多 agent 编排；按已提交配置重估既有采用面板。

441 个仓库，保留样本中人工标注与仓库分层一致率 97%，73.8% 配置只提交一次。agent-first 仓库中，无/有已提交配置时认知复杂度增幅约 53%/27%。 跨团队分批引入有 owner 的配置，记录真实使用、团队先验纪律和模型版本；以复核工时、变更缺陷验证因果。作者明说分层观察可被工程纪律等混杂解释。

在 B01–B05 的席位、使用与交付指标之间加入可观察的团队治理异质性。 [作者摘要](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/250/A-Few-Pages-of-Markdown-Committed-AI-Configuration-and-Lower-Quality-Cost-after-Codi)

### F06 · 当剩余预算无法发现目标差异时停止

Stop When It Matters: Detectability-Guided Microbenchmarking for Performance Regression Testing。预设可忽略减速与业务重要回退两个阈值，用最小可检测效应重估所需样本数；分辨率足够时提前结束，在预算内无法达到分辨率时中止，再按相同规范判断。

三个开源项目的 1,702 个微基准，执行时长最大降幅 93%，同时检查经验假阳性与检验力。最大值不可充当平均节省，论文对象是微基准。 在代表性性能门禁注入已知幅度减速，逐桶核对决策率与分配的机时；灰区标为证据不足。小样本中止不得记为通过。

相比 P03 对重跑结果做预测，该方法可显式标记某个预算下不可判定。 [作者摘要](https://portal.fis.tum.de/en/publications/stop-when-it-matters-detectability-guided-microbenchmarking-for-p/)

## 复算

在本目录及相邻 venue-review 目录执行下列命令。所需 Python 包为 requests、beautifulsoup4；读取额外八篇 PDF 需 pdftotext。快照存在时直接离线解析，初次补抓需要联网。frame.py 重新计算题名分母，frame_review.py 按事前规则检索、检查抽样、汇总裁定；fetch.py 从相应官方只读详情取回 142 个摘要。

```text
python frame.py
python frame_review.py
python ../venue-review/fetch.py
python ../venue-review/fulltexts.py
python ../venue-review/compile_review.py
```

报告记录的是研究者观察、作者报告及建议试验。六个新增机制为作者摘要级复核；八篇另行精读的论文有独立方法/结果/效度定位。[八篇正文复核](../venue-review/result.md)
