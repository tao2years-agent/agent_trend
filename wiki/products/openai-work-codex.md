# ChatGPT Work / Codex

## 判断

OpenAI 的协作产品结构不是单一“办公 Agent”，而是多个协作表面的组合：ChatGPT Work 承担长任务，Teams/Team Tasks 承担团队自动化，Space 承担可共同编辑和分享的产物，Slack/Teams surface 把 Agent 放进现有沟通场所，Codex 则提供代码与执行环境。[官方事实]

其最有价值的设计启示是：**执行者身份和协作空间身份被显式拆开**。Team Task 可以使用团队服务账号和共享连接；Slack 中请求 Codex Cloud 时，服务账号用于查找环境，但代码任务以请求用户身份运行。这比“Agent 自动继承频道里所有人的权限”更可治理。[官方事实]

## 协作对象

- Team：共享成员、连接和 Team Tasks；与 SCIM group 以及 Slack/Teams channel 不是同一个对象。
- Team Task：定时或事件触发，在云端运行；由团队服务账号和连接决定外部系统身份。
- Space：页面、幻灯片、文件与共享内容；页面可给团队 view/edit 权限。
- Surface：一个 ChatGPT workspace 到 Slack workspace 或 Teams tenant 的部署边界。
- Agent thread/subagent：并行执行的内部工作单元，活动可检查，但通常不等于多个人共同对话。

## 风险边界

- Team 的单个任务和单次运行不能各自设置独立访问限制，邀请成员前要理解历史运行与生成文件的可见性。
- Surface 的共享公司连接可能拥有不同于参与者个人账号的权限；使用者可通过 Agent 间接触达服务账号可见的数据。
- 私人记忆不默认进入团队任务；这是隐私保护，也是上下文连续性的产品挑战。
- Work Cloud、Work Local、Codex Local 与 Codex Cloud 是不同执行边界，托管配置、RBAC、沙箱和网络控制不能互相替代。

## 跨组织判断

官方资料要求为每个 Slack workspace/Teams tenant 配置 surface，并以一个 ChatGPT workspace 为管理边界。本轮未找到“两个 ChatGPT workspace 共同拥有一个 Team/Task/Agent”的证据。因此，可通过 Slack Connect 等宿主渠道形成的外部会话，不应未经验证就宣称为原生跨组织 Agent 协作。[研究推断]

## 证据

- [Working with agents](https://learn.chatgpt.com/docs/working-with-agents)
- [Set up and manage teams and Team Tasks](https://learn.chatgpt.com/docs/enterprise/teams)
- [ChatGPT Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [ChatGPT Space](https://learn.chatgpt.com/docs/enterprise/chatgpt-space)
- [@ChatGPT in Slack and Microsoft Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams)
