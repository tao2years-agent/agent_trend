# Auto harness 的采购边界：谁能把一次坏结果变成下一次发布的否决票？

**开发集从 1/2 提升到 2/2 的候选，在保留的 4 个事件上仍然重复写工单，也会在上下文缺失时写入。** 本地运行 LangSmith 的离线评估和 Promptfoo 的内建断言，两者逐行给出相同的 18 个结果。再执行 Opik 的通过率计算，去掉两条失败事件上的断言，显示值由 50% 变为 100%。这组确定性小样本测的是计分和分母，没有使用大模型，不说明三家产品的生成质量或成功率。[合成事件与输出](fixture.json) · [本地执行记录](probe-results.json)

本节把 Braintrust Loop、LangSmith、Langfuse、Arize Phoenix、Comet Opik 和 Promptfoo 视为另一个采购子市场。它们承担的是把生产反馈变成可复测数据、比较候选、为发布提供决策依据。六项不并入上游 35 项研发任务采购表，也没有把评估 SDK、优化算法各计成一个产品。选取依据是既有正式可用成品、能走通不同环节且能找到技术证据。Weave 等同类暂未进入这份定向样本；外层自动优化算法见[独立研究与源码复核](../optimizersrc/result.md)。[六产品逐阶段矩阵](matrix.csv) · [60 份一手证据索引](sources.json)

## 使用同一份失败报告

一个定时维护代理根据审批结果决定是否写工单。失败反馈来自同一工单的两次回调，内容含示例邮箱；另有一条在所有者变更时怎样做仍有分歧。研究夹具共有 8 条合成记录。先用规则遮掉示例邮箱，再按业务事件键去重，剩 7 个事件。开发集 2 条、盲测集 4 条，键互斥；两位假设标注者对第 7 条给出不同答案，隔离为待裁决。该标注来自夹具，并非真人对产品进行打分。

三个候选分别是总是写入、只要许可状态为 approved 就写、以及同时要求许可有效、工单未写且上下文完整。它们是研究者预置的决策函数；从反馈生成候选的厂商模型未运行。把函数输出交给两个评估实现，得到以下结果。

|固定候选|开发集|保留集|失败行为|
|---|---:|---:|---|
|当前版本，总是写|1/2|1/4|已过期、已经写过、上下文缺失仍写|
|只检查许可状态|2/2|2/4|重复写和缺失上下文仍写|
|同时核验许可、既有工单与上下文|2/2|4/4|本组 4 个保留事件均符合预设期望，第 7 个争议事件仍未定案|

