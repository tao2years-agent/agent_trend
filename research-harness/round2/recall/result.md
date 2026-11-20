# 第二次检索：以工作对象找回漏检，再用新摘要盲抽

首轮 1,738 个研究轨题名中有 164 个已知条目，不再用于泛化检验。剩余 1,574 个题名内，新词表召回 395 个，仍未命中 1,179 个。两层各检查 64 个此前未审阅的官方作者摘要。新增命中层有 38 个直接相关、21 个相邻、5 个离题；仍未命中层也有 23 个直接相关、21 个相邻、20 个离题。检索修订可发现有价值的工作，也继续遗漏论文。

## 冻结与复算

V1 的 142 个题名命中、37 个已核摘要、F01–F06 和原 P 系列、R2 papers 的已知题名以 UUID/规范题名取并集排除。固定 work item、工作会话、验证对象三组词，按新 salt 对每个会议年×V2 命中/未命中各取前 8 个哈希。全部 128 份官方响应均经 UUID、英文题名与 SHA-256 校验。这里只能保证档案中已知样本没有进入盲抽。研究者已熟悉该领域，没有双人独立、对标题与层别隐藏的盲审。

[事前方案](protocol.md) · [V2 精确检索式](rules.json) · [1,738 条逐项账本](ledger.tsv) · [128 条由研究代理逐项判读](review.tsv) · [官方原摘要与 SHA](abstracts.tsv) · [作者谱系](groups.md)

## 同一会议年内应如何读这两个比例

第一列分母是该层剩余总题名数；比例是固定哈希抽样中直接相关的比例，括号为 95% Wilson 区间。以哈希近似随机抽取的小样本为前提，各轨不确定度很大；这不是原规则的精确率或召回率。研究轨内可同时存在技术、经验和复现工作，未获正式子型时继续标 unknown。

|会议年|新增命中池|直接相关/抽核（区间）|仍未命中池|直接相关/抽核（区间）|
|---|---:|---|---:|---|
|ICSE-2025|52|3/8 · 38%（14%–69%）|180|3/8 · 38%（14%–69%）|
|ICSE-2026|77|3/8 · 38%（14%–69%）|210|3/8 · 38%（14%–69%）|
|FSE-2025|32|6/8 · 75%（41%–93%）|96|3/8 · 38%（14%–69%）|
|FSE-2026|49|4/8 · 50%（22%–78%）|142|4/8 · 50%（22%–78%）|
|ASE-2025|46|7/8 · 88%（53%–98%）|179|3/8 · 38%（14%–69%）|
|ASE-2026|69|5/8 · 62%（31%–86%）|158|3/8 · 38%（14%–69%）|
|ISSTA-2025|17|4/8 · 50%（22%–78%）|85|1/8 · 12%（2%–47%）|
|ISSTA-2026|53|6/8 · 75%（41%–93%）|129|3/8 · 38%（14%–69%）|

样本对 16 个层等额分配，整体池大小与会议结构不等。把两层 64 篇直接相除仅描述已审样本，不是合并八个研究轨的加权相关率。抽样波动不足以给会议排名。三个重点词群也带来明确误检：programmers 可指静息态脑成像，patch 可指专用检测，specification 可指控制参数推断。

## 五项值得保留的研究

### V009 · 上线前如何证明 agent 制作的替换实现能保持旧行为？

Formally Verified Cloud-Scale Authorization。生产授权引擎的更换经历四年开发。作者用 Dafny 重写并生成便于调试的 Java；除形式证明，还用差分和影子测试对照约 10^15 个生产样本，后于 2024 年上线。这个数指行为比对样本，系统是否零风险、有多大普适提效均未给出。

