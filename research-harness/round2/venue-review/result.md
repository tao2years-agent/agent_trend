# 从题名命中到实际决策证据

冻结的 142 个题名命中全部获得会议官网作者摘要，逐条标注后直接相关 89 项、相邻 43 项、离题 10 项、证据不足 0 项。八份作者全文作为其中的第二层复核，分别补充预算、评审、团队学习、计划、满意度及指标效度；它们与原 P01–P20、题名审计 F01–F06 均未重复。

## 证据如何核对

研究轨题名分母在 ../venue-frame/frame.tsv。fetch.py 读取会议专轨原页面的公开详情表单，按原 event UUID 请求只读详情，将官方响应、新旧同一 UUID 的题名、可点击 All Details、作者与单位、原始 SHA-256 关联在 abstracts.tsv。review.tsv 依次提供人工分类、具体摘意、机制与组织决策含义。机构字段使用会议页面明示的作者单位，部分作者未列单位，未推断实验室归属。

relevant 表示出现能回答研究问题的执行、决策或衡量机制；adjacent 表示仅有局部算法或特定领域的迁移价值；off-topic 表示关键词歧义或决策对象不符；unknown 表示资料不足。八篇正文按组织决策差异、是否已有覆盖及一手正文可得性目的抽取，不构成效果排序。全文案例中的量化结论属于作者研究，未独立重运行原实验。

## 八篇新增正文补读

### H028 · 执行预算

More with Less: An Empirical Study of Turn-Control Strategies for Efficient Coding Agents。从 SWE-bench Verified 500 个任务中抽取 100 个近似保留仓库分布的任务，在相同任务上比较三种模型和多种回合上限。各策略的回合预算、是否提醒和何时续期会改变空补丁数。

表5中 GPT‑4.1 固定 50 回合与动态 25→50 都解出 57/100，美元总额从 163.02 降至 123.41，重算相对下降 24.30%。同表 Gemini 2.5 Pro 此配置成本仅降 5.95%，说明文中常见的 12%–24% 摘要区间不足以覆盖所有表格配置。

