# 审批之后，哪一个版本可以执行？

**两种引擎都能让新进程接过正在等审批的任务。业务能否正确恢复，还要看三样东西能否一起找回：这次审批的对象、当时看到的版本、目标系统已有的执行回执。** 在两个最小实现中，目标从 v1 变成 v2 后送入对 v1 的同意，两个引擎最终都写入了 v2。目标系统提交后立刻杀死执行进程，恢复后也都留下了两条业务记录。使用相同的引擎、增加应用层版本校验和目标侧唯一键以后，前者留下零条，后者留下一条。[主实验逐次观测](evidence/observations.json) · [共同的目标系统与故障注入](target.py)

## 同一份契约，接入两个真实引擎

实验日期为 2026-11-20，Windows、Python 3.12.3。第一种是 LangGraph 1.2.24、langgraph-checkpoint 4.3.2、langgraph-checkpoint-sqlite 3.1.3，使用真实 SqliteSaver、同步写 checkpoint、thread_id 和 interrupt。第二种是官方 Temporal CLI 1.10.1 提供的 dev server 1.32.2、Python SDK 1.29.0，服务监听本机回环，使用文件持久化、Workflow Signal、查询和 Activity。整个实验没有模型参与。真实的是工作流引擎、进程、持久化、超时和重试。模拟的是批准者及接收最终“发布”操作的下游系统，后者使用独立 SQLite 数据库，与引擎状态库没有共同事务。[LangGraph 接入](graph_worker.py) · [Temporal 工作流](temporal_workflow.py) · [依赖锁](requirements-lock.txt) · [服务启动日志](evidence/server.log)

