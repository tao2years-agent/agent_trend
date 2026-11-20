# 35 个采购竞品的独立证据审稿

覆盖 35/35 个 BUY 产品，每项 2 条，共 70 条主张。按修订前口径：明确 60 条，部分支持 7 条，未证 1 条，冲突 2 条。所有需收窄的字段已回写采购事实源，另补证据阶段或版本区分。本次没有登录产品或重跑厂商基准。

先从 ledger 各选两条不同的具体主张，再直接读取原始 HTML、源码、Atom 或 Markdown；逐项对照对象、执行动作、验收权限或版本。HTML 的行号是 views.py 在相应快照去除导航和脚本后生成的正文行号，源码及 Markdown 使用原始行号；meta/time 定位到原始 DOM。positions.tsv 保存各片段哈希、完整快照哈希及链接。正文结果反映独立复查，不代表对其余字段全面背书。

[70 项判断与证据](claims.tsv) · [精确定位与哈希](positions.tsv) · [变更前后逐字段](corrections.tsv) · [版本源码补证](codex-tag-sources.json)

## 已写回的修订

- **BUY01 · human_takeover**　开发者可决定是否重试；/undo 可撤回本会话由 Aider 创建的最后一个 Git 提交。依据为 E04-3@553-575。
- **BUY03 · human_takeover**　开发者可选恢复文件、会话或二者；HEAD 偏离检查点基准时拒绝文件恢复，可仅恢复会话，或另行有意调整分支。依据为 E07-2@403-425;E07-3@51-58。
- **BUY05 · availability_version**　旧 IDE Quest 公告列出的退场节点为 2026-10-15 23:59（UTC+8）；当前说明新用户无入口、既有用户分批关闭。新版 Qoder 独立验收。依据为 CN01@1-20。
- **BUY06 · human_takeover**　团队 lead 可批准或退回成员计划并发出关停；操作者可停止成员，MR 是否需独立人工批准取决于 GitLab 仓库规则。依据为 CN05@167-176;CN06@12-23;CN08@1-38。
- **BUY14 · availability_version**　2026-04-14 以 Routines 进入 research preview；现行文档名为 Scheduled tasks，旧称与 SDK 不重复计数。依据为 F04-2@meta:article:published_time;F04-2@1-6。
- **BUY18 · human_takeover**　团队定义标准并验证结果；从 transformation registry 选择转换，用 def learnings 查看和管理该转换从历史运行提取的 lessons。依据为 P14@76-84;P14@430-435。
- **BUY20 · unknown_or_boundary**　v0.50.0 发布说明称自动批准配置只归宿主且该版执行路径仍禁用。另一个固定源码提交含有条件批准分支，版本分别记录。依据为 D07-3@95-100;D07-2@123-134;D07-1@2762-2781。
- **BUY24 · human_takeover**　有相应配置权限的操作者可调整队列并发、批大小和失败拆分次数，必要时暂停队列；细粒度角色权限需按安装复核。依据为 P21@25-36;P22@147-150。
- **BUY32 · human_takeover**　响应者审查证据并决定哪些规则保持人工。原生工具不回滚或重启；自动调查使用团队连接器凭据，连接器或 Private Agent 是否可外写需按授权核对。依据为 P05@249-261;P07@110-119。
- **BUY33 · human_takeover**　值班者可纠正原因并附遥测证据；有相应权限者可在 Monitor Management 查看、删除反馈生成的 memories。该页未列具体角色要求。依据为 P09@2018-2035。
- **BUY34 · human_takeover**　负责人选停止点并补 user_context；续跑首选 sentry_run_id（UUID），旧数值 run_id 仅作兼容；对生成的 PR 仍走仓库验收。依据为 P10@48-61。
- **BUY35 · availability_version**　CircleCI Cloud + GitHub App 的适用组织；当前文档标 beta，2026-02-27 增加 inline Fix Job。依据为 P02@2-5;P02@meta:article:published_time;P02@time:0。

## 如何复核

在本目录执行 python audit.py 重新核验 70 项数量、全部片段定位和哈希、修订后的事实源及 Codex 发布标签下两份源码的一致性。执行 python audit.py BUY32 可在本地显示该产品选中的原始段落。ledger-at-review.csv 是写回前的工作副本，CircleCI 日期在接到硬冲突后已先由主研究人员更正，因此其更早的原字段另记入 corrections.tsv。

核查边界最清楚的反例包括 Rootly 原生调查工具与连接器写权限不同、Cline 恢复文件与会话的约束不同、PR-Agent 发行说明与另一个源码提交中的条件分支不同，以及 PR 创建与业务部署的责任不同。没有把缺少文档说明的具体管理员角色推成已证实的购买条件。
