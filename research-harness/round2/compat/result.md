# 跨仓升级中，什么时候可以先发一边

用发行版构造两个真实依赖链：Flask 与 Werkzeug，Starlette 与 HTTPX。事先固定每条链各 3×3 个版本，在全新 Python 3.11 环境、相同辅助依赖、相同本地请求上检查四道门槛，再跑相应发行包自带的测试客户端模块。它们是有已知兼容问题的特意选样，不用于估计升级失败率。18 个格子里，15 个可由 pip 接受并安装，14 个可导入应用并通过不启动网络服务的 WSGI/ASGI 请求，13 个通过框架自带测试客户端的简单请求，12 个通过上游整模块。[试验约定](protocol.md) · [18 格结果](matrix.json) · [42 个发行文件及 PyPI SHA](sources.json)

**Starlette 的故障边界在测试客户端。** 0.36.3 配 HTTPX 0.28.1 时，ASGI 应用能返回预期正文，Starlette 的 TestClient 却无法创建，上游该模块 39 项均失败。先把 Starlette 升至 0.37.2、仍配 HTTPX 0.26.0，上游 41 项都过；再把 HTTPX 升到 0.28.1，41 项仍过。另一个中间态 0.36.3 配 0.27.2 可以用，但发出旧参数弃用提示。这与 Starlette 的 0.37.2 发布记录一致。一次“服务能正常响应”检查不会暴露这类集成测试阻塞。[Starlette 官方版本记录](https://www.starlette.io/release-notes/) · [0.36.3 失败日志](results/Starlette-0.36.3_httpx-0.28.1/tests.log) · [0.37.2 成功日志](results/Starlette-0.37.2_httpx-0.28.1/tests.log)

**Flask 说明有时需要寻找中间版本。** 在 2.2.2 × Werkzeug 2.2.3 的起点，25 个上游测试通过。先升 Werkzeug 到 2.3.8，简单请求仍过，但 session transaction 的 3 个测试失败；直接到 3.0.0，Flask 在导入阶段就失败。先单独升 Flask 到 2.3.3 又会与原 Werkzeug 的最低版本约束冲突。若只看最初登记的九个组合，似乎需要协调两侧同时发布。随后依据 2.2.x 的兼容修复发布记录加入 Flask 2.2.5；它配原三个 Werkzeug 版本时，三次各 25 个上游测试全部通过。当前判据下存在逐步路径：先发布 2.2.5，再升 Werkzeug，最后切换目标 Flask。桥接版是看过首轮结果后的探索，在其他约束、其他代码或其他测试下还可能失败。[Flask 2.2.x 发布记录](https://flask.palletsprojects.com/en/stable/changes/#version-2-2-5) · [原始上游问题](https://github.com/pallets/werkzeug/issues/2789) · [事后桥接方案](bridge-plan.md) · [三个桥接结果](bridge.json)

**对平台的要求。** 只报“仓 A 已经升级”会漏掉三类事实：生成的依赖解是否可安装、消费者的业务合同是否仍成立、下一批消费者需要先发还是后发。可验收的产物是一条逐步发布路径及每一步的独立证据。提交给 owner 时应包括会受影响的消费者、停留在中间态时能否提供服务/跑测试、失败时回到哪一对版本。研究未运行真实生产服务，也未证明历史桥接版本适合今天部署。缺失 CFFI 的首次环境装配另存原日志，统一修正后完整重跑。[环境复核](environment-note.md) · [执行程序](run.py)