每个单元独享空的目标和流程。批准消息含同意标志、请求 R1 或 R2、版本摘要和投递标识。基础接入只使用同意标志。LangGraph 接受标量 resume，Temporal 按 Signal 到达顺序交付给正在等待的关卡。两者都显式配置持久化，LangGraph 显式选择同步保存，Temporal Activity 配置 3 秒 start-to-close 超时并沿用默认重试策略；这里的“基础”仅指没有增加业务审批与幂等控制。[执行脚本](run.py) · [官方中断说明](https://docs.langchain.com/oss/python/langgraph/interrupts) · [Temporal 重试说明](https://docs.temporal.io/encyclopedia/retry-policies)

加强接入依然使用同一条工作流。关卡校验消息 request 与当前期望的 R1/R2。目标端在同一 SQLite 写事务内读取当前内容摘要，与批准的 SHA-256 比对，通过后按逻辑发布操作的唯一键执行。同一实例只发布一次，因此每个单独目标库中的键均可写作 publish。重复调用读到已存在的行，在本实验中返回相同的成功状态。在跨实例、跨环境的实现中，这个常量必须换成真实的逻辑操作标识；本实验没有实现权限、签名、TTL 或通用回执查询 API。[目标端实现](target.py)

## 主实验结果

16 个引擎、场景和配置组合各从空库独立运行两遍，两次全部一致。另做两个原生对照，共有 34 个场景实例。表内是**该引擎该配置最终在独立业务库中留下的版本和行数**。停住代表应用返回 held_request 或 held_stale 并结束本次流程。重复投递组的两个检查点分别使用 R1、R2，先等到 R2，再重复投 R1。两次投递具有相同业务内容，传输层分别调用一次。

| 输入及故障 | LangGraph 基础 | LangGraph 加校验 | Temporal 基础 | Temporal 加校验 |
|---|---|---|---|---|
| 等待 R1，原执行进程退出，另一个进程批准 v1 | v1 × 1 | v1 × 1 | v1 × 1 | v1 × 1 |
| 审批展示 v1，随后外部更新为 v2，此时收到 R1 对 v1 的同意 | v2 × 1 | 停住，0 | v2 × 1 | 停住，0 |
| 第一关已经收到过 R1，第二关等待 R2，调用者将 R1 业务消息重发一次 | v1 × 1 | 停住，0 | v1 × 1 | 停住，0 |
| 外部目标写入 v1 并提交，随即强制退出，工作流未收到结果，接手后再次调用 | v1 × 2 | v1 × 1 | v1 × 2 | v1 × 1 |

LangGraph 的首次调用在 R1 的 interrupt 返回后退出。后续调用启动新的 Python 进程，打开同一 SQLite 检查点。回执丢失时进程在 publish 节点内以 75 退出，另一调用者对同一 thread 使用 invoke(None) 继续。Temporal 在查询证实已到达 R1 后停止原 worker，由另一个 worker 对同一执行返回 R1 的查询结果。回执丢失组在 Activity 内提交后以 75 退出，再启动第三个 worker。四个丢回执单元都实际记录了来自两个操作系统进程的目标端调用。两个 Temporal 单元的服务历史均记录最终 Activity attempt=2。加了保护以后，第二次调用依然发生，业务唯一键让它复用第一次写入。[逐步状态、实际 PID、服务历史和目标端流水](evidence/observations.json)

## 两个反例：引擎原生提供了哪些保护？

- **LangGraph 可以按中断实例定址。** 以 Command(resume={interrupt_id: payload}) 投递，第一次完成 R1 后把原来的 R1 ID 再发一次，观测到流程仍返回 R2 的 interrupt ID，目标写入为零。用 R2 的真实 ID 再发一次后写入一条。若客户端保留并使用原始中断 ID，可覆盖本实验的跨关卡误投。该 ID 本身没有包含发布对象的外部摘要。[对照运行](evidence/native.json) · [探针](native.py)
- **Temporal 可以识别同一 Signal RPC 的重试。** 使用底层 SignalWorkflowExecution 接口，两次发送相同 request_id，第二次以后查询仍在 R2，业务库为空。换另一个 request_id 投入真正的 R2 后业务库有一条；三次 RPC 一共留下两条 signal history event。主实验通过高层 handle.signal 调用两次，分别被受理；上游把同一业务事件作为新请求交付，和传输重试是两种输入。[历史事件序号与对照结果](evidence/native.json) · [探针](native.py)

这两个反例可以指导买方验收。若界面已按中断定址，重复投递这一项可能已经满足；仍应分别测外部输入换版和外部已写未回执。若事件网关收到的是同一业务事件生成的新请求，网关应复用其原始标识，或者由接收方检查业务身份。

## 可证伪的产品需求

**对已经发给人的发布请求，接管流程必须能定位原审批、它对应的不可变目标和一次逻辑发布操作。** 验收安排为同一请求依次经历换执行进程、目标换版、以新传输 ID 重投旧业务消息、下游提交后丢失回执。单个场景中只要出现一次旧同意写进新版本、R1 放行 R2、同一操作产生两个业务效果，验收即失败。成功路径也要有观测，正确的 R2 能放行一次，未变更的请求可跨进程完成。对于无法由目标拒绝重复写、又查不到已提交回执的服务，应有“结果未知，需接管”的可见状态；本实验的 SQLite 目标支持原子校验和唯一约束，结果不外推到这种服务。

工程判断仍有边界。单机实验覆盖进程级硬退出和明确的故障窗口。没有重启 Temporal 服务、测试双活并发、多租户授权、分布式网络分区、目标端不支持原子比较写、持久化卷丢失或软件升级。4 个协议格没有估计生产故障概率、延迟、成本，也没有据此比较引擎吞吐。基础接入里的错误结果属于给定接入设计。

## 复跑与核验

从本目录创建 Python 3.12 虚拟环境，用 requirements-lock.txt 安装依赖，下载与本机匹配的官方 Temporal CLI。Windows amd64 在本实验中从官方发布地址取 ZIP，以发行方 checksums.txt 核对，再比对实际运行的 exe 内容。sources.json 另记录官方文档、3 个 Python 发布版本元数据和安装包实现文件的 SHA-256。源码文件均与相应 wheel 的 RECORD 一致。[来源索引](sources.json) · [官方 CLI 版本](https://github.com/temporalio/cli/releases/tag/v1.10.1) · [来源固化脚本](sources.py)

~~~shell
python -m pip install -r requirements-lock.txt
python run.py --temporal /absolute/path/to/temporal --out /new/path/first
python native.py --temporal /absolute/path/to/temporal --out /new/path/first/native.json
python run.py --temporal /absolute/path/to/temporal --out /new/path/second
python verify.py
~~~

run.py 拒绝覆盖已有观察文件。每次用新建的临时目录保存引擎数据库和目标数据库。发行包准备好以后，实验中的 Temporal 仅使用回环地址；校验已有证据只需标准库。Windows 虚拟环境的启动器 PID 与实际 Python PID 可不同；Temporal 的 runtime_worker_pids 来自 worker 内部，目标流水中的 pid 来自实际写入方。verify.py 对本目录留存的结果执行离线断言。[复跑记录](evidence/repeat/observations.json) · [离线校验](verify.py)
