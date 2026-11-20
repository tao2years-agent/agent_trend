# 协作内核：共享上下文、任务与产物

## 组织级产品的最小对象模型

一个团队协作 Agent 不应只是一条聊天线程。最小协作内核至少包括：

1. `Workspace/Space`：明确成员、组织归属、数据边界和保留策略。
2. `Goal/Brief`：成果、成功条件、允许行动和必须审批点。
3. `Task`：状态机、负责人、Agent 执行者、截止时间、依赖与重试语义。
4. `Artifact`：文档、表格、代码、页面等可共同编辑、版本化和授权的成果。
5. `Context source`：群聊、会议、数据库、文件等；保留来源权限和 provenance。
6. `Memory`：可查看、纠正、停用、过期，不把推断伪装成事实。
7. `Agent`：owner、版本、能力、身份、预算、连接、策略与生命周期。
8. `Decision/Approval`：谁在什么证据下批准了什么动作，后续能撤销或追责。

## 三种共享语义必须分开

- `share by reference`：Agent 查询原系统对象，权限和更新由原系统控制。
- `share by copy`：内容被复制进协作空间，之后可能脱离原 ACL、删除和更新。
- `share by service`：使用者不能直接看到数据，但可通过有独立权限的 Agent 获得回答。

Google Agent Designer、Notion Custom Agents、ChatGPT 的共享连接都说明第三种模式是真实产品需求，但也最容易形成 confused deputy 和隐性越权。UI 必须显示“本次由谁的凭据访问了什么”，不能只显示一个笼统的“已连接”。

## 产物优先于 transcript

组织协作的价值落在持久对象：可编辑文档、任务看板、代码提交、审批记录。聊天只是控制面。WorkBuddy 的统一文件、千问资料空间、ChatGPT Space/Slides、Notion 页面和 repo/PR 都在指向同一趋势：让成果离开对话，进入可治理的共享资产系统。[研究推断]
