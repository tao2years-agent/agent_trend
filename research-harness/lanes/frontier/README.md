# 组织级前沿样本的筛查与复核

[F01–F05 全部案例](cases.json) · [来源索引与摘要](sources.json) · [OpenSandbox 实测脚本](probe_sandbox.py) · [六种输入的运行结果](probe-sandbox.json)

该组从代理执行能力延伸至五类组织职责：工单调度、受控写入、技能评估、云端定时工作、可回收执行环境。F01、F02、F05 有公开源码；F03、F04 核查厂商服务的公开行为说明和带日期发布，对托管后端没有源码背书。单独列项是因为操作对象、触发和责任主体不同，不把同一厂商多个项目算作独立厂商。

| 样本 | 核心可证伪问题 | 对照证据与限制 |
|---|---|---|
| Symphony | 工单状态改变后，旧尝试是否仍接管 | SPEC、Elixir orchestrator、WORKFLOW.md、版本记录与厂商经验；样例并非全局强制人审 |
| gh-aw | 只允许预览时，是否仍要读权限 | 管理器代码、历史 changeset、Proposed ADR、预览与 GA 公告；各版本权限需真实编译核实 |
| Tessl | 技能加载是否等同于任务结果改善 | 场景评测文档与有日期的行为记录；未复跑服务端 |
| Claude Scheduled tasks | 预先创建的任务能否替代当次批准，任务属于谁 | 4 月公告与当前带旧名的官方文档；未使用真实账户 |
| OpenSandbox | 活动记录缺失时会不会立即休眠 | 源码函数、部署条件、RC 版本变化、固定提交六条件局部实验 |

## 如何复算

1. 使用 sources.json 的 path 与 sha256 验证字节，源码 URL 中的 40 位 SHA 与 git tree 比对。GitHub release 时间为所存 Atom 条目的 UTC updated；文档日期仅在来源明确记载时填入。动态网页每次下载独立存入内容摘要目录。厂商实践在直接读取失败时使用经定位的官方页面摘录并标明范围。
2. 检查 notes.txt 中的事实、推断和待验证条件，运行 python compile.py 生成 cases.json 并复核所有摘要。抓取代码 capture.py 保存源字节；如要做新的摄取批次，保留原 metadata 并在新的批次目录生成。
3. 运行 python probe_sandbox.py 执行本地判断函数测试。测试固定当前时间、门槛和六种遥测状态，完全不依赖 Redis、集群或模型。全栈自动休眠、可靠性和成本收益尚须外部验证。
4. OpenSandbox 的原 alibaba 仓库入口指向 opensandbox-group。处理重命名时保留同一稳定 ID。Claude 的 Routines 同理只保留一个案例；工单调度、SDK 边界和托管例程分别讨论，不宣称来自不同厂商。
