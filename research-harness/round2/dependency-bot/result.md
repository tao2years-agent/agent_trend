# 依赖机器人提出的更新，哪一步能发现消费方会坏？

Renovate 44.256.0 把 HTTPX 0.26.0 → 0.28.1 记为 minor、`isBreaking=false`。从同一个 Starlette 0.36.3 基线验收，普通 ASGI 请求成功，框架 TestClient 报不识别 `app` 参数，39 个上游 TestClient 测试全部失败。给两项依赖同一个分组，CLI 把 Starlette 0.37.2 和 HTTPX 0.28.1 放到同一候选分支，这一组合的 41 个测试全部通过。历史窗口相同、允许版本相同，改变分组就改变了可以单独合并的变更单位。[官方 npm 发行物](https://registry.npmjs.org/renovate/44.256.0) · [候选](candidates.json) · [消费方重跑](consumer-results.json)

## 观察口径

2026-11-20，Windows、Node 24.14.0、npm 11.9.0、Python 3.11。12 次独立的无远端本地 Git 仓库运行原版 npm CLI，使用 `pip_requirements` 识别 manifest。PyPI 四个包的原始 JSON 整包快照含 206、77、64、107 个 release key（依次为 Starlette、HTTPX、Flask、Werkzeug）；只读 HTTP 回放原文，Renovate 选版、过滤和拟定分支。11 次 lookup 共发 21 个 GET，每次 HTTP host 统计均仅有回环地址。受限场景刻意令版本落入已固化的历史测试矩阵。无界场景保留完整目录。未使用任何生产仓或真实批准者。[预登记及追加敏感性](protocol.md) · [来源与哈希](sources.json) · [运行器](run.py)

| 场景 | CLI 实际输出 | 另行测试的消费方结果 |
|---|---|---|
| 01 extract | 从一个文件识别两个 pin，零查包、零候选 | 基线 0.36.3 / 0.26.0 通过 39/39 |
| 02 只允许 HTTPX 升级 | 一个分支建议 0.28.1 | 保留 Starlette 0.36.3，失败 39/39 |
| 03 允许两项、显式分组 | 两项同为 `renovate/tested-asgi-pair` | 0.37.2 / 0.28.1 通过 41/41 |
| 04 阶段一只批准消费方 | 一个分支建议 Starlette 0.37.2 | 保留 HTTPX 0.26.0，通过 41/41 |
| 05 阶段二将已批准消费方作为基线 | 一个分支建议 HTTPX 0.28.1 | 通过 41/41；此处基线是研究者设置 |
| 06 等待 Dashboard 批准 | lookup 生成与 02 相同的候选 | 候选对应的独立验收失败 39/39；本地没有批准界面 |
| 07 禁用 HTTPX | 只查询 Starlette，无候选 | 没有升级待验收 |
| 08 两个允许集合都以当前值为上界 | 查两个包，无候选 | 与 07 区分了禁用与“查了没有合规更新” |
| 09 Flask 2.2.2 只升 Werkzeug | 建议 Werkzeug 2.2.3 → 2.3.8，minor、`isBreaking=false` | 基线通过 25/25；新组合的基础请求、简单 TestClient 都绿，会话事务失败 3/25，错误涉及 `inject_wsgi` |
| 10 Flask 桥接 | 建议 Flask 2.2.2 → 2.2.5，保留 Werkzeug 2.2.3 | 通过 25/25 |
| 11 移除包级版本和分组规则 | Starlette 0.52.1、1.10.0 与 HTTPX 0.28.1 分三个候选 | 两个新 Starlette 版本未在固化矩阵内；未追加运行。HTTPX 分支对应 02 |
| 12 两项允许版本与 03 相同、只移除分组 | 两项拆成 `renovate/starlette-0.x`、`renovate/httpx-0.x` | 从各自共同基线只合前者通过 41/41，只合后者失败 39/39 |

两种批准含义要分开。04、05 是团队事先将允许版本写入配置的情景，06 是声明需经 Dashboard 批准才创建分支。固定发行版分支工作器在需要批准且缺相应检查时返回 `needs-approval`；本地平台把非 extract 模式限制在 lookup，且无 Dashboard/分支创建，所以 06 没有执行那段创建路径，也没有人点击。12/12 的 CLI 在显式执行测试前都没触发仓内的 canary，工作树和 HEAD 均保持原样；主动执行同一 canary 的阳性对照留下了标记。这里的分支均为日志中拟定的名字。[本地平台说明](https://docs.renovatebot.com/modules/platform/local/) · [批准选项](https://docs.renovatebot.com/configuration-options/#dependencydashboardapproval) · [发行版工作器](raw/package--dist--workers--repository--update--branch--index.js)

## 独立验收与采购判断

从 CLI 每条候选分支所改的 pin 派生实际组合，共 7 个不同的基线/候选组合。每个组合使用新的 Python 虚拟环境、核对哈希的 wheel 和对应版本的上游源码测试，依赖完全离线安装。共运行 235 个测试实例，42 次失败，集中在两个组合。7 个组合的结果均与此前独立矩阵相符。总数跨版本、重复模块，不构成 235 项独立缺陷或产品故障率。两个模块代表框架自己的客户接口，生产应用的覆盖仍需额外契约。当前机器无 Ruby/bundler，Docker daemon 不可用，未给 Dependabot-core 赋实测结果。[逐次运行](runs/) · [XML 与失败日志](downstream/) · [此前所有组合](../compat/result.md) · [Dependabot CLI](https://github.com/dependabot/cli)

验收组织级工具时，可要求每次升级提供候选依赖组、合并所依据的消费方基线、触发的具体测试及结果。以 12 的两个分支和 03 的合组作为同一验收题，若平台仅用 minor、审批勾选或 HTTP 200 判定这里的 HTTPX 升级可合并，它就会在本样本接受一条实际失败的路径。将测试责任交给独立 CI 是可行设计，采购时需要核对这条证据能否回连到准许合并的确切版本。这里没有测托管平台、外部 CI 触发、真实 PR 创建、组织耗时或投资收益。

## 复算

PowerShell 在本目录执行。安装依赖需要访问公开 npm，已存原版 tarball 和 npm lock，四个 PyPI 回包、测试 wheels 和 sdists 已固化。Python 解释器需具备 pytest（canary 阳性对照）；消费方重跑还需相邻 compat、migration 研究目录。可先执行最后一行，离线核对所有派生表与测试 XML。

```powershell
$runtime = Join-Path $env:TEMP 'renovate-44-256-replay'
New-Item -Force -Type Directory $runtime | Out-Null
Copy-Item package.json $runtime
Copy-Item raw/npm-package-lock.json (Join-Path $runtime 'package-lock.json')
npm.cmd ci --prefix $runtime --registry=https://registry.npmjs.org --ignore-scripts --no-audit --no-fund
python run.py --cli (Join-Path $runtime 'node_modules/renovate/dist/renovate.js')
python judge.py
python -B verify.py
```

固定发行版的可选 RE2 模块未加载，日志报告使用原生 RegExp 回退。所有场景使用简短常规表达式。允许访问回环只读目录触发的内部 host 提示保留在 CLI 日志中。四份原始 JSON 不随重跑更新，重新获取来源的脚本不会覆盖已有历史快照。[抓取与校验实现](fetch.py) · [独立验收实现](judge.py) · [离线校验](verify.py)
