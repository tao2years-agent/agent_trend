import collections,json
from pathlib import Path
P=Path(__file__).resolve().parent
read=lambda p:json.loads((P/p).read_bytes())
cohort=read("cohort.json"); main=read("outcomes.json"); comparison=read("comparison.json")["whole"]; whole=read("full311/all.json"); variants=read("sensitivity.json")
descriptions={
22080:"负号与 Mod 的结合顺序；同时检查生成的乘幂字符串、Python 打印及空模块 lambdify。",
22456:"String 的 func(*args) 应能还原原表达式。上游给现有 test_String 增加了这个断言。",
22714:"evaluate(False) 环境构造二维 Point 不应报错。上游新增 test_issue_22684。",
22914:"PythonCodePrinter 应将 Min、Max 输出为可执行的 Python min、max。",
23262:"单元素元组经 lambdify 后应保留元组结构，例如 (1,)。",
23413:"Hermite 标准形应保留要求的行。两个模块各有同名测试，矩阵模块另含具体反例。",
23534:"嵌套符号列表带 cls=Function 时，内部对象应是 UndefinedFunction。",
23824:"Kahane 化简应保留首段未收缩 gamma 矩阵乘积的次序。"}
summaries=[]
for meta,row,extra in zip(cohort["selected"],main,comparison["by_case"]):
    key=meta["instance_id"];n=int(key.split("-")[-1]);body=read("raw/"+key+"/pr-body.json");issue=body["issue_references_in_closing_phrases"][0]
    phases=row["phases"]
    base=phases["original"]["selected"];ftp=[v["outcome"] for v in base.values() if v["role"]=="FTP"]
    changes=extra["same_tests_base_to_gold"]["contrasts"]
    summaries.append(f"| [{n}](https://github.com/sympy/sympy/pull/{n}) / [#{issue}](https://github.com/sympy/sympy/issues/{issue}) | {meta['row_index_zero_based']} / {meta['version']} / [{meta['base_commit'][:8]}]({meta['base_url']}) | {descriptions[n]} | {ftp.count('passed')} / {ftp.count('missing')} | {len(changes)} |")