这批任务、工具接口和当时价格决定估计对象；替换底模、任务实施成本或定价需重估。可复用的是按相同任务同时量解题率和美元，不宜将某个百分位直接设为所有项目的预算。 [PDF pp.3–5 表1、2；p.8 表5；p.10 表6](https://arxiv.org/pdf/2510.16786)

### H055 · 审查资源分配

Mitigating the Risk of Defects and Improving Knowledge Distribution with Code Reviewer Recommenders。回放三个大型长寿项目历史评审，Roslyn 8,646、Rust 17,499、Kubernetes 32,400 个已评审 PR；用不同缺陷概率阈值决定是否额外加专家，比较风险、知识和工作量集中度。

表4中阈值 75 时三个项目的平均额外审查 PR 比例为 8.09%，平均条件化 changeset safety ratio 变化 +18.82%，知识流失风险代理变化 −22.10%。阈值 25 时增派比例变为 59.56%。三项目平均值并非所有 PR 等权的合并值。

这是推荐策略模拟。专家实际会不会接单、能否发现缺陷、增加多少排队时间未由随机上线验证。可用小流量试点另测接受率、缺陷逃逸与额外工时。 [PDF p.5 表1；pp.10–12 表2–4](https://users.encs.concordia.ca/~pcr/paper/Sofia_Change_Safety_Ratio.pdf)

### H064 · 知识传递与人类学习

An Empirical Study of Knowledge Transfer in AI Pair Programming。同一编程任务，6 场人—人结对、7 场单人—Copilot；从发言及屏幕记录编码知识转移事件、终结方式和话题。分母为会话或事件，不能把一次发言当一位开发者。

人—人共 210 个事件，单人—AI 共 126 个，重算为每场 35.0 对 18.0；作者亦指出成功知识转移的频率有相似之处。总事件数、成功事件、事件占比和长期掌握是不同结局。

单任务、小样本，嵌套对话会拉长上层事件。主动口述和屏幕可见性也可能改变编码。推广前应再测独立复做和换人交接。 [PDF p.5 研究设计；pp.7–9 图2–6；p.11 效度](https://www.se.cs.uni-saarland.de/publications/docs/WSD%2B.pdf)

### H065 · 故事点估算

An LLM-based multi-agent framework for agile effort estimation。SEEAgent 在四个项目 Jira 用户故事上以历史团队给的 story points 为参照；离线预测评估的是单个经过微调的 SEEAgent。另有 12 名参与者的人机估算试验，不能把单代理离线误差记成讨论流程效果。

表II 中 DM 项目 MAE 为 4.251，优于 GPT2SP 的 4.303；另一个项目的 Fine-SE 为 4.659，SEEAgent 为 5.133。文中归纳四个项目中三个胜出。图4对信任和舒适度分别提问。

标的是团队原先的估算，并非最终真实耗时或商业价值。自报体验样本仅 12；应把估算会时间和实际交付偏差另行测量。 [PDF p.6 表I与 RQ；p.7 表II；pp.8–10 图4、效度](https://arxiv.org/pdf/2509.14483)

### H072 · 用户体验与选择偏差

"My productivity is boosted, but ..." Demystifying Users’ Perception on AI Coding Assistants。从 VS Code Marketplace 的 32 个 AI 扩展收集 5,908 条评论，抽 361 条人工编码；一条评论可有多个标签，标签频次与去重开发者数不同。排除安装或评论量不足的扩展。

表II 对喜欢/不喜欢的标签计数；喜欢栏的准确建议有 39 次、任务支持 24 次，不喜欢栏的建议帮助度为 17 次。其价值是定位采用障碍，无法估计组织中多少人因某功能而提高产出。

公开评论者自选且常表达极端体验，VS Code 生态和高安装量扩展限制外推。可将这些类别转为匿名团队调查选项，并与交付结果连接验证。 [PDF p.2 样本与方法；p.6 表I；p.8 表II；pp.10–11 讨论与效度](https://arxiv.org/pdf/2508.12285)

### H093 · 开发效能指标口径

Fragmented Markers, Mixed Results: A Systematic Review of AI Coding Assistants and Developer Productivity。先检索显式 productivity 研究，再以 SPACE 维度扩展开发者结局并标准化指标。去重纳入 45 篇，表2 的两阶段覆盖分别为 27 和 31，包含跨阶段重复，不能相加得 58 篇。

表2报 418 个指标出现项、187 个归一化独特指标。两阶段每论文独特指标中位数各 5，合并列为 6。独特标签数不意味着 187 个互相独立的效率维度，也不是平均效应。

研究设计、效应报告和主观/客观分母差异大，且 45 篇中 26 篇经同行评审。可复用归类体系，缺乏统一反事实时不合并收益百分比。 [PDF pp.3–5 两阶段筛查与编码；p.6 表2；p.11 效度](https://sws.informatik.uni-leipzig.de/wp-content/uploads/2026/07/Productivity_of_Software_Developers_with_AI_tools_LitRev.pdf)

### H100 · 验收者理解程度如何测量

On the Reliability of Code Comprehension Proxies。5 名专业工程师用三轮 Delphi 排序 8 段代码的难懂程度；两所学校的 44 名学生完成相同代码的任务，比较 14 种代理与专家排序的相关性。

表4中 28 对代码片段，严格一致的排序由首轮 13 对增加到第三轮 21 对；余下有 3 对弱一致、4 对不一致。输入输出语义和时间指标整体较能反映参考顺序，纯语法问题较差。

专家共识仍有分歧，8 个代码片段与学生人群限制外推；相关性也不代表引入代理能减少误审。实施前需以本团队真实评审任务校准。 [PDF p.7 表3、4；p.9 表5；p.10 图4；p.18 表8](https://arxiv.org/pdf/2605.23008)

### H127 · 解释、信任与正确采纳

Evaluating the Impact of Explainable AI on Trust in AI-Assisted Code Review。34 人组内设计，详细解释加反馈 A、仅反馈 B、仅建议 C。Prolific 参与者需有编程与 Python 经验；每人每条件 3 个判断，因此每组分母 102 次判断。预试后要求参与者给决策理由。

B 组 91/102 次同意 AI，A 组 79/102，均不等于正确率。信任 A 对 C 在 Bonferroni 校正后显著；同意率 B 对 C 显著，A 对 B 校正 p=0.0628。不能宣称所有两两差异显著。

任务次序和分配随机化存在限制；短任务与自报信任不能直接代表生产审查。产品试验宜同时量过度接受、错误拒绝、复核时长及决策理由。 [PDF pp.9–11 表1、2与招募；pp.13–15 表3–5；第4.7节效度](https://arxiv.org/pdf/2607.24601)

## 筛查后可直接改变的试验设计

动态续期的强基线是相同任务上的固定预算。至少同时记录解题成功、无补丁终止、总费用与单个难题的排队时间。把审核者工作量、知识覆盖、主观信任与真实缺陷分别保存，可避免把模拟风险比或点击同意错认成开发质量。

H055 的风险门槛、H064 的知识事件、H093 的指标词表分别回答不同层面的问题。将配置试点按仓库、变更难度和 reviewer 分组，预登记主要结局及人工负担并保留未使用者，才有机会区分执行优化和环节转移。
