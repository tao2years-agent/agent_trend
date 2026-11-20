# React 跨仓升级：依赖解析提前挡住了多少故障？

**这一次，标准包管理器已经完成了第一轮有效筛查。** 把 React 与同版 react-dom 的三个代际，交叉配上 React Testing Library（RTL）的三个代际，严格安装在 9 格中拒绝 5 格。允许安装的 4 格全部通过同一份交互及回收探针。另开环境，特意忽略 peer 约束后再测试被拒的 5 格，其中 3 格确实无法运行，另 2 格能完成这个有限流程，但会触发弃用提醒。这个样本直接限制了从 Python 个例得出的外推：有些生态组合里，增设代理重复判断版本兼容，在实际 DOM 旅程上没有比包管理器再发现一个受支持配置的故障。[预选协议](protocol.md) · [全部 16 次独立配置记录](results.csv) · [Python 对照](../compat/result.md)

## 九格与单独阴性对照

实测 Windows、Node 24.14.0、npm 11.9.0、jsdom 24.1.3。各项目在根声明精确版本的 React、react-dom、RTL 及 `@testing-library/dom@10.4.0`。旧 RTL 独立依赖 DOM 8，npm 允许嵌套，12.1.5 与 13.4.0 实际调用 8.20.1，16.1.0 调用根的 10.4.0。所有组合均用开发模式、同一小组件、同一 jsdom 宿主。首次检查用普通 `npm install` 加 `--strict-peer-deps`，只有这里 ERESOLVE 的组合才另开全新目录，改用 `--legacy-peer-deps`。表里的“通过”须完成全部断言。

| React 与 react-dom | RTL | 严格 npm 安装与旅程 | 忽略 peer 的附加诊断 |
|---|---|---|---|
| 17.0.2 | 12.1.5 | 安装并通过 | 无需重试 |
| 17.0.2 | 13.4.0 | ERESOLVE，未执行 | 可安装，导入 RTL 时缺少 `react-dom/client` |
| 17.0.2 | 16.1.0 | ERESOLVE，未执行 | 可安装，导入 RTL 时缺少同一入口 |
| 18.2.0 | 12.1.5 | ERESOLVE，未执行 | 本旅程通过；发出旧 `ReactDOM.render` 警告，React 将按 17 的旧 root 行为运行 |
| 18.2.0 | 13.4.0 | 安装并通过 | 无需重试 |
| 18.2.0 | 16.1.0 | 安装并通过 | 无需重试 |
| 19.0.0 | 12.1.5 | ERESOLVE，未执行 | 导入成功，首次渲染抛出 `_reactDom.default.render is not a function` |
| 19.0.0 | 13.4.0 | ERESOLVE，未执行 | 本旅程通过；警告测试工具的 `act` 已弃用，应改用 `React.act` |
| 19.0.0 | 16.1.0 | 安装并通过 | 无需重试 |

单独交换 DOM 工具版本作阴性对照。保持通过的 React 19.0.0 + RTL 16.1.0，将根 DOM 从 10.4.0 改为 9.3.4，严格安装明确指出 RTL 要求 `^10.0.0`，因此拒绝。绕开 peer 后原旅程仍通过，且实际加载 DOM 9.3.4。这证明解析器确实检查了第三个契约；简易测试通过不能代表全部 DOM API 兼容。该两次结果不计入九格。[拒绝原因](results/control-r19.0.0-rtl16.1.0-dom9.3.4-strict.install.txt) · [宽松探针](results/control-r19.0.0-rtl16.1.0-dom9.3.4-legacy.json)

## 声明、运行行为与撤退路径

- **旧测试库调用旧根。** 12.1.5 声明 React 和 react-dom 都须 `<18.0.0`；实际运行代码第 101 行调用 `ReactDOM.render`，第 112 行卸载旧根。18.2.0 保留旧入口并告警，19.0.0 移除了它。宽松安装得到的两个不同后果，与真实调用和 React 官方迁移说明相符。[12.1.5 声明](raw/testing-library-react-12.1.5.manifest.json) · [包内真实代码](raw/testing-library-react-12.1.5-pure.js.txt) · [React 19 官方迁移说明](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
- **新测试库在模块加载时就要求新入口。** 13.4.0 与 16.1.0 在包内实现第 35、45 行直接加载 `react-dom/client`；ReactDOM 17 的发布包无该入口，错误先于呈现发生。13.4.0 默认用 `createRoot`，但仍经 `react-dom/test-utils` 取得 `act`，在 19 上会有弃用提示；16.1.0 的适配代码优先选 `React.act`。这解释了“本探针能运行”与“发行方承诺支持”的差距。[13.4.0 渲染](raw/testing-library-react-13.4.0-pure.js.txt) · [13.4.0 的 act](raw/testing-library-react-13.4.0-act-compat.js.txt) · [16.1.0 的适配](raw/testing-library-react-16.1.0-act-compat.js.txt)
- **中间态决定发布顺序。** 在所选版本中，从 18.2.0 + RTL 13.4.0 到 19.0.0 + RTL 16.1.0，可先升级 RTL 至 16.1.0，在 React 18 上验证，再动 React 与渲染器。两步都通过严格安装和交互。从 17.0.2 + RTL 12.1.5 出发，九格里没有只改一个轴就能走通的第一次单步；在该版本窗口，协调升级是可见方案，未检索其他桥接版本，不排除矩阵以外另有路径。[机器可读结果](matrix.json) · [16.1.0 声明](raw/testing-library-react-16.1.0.manifest.json)

## 验收与复现范围

探针用真实 React、ReactDOM 和 RTL 建树，通过可访问名称找到输入框与按钮，派发 DOM change 和 click 事件，提交修剪过的文本、核对列表与输入重置，改变 props 后检查状态保留，再清空列表、卸载、核对 effect 销毁恰好一次和容器回收。它实际运行在 jsdom，不启动任何服务、不访问外部业务系统；没有调用真实模型、客户仓库、真实浏览器、TypeScript 编译器或完整上游测试套件。5/9 是刻意跨代选的矩阵比例，不是 npm 生态升级失败率。[交互探针](probe.cjs) · [环境](environment.json) · [发布包溯源](sources.json)

第一次环境检查中，React 17 组合的组件断言可以完成，但旧调度栈在当前 Node 留有 `MessagePort`，等待进程自然退出时 60 秒超时。正式运行把所有版本统一到 jsdom 的可视时钟模式，明确关闭窗口，留下活动资源类型，刷新 JSON 后显式结束测试进程，然后从空项目重新跑完全部严格与宽松格。这里声明的“回收”仅指组件 effect、DOM 容器及窗口，未把进程自然退出列为组件兼容结论。[React 17 环境记录](results/r17.0.2-rtl12.1.5-dom10.4.0-strict.json) · [完整执行器](run.py)

**可离线重放。** 13 份直接选用或实际解析到的发行包逐份核验官方 SHA-512 SRI 并保存 SHA-256。成功安装产生 10 个 lockfile，按内容去重后的全部 154 个 npm 发行档案（9,674,971 字节）随证据包保留。在新建的本地 npm 缓存中，仅投入这 154 个校验过的公开档案，全程 `npm ci --offline` 重装 10 次；初次的成功/失败阶段、警告和解析版本全部重现。装新版本前，可先用严格解析做廉价基线，再把执行预算投向能增量检验的业务契约、未建模的消费者和可撤回的升级顺序。[离线包清单](locked-archives.json) · [重放脚本](replay.py) · [十次复跑](replay.json)