迁移试点应为同一输入记录原实现与候选结果、豁免的预期差异、阻断阈值与回滚 owner；先找影响用户但测试全绿的反例。 仍未命中，题名只说正式验证和云规模授权。 [官方作者摘要](https://conf.researchr.org/details/icse-2025/icse-2025-research-track/119/Formally-Verified-Cloud-Scale-Authorization)

### V034 · 某个上游的维护人离开时，谁应该重估下游变更风险？

Core Developer Turnover in the Rust Package Ecosystem: Prevalence, Impact, and Awareness。作者观察 36,991 个 Rust 包构成的生态，并调查开发者怎么看待上游核心人员流失；许多包只有一名核心开发者。受访者提出健康状态透明和及时通知需求。包数不是调查回答人数，也不是人员离开导致缺陷的因果估计。

变更清单除引用数量外可收录 owner 是否可联系、最近的接班是否成功；先检验新增信号能否减少最后一刻无人确认，观察无谓告警数。 新增命中，来自 contributor/turnover 的工作对象。 [官方作者摘要](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/97/Core-Developer-Turnover-in-the-Rust-Package-Ecosystem-Prevalence-Impact-and-Awaren)

### V098 · 把哪些运行记录交给人，能更快知道下一步？

What Happened in This Pipeline? Diffing Build Logs With CiDiff。CiDiff 区分同一管线的通过与失败日志，在 17,906 个 CI 回归上与 LCS-diff 比较，同时做人类研究。中位输出体积约少 20%，待查新增行数约少 60%；70% 的回归案例中多数参与者偏好 CiDiff，分母为案例。

失败分诊必须同时对照原日志、普通 diff、专用 diff 和带 agent 解释的证据包。若专用 diff 已同样减少真实复核时间和误诊，生成式解释可退出。 新增命中，来自 build。 [官方作者摘要](https://conf.researchr.org/details/issta-2025/issta-2025-papers/88/What-Happened-in-This-Pipeline-Diffing-Build-Logs-With-CiDiff)

### V114 · 规则或需求改动后，如何知道该重验哪些制品？

CARE: Cascading Impact-Aware Compliance Test Suite Evolution under Regulatory Changes。CARE 显式连接规则、需求、场景与测试用例并沿层传播变更，保留不受影响的用例。在跨域合规任务中，作者报告更新后套件的平均 F1 为 90.3%；这个值没有表示未漏审的法规比例或法律正确性。

给治理规则变更使用版本化依赖图，再用独立全量核验检测“被复用项实际受影响”的错误。高风险合规场景需人工确认和外部判据。 新增命中，来自 test suite/changes。 [官方作者摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/204/CARE-Cascading-Impact-Aware-Compliance-Test-Suite-Evolution-under-Regulatory-Changes)

### V117 · 同样高的测试覆盖是否足以支持两种不同的交付承诺？

Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate With Their Effectiveness? (Replicability Study)。复制研究对比两类生成测试场景。输入被合理假定无缺陷且用于以后防回归时，覆盖与变异分可给跨模型比较提供线索；输入已可能有错而目标是当场揭错时，两者并非可靠替代。作者还报告套件大小不是主要混杂的证据。

为“保护已验收行为”和“发现当前未知缺陷”分设 cohort，直接用未来阶段真实回归和盲植故障验证代理指标。若真缺陷揭示无增益，即使覆盖上升也保留旧 harness。 新增命中，来自 test suites；题名自报 replicability study。 [官方作者摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/2/Do-Coverage-and-Mutation-Scores-of-LLM-Generated-Test-Suites-Correlate-With-Their-Eff)

## 对首选试点的影响

有明确退出日期、owner 与兼容判据时，真实依赖迁移仍可以先做。V009 提醒团队把上线前的影子行为比较写进验收；V034 说明跨仓迁移还可能卡在维护人离开，应以该依赖有无承接人分层。CI 失败分诊的对照则需要实质改变：加入 CiDiff 一类只呈现成功/失败差异的轻量基线。若人工从专用 diff 得到同等结论并花费同等时间，停止给这一类失败增加生成式解释。两条路径的优先级仍取决于本组织的待迁移量和失败诊断分钟，论文没有提供跨组织净收益排序。

自动优化 harness 也有更具体的否决条件。修改规则后需要沿需求和制品追踪受影响范围；用含已有缺陷的任务验证真实揭错能力。若新版本只提高覆盖而未在该类任务上增加真缺陷发现，拒绝推广。五项补充给出产品应做的对照和停机条件，不必把它们全部扩为新的功能线。

## 剩余盲区与下一次更新

V009 只说 cloud-scale authorization，V080 只说统计错误，V121 只说 contamination；这些工作在题名不直接写出组织工作对象。反过来将所有验证、上下文和安全名词全部加入词表，会使筛选量膨胀。下轮可先在独立年份用有限预算做摘要或引文追踪，并检测这三种盲区是否复现，不能再用这 128 篇作验证集。

这项研究对指定八份研究轨目录有完整题名清单，对命中和漏检区有二阶段摘要核查；其他年份、SEIP、非英语出版源、工业白皮书和所有未命中项的人工全文判定不在该抽样框。主题划分与评级仍包含分析者判断，置信区间仅衡量抽样误差，未校正标签误分、同一研究组聚类、不同会议年框架差异或多重区间。如此不能声称这是穷尽领域的系统综述。

离线重算时运行 python select_fetch.py、python groups.py、python report.py。新增的五项均为作者摘要级复核，未独立复现实验，勿计作八篇既有全文新增数。
