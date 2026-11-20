# 商业与托管产品补样

2026-11-20，Asia/Shanghai。交付链主样本偏向可审阅实现的项目。本轮补查“谁接受持续目标、谁能批准、如何看整合队列、产品退场能带走哪些记录”。补样按机制、证据可获取性和与相邻样本的区别选择，不以公司估值、客户数或榜单热度排名。

| 入选 | 主问题 |
|---|---|
| Factory Droid / Missions | 里程碑验证责任、恢复后补验 |
| Cognition Devin / Devin Bots | 持久目标、子会话与共享授权 |
| Google Jules | 定时运行历史、只读期、停服导出 |
| GitLab Duo Agent Platform | 区分 UI / CLI / IDE 执行语义、定时自动化成熟度 |
| CodeRabbit | 自然语言策略与 GitHub 必检的连接 |
| Graphite | 推测验证与批处理、外部平台故障 |
| Google Antigravity | 在原 Jules 官方提及的平台上独立查证计划与里程碑审阅 |

本轮选 Factory 而未选择 Salesforce Agentforce Vibes，原因是 Factory 有可核对的 milestone 验证和中断恢复变更。Graphite 的现行产品页和实际事故记录可查，因此保留其集成阶段角色。Augment Intent 进入后续储备，不计入 7 个案例，也未就其可用性或优劣作判断。

## 复算与证据层级

从发布方检索和官方 llms 索引定位文档，优先选择至少两种材料，记录 URL、原始字节摘要与 UTC 抓取时刻。运行 `python fetch.py` 可重新抓取当前资料并按内容哈希存为新快照；`python compile.py` 生成 `cases.json` 并对 manifest 的每个文件计算 SHA256。变动页面的日期为空时仅代表抓取时状态；有日期的 launch、release 或事故才用来定位事件。旧版说明与新版本文档不合并为同一版本结论。

7 个补充案例共 26 条正文引用，28 份原始材料。其中 GitLab 的旧 triggers 地址正文仅提供迁移指向，已另存实际 automations 目的页并用后者作为行为证据。GitLab 和 Graphite 的可公开组件未用于推断托管执行。未对七项商业产品登录、运行试验或访问内部源码。Jules 属只读历史案例；其余六项观察到现行官方产品材料，未检查账号/地域/套餐资格。

## 纠错和反例

- Jules 的排程帮助页仍称不支持编辑；2026-01-26 更新页已明确支持编辑、暂停和恢复。10-29 退场公告优先决定 11-20 的状态。
- GitLab 19.2 的自定义流程 GA 与 19.6 的排程 beta 分开。不同执行入口不能共用一套审批推断。
- CodeRabbit 的早期 YAML 例子属于 V2。V3 去掉部分内置检查，GitHub 分支规则需另行设置，检查身份随目录作用域或 ID 改变。
- Graphite 的事故记录仅用于说明共享依赖发生过阻塞；不从个例推算长期故障率。
- Google 将 Jules 经验用于 Antigravity，并推荐用 CLI 辅助导出。资料未证明能导入原有任务与会话语义。
