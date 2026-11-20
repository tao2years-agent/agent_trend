from pathlib import Path
import json
P=Path(__file__).resolve().parent
def read(n):return json.loads((P/n).read_bytes())
h=read("holdout.json")["registered"];base=read("holdout.json")["complete_sequence_only"]
transition=read("transitions.json");c=read("census.json");jp=read("job-pairs.json")
pct=lambda a,b:f"{100*a/b:.2f}%"
table="\n".join(f"| {int(row['target']*100)}% | {row['test_dispatched']:,} | {row['avoided_red']} | {row['missed_green']} | {row['green_recall']*100:.2f}% | {row['break_even_loss_over_cost']:.2f} |" if row['break_even_loss_over_cost'] else f"| {'全部派发' if row['target']==1 else '99%'} | {row['test_dispatched']:,} | 0 | 0 | 100% | 无少派 |" for row in h['policies'])
result="""# GitHub Actions 能否替 OpenStack 验证“少跑 CI”？

**两个生态都观察到，少派工作的同时会漏掉本来能转绿的请求；同一采购算式给出的临界值相差六倍。** GitHub Actions 2023 研究包的有序留出有 1,472 个可比较原生重跑，其中 836 个会在下一次转绿。开发侧以保留 95% 转绿为目标的仓内历史规则少派 83 次，40 次会继续红，43 次本可绿。按每次少派省 C、漏掉一次转绿损失 L 计算，平衡点 L/C≈1.93。OpenStack 的 70,740 个留出请求中同类项目基线少派 5,061 次，漏掉 430 次转绿，平衡点约 11.77。两套数据都没有测量真正的 C、L、等待或人时。[GitHub 规则与留出](holdout.json) · [OpenStack 原实验](../ci/result.md)

**“没有被重跑”的分母很大，且没有反事实。** 另对 238 天 GHARuns 的 130,338,516 个 workflow run 元数据行做全量列普查。11,990,989 条在采集时仍为 attempt=1 且以 failure 结束。在本表中没有第二次执行结果，不能将这些工作归类为“一定重跑失败”或潜在可节省算力。[普查结果](census.json) · [作者固定发布](https://zenodo.org/records/23458821)

## 三份正文为什么给出不同的“重跑成功率”

| 原始工作与证据 | 它实际回答的问题 | 采购时应保留的口径 |
|---|---|---|
| Huang、Lin，TOSEM 35(10)，2026。作者研究 3,320 个 Java 仓库的 2023 年工作流。已读取正式发表版第 3.2、4.2 节、表 3 及固定仓库笔记本。 | 文中的 workflow rerun 是相邻两个不同 run 的重复运行，由相同提交或项目文件未改等条件识别。作者的 job rerun 沿同一 workflow run 的 previous_attempt_url 取多次结局。 | 两者的集合边界不同。名为 job rerun 的表记录整次 workflow attempt 的 conclusion，不能直接回答某个编译或测试 job 会不会成功。 |
| Ge、Zhang，arXiv:2602.02307v1。已读取第 3.1、4.1、5.1、6.1 节及公开附件说明。 | 若某个 job 在多次执行间既成功又失败，则相应 build 可算 flaky。作者排除 102,878 个由首次 action_required 引起的重跑后，52,610 个剩余 build 中 35,634 个（67.73%）符合定义。其失败 job 标注还结合了本地重复执行以降低“从未重跑=稳定失败”的错标。 | 这里的 67.73% 是“至少一个 job 曾翻转”，可以包括不同方向；和“首次红、下一次整个 workflow 绿”是两种终点。模型研究只从无需私密凭据的项目抽取十个，不能把 F1 直接换成被阻断的可恢复工作数量。完整标签包作者站点注明需索取，因此本文没有重算其模型。 |
| Talebzadeh Bardsiri 等，Stuck on Red?，arXiv:2610.41863v1，已读取数据、序列定义、威胁与可用性章节。 | 对默认分支过滤 fork/PR 触发、只留成功和失败，两端不能闭合的失败序列另行排除。底层 GHARuns 只保留最近 attempt；作者为 147,638 个重复运行补取了 204,106 条早先 attempt，其中 182,871 条红/绿进入其分析。 | 同一工作流跨多次 run 的连续红可以跨提交、定时或手动触发；连续红结束也不能独立归因于新代码。本文重算底层 GHARuns 边际和连接，不把它冒作论文经过补取和过滤的 streak 表。作者 Figshare 匿名链接在本机返回空的 HTTP 202，相关结论按论文原文使用。 |

作者网页与出版记录有时间区别，Huang 和 Lin 的 ACM/Crossref 正式在线日期为 2026-09-18；两份作者 PDF 的表 3 数字均核对过。Ge v1 的摘要写受影响项目 1,055 个，正文观察 2 写 1,005 个，只有后者与 1,960 的 51.28% 相符。本研究不沿用该冲突数字估算客户覆盖。GitHub 官方另明确，原生重跑可选择全部、失败或指定 job，沿用原 GITHUB_SHA 和 GITHUB_REF。[Huang 正式版](raw/huang-published.pdf) · [ACM DOI](https://doi.org/10.1145/3795771) · [Ge 论文](raw/ge.pdf) · [Ge 作者附件](https://flaky-build.github.io/) · [Stuck on Red 论文](raw/stuck.pdf) · [GitHub 文档](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)

## 2023 年，同一个 run 的下一次执行会怎样

按完整 SHA 核验作者两张公开压缩表，分别解析每个集合的 ID、作者记录的重跑次数、末态、逐次结局。不访问运行日志。原生表有 4,261 个分组，展开 17,034 项。按 run ID 去重后为 16,968 项，66 项重复记录一致。2,945 项完全没有逐次结局，另有 8 项序列长度与名义次数不符、3 项非空序列末态与作者单独保存的末态字段不同，均保留审计。14,023 项有至少两个可见结局，其中首次 failure 7,577 项、action_required 5,660 项、success 382 项，其余为其他状态。即使同一 run 有后续 attempt，也不能推断它最初就失败。[逐次序列统计](transitions.json) · [作者锁定代码](https://github.com/jiangnanpro/Reruns-of-GHA-workflow/tree/080aa9edd5f54c4e9dc5675ea75bc0f545c37ff3) · [独立 SQL 校验](sql-check.json)

| 在去重后的集合中，以首态明确 failure 为起点 | 原生 attempt，同一个 run ID | 作者识别的重复 workflow，不同 run ID |
|---|---:|---:|
| 起始红且有后续的集合 | 7,577 | 6,302 |
| 第一次重跑绿 / 红 | 4,437 / 2,921 | 1,966 / 4,047 |
| 第一次重跑其他或未知 | 219 | 289 |
| 任意后来一次变绿 | 5,616 | 2,498 |
| 最后一次为绿 | 5,604 | 2,137 |
| 前两次都红，后来至少一次绿 | 1,107 | 471 |

作者表 3 的 12,537/17,034（73.6%）与 2,137/6,302（33.9%）都可以直接用发表时保存的末态字段复算。若要决定“现在这次失败是否重试”，原生样本按下一次是否绿色计算则是 **4,437/7,577=58.56%**，只在下一次明确红或绿中计为 **4,437/7,358=60.30%**。按这 7,358 项涉及的 1,115 个仓逐仓算再等权，比例为 54.35%。有 53 个原生序列甚至从 success 变为下一次 failure。失败并重跑的选择机制、后续执行次数、状态过滤和仓权重都会改变结果。[复算脚本](huang.py) · [原始单位和分母](transitions.json)

## 已经申请的重跑，拦掉会损失什么

在 7,358 个可比较的原生 run 中按数字 run ID 排序，前 4,414 项训练，中间 1,472 项选择门槛，最后 1,472 项冻结测试。作者结局表没有绝对提交时间：**这是 ID 顺序留出，不是已验证的墙钟时间留出**。规则只用训练集的同仓恢复率，加入 20 个总体先验虚拟观测以平滑小仓；验证集在能达到目标召回的阈值中尽量少派，分数并列不拆。留出涉及 410 仓，271 项在训练中没有本仓历史。对照全都派发。[预登记](protocol.md) · [可重算留出](huang.py)

| 开发侧目标 | 测试实际派发 / 1,472 | 省下会继续红的重试 | 错过会转绿的重试 | 实际保住转绿 | L/C 平衡点 |
|---|---:|---:|---:|---:|---:|
"""+table+"""

只收录逐次序列长度吻合且末态一致的 7,350 项重做切分，在 1,470 个留出 run 上 95% 规则少派 85 次、漏 44 次，结论方向不变。更重要的异质性来自仓库：主检中只有 **3 个仓** 的请求被拦；其中一个仓贡献了 80 次拟拦截、41 次误挡。在不重新训练的情况下去掉该仓，1,392 个请求中只拦 3 次、误挡 2 次。1.93 也不应当作整个 GitHub Actions 的“真实价格比”。若人工给 L/C=2 作为情景假设，原 OpenStack 账本仍是 +4,201C，而此 GitHub 留出变成 −3C；两者都没有真实计价。「红两次就永远红」同样有反例，2,921 次原生红→红中 1,107 次后来至少转绿一次，不能从观察数据推断若采取跳过策略是否仍会补跑。[门槛敏感性](holdout.json) · [按仓复核](heldout-sensitivity.json)

## 2026 年，全运行分母与实际 job 能补充什么

在 GHARuns 2026-10-19 发布中，只读 runs 的 attempt、status、conclusion 和 jobs 的 status、conclusion。验证每一个 HTTP Content-Range，冻结 500 段内容哈希，53,588,986 字节覆盖全部 139 个 run 行组和 222 个 job 行组。它覆盖 2026-02-01 到 09-26 的 238 天，作者已移除平台生成的 dynamic 事件。下面是发布表的行计数，作者将 run 表定义为每个 workflow run 一行；未扫全部 run ID 来独立证明主键唯一。[官方数据卡](raw/gharuns-zenodo.json) · [全量行组汇总](census.json) · [列块与计数](aggregates/)

| 可在发布快照直接看见的事实 | 数量 |
|---|---:|
| 全部 workflow run 元数据行 | 130,338,516 |
| 仅一次 attempt，无论末态 | 127,303,665 |
| 仅一次且以 failure 结束 | 11,990,989 |
| 已经重跑过，无论末态 | 3,034,851 |
| 已经重跑、末态 success / failure | 2,182,205 / 575,622 |
| 不限次数、末态 failure | 12,566,611 |
| 全部独立 job 表行 / 其中 failure | 221,534,997 / 9,544,484 |

在这份快照里，所有末态 failure 中的 95.42% 尚无第二次 attempt。重跑过的记录末态成功率 71.90%，前态未知，不能报告为红转绿比例；另有 cancelled、skipped、startup_failure 等状态。这张表与 2023 论文既不是同一批仓，也不是相同时间和筛选条件。9.64% 的 run 末态 failure 和 4.31% 的 job 末态 failure 是不同实体、不同分母，不能据此说“跑 job 更可靠”。[全状态和次数分布](census.json)

再以预定的三个 check_suite_id 整数段精确连接两张表，扫描全部可能落入区间的行组，不读仓名、job 名或日志。三个区段有 9,544 个 run、12,977 个 job，3,416 个 run 能连到至少一行 job；6,128 个未连到，其中包括 640 个失败 run，不能把无记录当作“没有执行任何 job”。在已连接的 290 个失败 run 中，**119 个同时有成功 job 和失败 job**，151 个的已连接 job 全部失败。2,357 个已连接的成功 run 中也有 3 个包含失败 job。数据不能判定是允许失败配置、执行/关联语义还是其他原因；这足以否定“顶层一绿所有下层都绿”的标签复制。三个键区段是有界反例搜索，非随机平台比例估计。[连接方案](job-pairs-protocol.md) · [分段实数与覆盖](job-pairs.json) · [匹配器](job_pairs.py)

## 对采购判断的修订

GitHub 和 OpenStack 都支持先让工具找出失败证据、列出受影响的具体 job、保留人工覆盖和可补跑记录。支持这一选择的是两项观察：在真实已请求的重跑中，压低派发会错过本可转绿的结果；在同一 workflow 中，不同 job 的结果可以相反。直接在客户 CI 上自动压掉整条运行，仍需要使用**客户自己的请求/attempt/job 对照和代价**证明。

验收合同应要求厂商分别交付判断时可见的初态、建议的最小重跑单位、真实下一次和最终结局、未重跑覆盖，以及误挡后多久被人工发现和补发。基线应包括全部派发和已有仓内历史规则。先按仓和时间做影子评估，再在有人工兜底的范围内测真实等待、扣费分钟和漏恢复成本。现有公开数据没有未重跑失败的反事实，也没有给未请求的 1,199 万条记录测出节约金额；只报总体失败率或 flaky 模型 F1 无法完成上述验收。

## 复算路径

已有报告可用 verify.py 离线核验。huang.py 在临时缓存保存两份作者正式 run 序列表，以固定提交的 Git blob 和 SHA-256 校验后重算；sqlcheck.py 做独立 SQLite JSON 数组查询。range_counts.py 重取固定 Zenodo 记录中必要的压缩列，census.py 汇总全表。job_pairs.py 在同一临时缓存外加 101 个已哈希连接键列块（195,149,737 字节），默认不输出真实键、仓名或任务内容。没有使用仓库凭据、运行作者的重跑工具、下载 CI 日志或回写 GitHub。[来源与版本](sources.json) · [离线核验](verify.py)
"""
(P/"result.md").write_text(result,encoding="utf8")
if __name__=="__main__":print("compiled")
