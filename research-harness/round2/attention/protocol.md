# 真人注意力研究的筛选与复算

## 目标及完成条件

检索截至 2026-11-20，问题有三类：开发者在哪种工作状态下适合被打断；一次跨人交接需要提供哪些信息；能继续操作是否等于理解工作。此专题按问题定向找原始人类研究，保留现场行为、自记、程序理解测验、协作观察各自的分母。允许历史研究帮助界定机制，以近年 IDE 研究校验外推。当前样本 8 个独立研究数据集、9 份作者或机构全文。A04/A04f 是同一研究的扩展作者稿和正式会议排版稿；A07 是上一轮 R04，跨轮不增计。不同作者共同参与、同一机构和类似学生群体不能视作八次独立行业复现。

## 可复刻的检索与选择规则

以下英文检索式是本轮实际检索的主要词组，可在公开网页搜索复跑；通用搜索的结果顺序会变化。定位标题和作者后直接打开作者、机构、会议或作者提交的 arXiv 全文。为避免排序漂移，固定候选标题、决定和 URL，复跑选样从下表及已保存的来源清单开始。未逐会逐年穷尽，不报告总体召回率。

| 问题对象 | 实际检索式或关键短语 | 锚点 |
|---|---|---|
| 人被同事打断 | `software developers interruptions timing programming tasks resumption cues`；`FlowLight reducing interruptions at work a large-scale field study` | A01 |
| 任务中断及恢复 | `Parnin DeLine evaluating cues for resuming interrupted programming tasks`；`software developers interruption task switching field study` | A02 |
| 跨人寻求解释与交接 | `information needs software developers in software development teams Ko DeLine Venolia`；`Bacchelli Bird Expectations Outcomes Challenges Modern Code Review` | A03、A08 |
| AI 是否应该主动介入 | `proactive coding assistant timing unsolicited suggestions software developers controlled user study`；`When to Show a Suggestion Integrating Human Feedback in AI-Assisted Programming` | A04、A05、A06 |
| 独立理解 | `AI generated code developer understanding randomized controlled experiment skill formation Trio`；沿作者论文追到公开研究数据 | A07 |
| 边界核对 | `software incident response field study incident commanders software service engineers cognitive incident management handoffs` | 排查真实事故资料的测量对象 |

纳入须同时满足三项：真人在实际或受控开发任务中参与，或组织中包含开发人员的直接打断观察；有清晰实验对照或可定位现场观察对象与采集设计；可读取含分母、结果与限制的作者/机构正文。优先选能提供当前样本缺少的测量方式的研究，每类保留至少一个能改变产品判断的反例。处理同名作者稿和会议版、相同试验不同来源及此前 R04 的重复后停止。好坏方向都保留，包括不显著结果、公开数据对不齐、无提示也会恢复等。此为可审计的目的性样本，非预注册系统综述。

| 其他具体候选 | 决定及原因 |
|---|---|
| Parnin 与 Rugaber，Resumption Strategies for Interrupted Programming Tasks／其后续经验扩展 | 与 A02 共一位作者，且 A02 中也使用了 414 人调查；无法把该问卷单列成独立重复。这一轮保留 A02 的 14 人受控恢复任务。[后续论文](https://chrisparnin.me/pdf/parnin-sqj11.pdf) |
| Two Sides of the Same Coin: Software Developers’ Perceptions of Task Switching and Task Interruption | 同主题感知资料，候选保留。前后自记已经由 A01 覆盖，本轮转向受控恢复与实时行为。[作者公开稿](https://opus.lib.uts.edu.au/bitstream/10453/132915/1/1805.05504.pdf) |
| Iqbal 与 Bailey，Effects of Intelligent Notification Management on Users and Their Tasks | 通用人机通知，并非此轮软件研发场景的必要样本；未用来证明编程或 agent 生产效率。[会议记录](https://doi.org/10.1145/1357054.1357070) |
| How to Fight Production Incidents? An Empirical Study on a Large-scale Cloud Service | 是生产事故的重要边界证据，研究重点是高严重度事故及复盘，而非对收件人的受扰状态、理解测验或两种通知策略直接观察；未计入真人注意力效果。[作者记录](https://www.microsoft.com/en-us/research/publication/how-to-fight-production-incidents-an-empirical-study-on-a-large-scale-cloud-service/) |

## 观察等级与开放程度

- A01 的设备总安装数、可比的自记打断、访谈、调查分别计；自记前后变化不能读成对 449 人进行随机实验。
- A02 同参与者三种条件，表 3 公开的是任务成功聚合；A03、A08 是观察、访谈与内容编码，不用非独立事件数量替代独立人数。
- A04 的建议接纳来自真实遥测，隐藏策略仅在历史数据上测试。A05 是实验室研究者行为编码，A06 是现场操作、问卷和不完整参与者群的组合。没有中断整个 agent 工作流的受控组织研究。
- A07 主实验使用独立知识测验。公开仓库含每份转写的条件及整数分钟，但没有公开同一套参与者的个人知识总分；这里只发布最少数值字段、原始文件名及校验值。相关作者私密逐事件遥测不抓取、不模拟。

## 可重复计算

运行 `python collect.py` 获取按 SHA-256 命名的正文并生成页码化文本，`python public_time.py` 从作者固定 Git 提交提取分钟字段，再运行 `python recompute.py` 验证全部 PDF 哈希、计算 A05 图 4、A02 表 3 和分钟差。不运行作者代码。复核 A05 六个触发器时曾直接渲染查看作者图 4；见 `raw/A05-Fig4-counts.csv`。A02 列名为任务、行名为条件，每个条件 14 个任务暴露；公开表不能恢复个人配对效应。A07 数值投影按源文件逐一哈希，上传到作者仓库的原始注释不在本地产物重复分发。[来源索引](sources.json) · [转录运算](recalculated.json) · [固定提交元数据](A07-recalculated.json)

检索交付边界为已发布公开证据及离线运算。本专题没有自行实施面向开发者的现场实验。
