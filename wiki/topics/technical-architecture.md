# 技术参考架构

## 分层

```text
Collaboration surfaces
  Chat / channel / docs / tasks / IDE / external portal
        |
Collaboration kernel
  Space + membership + goal + task state + artifacts + memory + approvals
        |
Agent control plane
  Registry + versions + owner + policy + budget + scheduler + evaluator
        |
Orchestration plane
  Planner + subagents + A2A adapter + durable workflow + event bus
        |
Identity & policy plane
  IdP/OIDC + Agent Identity + token exchange + PDP/PEP + secrets broker
        |
Tool & data plane
  MCP/API/connectors + ACL-aware retrieval + DLP + provenance
        |
Execution plane
  local sandbox / managed cloud / self-hosted runner / browser / code runtime
        |
Observability & compliance
  trace + audit + cost + eval + incident + retention + export
```

## 关键技术决策

### 1. Durable task state

长任务不能只存在模型上下文。任务状态、步骤输入输出、审批、重试、幂等键和 checkpoint 要进入持久工作流引擎。模型负责计划建议，状态机负责可恢复性和副作用边界。

### 2. Context broker

检索层要携带 principal、tenant、purpose 和 classification，按原 ACL 过滤并返回 provenance。共享空间里的摘要不是天然可信事实；每条关键记忆保留来源、更新时间、置信度和可见范围。

### 3. Agent gateway

所有 Agent→Tool 和 Agent→Agent 调用经过统一执行点：身份验证、策略评估、schema 校验、DLP/内容检测、限流、成本计量和 trace。不要让每个 Agent SDK 独自实现安全逻辑。

### 4. Delegation service

将用户授权编译为短期、可撤销、可降权的 capability/grant；每次向子 Agent 或外部组织委托时缩小 scope。跨组织时记录 issuer、audience、purpose、data classes、maximum actions、expiry 和 approval chain。

### 5. Artifact service

产物采用独立对象和 ACL，支持版本、评论、共编、出处和发布状态。聊天里的附件只是引用；复制到新空间时产生 disclosure 事件。

### 6. Multi-tenant isolation

tenant_id 必须贯穿数据库键、缓存、向量索引、对象存储、任务队列、trace 和 billing。测试要包含对抗性跨租户查询，而不是只做正常路径单元测试。

## 不建议的捷径

- 让团队 Agent 永久持有创建者 OAuth refresh token。
- 只在系统 prompt 里写权限规则。
- 用一个共享超级账号连接所有系统。
- 把 Agent 间自然语言消息当成授权凭据。
- 把向量数据库 metadata filter 当唯一租户隔离层。
- 只记录最终答案，不记录工具与委托链。
- 对外部 Agent 只做域名 allowlist，不验证 issuer、版本和能力声明。
