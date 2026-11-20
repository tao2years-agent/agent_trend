# 同一份部署记录，为什么仪表盘会给出 40% 和 120%

在 Apache DevLake 自己的一套端到端测试数据上，2022 年 9 月 project1 有五次符合条件的生产部署。两次部署关联了事故，其中一次关联五起，另一次关联一起。将同一批记录原样投影到查询所需的四张表，在 **v1.0.3-beta13 的 Change Failure Rate 详情页第 86 号面板**运行其原有查询，MySQL 8.4.5 返回 **40%（2/5）**，PostgreSQL 17.5 返回 **120%（6/5）**。beta19 的同一面板得到相同结果。后者计算出每次部署关联的事故数，在多起事故对应一次部署时不能用作失败部署的比例。这一反例的输入来自上游测试夹具，不能据此估计客户仪表盘受影响的频率。[Apache MySQL 面板](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/mysql/dora-details-change-failure-rate.json) · [同版 PostgreSQL 面板](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/postgresql/dora-details-change-failure-rate.json) · [逐个运行结果](replay.csv)

### 从指标的定义追到发布历史

DORA 的现行交付绩效模型衡量五项指标。变更失败率关注需要立即干预的部署占比；部署返工率关注由线上事故引发的非计划部署占比。一次发布引发多条工单，两项指标都需要先说明什么算一次部署、哪段窗、谁确认需要干预。DORA 的 Quick Check 于 2026 年 4 月更新，增加部署返工率并使用新版比较基线。采购或迁移历史报表时，应同时登记指标版本、采集方式和来源。[DORA 官方定义](https://dora.dev/guides/dora-metrics/) · [2026 年 4 月更新](https://dora.dev/insights/quickcheck-updates/)

2026 年 5 月 28 日作者提交修复，5 月 30 日合并，改为“本部署是否关联至少一条事故”。作者在 PR 中提及一次真实窗口的 23 次部署、6 起事故涉及 4 次部署；生产明细未公开，本报告仅在本地构造相同计数另行验证。6 月 5 日合并的 PostgreSQL 支持拆出了两份 SQL；6 月 19 日发布的 beta13 说明同时列出两项变更。独立复核追到 beta13 至 beta19 的七个标签以及 11 月 19 日主干固定提交，面板 86 的两份 SQL 各自在这些版本保持字节一致。该版 PostgreSQL 的按团队看板中另外两个面板按部署去重，不能把这个结论推广到全部 PostgreSQL 看板。[修复 PR](https://github.com/apache/devlake/pull/8890) · [方言支持 PR](https://github.com/apache/devlake/pull/8870) · [beta13 发布](https://github.com/apache/devlake/releases/tag/v1.0.3-beta13) · [独立复核与例外](independent.md)

### 怎样拆开查询错误、关联缺失与事后时间

在临时目录中启动 Oracle 发布的 Windows MySQL（仅本地共享内存），另用 PGlite 0.3.7 内含的 PostgreSQL 17.5 执行 PostgreSQL 查询。每次只替换 Grafana 项目与时间变量，保留过滤、聚合和除法。范围包括修复前后和两个发布标签的六份 SQL 版本，每份使用八种合成历史、完整上游用例和按事故创建日截断的上游用例，共 **60 次数据库查询**。DB、自建表和输入分别登记。未运行整套 DevLake 采集后端、Grafana 或客户数据库。[固定引擎和校验](engine-lock.json) · [原件清单](sources.json) · [实际版本及查询指纹](audit.json)

|同一输入|beta13 MySQL|beta13 PostgreSQL|该测试区分什么|
|---|---:|---:|---|
|同 23 次部署，6 起事故对应 4 次部署，合成|17.39%|26.09%|部署去重与事故去重不是同一个分子。|
|同 23 次部署，6 起事故分别落到 6 次部署，合成|26.09%|26.09%|只在一对一演示数据上验收会漏掉差异。|
|上游 project1，冻结全部已出现的事故|40%|120%|同样五个部署，生产事件与工单的一对多关系可在产品原有测试资料中重现。|
|同一上游部署，只保留 9 月底前创建的事故|20%|20%|其中五起 11 月创建的事故，在完整记录中仍进入 9 月部署的分子。此行按创建日做敏感性测试；无法回到真实 9 月底重建工单何时完成关联。|
|4 次部署真实有 2 次需干预，故意漏记一条关联，合成|25%|25%|即使计算正确且看板一致，也会低于夹具中实际的 50%；需独立校验事件关联覆盖。|
|没有符合条件的成功生产部署，合成|空|空|保留“没有分母”，不能显示为“失败率为零”。|

**交给采购团队的演示。** 拿同一受影响的发布制造两张不同事故单，再加入一次分三步写入的部署和一件晚报的事故。要求供应商从结果钻取到分子、分母、关联时间和过滤条件；隔月回填时保留“当时知道的数字”及“用今天记录重算的数字”。当管理者要决定某条自动化是否可以扩面，最先应确认该口径能从排障故障中区分“几次部署失败”与“产生多少工单”。多个商业平台的 AI 参与率还有额外的人与任务定义差异，应分别验收。[三家组织效能平台](../eng-intel-vendors/result.md) · [独立复核脚本](independent-check.py) · [引擎回放](replay.py)

获取固定引擎后运行 `python devlake/engine_inputs.py`、`python devlake/replay.py`。原生 MySQL 回放在带 Node 的 Windows 下执行，需要临时文件空间；已归档的明细与独立源码/夹具复核可直接离线阅读。
