# 一次“已批准、已写入、已恢复”能否在厂商之间还原

**只消费工作流成功事件，无法判断业务系统究竟写了一次还是两次。** 本轮从前面的 Temporal 实测取出两次独立空库运行。每次都比较基础配置与目标端去重配置：两者都报告 published，两者都实际调用目标两次；基础配置留下两行，去重配置只留一行。映射到标准 CDEvents taskRun.finished 及其 CloudEvents 外层以后，四份完成消息都合法，都能表达 success，业务结果却不同。只有回到目标记录，才能区分 insert/insert 和 insert/reuse。[实际记录、散列和验证明细](checks.json) · [可复跑样例](examples.json)

## 现成规范负责哪一段

下表比较五种可组合的接口或规范族。版本为本次实际核对版本，适用日期 2026-11-20。原始文档、正式 tag / 固定提交、获取时间和 SHA-256 均在[一手来源索引](sources.json)。

|现成能力及版本|谁发，天然能表达什么|若要回答审批、目标与恢复，还缺什么|
|---|---|---|
|**CloudEvents v1.0.2**，结构化 JSON 的 specversion 为 1.0，JSON Schema 为 Draft-07|事件生产者设 source、id、type、specversion。规范要求不同事件的 source+id 唯一；重发同一事件可以沿用原 ID。subject、time、数据体和扩展可携带更多信息。|source 是生产者提供的上下文标识。合法消息不证明身份、授权或写入。两次传输可以是同一事件，不同 ID 的两次调用仍可能是同一业务操作。要用目标记录判断业务去重。[CloudEvents 固定规范](https://github.com/cloudevents/spec/blob/fc1f6f31f5f011a72183f1bcea20c987cb683ade/cloudevents/spec.md)|
|**CDEvents v0.5.0**，本案具体事件类型后缀为 0.3.0，JSON Schema 为 Draft 2020-12|SCM 适配器可发布 change.reviewed；编排器发布 taskRun.finished；部署系统发布 service.deployed/rolledback；事件管理方发布 incident.resolved。context.chainId、links 可协助关联，回滚事件原生要求 environment、artifactId，规范将后者定义为 PURL。|一次审查可能由人或系统提交。正文希望写明批准/需修改/拒绝，字段表和 schema 却只提供 change 的 id、来源及可选 repository。若跨厂商传递批准，用 customData 引用权威审批记录并明确版本。incident.resolved 是来源方声明，需要另联独立恢复信号和观测窗。[审查事件正文](https://github.com/cdevents/spec/blob/78e5ee85b3e094de0a06aeb6b44c62e4dab2148d/source-code-version-control.md) · [回滚 schema](https://github.com/cdevents/spec/blob/78e5ee85b3e094de0a06aeb6b44c62e4dab2148d/schemas/servicerolledback.json)|
|**OpenTelemetry**，语义约定主仓 v1.45.0；GenAI 单独固定提交 622b2b6|应用、agent SDK、工具或 CI 适配器埋点，trace/span 标识及父子关系用于关联调用。CI/CD 的 pipeline run、task run span 标为 **Release Candidate**，有 cicd.pipeline.result、cicd.pipeline.task.run.result 等。GenAI 主仓入口已迁移，独立仓的 client agent invocation 与 execute-tool 文档都标 **Development**；仅在模型或提供方给了标识时记录 gen_ai.tool.call.id。|工具调用标识由模型/提供方产生，不是目标系统确认收讫的操作键。trace 能说明记录到哪些操作与失败，不能签发用户批准或证明数据库事务已提交。跨系统要显式关联权威记录；一次 trace 或 span 状态不能充当审计完整性的保证。[CI/CD 固定约定](https://github.com/open-telemetry/semantic-conventions/blob/fb30ca17193b551473b1f43c315482918ab6987c/docs/cicd/cicd-spans.md) · [GenAI 执行工具约定](https://github.com/open-telemetry/semantic-conventions-genai/blob/622b2b6073b15e5ed886c3c12a65a892b9cd5c70/docs/gen-ai/execute-tool.md)|
|**GitHub Checks、Actions 环境审批与 Deployments**，REST API 2026-03-10，官方描述 OpenAPI 3.0.3|有权限的检查方对 head_sha 提交 Check Run，得到检查状态及 conclusion；环境评审人以 run_id、environment_ids、approved/rejected、comment 评审。查看历史可得 user、environments、state、comment。部署对象有 deployment_id、sha、ref、environment；有权限的发布方可给该 deployment 发 success/failure 等状态。|这比一条普通事件更接近可判定的系统记录，但审批对象是运行/环境，审批请求与历史条目都不原生要求最终产物 digest 或外部操作键。check 成功不是人签字；deployment.creator 也不是审批人。先按 GitHub 的对象关系取证，再联制品摘要、目标回执及服务恢复。在多运行、多制品时不要按 SHA 或近似时间“猜”是哪一次审批。[官方审批接口](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2026-03-10) · [官方部署状态](https://docs.github.com/en/rest/deployments/statuses?apiVersion=2026-03-10) · [本地六个接口摘录](github-fields.json)|
|**SLSA v1.2 Build Provenance + in-toto Statement v1**，核对 in-toto 仓库 tag v1.2.0|构建方签发声明，subject 的每个产物都要求 digest；构建定义、runDetails.builder.id、已知 resolvedDependencies 能把产物和构建输入相连。SLSA v1.2 规范状态 Approved，谓词 URI 是 https://slsa.dev/provenance/v1。另有 in-toto release v0.2 谓词可由注册表把包版本映射到多个制品摘要。|验证方须核对签名、受信构建者、subject 与实际下载内容，以及预期输入/构建参数；依赖记录完整度取决于构建方与级别。即使签名有效，构建者证明的也是其声明范围，不能当作用户同意部署此摘要，也不能说明服务恢复。其他专用谓词不在本次结论范围。[SLSA 构建来源](https://slsa.dev/spec/v1.2/build-provenance) · [验证步骤](https://slsa.dev/spec/v1.2/verifying-artifacts) · [in-toto Statement](https://github.com/in-toto/attestation/blob/df02077bf97218a8860a5c534eff1f1381f56984/spec/v1/statement.md)|

## 对哪些数据做了实测

使用 Python jsonschema 4.23.0 的 Draft7Validator 和 Draft202012Validator，开启格式检查。全部输入与 schema 均来自本地，未调用 GitHub API、发布消息、签发证明或改动产品。共有 **26 次 schema 判定，23 次通过、3 次按预期拒绝**。其中包含对同一文档分别执行内外层检查和重复投递；不是 26 个互相独立的样本。[探针](probe.py) · [逐条验证结果](checks.json)

1. **从实测投影两种格式。** 两个实测批次各取 Temporal 的 lost/基础与 lost/去重两行。只把 taskName=publish、outcome=success 映到原生内容，适配器为四次演示分别派事件 ID/subject；timestamp 取整个实验记录完成时间，真实首次写入和重试时间没有被恢复。之后按 CDEvents 绑定，将完整 context、subject 及可选 customData 放进 CloudEvents.data，并按规范镜像 id、source、type 等字段。第二份投影用 customData 放入原始记录指针、实际 verdict 和目标行数。这些是研究方添加的证据摘要，不能只因被搬进标准消息就获得可信身份。[两种序列化的完整输入](examples.json) · [原始空库重复](../handoff/evidence/repeat/observations.json)
2. **合法重投与关联歧义。** 重投同一 CloudEvents source+id 的同一文档，单条校验仍通过。另做两条 CDEvents service.rolledback，使用同一个 chainId、同一环境、不同 artifactId，两条均通过，说明同一调查链能包含不同目标。去掉 CloudEvents 的 source，或去掉回滚的 environment、artifactId，三条阴性对照逐一被拒绝。这些回滚样例是合成输入，未真实切换服务。
3. **过了 schema，仍可能违背文本合同。** change.reviewed 没有批准人、批准结论或目标摘要仍过 schema；其正文却说明应包括审查意见，不能称为已获批准。taskRun.finished 的 outcome 在正文限于 success、failure、cancel、error，官方 schema 中该属性仅检查字符串，故一个非规范值也能通过结构校验。最后，刻意让外层 CloudEvents id 与内层 CDEvents context.id 不同，两个 schema 各自判有效，CDEvents binding 明文要求二者相同。分层校验后仍需做跨层关系检查。[官方绑定](https://github.com/cdevents/spec/blob/78e5ee85b3e094de0a06aeb6b44c62e4dab2148d/cloudevents-binding.md) · [任务事件正文](https://github.com/cdevents/spec/blob/78e5ee85b3e094de0a06aeb6b44c62e4dab2148d/core.md)

## 最小客户合同：现有系统各留一份可重查依据

- **批准归审批服务。** 用真实审批记录（采用 GitHub 时先取环境审批历史）保存或引用决策者、作用范围、允许动作、环境、不可变输入或产物摘要，以及失效/撤销状态。一个 run 可有多个目标；将决策与确切目标配上。已过期或内容已变时由接单方要求重新核准。
- **交付对象归构建与部署系统。** 采用已经存在的 commit、build identity、in-toto subject digest 和 deployment ID。部署前核验将运行的 digest 确由受信构建产生，而且等于所批对象。部署状态声明与应用恢复应分开留证。Git commit、包版本和容器字节分别指向不同对象。
- **业务写入归目标端。** 在支持的现有 API 使用一次逻辑操作一个业务键，目标端对第一次提交与随后复用返回可重查回执。CloudEvents id 或 OTel tool.call.id 仍用于事件/调用关联。若下游没有原子去重、也查不到回执，丢回执后把写入标为未知，交接时保留原请求，不能根据 workflow success 推定仅写一次。是否需要补偿以及补偿权限由业务 owner 决定。
- **恢复归实际服务与业务 owner。** 用现成 deployment / rollback / incident 记录关联受影响实体，由独立探测、审计读回或业务验收在指定窗口确认结果。审批、构建、写入、恢复四份记录用各自既有 ID 和摘要可相互定位即可；没有必要要求统一事件总线或统一 trace 产品。

在采购演示中，最有区分度的是让供应商找齐同一次动作的四份原始证据，再切断外部写入后的回执。若仍能给出目标侧的既有行及对应授权，它能接手这一部分工作；若只给出同一 trace、绿色 check 或格式正确的 rolledback 消息，能验收的是传输与观测能力。[用于对照的实测故障窗口](../handoff/result.md)
