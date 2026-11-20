"""Compile read-throughs with official source locators. Dates refer to the documented event."""
from fetch import BASE,ROOT
from hashlib import sha256
import json
rows=[
('M01','Factory Droid / Missions','多 worker 工程任务编排',
'迁移或跨模块改造超出单次会话；需要先把目标分成 feature 与 milestone，并指定何时检查。',
'团队与 orchestrator 明确范围、依赖、技能和里程碑；每个 milestone 末安排 validation workers。文档给出的资源估算按每个里程碑在首轮通过时执行两次验证计算；发现问题后可生成新的修复任务。CLI 的 Mission Control 展示进度。',
'先批准计划；执行过程中可暂停 orchestrator、解释阻塞、改方向。验证频率由里程碑划分决定，QA 验证可在设置中关闭。',
'团队可以把一键启动服务、对应用输入、持久日志等作为仓库准备工作，帮助其他人复用验收方式。产品文档没有承诺增加 worker 就能缩短总工期。',
'公开技术文档和版本记录已核对；未接入产品，未检查托管调度实现。验证者与实现者共享错误假设时仍可能一起放过问题。',
'2026-08-29，CLI v0.208.0 / Desktop v0.165.0 修复 Mission 被中断、暂停或恢复后里程碑验证仍应执行的行为。',
'最能区分编排质量的问题是恢复后还欠哪些检查。审批内容应能说明验收标准何时执行，以及更改标准需谁重新确认。',
'喂入同一小迁移，在验证前暂停并恢复；比较任务状态、验证记录、追加修复和最终可重放证据，独立验收者另测隐藏用例。',
[('plan','Planning & Validation：Validation、Development scripting for QA、成本估算',''),('run','Running in the CLI：Intervening and redirecting，计划批准后的监控与暂停',''),('log','CLI v0.208.0 / Desktop v0.165.0 的 Mission milestone validation 修复','2026-08-29')]),
('M02','Cognition Devin / Devin Bots','持续目标、子会话与人工决策队列',
'团队想持续维护某个产品目标，例如减少一类回归；任务顺序需要根据上一轮结果持续决定。',
'Bot 保存自己的会话、记忆、工具与权限，为子任务启动 Devin sessions，跟踪结果并决定下一个动作。Needs you 汇集 PR、权限请求与待决策项；Bot 的访问资源与能向 Bot 发消息的人分开配置。',
'新 Bot 默认私有；分享 Bot 也分享请求其使用既有授权资源的能力。管理员可查看/撤销 grant；若只需传播做法，应分享 template。Mark done 清理个人侧栏的语义与停止工作不同。',
'团队能为长期结果指定负责人，用一个异常队列处理分散会话的决定；持久授权使“谁能调用 Bot”和“Bot 能访问什么”都成为组织治理对象。',
'2026-11-17 上线，属于早期产品。内部案例是厂商自述，未取得独立对照、真实组织采纳数据、托管引擎源码或授权环境运行证据。',
'2026-11-17，Cognition 发布 Devin Bots，将持续目标委托给可以并行发起多个 Devin 会话的 Bot；11-16 的 Cloud 更新还区分个人 Mark done 与关闭会话。',
'收件箱应计量每项决定的到达、等待、打断次数与结局；仅记录 Bot 完成的子任务数可能掩盖等待人处理的关键瓶颈。',
'在无生产连接的试用组织给 Bot 一项带停止条件的持续维护任务，对比共享模板与共享 Bot；核对新任务、权限请求、撤权后访问及人工决策时长。',
[('bot','What needs you、权限请求与 Bot 默认行为',''),('access','Who can use、What it can access、Resources 和 revoke；模板与共享 Bot 的差别',''),('launch','Introducing Devin Bots：持续目标、多 Devin 会话、内部自述案例','2026-11-17'),('log','November 16：Subscribers and Mark done，个人完成与后台会话状态的区别','2026-11-16')]),
('M03','Google Jules（已只读）','异步工程任务的历史参照',
'历史上将 GitHub 仓库例行维护设为定期任务，或启动单个异步任务，侧重用计划、活动记录和 PR 监督工作。',
'历史任务先克隆仓库、初始化虚拟机并安装依赖，再给出步骤和假设；人可以反馈后批准。历史计划文档还明确离开页面后计时器可能自动批准。曾支持定时启动任务、产生 PR；退场时可导出提示、计划、活动、补丁和配置。',
'计划反馈与手动批准曾提供干预窗口，但离开后的自动批准不满足必须显式同意的控制要求。当前优先回收配置与任务证据，已有代码分支和 PR 留在 GitHub。',
'这是选择平台时必须考虑的数据可携带性案例。团队的长期资产包括判定依据、排程与历史，不仅是最终的代码。',
'截至 2026-11-20，官方时间表已进入只读阶段，不能列为可启动新任务的在售选项。退场公告提及 Antigravity 并给出辅助导出方式，未承诺将原会话状态无损导入新平台。未登录服务确认租户状态。',
'2026-10-29 发布退场公告，列明 11-11 后转为只读、计划于 12-31 结束；另一处文档对编辑排程仍写需删除重建，而 2026-01-26 的更新已允许编辑、暂停与恢复。',
'用时间有界的历史证据解释产品演进；合同或试点应明确停服时可导出哪些交付证据，迁移后能恢复哪些语义。',
'利用用户自愿提供的脱敏导出样本查验计划、记录、补丁、定时任务是否可索引及关联；新方案独立验证只读和迁移流程。',
[('log','Jules Turndown，以及 Update Scheduled Tasks 的时间线','2026-10-29'),('schedule','Scheduled Tasks 文档 Creating / Managing；与 2026-01-26 发布记录并列复核',''),('plan','Reviewing the plan：虚拟机设置、审批以及离开后计时自动批准','')]),
('M04','GitLab Duo Agent Platform','事件和定时触发的组织研发流程',
'团队要将 issue、CI 与 merge request 连起来：浏览器事件或计划发起任务，后台执行，再将阻塞或需要决定的会话集中给人。',
'Foundational flows 与团队自定义 flows 分开。GitLab UI 中 Developer Flow 由 runner 运行并创建/更新 MR；CLI 在本机执行；IDE 的 Software Development Flow 拟计划并暂存改动。Sessions 的 Needs a decision 汇集待回应会话。19.6 的定时自动化使用有限服务账号并记录运行历史。',
'顶级 group 与项目控制启用条件，具权用户配置服务账号、触发器和流；负责人在合适界面审阅 MR 或确认操作。由 Web Chat 发起独立后台流时，不能沿用 Chat 工具审批的语义。',
'直接利用团队原有 issue、runner、CI 和 MR 对象传递任务标识，结合每个自动化的运行量、成功率、失败原因和会话详情判断是否需要人工接管。',
'Custom Flows GA 与 19.6 scheduled automations beta 的成熟度不同。定时执行仅适用于启用的 AI Catalog 自定义 flow 或 Developer Flow，其他 foundational flows、外部 agents、用配置文件定义的 flows 不适用。有公开 GitLab 组件，本案例证据为文档与发行记录，未复核其服务端实现或部署。',
'2026-07-16，19.2 将 Custom Flows 发布为 GA；2026-11-19，19.6 的 scheduled automations 进入 beta，并在 Automations 界面整合定时/事件触发、运行历史和会话详情。',
'同一个品牌内部可以同时存在交互式与无人值守的运行合同。平台应将执行位置、运行主体和审核策略附着在一次 run 上。',
'在试验项目触发同一修复意图的 Web、CLI 和 IDE 路径，再用有资格的 flow 配置定时执行；核对运行身份、审批归属、会话 ID 和重复触发。',
[('flow','Choose a flow for coding tasks 对比 UI、Chat、CLI、IDE 的执行与审批',''),('sessions','Needs a decision 和 Cancel a running session',''),('log','GitLab 19.2：Custom Flows 与 CLI 一般可用','2026-07-16'),('new','GitLab 19.6：scheduled automations 为 beta、运行记录、独立 service account','2026-11-19'),('automations','Scheduled automation prerequisites：获准账号角色、启用条件和不支持的 flow','')]),
('M05','CodeRabbit','PR 评审及合并前规则验证',
'组织希望在 PR 上一致执行评审规范，部分如变更是否越出工作项范围难以用纯规则表达。',
'内置与自然语言自定义检查支持不同配置方式。V2 可通过 pre_merge_checks 表达部分内置检查；V3 无此 YAML 节点，禁用若干内置检查，仓库可在 .coderabbit/pre-merge-checks/ 设置自定义定义。适用版本可向 GitHub 发布 Check Run。',
'管理员选择策略和告警/错误等级。要成为合并必检，需要在 GitHub branch protection 或 ruleset 中自行将真实检查标识设为 required；修改规则 ID 或目录作用域会影响检查身份。',
'可以从 warning 阶段收集争议和例外，再决定是否把具体检查升级为必检；需要指定归属，避免自然语言策略扩张后无人维护。',
'商业评审服务内部推理和误报率未实测。配置 V2 与 V3 的语义有别；路径不匹配可标 skipped，未载入定义时可能不报告检查。仅有“发布 Check Run”不能证明违反规则时一定挡住 merge。',
'2026-03-11 公布内置与自然语言自定义 pre-merge checks、warning/error 和配置方式。当前文档另列 V3 迁移语义，发布日期不作为 V3 推出的证据。',
'要分别测量建议是否合理、平台是否收到状态、分支规则是否强制。三处中任一处缺失，都可能出现“看见红灯仍能合并”。',
'准备匹配、不匹配路径、跳过评审三类 PR；把一条可客观核对的检查从 warning 升为 required，比较报告、规则 ID、是否可合并和所有者处置。',
[('checks','V2 与 V3 差别、Require a check before merge、真实检查身份和 skipped',''),('custom','How Custom Checks Work、重跑与已失败检查、链接仓库上下文',''),('log','发布说明 Pre-merge checks 的检查类型、运行时机与 warning/error','2026-03-11')]),
('M06','Graphite Merge Queue','栈式 PR 与批量合并',
'多个团队同时推送有依赖的 PR；单个分支检查已绿，仍要确认最终组合能通过 CI 并依正确顺序合并。',
'以 stack 为队列单位；支持同一 stack 内快进并行测试、多个 stack 的推测性并行 CI、以及成批测试。批失败时可缩小子集定位问题 stack 并剔除；前序失败时随后推测的组合需要重跑。',
'管理员配置 GitHub 条件和队列优化、并行度与批策略，团队查看排队和失败状态；平台停摆时需由负责人选择暂停、等待恢复或启动受控替代流程。',
'适合把 PR 生成吞吐与整合能力分开观测。可按仓库计量排队时间、重跑成本、合并失败率与批失败后定位成本。',
'官网仍展示产品与试用入口，Cursor 于 2025-12-19 宣布收购协议并表示产品独立运营。没有检查托管队列源码或租户功能。易抖动 CI 会放大下游重跑；单次故障不能推断普遍可用性。',
'2025-12-19 Cursor 公告确认整合关系，未将未来集成计划当作已实现功能。另据官方状态页，2026-10-30 一次 PR 无法合并事件持续 15 小时 20 分钟并已恢复；这是事故记录。',
'组织级收益取决于下游队列与测试稳定性；多 agent 生成更多 PR 时，应事先衡量推测 CI 增量成本和外部平台故障的等待损失。',
'用历史有依赖的 PR 到达序列仿真串行、并行与批处理；在隔离环境复现普通测试失败，统计 CI 重跑、队列尾延迟，再演练供应商不可用时的待办回收。',
[('home','产品官网的 GitHub 接入、试用和 Merge queue 入口',''),('queue','Parallel CI、batch merge failures、flaky tests 的代价',''),('setup','Set Up The Graphite Merge Queue 的仓库配置与接入',''),('status','Notice history，Oct 30 PRs are unable to be merged，持续时间与已恢复','2026-10-30'),('log','Cursor 公司公告 Graphite is joining Cursor，协议和保留独立产品声明','2025-12-19')]),
('M07','Google Antigravity','并行开发任务与里程碑产物审阅',
'多项开发工作并行，负责人需要在关键检查点查看计划、diff 或浏览器录屏，并针对具体产物反馈。',
'Google I/O 公布的 2.0 桌面应用整合多 agent、动态子 agent 和后台定时任务；当前 Artifacts 文档列出计划、diff、架构图与录屏，在 App 与 CLI 提供不同的查阅入口，可在计划上内联评论。',
'在需要先计划的任务选择适当的 review policy；Always Ask 会停下来等待批准。按当前文档，显式 /plan 默认仍等待批准，即使设置 Always Proceed，除非提示明确要求计划后继续。',
'通过共享验收产物给负责人减少逐工具调用盯守的需要；针对 UI 任务可将录屏与测试断言、变更版本一起留档。这里的跨团队共享流程是研究建议。',
'官方仍提供产品文档。未核对专有 harness 源码或运行实测，录屏不能覆盖未执行的 UI 路径。Jules 公告举例使用其 CLI 辅助导出，但没有证明两个产品的调度、批准或记忆可直接兼容。',
'2026-05-19，Google I/O 宣布 Antigravity 2.0 独立桌面应用及 CLI，列出并行 agents 和定时任务；2026-10 的 Jules 公告将 Antigravity 列为开发方向去处之一。',
'用少数可检查产物管理并发工作，同时保留上游需求和下游验收；在迁移场景中尤其要复核显式批准、默认继续与等待超时的差异。',
'测试同一含页面交互的任务，通过 App 与 CLI 各自产出计划、diff、录屏；按默认与显式 /plan 做对照，记录停止点及验收者能否复核对应 commit。',
[('review','Artifact review policy：Always Ask、Always Proceed、显式 /plan 及继续条件',''),('artifacts','Reviewing artifacts across surfaces：计划、代码差异、浏览器录屏与 CLI 提醒',''),('log','Google I/O 2026：Antigravity 2.0 / CLI、dynamic subagents、scheduled tasks','2026-05-19')])]
mf=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));idx={(s['id'],s['key']):s for s in mf};cases=[]
for s in mf: assert sha256((BASE/s['path']).read_bytes()).hexdigest()==s['sha256']
for id,name,category,scenario,mechanism,human,org,limits,change,insight,experiment,refs in rows:
 fields=locals().copy()
 case={k:fields[k] for k in ('id','name','category','scenario','mechanism','human','org','limits','change','insight','experiment')}
 case['sources']=[dict(url=idx[id,k]['url'],path=idx[id,k]['path'],detail=detail,date=date) for k,detail,date in refs]
 case['evidence']='官方产品/版本文档交叉复核；未登录实测，未据此确认服务端实现'
 case['status']='已公告进入只读；计划停服' if id=='M03' else '有现行官方产品文档；租户可用性未实测'
 cases.append(case)
(ROOT/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(cases),'cases;',sum(len(c['sources']) for c in cases),'references;',len(mf),'snapshots')
