# 从 1,738 份作者摘要里找回哪些遗漏

在 ICSE、FSE、ASE、ISSTA 的 2025 和 2026 年八个主研究轨中，逐项核对到 **1,738 个唯一会议条目、1,738 份有正文的作者摘要**。286 件沿用了前面已经冻结的官方页面，另抓取 1,452 件。按原件哈希重建 SQLite 全文索引，可按题名、正文和届次离线查询。这里的覆盖是目录全收、摘要可查。实际逐项判断另有分母。[八份官方目录](../venue-frame/result.md) · [归档完成记录](audit.json) · [离线查询程序](query.py)

### 摘要改善了哪一种检索

先用第一批已判读的 142 篇训练两个固定排序器。两者使用相同的 TF–IDF、逻辑回归、参数和随机种子，差别只在可读取题名还是题名加摘要。在另一批 128 篇上检验，其中 61 篇被先前评审列为直接相关。两个分层抽样批次的 UUID 零交集。为了避免把高分都叫作相关，排除了这两批、已知论文与先前抽样，再在每届取四个新样本。32 条属于定向核对，不能推算会内相关论文总数。[固定方案](protocol.md) · [抽样规则](adjudication-plan.md) · [留出明细](holdout.csv)

|冻结的 128 条留出|题名|题名与摘要|
|---|---:|---:|
|平均精度 AP|0.741|0.813|
|ROC AUC|0.755|0.837|
|前 20 项中原先判为直接相关|17|17|
|前 40 项中原先判为直接相关|30|33|
|仍未命中第二版关键词的 64 项中，按本层得分取前 20，命中直接相关|10|14|

AP 增量为 0.073。在相同 16 个预设层内对同一条目的两种预测做 2,000 次配对重采样，95% 百分位区间为 −0.025 至 +0.174。只有 20 个阅读名额时，两种方法本次找回的相关项数相同。ASE 2026 层的 AP 还从 0.681 降至 0.559。适宜让摘要检索为关键词补一批候选，同时继续留出随机未命中的条目；没有依据把旧检索整个替换。[全部分层结果](model-metrics.csv) · [区间与假设](uncertainty.json) · [低分却相关的反例](low-ranked-relevant.csv)

### 四个足以改变试点的问题

- **失去维护者后谁接班。** ICSE 的 Python 包弃用研究指出维护者和消费者的通知预期存在差异，部分包没有替代选项。ISSTA 进一步从 4,011 个常用弃用 npm 包中找到 864 个需求仍增长的包，并访问维护者与用户。迁移产品演示应保留没有替代包、没有明确 owner、以及仍由间接依赖拉入旧包这三种状态，把它们放进剩余工作清单。这是两个生态提供的试点设计依据。[Python 论文](https://conf.researchr.org/details/icse-2025/icse-2025-research-track/35/An-Empirical-Study-on-Package-Level-Deprecation-in-Python-Ecosystem) · [npm 论文](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/89/Deprecated-but-Not-Abandoned-A-Large-Scale-Empirical-Study-on-Growing-user-demand-De)
- **什么算一条有用通知。** ASE 的 Good First Messages 把研究对象放到真实云服务事故讨论，与工程师接下来的调查行动对照。现场试点可让值班人记录这条消息是否改变了下一步、依据是什么，和点击或满意分另计。部分信息无法从观测对话知道，应保留“无法判定”。[会议论文](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/177/When-Does-AI-Actually-Help-in-Incident-Response-Identifying-Good-First-Messages-in-C)
- **补丁正确和解释可用能否分开验收。** ASE 的 ExplainBench 用下游行为题评估解释；修复排名与解释排名可以不同。对交接卡试点应分别查补丁、陈述与代码行为的一致性，以及下一位工程师是否真能据此继续工作。模型回答行为题只支持前两项的一部分。[会议论文](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/65/ExplainBench-Evaluating-Code-Explanations-from-Agents) · [两篇工作的原件与复算](../message-quality/result.md)
- **哪些工程师会被现有交接界面排除。** ICSE 对 39 名盲人或低视力软件从业者的访谈说明，获取信息更方便的同时，核对不可靠输出仍会花费精力，组织的工具准入也会影响使用。验收接管功能时，邀请有不同阅读方式的工程师，用可访问的文本、变更和独立证据完成同一交接任务。截图与模型摘要的可读性要分别检验。[会议论文](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/130/-Game-Changer-or-Overenthusiastic-Drunk-Acquaintance-Generative-AI-Use-by-Blind-a)

### 给筛选结论也做独立复查

两路研究代理在封存各自判断前不看对方标签。32 项中完全一致 26 项，未加权 Cohen κ 为 0.667；17 项双方都判直接相关。主审分布为直接 19、相邻 9、排除 4；复审为 19、7、6。两份“19”中有 4 个单边决定。两项按题名即排除；其余主审记录指明所用作者摘要。两路均为模型审阅，无法据此证明真人评审一致或领域无遗漏。[主审逐项结论](adjudications.tsv) · [未经改写的两路判定](paired-decisions.tsv) · [列联表](review-agreement.json)

逐个复核六项分歧后，保留原始投票。旧注释影响生成结果、静态检查的维护者采纳，适合作局部验收反例；在公开证据里还缺少对本团队生产效果的验证。ADHD 工程师支持、构建脚本问题分类，能改变招募分层或确定性基线，尚未测到产品介入后的净工时。通用应用市场调查、专用 HDL 编译器缺陷分类，留作相邻参考，不据以决定这一轮优先级。这样既能找到关键词漏掉的场景，也不会把邻近学科的结果说成本产品已有成效。[分歧逐条处置](disagreements.tsv)

**更新路径。** 增加新会期时先保存会议页面与唯一 ID，再重建可全文检索的本地库；每次更换排序规则均新增互斥审阅集，保留上版标签、未命中随机样本和同一预算下的查准比较。公开作者摘要供本地研究检索，离线分享报告只列转述和官方入口。

本次在初次冻结后实际重新请求了两条官方记录（ExplainBench、弃用 npm 包），分别保存获取时间和内容地址。两项原始字节及题名、摘要相同，保留已有判断。以后出现正文变化时记录会标出需重开审核的字段，继承旧结论前仍要有人判断。运行 `python abstract-index/refresh.py <会议UUID>` 即可追加一条观察；同样内容重复观察仍保留获取时间。[更新程序](refresh.py)
