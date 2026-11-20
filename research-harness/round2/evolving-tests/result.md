# 跨版本迁移除了“换成新名字”，还要验什么

从第二轮未命中盲样中挑出 V012、V058、V122。三者分别谈 Python 补全、JavaScript 消费者和 Android GUI 测试，能检验同一个迁移建议在不同层级是否成立。前两篇读到作者全文表格，第三篇有会议/学校材料、固定源仓和可复算个案表，出版社 PDF 在本环境返回 403。[原始盲样](../recall/review.tsv) · [来源及失败记录](sources.json) · [固定 Git 树](git-trees.json)

**代码是否引用了适用版本的 API。** ICSE 2025 的 Wang 等从 8 个 Python 库构建 145 组 API 映射、28,125 个补全提示，比较 7 个当时的模型。论文 §III 和表 III 的两个分母很重要：全部提示中，命中所研究新/旧调用任一方的比例 AUP 仅约 9%–23%；这部分命中里仍使用旧调用的比例 DUR 约 25%–38%。后者不能解释为所有生成代码的弃用率。作者以映射替换及将信息插入提示作为低成本基线。迁移平台可以先为目标分支取准确版本和弃用映射，待验证的是在已经喂给相同映射的情况下，agent 还能省下多少维护者劳动。模型代际与单行补全约束限制外推。[作者版全文，表 I、III](https://yebof.github.io/assets/pdf/wang2025icse.pdf)

**知道有 breaking change，是否知道该仓的哪些行为须保留。** FSE 2026 的 BDUpdater 把库发布记录整理为细粒度变更知识，从受影响消费者的情境生成适配。在 RQ2 表 9 的 26 个 client–library 案例里，仅告知受影响文件通过 7 项，给粗粒度记录通过 16 项，给细粒度知识的方法通过 24 项。按类型看，后者在 module 4/4、property 8/8、function 12/14；仍有两次未成功。作者用相同 npm script 协议评判，限定客户端有可运行测试。一些比较还需额外花费探索仓库的 token，不能把成功数直接等同成本优势。我们在固定作者仓中核对了 ablation.json 的 26 个客户端到文件的映射；它不含所有运行结果，24 的成绩来自论文原表。[作者全文，表 9、§6](https://nesa.zju.edu.cn/download/auto_20260423_yifan-2026fse.pdf) · [作者工件](https://github.com/EvanXiaa/BDUpdater/tree/3152cf47c7749d10d644c2c8016f4fe8adec2a1e) · [文件及 Git blob 对账](ablation-sources.json)

**更新验证器时，能否证明仍然测同一行为。** ISSTA 2026 的 GUIRevive 对 Android 界面演化后的旧用例做元素定位、功能保持验证和路径探索。按作者公开 All_cases.csv 独立复算，736 行、36 个 app、669 个有向 app+旧版+新版组合，无重复的 app/旧版/新版/运行序号。定位器失效 297 项、控件遮挡 161 项、移至下一级及另一页各 139 项。最大的一个应用占 106 项，前五个占 319 项；按用例权重定位失效占 40.35%，按应用等权则为 49.86%。这两种都是对已失效用例的描述。公开表不含所有成功回放，无法估算一款应用升级会使多少测试失效；本次也未启动 Android 模拟器或独立重现论文的修复成功率。[作者固定数据](https://github.com/shiwen-song/GUIRevive/blob/f8c5a072f7a8da9c7c42dd358868606d480eb648/All_cases.csv) · [学校论文记录](https://ink.library.smu.edu.sg/sis_research/11342/) · [逐应用复算](android-by-app.csv)

**对 auto harness 的取舍。** 把“更改实现”和“更改测试”作为两次可独立否决的操作。若只是元素移动，便应验证用户仍能完成原行为；若业务语义已改变，则让原约束的 owner 重新批准验收定义。试验用三个基线：仓库已有更新规则、相同变更知识加确定性测试、以及另加 agent 的方案。尤其记录适配虽然让用例变绿、却悄悄改变用户约定的例外。[实际依赖机器人](../dependency-bot/result.md) · [历史和发行版中的验收反例](../oracle-releases/result.md)
