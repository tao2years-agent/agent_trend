# 组织试点该按什么付钱

截至 2026-11-20，抽取 35 个采购候选中的 8 个，覆盖开发者工作台、云端委派、PR 集成、质量门禁、灰度发布、事故与 CI 分诊七类购买任务。检索单位是可签约套餐或已发布的计量条款。**同样 6 人、同样 12,000 credits，工作集中在一个人还是平均分给六人，足以翻转 Qoder 国际站 Teams 与 Enterprise 的本月现金成本顺序。** 对事故分诊，同样 100 次调查也可能跨过按需采购与年约折算价的分界。试点应先采集真实工作分布和账单，再承诺规模。8 项均有官方来源，以下演算没有客户实际订单、账单或节省率。[逐项价目与询价表](tariffs.csv) · [27 项原页索引及抓取时间](sources.json) · [可复算结果](sensitivity.json)

## 哪些供应商会为哪一步收费

|购买项|公开口径和合同边界|
|---|---|
|Qoder|国际站 Teams 每席每月 40 美元、含 3,000 credits，各席内含量不能共享；Enterprise 每席 20 美元，不含模型配额。共享包 3,000 credits 为 40 美元，一年有效，国际官网至少 2 席。中国站“全家桶”对应的三版是每席月 99 / 149 / 199 元，分别从 1 / 10 / 50 席起购。中国站 Enterprise / Enterprise VPC 含每席 3,000 且可团队共享，与国际站同名档的内容不同。国际与人民币价目不换汇比较。[国际组织价](https://docs.qoder.com/account/teams/teams-pricing) · [中国站计费](https://docs.qoder.cn/product-overview/billing-description)|
|Cognition Devin|自助 Teams 对全队每月收 80 美元，并将这 80 美元全部计入共享预付余额。选型时不应再给起始这 80 美元加一次模型费。企业按订单 ACU 计价，公开资料提供每会话归集方式。实际工作会产生计算用量；等回复、测试、克隆时还有少量 VM 用量，睡眠期间不消耗。应按合同确认何时进入睡眠和生产 OS 的费率。[自助条款](https://docs.devin.ai/admin/billing/self-serve) · [使用计量](https://docs.devin.ai/admin/billing/usage) · [企业计量](https://docs.devin.ai/admin/billing/enterprise)|
|GitHub Copilot cloud agent|Business 席位每月 19 美元，每席 1,900 AI credits 汇入池，超出按每 credit 0.01 美元。自动化同时消耗 Actions 计算，仓主承担这部分；个人自动化与共享自动化的 AI 用量可归不同账户。可设每次、每日等耗用上限。自 10/28 起，部分通过客户团队办理的企业可自愿采用 Copilot access，已有 Enterprise Cloud 许可可获零增量席位、用量从第一笔计，自助账户未普遍开放。同一企业不能叠套两种席位规则。[组织价格](https://docs.github.com/en/copilot/get-started/plans) · [方案迁移](https://docs.github.com/en/copilot/get-started/whats-changing-with-github-enterprise-and-copilot) · [自动化账单](https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations)|
|Mergify|国际站 Max 月付 21 美元/活跃席位，年付折合 18 美元；原页切到欧元为 18 / 15 欧元。30 天滚动窗口内开 PR 或更新其 head 的自然人可被计入，跨仓去重、按天比例结算，机器人排除。部分方案按拥有写权限的 Collaborators 计费；应取得客户账单字段。180 个 PR 由同一批人完成，单凭 PR 总数算不出价格。[定价切换页](https://mergify.com/pricing) · [详细账单规则](https://docs.mergify.com/billing/)|
|SonarQube Server|按实例、年和许可代码行数报价。每项目取最近分析中代码规模最大的分支或 PR，跨项目再相加；测试、注释、空白等排除，重复扫描相同规模的代码不会反复占用容量。会超许可的分析可能被拒，旧数据仍可浏览。需要按目标生产、集群或灾备拓扑询价，云 Team 起价不能填入自托管预算。[Server 价目与边界](https://www.sonarsource.com/plans-and-pricing/sonarqube/) · [LOC 口径](https://docs.sonarsource.com/sonarqube-server/2025.6/server-update-and-maintenance/monitoring/lines-of-code)|
|LaunchDarkly Guarded Rollouts|11/20 取得的套餐文档将 guarded rollouts 列入 Release Autopilot。定价交叉表列 Developer 有限使用、Foundation 优惠至 2027-02-01、Enterprise 附加项；基础项目如 SDK service connections、客户端 MAU 仍有各自的量阶。旧支持 FAQ 说完整权益要 Enterprise+Guardian，本轮已将两种说法并列回写 BUY26。公开页未说明旧合同如何迁移、限免结束后的统一 guarded rollout 单价，均应询价。基础 AgentControl AI run 的单价也不能乘以发布次数。[现行套餐](https://launchdarkly.com/docs/home/account/plans) · [现行定价](https://launchdarkly.com/pricing/) · [旧条款快照及前值](buy26-prior.json)|
|Datadog Bits Investigation|US 定价资料对自主调查给出约 4 AI credits 的**估计平均数**，按上下文和复杂度浮动。年约起价每月 500 美元含 500 credits，按需每 credit 1.30 美元；所购月额度不滚存，超过后自动按需。AI Credits 也可被其他产品使用。自动触发归 Autonomous Agents，个人可设限额，组织总额默认未设。监控、日志等基础消费应另看已有合同。[美国公开标价](https://www.datadoghq.com/pricing/?product=ai-credits) · [计量](https://docs.datadoghq.com/account_management/billing/ai_credits/) · [上限和归属](https://docs.datadoghq.com/account_management/billing/ai_credit_limits/)|
|CircleCI Chunk|当前文档仍标 beta，无额外 Chunk 功能费。运行可耗 CircleCI compute credits，BYOK 再走各自模型商账户。默认托管密钥每日 400,000 tokens，12:00 UTC 重置。Performance 额外 25,000 CI credits 为 15 美元，Linux Medium 10 credits/分钟仅是指定资源类的例子。2026-01-20 发布说明把托管密钥优惠限定于 beta；GA 后收费项目与单价须另问。[Chunk 当前说明](https://circleci.com/docs/guides/toolkit/chunk-setup-and-overview/) · [CI 计划价](https://circleci.com/pricing/) · [有日期的发布说明](https://circleci.com/changelog/use-circleci-managed-keys-for-chunk/)|

## 同一次试点的分母和账本

**假设**一个 30 天的整月，12 人研发组新增 6 个 Copilot Business 席位，用共享自动化交付代码，再交给 Mergify 排队。该 GitHub 组织没有其他可用 AI 额度，共用量 14,400 credits；标准 Linux 2-core x64 的 **600 分钟**已经按作业取整、扣除原有计算额度，假设它们是该试点唯一的增量可计费运行。8 个自然人整月符合 Mergify Max 活跃席位条件；其余人未符合，不由 12 人的编制数推算账单。最终验收 72 个互不重复的变更。一项变更经过两个工具只在分母中出现一次。[假设输入](assumptions.json) · [逐行试点账本](pilot-ledger.csv) · [Actions 单价与取整](https://docs.github.com/en/billing/reference/actions-runner-pricing)

|归属|计算|当月美元|
|---|---|---:|
|GitHub 席位|6 × 19|114.00|
|GitHub 超额|max(0, 14,400 − 6 × 1,900) × 0.01|30.00|
|仓主新增 Actions 计算|600 × 0.006|3.60|
|Mergify Max|8 × 21|168.00|
|**新增现金支出**|前四行|**315.60**|
|新增人工复核机会成本|300 个实际工作分钟 ÷ 60 × 假设时薪 60|300.00|
|**含人工的新增经济成本**|315.60 + 300.00|**615.60**|

另记 1,000 分钟排队历时，只用于交付时间指标。现有共享平台的 200 美元分摊可用于全成本表，本试点假设没有触发扩容，所以不进入上述增量总计。已经过账的模型额度、同一次提交的 CI 和人的等待时间都不能再次按任务重计。若出现新增 runner、存储、税费，应从真实账单选择单一归属行。72 件时每件现金约 4.38 美元、含新增人工约 8.55 美元；最终只验收 48 件、现金与人工保持上述值时，后者变为 12.83 美元。假设每小时机会成本为 60 美元，需要约 10.26 个小时可归因的毛工时收益，才能覆盖现金及新增复核机会成本；这些数字来自演算，未观察实际节约。[敏感性输出](sensitivity.json)

## 两个会翻转决策的计量错误

**把每人余额错误并成组织池。** 国际 Qoder 假设月初一次全月采购 6 席，无历史包或成员个人包。令第 i 人的实际耗用为 uᵢ。Teams 本月现金 = 6 × 40 + 40 × ceil(Σ max(0, uᵢ − 3,000) ÷ 3,000)；Enterprise = 6 × 20 + 40 × ceil(Σ uᵢ ÷ 3,000)。6 人各用 2,000 时，两者是 **240 / 280 美元**。若仅 1 人用 12,000，其余闲置，同样总消耗变为 **360 / 280 美元**。错误做法会给重度用户调用别人的剩余额度。算例只比较美元与公开配额，未把权限差异、套餐不能平滑切换或中国区价目折算进去。次月要结转有效共享包剩余量，不得每月重复购置。[席位与共享包规则](https://docs.qoder.com/account/teams/teams-pricing) · [两种分布](sensitivity.json)

**把一个调查工单错误当成一个 credit。** 假设 Datadog 每月 100 次自主调查、全年每月负荷相同、无其他产品消耗、无定制折扣。若每次平均耗 3 credits，按需 390 美元/月，对比最低年约折合 500 美元；若耗 5 credits，按需 650，年约折合仍为 500。两种负荷分别位于约 **384.62 credits/月**的收支线两侧。当前页面约 4 的示例只给出测量起点。遇季节性负荷，应逐月计算不可跨月结转和超额后再合计全年；仅试用一个月时不得把 500 美元当成可随时取消的全年承诺。低风险验证是取每次调查的实际 credits 与监控触发来源，并核月账单。[年度与按需口径](https://www.datadoghq.com/pricing/?product=ai-credits) · [逐场景结果](sensitivity.json)

另一类错误会阻断发布。假设两个 SonarQube 项目的分析分支分别为 80k/60k 和 55k/40k 有效 LOC，正确用量是 135k。相加所有分支会误得 235k。在假设的 150k 许可上限下，后者会错误触发增购决策；若随后第二个项目最大分支真的增到 80k，总量会到 160k，应测超限处理。这一算例没有为 SonarQube Server 编造单价。[许可计量](https://docs.sonarsource.com/sonarqube-server/2025.6/server-update-and-maintenance/monitoring/lines-of-code)

## 价格时点、回写和下一轮询价

27 项来源中，26 份为本轮取得的完整官方 HTML，1 份复用旧 BUY26 支持页。每项有网址、获取 UTC 时间、文件哈希和可检索文本；服务商的抓取时间不自动等于价格生效日。旧 Guardian FAQ 本轮直抓返回 403，沿用当时记录的原页与 SHA；新套餐文档和价目同时保存。买方台账在 11/20 从 123 份复用与新增来源补到 125 份，仍为 35 个去重购买项；此前源码核查基线继续保留 123 份。其余七项此次增加的是定价视图，没有用标价修改原采购对象的交付机制。[来源总账](sources.json) · [BUY26 勘误前值](buy26-prior.json) · [买方修订材料](buyer-sku-sources.json)

复核时先在同法人、同地区、同计划的控制台导出一个完整账期。要求供应商明确资格判定、额度所有者、免费余额何时重置、超额是停止还是自动收费、是否含税和最低承诺。把组织共享池与个人池分列；财务预算用新增现金，产能比较另记真正投入的复核分钟和基准对照。每项的专属询价问题均在价目台账最后一栏。季度续约、促销到期、GA 或账单单位变化时，保存带新日期的新快照，调整公式后重算同一组输入，不覆盖旧条款。[询价与公开价目](tariffs.csv) · [计算脚本](calculate.py)
