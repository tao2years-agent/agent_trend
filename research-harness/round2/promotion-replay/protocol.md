# 提示提升和回滚的本地验收约定

将 MLflow Prompt Registry 作为原六项评估产品以外的公开开源参照。冻结 PyPI 的 MLflow 3.18.0 完整发行版，同版 mlflow-skinny 与 mlflow-tracing，Windows CPython 3.12，真实 SQLite backend。出于实验设计，注册普通会议文案的三个版本，配置中使用不存在的合成模型名；只调用模板 format，不运行推理。通过公开的 mlflow.genai API 写入，另开只读 SQL 连接核对。每次试验新建 SQLite 文件，以多个 OS 进程隔离 SDK 缓存。下载 Python wheel 的资料准备过程与无网执行过程分开；在 SDK 工作者禁止任何 socket.connect。

## 验收项目与失效条件

1. 注册独立 v1、v2、v3；分别显式设置 production、candidate。按数字取回模板并计算摘要。若跨进程或窗口关闭后无法读回，持久性验收失败。
2. 研究夹具记录批准的候选版本，之后移动 candidate。分别测试仅记 alias 然后重新解析、直接按批准的固定数字版本落位。设向不存在的版本 999 赋值的阴性对照；检查失败后现行版本是否被改变。
3. 给夹具的授权设置确定性时钟：现在为 100，过期值 99、有效值 200，均不是产品产生的真实人员授权。对比公开 setter 是否要求票据，以及调用方选做的显式校验。受信任操作者已可调用本地 API，不测账号登录、权限绕过、多人签署。
4. 切换 production 后同时检查写进程、独立已缓存读进程、禁用缓存读取与已取得模板对象。等待生产库真实默认 TTL 后再读一次。回滚后测持有旧对象、其他读进程默认读取和不走缓存的新读。保留值和 wall-clock 间隔。
5. 决策 A/B 都读到同一前置 production，用两个已校验的版本先后写入，观察是否能拒绝基于旧前置版本的后写。特意安排执行顺序，证明某个合法交错是否存在，不估计真实并发冲突率。回滚到同一版本以后尝试重放旧票；另设额外的一次性票号检查，明示该对照只在夹具内生效。
6. 额外测试固定版本的模板摘要相同但模型配置被公开 API 更新。区分文案的版本、整个候选配置和应用未知的外部模型版本。此处没有生成质量或成本指标。

核验以 SQLite 投影和跨进程读取为准。产品原生检查、用户编写的顺序校验、仍需共享事务保障的部分分别记录。采集匿名合成正文、配置、版本、时间、错误与二进制哈希。无需服务器监听端口、浏览器、商业账户、模型密钥或外部工作流。

## Windows 上的重跑入口

在本目录、64 位 CPython 3.12 中，联网准备介质一次即可。第一条从 PyPI 校验 91 个固定 wheel 的 SHA-256，第二步起可以断网。若已有此次同平台 wheelhouse，可直接从建环境起步。脚本每次使用新的临时数据库，运行时间包含等候真实 SDK 缓存到期。

```powershell
py -3.12 -m pip download --require-hashes --only-binary=:all: --dest wheelhouse --index-url https://pypi.org/simple -r requirements-win-py312.lock
py -3.12 -m venv registry-env
.\registry-env\Scripts\python -m pip install --no-index --find-links wheelhouse --require-hashes -r requirements-win-py312.lock
.\registry-env\Scripts\python lock.py wheelhouse
.\registry-env\Scripts\python probe.py
.\registry-env\Scripts\python sqlcheck.py
.\registry-env\Scripts\python validate.py
```

已经固定的来源与实际环境分别在 [发行包索引](sources.json)、[环境与依据](environment.json)、[安装模块与源码字节比对](runtime-source-match.json)。工作者均安装了真实发行版；SQLite 直接使用包内 SQLAlchemy 实现，未使用 REST 传输，因此不证明网络身份认证或托管版行为。
