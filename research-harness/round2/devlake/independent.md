# Apache DevLake 变更失败率详情的独立复核

核验日为 2026-11-20。DevLake 的官方算例有五次部署，其中两次引发一个或多个事故，CFR 为 40%。v1.0.3-beta13 同卷的 Grafana **Change Failure Rate 详情页第 86 号面板**有两份实现。在完全相同的官方测试数据上，按 MySQL SQL 口径得到 40%，按 PostgreSQL SQL 口径得到 120%。此处独立核验的是发布源码、上游测试输入及关系运算；实际数据库回放另见本目录主研究。线上数据受影响的频率未知。[官方定义](https://devlake.apache.org/docs/v1.0/Metrics/CFR/) · [MySQL](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/mysql/dora-details-change-failure-rate.json) · [PostgreSQL](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/postgresql/dora-details-change-failure-rate.json)

## 分母和差异发生条件

指定同一非空项目、同一时区、相同起止时刻。两份面板都经 project_mapping 的 cicd_scopes 选出成功的生产部署记录，再按 deployment ID 分组，用每组最晚完成时刻决定是否进窗。设入窗部署数为 D，每次部署经关系表连接到的不同、存在的事故 ID 数为 k。MySQL 累加 k>0 的部署数再除以 D，PostgreSQL 累加 k 再除以 D。当 D>0，差额等于所有部署的 max(k−1, 0) 之和除以 D。重复连接同一个事故 ID 会被 DISTINCT 消除。选择纯 0/1 样本会让两份查询相同。存在一对多就会有差异，即使显示比例低于 100%。86 号 Stat 采用 percentunit 和 lastNotNull，配置未截断高值。两份查询都只按 deployment_id 连接关系，若不同项目复用该 ID，尚需核实归属；本样本的目标 ID 无这一干扰。

## 能否用真实上游输入复现

上游 TestConnectIncidentToDeploymentDataFlow 明确导入 16 行部署 commit、8 行项目映射与 7 行 incidents，并验证 6 行事故部署关系。86 号面板读取 incidents；issues 仅用于相邻列表补充展示。以测试项目 project1、2022 年 9 月 UTC 计算，pipeline1、2、4、6、7 的不同事故数分别为 0、1、0、0、5。后五个挂在 pipeline7 的事故开在 11 月，仍会进入 9 月分子，因为第 86 号面板按部署完成时间入窗。原始任务把项目范围内事故连到其创建时刻之前最近一次成功生产部署，这种规则可以形成一对多，业务因果仍需事故归因核实。这是 Apache 项目公开的成套测试夹具；未抽取客户生产记录。[测试输入和预期](https://github.com/apache/devlake/tree/57b2641eb922052d859c5b7530c5b2f218fe3faf/backend/plugins/dora/e2e/connect_incident_to_deployment) · [测试入口](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/backend/plugins/dora/e2e/connect_incident_to_deploy_test.go) · [关联实现](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/backend/plugins/dora/tasks/incident_deploy_connector.go)

## 一条修复公告如何留下两种口径

|可核查时点|该时点源码能说明什么|
|---|---|
|beta12，标签指向 2026-04-26 的提交|旧单文件已经按每次部署的事故数求和。|
|2026-05-30，修复 PR #8890 合并|修改旧单文件的分子与配套标签。合并后的 86 号 SQL 指纹以 df25090adb89 开头。|
|2026-06-05，Grafana PostgreSQL 支持 PR #8870 合并|在这一合并提交上，MySQL 详情 SQL 与刚修复的旧文件逐字相同，新增 PostgreSQL 文件中的 SQL 指纹为 8710adf49558，使用事故数。|
|2026-06-19 发布 beta13 至 2026-11-02 发布 beta19；2026-11-19 主干提交 652d7da9|beta13 发行说明同时列出上述两个 PR。连续七个 beta 标签和当日取得的主干快照内，两种方言各自的 86 号 SQL 哈希均保持不变。结论覆盖这些固定版本；未核验自定义看板或每个中间提交。|

[修复 PR](https://github.com/apache/devlake/pull/8890) · [方言支持 PR](https://github.com/apache/devlake/pull/8870) · [beta13 发行说明](https://github.com/apache/devlake/releases/tag/v1.0.3-beta13) · [beta19 发行说明](https://github.com/apache/devlake/releases/tag/v1.0.3-beta19) · [主干固定提交](https://github.com/apache/devlake/commit/652d7da9323fd4447d3c2d3705f482ff5a9f54d8)

## 足以推翻扩大解释的反例

- 同卷 PostgreSQL 的 DORA by Team 第 14、5 号面板，对有事故的 deployment ID 做 DISTINCT，在单次部署组内上限为一。不能将详情 86 的偏差概括为所有 PostgreSQL DORA 看板。[按团队看板](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/postgresql/dora-by-team.json)
- 详情 85 号面板列部署与事故的关系列，并连接 issues 取标题；58 号时间线对事故创建时间另设窗口，且允许成功的非生产部署。分别数这两张表的行数，都无法直接复核 86 号面板的分子。实际采购验收应记录部署 ID、事故 ID、项目、时区、面板和版本，并保留有多个事故的样本。[详情面板固定文件](https://github.com/apache/devlake/blob/57b2641eb922052d859c5b7530c5b2f218fe3faf/grafana/dashboards/postgresql/dora-details-change-failure-rate.json)

运行 `python independent-check.py` 可在本目录离线检查三份来源索引的 SHA256，复算固定标签 SQL 指纹与逐部署计数。[版本与看板索引](independent-sources.json) · [上游夹具与定义索引](independent-fixture-sources.json) · [变更索引](independent-history-sources.json) · [复算结果](independent-check.json)