phase_weak={p:sum(x["phases"][p]["seconds"] for x in main) for p in main[0]["phases"]}
phase_full={p:sum(r["seconds"] for r in whole["runs"] if r["phase"]==p) for p in ("original","regression_on_base","regression_on_gold")}
costrow="\n".join(f"| {n} | {phase_weak[p]:.2f} 秒 | {phase_full[p]:.2f} 秒 |" for (p,n) in [("original","原代码及原测试"),("regression_on_base","原代码及补充测试"),("regression_on_gold","金标代码及补充测试")])
result="""# 绿灯能识别错误补丁吗？8 个上游缺陷的独立验收实验

**8 个未修复版本在选定的原有测试上全部通过。加入上游针对问题新增或增强的测试后，8 个未修复版本全部失败；同样的测试配上金标改动，8 个全部通过。** 判断发生变化的原因是检查了原先没检查的行为。对研发组织，验收台应能回答“这条命令能否区分已知错误版本和候选”，仅记录通过次数会漏掉这个问题。[逐次结果](outcomes.json) · [官方发布数据](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified)

扩大到完整模块后，发现了数据集 FAIL_TO_PASS 名单外的一项判别测试。再人为制造 7 个不完整补丁，有一项在小集合中只暴露 4 个失败，在全模块中暴露 15 个；也有两个不完整补丁同时通过两种验证。完整模块增加了这批候选的故障定位信息，最终按“能否通过”判定的候选数量没有再改变。[配对比较](comparison.json) · [逐个不完整补丁](sensitivity.json)

## 选样和执行

官方 SWE-bench Verified 固定修订 c104f840… 的测试分片有 500 个问题，其中 75 个来自 SymPy。选用本机可运行、无需服务或模型的纯 Python 数学库。版本号至少 1.10，必须同时有生产补丁、测试补丁、FAIL_TO_PASS 和 PASS_TO_PASS；共 15 个通过字段筛选。按 PR 的数字顺序预先取前 8 个，逐项确认是数值、打印、表达式和符号行为问题，均无需联网或处理安全缺陷。未按结果替换样本。原分片 2,096,679 字节，SHA-256 为 a45b1fe4…；本地保留分片、锁定行、与 PR 关联的 issue、两份原补丁、测试涉及的原版本文件和 8 个完整上游归档的校验值。完整源码压缩包放在本机可重建的缓存，项目内保存的是选中文件。[预注册规则](preregister.md) · [覆盖与版本](cohort.json) · [54 个来源指针](sources.json)

每项比较原代码和原测试 A、原代码和上游 test_patch B、金标生产代码和相同 test_patch C。第一环境使用 Windows CPython 3.12.3、pytest 7.4.4、NumPy 1.26.4、SciPy 1.13.1 和 mpmath 1.3.0，验证模块确实从上游检出目录导入。运行全部 FAIL_TO_PASS；PASS_TO_PASS 按名称排序，最多五个。8 项共抽取 10 个问题特异标签、34 个回归标签。SymPy 基准标签是函数短名，在发生测试变更的模块内做精确匹配，同名匹配多个真实节点则全部运行。“缺失”表示该基线没有该函数，不能记作成功。[节点运行器](run.py) · [本地逐项日志](runs/)

第二环境是新建的独立 Windows CPython 3.11.9 venv，安装固定版本的 pytest、mpmath、NumPy、SciPy 和 numexpr。按上游 test_patch 自身列出的每一个测试模块全量运行。8 个问题有 11 个问题—模块组合，A/B/C 三组 33 次 pytest，另为部分补丁执行 13 次，共 46 次。每次只运行一个模块，独立进程、最多两个并发、480 秒上限。节点试验限时 160 秒。未使用官方 Docker 镜像或全仓套件。[整模块协议](module-protocol.md) · [运行器](modules.py) · [独立环境](full311/environment.txt) · [全部 46 次结果](full311/all.json)

## 八个问题分别检查了什么

“原本绿 / 缺失”按官方 FAIL_TO_PASS 短名计；最右列按固定测试集 B→C 真实 pytest 节点计，原本失败且在金标后通过。行号从 0 起。完整 SHA、issue 文本及断言保存在各 case 的原件中。

| PR / issue | 发布数据行 / SymPy 版本 / 基线 | 针对的行为 | 原本绿 / 缺失 | 整模块红→绿节点 |
|---|---|---|---:|---:|
"""+ "\n".join(summaries)+"""

8/10 个 FAIL_TO_PASS 名称在原版本已经存在并且通过，另 2 个不存在。装入 test_patch 后这 10 个名称全部能区分原代码和金标；它们实际对应 11 个执行节点，因为 #23413 的同名 test_hermite_normal 位于两个模块。原地加强一个现有测试的断言可以显著改变验收意义，而测试名和报告展示的用例数可保持不变。[#22456 的单条新增断言](raw/sympy__sympy-22456/test_patch.diff) · [#23413 两个模块](raw/sympy__sympy-23413/test_patch.diff)

## 整模块多检查了什么，付出了多少成本

第二环境在 B、C 各收集 356 个**问题内模块节点**。同一模块在不同历史提交参加试验时分别计数。B 有 313 通过、12 失败、30 跳过、1 预期失败；C 有 325 通过、30 跳过、1 预期失败。12 个 B 失败节点在 C 全部通过，未观察到同组中由通过变失败的节点。新增信号是 #23413 的 test_issue_23410，直接用具体矩阵检验 Hermite 标准形；作者将它写入上游测试补丁，Verified 的 FAIL_TO_PASS 字段只列 test_hermite_normal。面向增量验收，测试补丁涉及的模块可在 benchmark 短名单之外再提供检查。[旧代码完整模块](full311/sympy__sympy-23413/regression_on_base_m1.txt) · [金标完整模块](full311/sympy__sympy-23413/regression_on_gold_m1.txt)

原代码的原测试 A 共收集 353 个节点，322 通过、30 跳过、1 预期失败。金标的 30 个跳过主要涉及缺少 TensorFlow、CuPy、ANTLR、Cython 和 Numba。这些组合的行为仍未验证。全体正式模块运行没有超时；一个部分候选缺少 Atom 导入，导致模块收集错误，已单独计入。首次准备第二环境时抢先启动运行器，mpmath 尚未安装，预检中止；该次未执行测试，另留安装失败记录。[各项目跳过原因](comparison.json) · [安装阶段记录](modules311/setup-failure.md)

| 8 个问题合计的子进程耗时 | 3.12 选定节点，8 次 | 3.11 整模块，11 次 |
|---|---:|---:|
"""+costrow+"""

耗时包含 pytest 启动。全模块连同部分候选共累计 """+f"{comparison['elapsed_subprocess_seconds']:.2f} 秒，墙钟 {comparison['wall_seconds']:.2f} 秒。"+""" 两套解释器、依赖和缓存状态不同，不能将表中相除解释为普适开销倍数。[原始耗时](full311/all.json)

## 刻意漏掉一部分修复会怎样

在主实验结束以后追加预注册。8 个问题中两个金标有多个生产 diff hunk，分别 3 个、4 个。每次只去掉一个 hunk，保留其余金标和完整测试补丁，得到 7 项。仅看选中的 PASS_TO_PASS 冒烟节点时，5 个通过、1 个断言失败、1 个收集失败。加入选定 FAIL_TO_PASS 后，2 个通过、4 个断言失败、1 个收集失败。独立环境的整模块给出相同的候选分类。[追加协议](sensitivity-protocol.md) · [逐候选日志和原补丁](sensitivity/) · [逐节点对照](comparison.json)

- #22080 去掉第一段导入改动后，小集合报 4 个失败，全模块报 15 个。额外 11 个失败遍及积分、分段函数、NumPy 或 numexpr 相关路径。它原本就被小集合挡住；整模块补出了回归影响范围。其他两个变体分别有 3、2 个全模块失败。[小集合](sensitivity/sympy__sympy-22080/without-1.txt) · [lambdify 整模块](full311/sympy__sympy-22080/without-1_m3.txt)
- #22456 漏掉 Atom 导入，会因 NameError 在收集期失败。漏掉空行删除，或漏掉让 String 继承 Atom 的 hunk，两种验证都通过；漏掉 func/kwargs 行为改动则失败。前一个通过者只有格式差异，后一个结构不同但已观察的目标不变式和整模块均通过。这里没有证据宣称后者仍有用户可见缺陷；只比较与金标的 diff 完全一致会误伤至少那个纯格式候选。[上游问题](https://github.com/sympy/sympy/issues/22455) · [金标补丁](raw/sympy__sympy-22456/patch.diff) · [候选的整模块结果](full311/sympy__sympy-22456/without-3_m1.txt)

## 对工程验收的含义

把两份记录附在同一候选上。第一份给出独立保存的期望行为，在基础版本上运行会失败、在候选上运行通过；名字相同也要保存测试版本与断言来源。第二份运行被改测试涉及的完整模块，分别记录新失败、共同失败、跳过、收集错误和时间。部署是否放行再由代码所有者按变更风险决定。一个可证伪的验收要求是：若只交给系统全绿的旧测试，它必须显示问题特异检查缺失；给出上游触发条件后，旧缺陷仍能放行，就判验收失败。本次 #23413 还表明，按短函数名计数会混淆模块，流水线应保存路径加节点名。

这里的“独立”有两层：测试依据来自公开上游维护者，执行环境独立重建。生产补丁和测试补丁来自同一个已知上游修复，实验未做盲测，没有让代理自行生成补丁或验收测试。Verified 本身按可复现缺陷筛选，八项又来自同一软件；8/8 的区分能力不能外推到新任务、其他项目、线上事故率或开发时间收益。

## 复算

先运行 ingest.py 校验固定分片、恢复 8 个上游归档，再运行 run.py 和 sensitivity.py。单独准备 CPython 3.11 环境，按 full311/environment.txt 安装依赖，用 modules.py --python 指定其解释器、--out 指向全新目录。compare.py / verify.py 对随附证据做离线比较和一致性校验。原始标准输出、JUnit XML 和每个运行的退出码均保留。[摄取](ingest.py) · [部分补丁生成与测试](sensitivity.py) · [整模块运行](modules.py) · [离线校验](verify.py)
"""
(P/"result.md").write_text(result,encoding="utf8")
