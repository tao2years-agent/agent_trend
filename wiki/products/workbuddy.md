# Tencent WorkBuddy

## 判断

WorkBuddy 的差异化不是单纯“能做 PPT/表格”，而是把能力组织成三层：个人工作台、云端助理、多 Agent 项目空间。其官方产品页明确描述项目空间内多个 Agent 并行处理任务，调试后的专家、Skill 和连接器可供多人复用，并可在统一知识库和权限边界下跨部门推广。[官方事实]

官方博客进一步把多 Agent 表述为“团队负责人拆解任务、专家并行、过程共享信息、最后整合成一个文件”。这仍主要是**一个用户指挥一支 AI 专家队伍**，不自动等同于多人共同拥有任务、共同修改产物或共同审批。[官方事实 + 研究推断]

## 产品设计拆解

- 触发：用户以自然语言交办复杂任务。
- Agent 组织：100+ 预置专家；系统可按任务组队并设协调角色。
- 执行：本地文件操作与云端托管并存；云任务在关闭客户端后可继续。
- 团队复用：专家、Skill、连接器和知识进入项目空间。
- 交付：强调可验收文件而不是多份 Agent 对话记录。

## 组织协作边界

官方公开材料证明了组织内团队复用和跨部门推广，但尚未公开证明：外部客户/供应商加入同一 Agent 项目、跨租户身份联邦、对外委托链、跨组织审计对账或数据使用合约。因此本研究把其跨组织能力标为 `open_question`，不能从“跨部门”外推成“跨公司”。

## 证据

- [WorkBuddy 产品页](https://cloud.tencent.com/product/workbuddy)；本地抓取记录：`raw/src-tencent-workbuddy-product/2026-11-16/metadata.json`
- [你的AI新同事，还带了几个朋友来上班](https://www.tencent.com/zh-cn/your-new-ai-colleague-brought-a-few-friends/)；本地抓取记录：`raw/src-tencent-workbuddy-team/2026-11-16/metadata.json`
- [WorkBuddy 企业版](https://www.workbuddy.cn/enterprise/product)；动态页面公开细节待补抓。
