# 研发自动化研究 Wiki · 第二版

读者可以从同一证据库进入[深度分析](../outputs/deep-report-v2.html)、[决策版](../outputs/insights-decision.html)和[四页 PDF](../outputs/insights-decision.pdf)。首轮资料和当时结论留在[原始项目索引](../wiki/index.md)。

## 从团队的决定开始

|下次会上要决定什么|应先查什么|决定什么时候需要改|
|---|---|---|
|预算先给谁|[路线选择](decision.md)、[35 产品台账](buyers/ledger.csv)、[版本和部署形态](product-code/result.md)|现有规则能否吃完难例、实测瓶颈是否仍在工程劳动。|
|可以把哪一步交出去|[迁移边界](compat/result.md)、[双引擎](handoff/result.md)、[跨系统回执](interoperability/result.md)|换人、改版本或丢回执后，外部动作能否独立查证。|
|什么时候提醒人|[谁来接手](ownership/result.md)、[提醒时机](supervision/result.md)、[真人研究](attention/result.md)|看到公开审批、找到 owner、真正节约人的时间需要不同证据。|
|让哪种自动化运行到哪一步|[CI 跨生态](ci-cross/result.md)、[特征是否提前可见](ci-availability/result.md)、[选版](optimizersrc/result.md)|时间留出、误阻成本、独立拒绝机制能否支持扩大范围。|
|跟哪些论文和团队|[研究组](labs/result.md)、[共同署名与课题](recall/groups.md)、[摘要全库与检索](abstract-index/result.md)|抽检未命中记录，区分方法、观察对象和可复现实验。|

## 证据覆盖和研究状态

[覆盖台账](state/coverage.md) · [本轮检查点](state/checkpoint.md) · [变更日志](state/log.md) · [原始筛查协议](protocol.md) · [独立审稿](state/editorial-review.md)

## 按专题查证

### 执行摘要

- [从 code agent 团队的角度，下一步投什么](executive.md)

### 选题和试点

- [本团队先投入哪里](decision.md)
- [怎样用一次内部试点决定是否扩面](pilot/protocol.md)

### 采购

- [35 个有可验收产物的选择](buyers/result.md)
- [70 个产品主张的独立核对](buyer-audit/result.md)
- [35 项产品中能直接查到哪些实现](product-code/result.md)
- [反馈、评估与发布判定的产品](evalops/result.md)
- [同一次试点分别在哪些地方计费](economics/result.md)
- [组织效能平台如何界定开发者、AI 使用和交付](eng-intel-vendors/result.md)
- [全球产品的三组同题对照](workflows/result.md)
- [国内产品的授权与接管](workflows/domestic/result.md)

### 演进

- [固定窗口内的发布与变更](evolution/result.md)
- [每项采购候选有哪些带日期的变化](product-history/result.md)
- [十项选型判断的版本与日期](version-anchors/result.md)

### 组织效能

- [同一个变更失败率，换数据库还会得出同一个答案吗](devlake/result.md)
- [CI 重跑的历史留出与成本](ci/result.md)
- [做重跑决定时已经知道哪些信息](ci-availability/result.md)
- [换到 GitHub Actions 后，重跑数据能说明什么](ci-cross/result.md)
- [公开 PR 的分层抽样](empirical/result.md)
- [共同仓库和月份的敏感性](cohorts/result.md)
- [历史能否找对接班人](ownership/result.md)
- [排队一天的 PR 是否值得提醒维护人](supervision/result.md)
- [从真人研究判断什么时候该打断工程师](attention/result.md)
- [怎样验收真正帮助接班人的一条消息](message-quality/result.md)
- [论文正文与统计量复算](papers/result.md)
- [从提交到交付的独立口径](throughput/result.md)
- [复算公开开发者研究](replication/result.md)
- [谁愿意进入开发者提效试验，谁会退出](selection-effect/result.md)

### 工程现场

- [迁移、质量与事故恢复](field/result.md)
- [Stripe、Ramp、OpenAI 和 StrongDM 的取舍](factories/result.md)

### 本地实验

- [12 个发布版本的规则迁移](migration/result.md)
- [真实依赖升级要按什么顺序](compat/result.md)
- [依赖更新机器人会验收到哪一步](dependency-bot/result.md)
- [公开修复与独立验收](oracles/result.md)
- [整个测试子包也漏过的错误](gates/result.md)
- [把历史验收反例追到十个正式发行版](oracle-releases/result.md)
- [换到 JavaScript 后，安装约束能挡住哪些错配](js-compat/result.md)
- [跨进程接管与丢失回执](handoff/result.md)
- [五组现有规范怎样记录批准、运行与回执](interoperability/result.md)

### 论文

- [从三篇顶会工作看跨版本验收](evolving-tests/result.md)
- [八届顶会的检索边界](venue-frame/result.md)
- [候选复核与研究组](venue-review/result.md)
- [改写检索词后还能找到什么](recall/result.md)
- [研究团队与持续跟踪问题](recall/groups.md)
- [六条能提供可复用实验工件的研究线](labs/result.md)
- [用摘要作第二道筛查能找回哪些问题](abstract-index/result.md)

### 自动优化

- [六种外层优化方法](optimizers/result.md)
- [两个固定提交的选择逻辑](optimizersrc/result.md)
- [同一模型的五次提交与任务分派](pairing/result.md)
- [提示版本真的能按获批对象发布和回滚吗](promotion-replay/result.md)

### 本地复算

- [模拟同事补全需求后，能否整件交付](cowork/result.md)

### 复核

- [复算、反例与覆盖边界](protocol.md)

### 研究建议

- [给下一次研发平台评审的决定](conclusion.md)

## 增量维护

优先从专题表中的稳定 ID、官方 URL、修订、下载哈希追到原始材料。新版本另存快照，再对比旧版；修正进入相应事实源和章节。用 scripts/build.py 更新初版入口，round2/publish.py 生成第二版视图，round2/check_reader.py 校验离线浏览与打印，再运行 round2/verify.py。完整指令及依赖范围见[协议](protocol.md)。
