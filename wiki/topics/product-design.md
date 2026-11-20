# 产品设计清单与路线图

## 首要产品原则

1. **共享工作，不只共享聊天**：任务、资料、产物、决策和 Agent 配置都要成为可授权对象。
2. **Agent 是有身份的组织资产**：个人 Agent、团队 Agent、外部 Agent 使用不同权限与生命周期模型。
3. **默认可见的代理关系**：任何结果都能回答“谁要求、哪个 Agent、用谁的账号、访问了什么、谁批准”。
4. **人控制高影响决策**：Agent 可以准备和推荐；发布、付款、授权、删除、对外发送等按风险审批。
5. **记忆可治理**：可见、可改、可停、可过期、有来源。
6. **失败是产品状态**：暂停、阻塞、重试、部分完成、等待审批、权限不足都要可见，不用“正在思考”掩盖。

## 关键角色

- requester：提出目标。
- task owner：对完成标准负责。
- reviewer/approver：判断结果与高风险动作。
- agent owner：维护配置、版本、连接和预算。
- data owner：决定来源是否可被 Agent 使用/复制。
- workspace/admin/security：控制政策、目录和事件响应。
- external collaborator：来自另一信任域，权限和责任需单独定义。

## MVP 建议

### Phase 1：团队协作内核

- 企业内 space、成员、共享 brief、任务、产物和评论。
- Personal agent 与 Team agent 分型。
- 共享来源按原 ACL 检索；显示 acting identity。
- 草稿/只读动作自动执行，高风险动作审批。
- Agent owner、版本、预算、运行记录、暂停/撤销。

### Phase 2：组织治理与自动化

- Agent catalog、发布审批、模板/Skill/连接器复用。
- 事件触发、定时任务、durable workflow、幂等与补偿。
- 管理员 inventory、成本、质量、风险和 orphan 处理。
- 本地/云/自托管执行策略与数据驻留。

### Phase 3：受控外部协作

- 先做外部 guest + 双边 workspace contract，再做开放 Agent federation。
- 结构化 external grant、最小数据披露、双方 trace 对账。
- A2A adapter、Agent identity federation、token exchange、协议版本策略。
- 合同、地域、保留、退出、incident 和争议流程产品化。

## 评价指标

- 业务：任务 cycle time、交接次数、产物采纳率、重复工作减少、跨团队复用率。
- 质量：事实错误、返工、人工覆盖率、审批拒绝率、任务真实完成率。
- 安全：越权阻断、敏感外发、orphan agent、凭据超期、跨租户测试通过率。
- 运营：每成功任务成本、fan-out、重试率、等待审批时间、Agent 利用率。
- 协作：多人参与率、上下文复用、产物共同编辑、决策可追溯率。

避免把“生成次数、消息数、节省百分比”当作唯一价值指标；组织级产品的核心是可靠流转、责任清晰和可复用资产。