**数据环境决定“盲”的含义。** Opik Optimizer 默认复用训练集进行候选排名，需显式给 validation_dataset。Promptfoo optimize 默认搜索全部已配置测试，可显式用 --validation-split 留出约定比例判断是否采纳候选；该模式要求显式 tests。被优化器重复查看以选择候选的验证集仍参与选择。最后的签收集应另行维护，以事件族分组、版本冻结和访问记录证明它未参与选择。Phoenix 12.0+ 提供自定义 splits；固定服务端接口允许同一样本有多个 split ID，挂上 train/test 标签并不自动形成互斥。[Opik Optimizer FAQ](https://www.comet.com/docs/opik/development/optimization-runs/faq) · [Promptfoo 优化选项](https://www.promptfoo.dev/docs/usage/prompt-optimization/) · [Phoenix 12.0+ 发布说明](https://arize.com/docs/phoenix/release-notes/09-2025/09-27-2025-dataset-splits)

## 一项任务交出去，分别能拿回什么

|采购候选|这个失败案例可交付的中间或终点产物|仍由采用方负责或待实证|
|---|---|---|
|Braintrust Loop|从失败日志构建评估集、建议提示改动或新评分器，运行实验后对照基线。工程团队可让自定义 reporter 给出发布失败信号。|技术文确认 terminate_on_failure 处理执行异常。低分需要 reporter 明确返回失败，而且仓库必须将该 job 设成必需检查。评语或 PR 评论本身不拦截。|
|LangSmith|按条件将 trace 放进数据集或标注队列。多人评审可设置人数和预留时间，队列能等到成员全部完成。按指定 split 比较候选，并按 tag 或 commit 拉取提示。|到齐与达成一致是不同事件。独立仲裁、最后盲集访问控制、CI 和审批权需要额外验证。|
|Langfuse|使用来源 trace 建样本、按 item ID 更新、版本化后对照实验，查看逐项退化；按 production 标签服务提示。|若两份反馈有不同 trace ID，团队须提供同一业务键方能合并。重新指定 production 标签能切回提示；缓存生效时间、在途任务以及外部工单恢复要另测。|
|Arize Phoenix|对 span 做标注和属性屏蔽，用多个版本的数据集和 splits 运行实验；可使用提示标签及官方优化教程。|教程演示不等于服务端持续自动优化。未找到 Phoenix 默认有权拒绝企业 CI 或一次性补偿外部副作用的证据。|
|Comet Opik|失败 trace 可生成测试项，队列支持多名标注者；优化器用指定训练与验证集生成、排名候选；套件可规定重复次数与最低通过次数。|读时遮盖与摄取前脱敏不同；阈值之外须校验分母及关键切片。环境归属更新为一个原子事务，只覆盖提示环境关系。|
|Promptfoo|团队把事件变成测试项后，可按确定性断言评估，带显式验证拆分做提示优化。CLI 默认通过率阈值 100、测试失败码 100，可配置。|本案的生产反馈采集、语义去重与争议仲裁需接外部系统。CI 应把失败传播到必需检查，并核对可覆盖的环境变量和审批豁免。|

每行的采集、去重与脱敏、三个数据用途、候选、人工分歧、门禁、回滚与许可 / 费率证据均可在矩阵中分别查找。厂家仅提供界面说明时，未据此断言生产侧已有强制执行。[逐项采购矩阵](matrix.csv)

## 两个“已开启”值得追问

**“已经开启脱敏”，原文还会不会出现在数据平台？** Opik 的 Enterprise 预览功能在读取时根据角色遮盖，服务端仍保存日志原文，默认工作区角色含“查看原文”权限。要让原文不离开应用，应使用发送前的 SDK 匿名化。Langfuse 也提供摄取前 masking。对本案应分别检查网络载荷、普通标注员看到的值及管理员看到的值，再决定生产反馈能否进入训练材料。以 ID 去重仅能防同一标识重复写入，无法自动合并语义相同、标识不同的用户报告。[Opik 两类匿名化](https://www.comet.com/docs/opik/administration/data_anonymization) · [Langfuse 发送前的 masking](https://langfuse.com/docs/observability/features/masking)

**“已经开启质量门禁”，低分和评分器崩溃会走同一条路径吗？** Braintrust 的 Action 源码把 terminate_on_failure 映射为 CLI 参数，默认 false。厂商技术指南明确区分异常、成功完成但低分、仓库是否要求检查三种条件。Promptfoo 的 doEval 还区分 CLI 调用与编程调用；CLI 进程退出码的默认行为不能套到返回结果对象的集成。合同验收应分别制造低分、评分器异常、少跑关键项，核对进程退出码、PR 检查状态和实际合并权限。[Braintrust CI 技术指南](https://www.braintrust.dev/articles/llm-eval-pipeline-github-actions) · [Braintrust 固定 Action 实现](https://github.com/braintrustdata/eval-action/blob/957f8d48a2dd0f63e52ff0425b8dba24d1c99bca/action.yml) · [Promptfoo 固定 CLI 实现](https://github.com/promptfoo/promptfoo/blob/cbf602f0a02691ccf3eb11d3574ae57160f50cc3/src/node/doEval.ts)

## 怎么选，哪些证据会推翻判断

- **已有生产 trace，希望较快拿到候选改动。** 先比较 Braintrust Loop、Opik Optimizer、LangSmith 的提示改进流程。将优化器可见的训练/排名集与最终签收集物理分开。若供应商能用客户给的版本证明保护集不可被优化器读、争议事件能冻结发布，才把这两个控制计入产品交付。
- **强调自托管与独立数据控制。** Langfuse 可以将生产提示版本、数据集与逐项退化连起来；Phoenix 可细分样本、用开放协议的遥测与数据实验对接既有系统；Opik 多提供面向优化与测试的路径。核准具体目录许可，Langfuse 的指定企业目录有例外，Phoenix 采用 ELv2，Opik 为 Apache-2.0。“源代码能看到”的产品不能按同一分发条件采购。[Langfuse 自托管条款](https://langfuse.com/pricing-self-host) · [Phoenix 固定许可证](https://github.com/Arize-ai/phoenix/blob/33d17e2455307384a0a29bed33be56de266d216e/LICENSE) · [Opik 固定许可证](https://github.com/comet-ml/opik/blob/a64b914047597f2693d4073fbe8a31b4e0a794e4/LICENSE)
- **已有业务反馈仓、人工仲裁和 CI，只缺可执行的提示回归。** Promptfoo 能直接提供本地断言和 CLI 失败信号。相反，若采购的主要目标是从真实反馈持续抽样、调度双人标注，本轮证据不足以让 Promptfoo 独立承接。独立提供一条实际生产 trace 入库、双人冲突及其审计日志，会改变这项判断。
- **若必须能撤销已经发生的外部写入，六项都需外接研发工作流验证。** 能回滚提示版本的供应商应演示还原前后新请求读取哪个版本；另外索取已在途请求的实际版本、先前工单是否保留、补偿工单由谁签发。六项的本轮证据没有涵盖最后一个保证。

## 复核方法与限制

使用官网发布材料、技术文、定价、许可证及六个公开仓库在固定 commit 的实现。60 份证据含 21 份固定源码、配置与许可证；其他 39 份为官方网页或技术文。价格只描述 2026-11-20 快照上可见的公开套餐，表内金额没有纳入模型调用、存储和部署成本。[来源及哈希](sources.json) · [版本与运行时包核对](runtime-versions.json)

在此目录运行 python probe.py，再运行 python compile.py，可复算合成事件、18 次逐项比对与断言缺席时的通过率。前者使用 LangSmith Python 0.2.11 的 evaluate(upload_results=False)、Node.js v24.14.0 执行未经改写的 Promptfoo equals 与 normalize 源文件、Opik 固定源文件中 TestSuiteResult.pass_rate。LangSmith 已安装的评估器与官方 PyPI wheel 哈希一致，该历史 SDK 的本地结果不代表当前云端。该 SDK 在启动时曾尝试请求 GET /info，由本地拦截器拒绝，未发送样本；Node 断言只读取研究目录，网络调用被禁用。没有采购或登录账户、私有数据、发版、模型调用或外部工单写入。自托管全栈、实时标注流、付费优化、CI 端到端和线上恢复均未实测。[执行输入与脚本](probe.py) · [运行结果](probe-results.json)
