# 组织研发侧样本与复核

基线为北京时间 2026-11-20。筛查单位为可独立采用的软件项目；发布包、同仓多个插件与实验端点不分拆计数。11 个入选项目分别说明责任目录、交付归因、证据运输、人工复核、轨迹重放、断言汇总、灰度、授权、告警、性能、基础设施成本。它们是按机制选出的代表，样本未按市场份额或性能排名。

## 筛查决定

|候选|决定及理由|
|---|---|
|Backstage、Apache DevLake|保留。前者回答服务是谁负责的，后者在多个交付系统之间连接时间与结果。|
|OpenTelemetry Collector、Langfuse、Arize Phoenix、Promptfoo|均保留。对象分别是管道的传输、人的判断、版本化实验运行及测试断言。相似的观测界面不意味着它们的责任相同。|
|flagd、OpenFGA、Alertmanager|均保留。分别在请求分组、动作授权、例外通知时运作。|
|Grafana k6、OpenCost|保留。一个能用指标阈值决定测试进程结果，另一个把成本按工作负载归属。|
|Conftest|最初完成源码阅读及本地 CLI 正反对照，交付组也研究了同一项目。退出本组计数，原始材料与实测留作交叉复核，由 OpenCost 补足不同机制。|
|Grafana 整体平台、Unleash、Sentry、SonarQube|未深挖本轮候选。分别与已入选的度量展示、灰度控制、异常接管或质量门存在交叉；没有据此评价未入选产品优劣。|

## 证据处理

1. 查询仓库和官方发布目录，再用 GitHub 返回的完整提交号定版。来源清单及该提交时间见 `refs.json`、`commit-metadata.json`。逐仓库读取该 SHA 的 codeload 归档，枚举路径，按具体对象选择可证伪的分支、默认值与反例，选择见 `selection.json`。源码证据日期记录该快照提交时间。
2. 固化官方 Releases Atom，每仓 10 条可见条目供筛选；产品/子模块区分。归档选中条目的 HTML，取单版本页显示的发布日期，OpenCost 单独取标签日期。OpenFGA 的 Atom 更新时间晚于原始发布日，修订与首发已分开；其它发行记录只解释该版本的增量。
3. 用源代码验证产品抽象，如 DevLake 的不可比指标空值、k6 缺采样处理、Langfuse 完成标记。演进页只为其实际提及的改变提供时间证据。未针对任何项目做完整代码审计。
4. 对 k6、Conftest 从官方 release 取 Windows x86_64 二进制并核对发布者的 SHA-256，不安装到系统；在临时目录执行正反例，保存参数、输入、输出、版本及退出码。每个工具只验证所列分支，不代表产品整体或组织收益实测。
5. 依据源材料形成 `review.json` 的判断，`build.py` 固定顺序连接证据、校验 SHA-256，生成 `cases.json`。第二轮跨组去重保留了 Conftest 的交叉复核，同时加入 OpenCost 的标签发布日期与独立清单。

## 重放与状态

已有快照时，在本目录运行 `python build.py` 即可离线重新生成 11 个案例和 39 个证据指针。在线重新核对可用 `python collect.py --ingest`、`python releases.py`、`python verify_dates.py`。归档 ZIP/仓库 tarball 仅用作临时缓存；留存的代码是完整选中文件。原始字节与哈希见 `raw/manifest.json`、`raw/release-pages.json`、`raw/release-manifest.json` 和追加的 `raw/opencost-manifest.json`。生成后的研究卡仅引用归档中直接支撑正文的证据，不将整个仓库计为已审阅源码。

在 Windows 上运行 `python runtime_check.py` 可重新下载两个指定版本并重放。交叉复核的 Conftest v0.71.0 以 Rego 检查 owner 非空，输入存在 owner 时返回 0，空值时返回 1，结果在 `runtime/conftest.json`。k6 v2.4.0 返回码在 `runtime/k6.json`。其他 10 个计数项目本轮均未部署。当前仍缺真实组织任务分布、交付归因漏链率、告警假阴性与人工接管耗时，建议按各案例的实验设计续查。
