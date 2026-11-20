# 治理、安全、审计与成本

## 组织级风险台账

| 风险 | 典型失效 | 必要控制 |
|---|---|---|
| 权限混淆 | 使用者通过共享 Agent 读取本无权看的数据 | 显示 acting identity；按调用者裁剪或明确 service 权限；输出过滤 |
| 委托升级 | 子 Agent 获得比上游任务更大的权限 | token exchange 降权；逐跳 PDP；最大 delegation depth |
| Prompt injection | 文档/网页诱导 Agent 泄露或写入外部系统 | 内容/指令分层；工具结果标记；高风险审批；egress policy |
| 记忆污染 | 错误信息变成团队长期共识 | 可见/可纠正/有来源/有 TTL；事实与推断分层 |
| 自动化失控 | 定时任务重复发送、重复扣款或反复修改 | 幂等键、去重、租约、重试上限、补偿、kill switch |
| Orphan agent | owner 离职后 Agent 仍持有权限和预算 | owner transfer、定期 attest、自动暂停、凭据回收 |
| 供应链 | Skill/MCP/插件更新后能力或权限变化 | 签名、版本固定、清单 diff、审批、沙箱和最小权限 |
| 成本爆炸 | 多 Agent fan-out、重试、周期任务持续消耗 | 每任务/Agent/团队预算、并发限制、预测与异常告警 |
| 审计断链 | 只记录最终答案，不知道谁调用了什么 | end-to-end trace、授权链、工具 I/O 摘要、产物版本与审批 |

## 治理不是一个管理员页面

至少有四层：

1. **Access**：谁能使用、创建、发布 Agent。
2. **Agent portfolio**：owner、版本、模型、连接、预算、状态、下架。
3. **Runtime policy**：文件、网络、工具、命令、数据和审批规则。
4. **Source-system policy**：CRM/网盘/代码库等原系统真正执行的 ACL。

OpenAI Work Admin FAQ 明确这些控制不是一个统一表面；Claude Code 也区分 repo/user/managed settings；千问的后台页面权限与开放平台 API 权限分开。产品设计若只画一张 RBAC 表，会漏掉运行时和源系统授权。[官方事实 + 研究推断]

## 审计事件的最小字段

`event_id, trace_id, task_id, tenant_id, human_principal, agent_id, agent_version, runtime_id, acting_credential, tool/resource, policy_decision, approval_id, input/output classification, artifact_version, cost, timestamp, outcome, retry_of`。

日志应支持组织内调查与跨组织对账，但敏感 prompt/结果不能默认全量长期存储；需要可配置的内容日志、哈希/摘要、脱敏和保留期。
