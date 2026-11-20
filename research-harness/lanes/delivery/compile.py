"""Research judgments, source locators and planned falsification tests for delivery mechanisms."""
from pathlib import Path
import json, hashlib, re
from fetch import BASE,ROOT
# Ordered fields: id, repository key, product, category, trigger, mechanism, human control, organizational use, limit, release observation, inference, experiment, source locators.
rows=[
('D01','runner','GitHub Actions Runner','作业执行与宿主控制',
'自托管 runner 接到仓库 workflow 作业；平台团队要在各仓库步骤外统一校验执行条件或收尾。',
'Worker 先准备动作，读取宿主的 ACTIONS_RUNNER_HOOK_JOB_STARTED，将同步脚本纳入 pre-job；另读取 JOB_COMPLETED 注册 always() 的 post-job。ADR 约定脚本非零退出使作业失败。',
'runner 管理员配置宿主脚本和退出码；开发者可从作业结果查到失败，再决定修改工作负载还是调整宿主策略。',
'在共用 runner 池集中实施环境检查、留存审计信息；前置脚本本身的耗时和故障会影响整池。',
'入口在自托管 runner；动作准备早于 pre-job hook。宿主失联、强制终止时能否完整收尾未实测，不能把注册 post-hook 当作交付凭据。',
'v2.338.2 的变更记录包含 Docker 29.8.0 和 Buildx 0.37.0 更新。这里记录运行环境演进，hook 的既有设计另由 ADR 与源码证明。',
'治理可以下沉到维护者可控制的 runner，使大量仓库复用一份规则；要单独测量宿主检查故障引起的全局阻塞。',
'在隔离池令 pre-hook 对带错标签的作业返回非零；提交同一任务到有/无 hook 的池，核对本体是否执行、失败分类、正常结束与人为终止时的清理记录。',
('JobExtension.cs L297–315、572–586：准备动作、加入启动钩子、注册完成钩子','ADR 1751 L60–76：同步、退出码和管理员责任','发布页 变更列表 中的 Docker / Buildx 更新')),
('D02','buildkite','Buildkite Agent','分布式执行与远程中止',
'自托管 worker 已经运行构建；控制端收到取消或超时，此时需把中央意图落实到具体作业进程。',
'JobRunner 在进程启动后轮询 job state，带抖动；服务返回 canceling/canceled 或 timing_out/timed_out 时分别调用 Cancel 并传递原因。401 也触发因凭据无效而取消；短暂的普通请求失败等待下一轮。',
'操作人员可以从控制端请求取消，runner 管理员配置检查间隔和信号。用户点击中止后，执行端仍需收到状态并处理信号。',
'平台团队可对不同队列统一记账，区分人工中止、凭据失效、运行超时，从而定位基础设施滞后。',
'Agent 源码可见；托管控制端的内部调度未核对。文档与源码不提供用户点击到外部副作用停止的端到端时限。',
'v4.12.0 将产物上传路径纳入 signed jobs 的签名与校验，并提示先更新验签 agent，再用新版本签署 pipeline。',
'作业取消应产生可测的控制延迟；签名协议升级也需要兼容性发布顺序。',
'记录取消请求、runner 观测、子进程退出三个时间戳；比较不同轮询间隔、短时离线及有无外部异步子任务时的尾延迟和残留作业数。',
('agent/job_runner.go L1032–1105：轮询、抖动、401、cancel 和 timeout 分支','README L19–48：agent 子命令、build queue 与安装入口','v4.12.0 Security 条目以及升级验签 agent 顺序')),
('D03','tekton','Tekton Pipelines','Kubernetes 流水线与中止语义',
'测试或部署 PipelineRun 在并行执行中被叫停，还需要决定是否让在途任务收尾、保留清理或取证步骤。',
'控制器从 PipelineRun 状态协调 TaskRun。CancelledRunFinally 中止正在运行的任务并继续 finally；StoppedRunFinally 允许在途任务及其重试走完，阻止新的普通任务，再调度 finally。普通 Cancelled 不调度待运行的 finally。',
'具备相应权限的调用方选择中止语义；创建时设 Pending 可将启动推迟到条件满足，不等于自带审批身份验证。',
'分别编码紧急刹车、温和排空和清理证明，跨团队可对齐同一运行对象及父子任务归属。',
'需要 Kubernetes 与 Pipeline 控制器；finally 仍受总时限等条件约束。服务端 RBAC、集群故障和副作用回滚未实测。',
'v1.18.0 通过 webhook 使控制器设置的 pipeline、pipelineTask、pipelineRun 标签一经写入不可被更新者改写。',
'为组织提供一个取消按钮之前，需要明确它对在途动作与证据留存的承诺。',
'让任务 A 处于写产物阶段、B 等待依赖、finally 归档；分别发三种取消请求，比较运行任务、重试、子任务归属和归档结果。',
('pipelinerun.go L349–355、867–875：finally 超时与温和中止分支','pipelineruns.md L1695–1756：三类取消/停止和 Pending 时机','v1.18.0 controller-managed labels immutable via webhook，#10687')),
('D04','argocd','Argo CD','GitOps 期望状态协调',
'集群对象与 Git 期望配置发生偏离，团队需区分检测差异、修正漂移，以及是否删除额外对象。',
'controller 将目标与 live 对象配对，对额外且属于本应用的对象设置 RequiresPruning；资源忽略规则、所有权和比较错误会影响 Synced、OutOfSync 或 Unknown。automated、prune、allowEmpty、selfHeal 分别控制动作。',
'应用维护者选择是否开启自动同步、清理、空目标和自愈；自动同步开启时直接 rollback 有限制，紧急干预需要预先定义流程。',
'把版本库作为变更入口、把现场差异作为运行证据，平台团队可单独放宽自愈或收紧删除。',
'多源应用关闭 selfHeal 仍不能保证现场修改永久保留；同步状态描述配置差异，不能证明服务正确或业务指标正常。',
'v3.6.2 修正 Unknown 同步状态之后仍复用差异缓存的问题，并在 manifest-generate-paths 无变化时保留服务端差异缓存。',
'期望状态、测不到状态、实测业务结果应分字段保存，否则会以缓存状态误报完成。',
'测试命名空间制造现场漂移、额外对象及无法读取对象；分别开启 selfHeal/prune，观察状态与动作，再与业务健康检查对照。',
('controller/state.go L992–1029、1058–1089：比较错误、所有权、清理标志、状态判断','auto_sync.md 的 Automatic Pruning、Self-Healing、Automated Sync Semantics 以及 L209–215 限制','v3.6.2 controller diff cache 的 #30893 / #30899')),
('D05','rollouts','Argo Rollouts','金丝雀分析与例外升级',
'金丝雀达到特定步骤后，应根据一段指标窗口判断能否放量、是否中止，或转人工处理。',
'AnalysisRun 记录各指标的测量和计数。控制器在判断连续成功前先检查失败、无结论和错误限额；配置 dryRun 的指标仍产生测量数据但不左右最终判定。分析可得到 Successful、Failed 或 Inconclusive 等状态。',
'在 rollout 的分析语境中，维护者可在无结论时检查测量，再决定继续或中止；可先以 dry-run 收集新指标的行为。',
'业务服务团队制定指标和阈值，平台复用分析流程；可拆开统计“明确退化”与“证据不足”两类等待。',
'结果强依赖采样窗口、流量、数据源和条件表达式。未运行集群或测量真实告警误报。不同终止方式有独立语义。',
'v1.11.0-rc1 的 Web metric provider 对空响应或非 JSON 响应也计算成功/失败表达式，改变以往直接 Successful 的行为；这是候选版本。',
'需要把空样本和解释不清的结果带给人；把两者折叠为成功会向更多用户扩展不确定变更。',
'在隔离金丝雀中注入正常指标、阈值边界、空正文、持续无数据；记录 AnalysisRun 原始测量、最终相位和人工处置，对比 RC 与旧版。',
('analysis/analysis.go L104–136、398–439、620–722：测量归集、失败优先和计数阈值','analysis.md Failure Limits and ConsecutiveSuccessLimit、Dry-Run、Inconclusive Runs','v1.11.0-rc1 Breaking Changes 中 Web metric provider 成功/失败表达式')),
('D06','renovate','Renovate','依赖维护及条件合并',
'自动依赖更新已经产生分支，高频的小更新若逐个等待审批会积压，团队需选择可放行的更新类型。',
'tryBranchAutomerge 要求启用 automerge 且类型为 branch，检查 automergeSchedule、分支是否已有 PR，再读取分支状态。green 才尝试 mergeAndPush；红色、非就绪、队列或分支保护产生各自结果。PR 类型走另一条路径。',
'维护者设置 packageRules、必检项、保护分支和 merge queue；组织 preset 可继承，仓库可以覆盖规则。',
'精细缩小无需逐项人工审查的范围，同时用队列分歧或保护规则失败解释等待。应按更新类别跟踪返工。',
'ignoreTests 与平台检查配置会影响什么能被认作绿色。高频主分支提交也会缩小合并机会；自动成功不等于依赖升级无兼容问题。',
'44.253.4 在 GitLab 平台修复重新为已推送 commit 启用 automerge 的行为，显示平台侧合并状态要随新提交更新。',
'可自动批准的单位应是具有明确影响面和可复查检查集的变更类别；不要笼统授权全部低行数改动。',
'同一仓库以 patch/minor/major 与检查齐全/缺失分层，先用 dry-run 分类，检查主分支再更新时的重新评估情况。',
('automerge.ts L21–111：类型、时段、已有 PR、状态、dry-run、保护分支与错误处理','automerge.md Automerge / Merge Queues / Overriding global automerge','44.253.4 的 platform/gitlab 修复 #47980')),
('D07','pragent','PR-Agent','模型评审与覆盖度反馈',
'PR 大于单次上下文，部分分片可能未成功。评审者需要知道模型看过什么，哪些反馈值得再次核查。',
'PRReviewer 合并各片推断前过滤低置信发现，以免挤占结果上限；发布判断考虑 finding 状态变化、状态阻塞或部分分片失败。部署端保留特定配置键的控制权。',
'负责人复核 PR 反馈与未覆盖部分；v0.50.0 明确 auto-approval 路径仍禁用，配置项归宿主所有。社区项目的行为不外推至厂商商业产品。',
'评审队列可按未覆盖或失败部分分派复核，避免把空评论计成完整检查。可收集每条建议的采纳与误报。',
'本地调用固定 SHA 的配置判定函数，自动批准与重试次数均返回宿主专有，仓库可调整 skills.enabled 与 max_skills_tokens。未运行模型或连接 PR 平台；分片之间跨文件依赖、过滤阈值和供应商超时均可能影响覆盖与准确率。',
'v0.50.0 收紧仓库可改写的重试和调用次数配置，同时把 enable_auto_approval 改为宿主专有；该版本发布说明区分“增加配置约束”与“已启用自动批准”。',
'把模型覆盖情况作为交付证据的一部分交给人，独立维护“评审者是谁”和“谁有批准权”。',
'固定有跨文件关联的 PR，让一片超时并重复运行；比对覆盖提示、模型发现、人工标注，以及失败片重跑后仍未发现的缺陷。',
('pr_reviewer.py L920–939、1809–1834：公布状态、分片结果过滤及合并','config_security.py L42–155：宿主专有键及判定','v0.50.0 Breaking changes：Host-only settings、Auto-approval、#4700')),
('D08','atlantis','Atlantis','基础设施变更的计划与应用',
'团队在 PR 里查看 Terraform/OpenTofu 计划，再由有权者执行 apply；并发和计划版本变化会影响当初审阅的内容。',
'执行端先检查项目 apply 要求与依赖，然后获取项目/目录工作锁，加载已保存计划。在托管 plan/apply 路径中检查计划，并紧邻具体 apply 步骤再次验证。v0.49.0 为新生成的计划记录哈希。',
'有权者检查计划后触发 apply；审批规则检查与已保存计划摘要验证是两个条件。发布说明明确 approval 自身没有与某一条 plan 记录绑定。',
'将 PR、项目、workspace、计划摘要、审批和实际应用结果联系起来，区分“谁授权”与“授权时/应用时是什么产物”。',
'使用定制步骤的工作流是否采用 Atlantis 托管计划需要逐项确认；默认保证仅适用于对应路径，旧版本留下的计划也不能一概视为已有哈希。',
'v0.49.0 拒绝应用生成后被改动的已记录计划，要求重新 plan；审批条件在 GitHub/Gitea 以每个评审者最新 review 为准。',
'高影响操作可借鉴 plan→review→apply，但应显式检查人实际看到的版本以及即将应用的摘要；重新规划也应重新评估审阅需求。',
'沙盒使用无外部资源的 IaC，分别保留和刷新计划、制造并行 PR；核对被应用产物、锁持有者、最近 review 和重计划日志。',
('project_command_runner.go L943–1008、1207–1256、1296–1302：要求、锁、计划加载和再次验证','README 的项目说明及官方用户文档入口','v0.49.0 Upgrade checklist 及 Apply/Approvals 关于计划摘要和最新 review')),
('D09','conftest','Conftest','配置策略验证',
'待合并的配置、IaC 或所有者清单发生变化，团队希望在调用外部系统前运行可重复的规则。',
'TestRunner 按格式解析输入，加载 Rego 策略、数据、能力集与命名空间；通常按文件检查，也可合并后跨文件检查，返回结构化结果。已运行 v0.71.0 CLI，以自编生产 owner 规则得到预期退出码。',
'领域负责人维护规则、例外和何时阻断，CI 管理者决定将退出码接成必检。团队可以把结构化的命中原因交给变更作者。',
'让可机械验证的要求共享同一套策略；对要求 owner 的演示，生产环境有 owner / 缺失 / 开发环境缺失分别返回 0 / 1 / 0。',
'已实测的只是 Windows 本地 CLI 的三组 JSON，不代表 CI 分支保护、真实所有权、线上漂移或团队生产率已经验证。',
'v0.71.0 新增 CODEOWNER 文件解析器，并修复多文件时 TAP 输出产生多份计划的问题。本文的最小实验使用 JSON，未实测这个新解析器。',
'优先把重复评审意见中语义稳定的一部分转成有版本的规则；统计规则覆盖的真实事件与误阻断。',
'在历史配置变更做留出回放，比较现有人工审查与策略输出；重点复核例外、缺少上下文的通过样本、误阻断率及修复耗时。',
('runner/test.go L45–122：格式解析、规则加载、命名空间、独立与组合检查','docs/index.md 的 deny、JSON 输出、query 与上下文','v0.71.0 New Features #1404、Bug Fixes #1435')),
('D10','temporal','Temporal（Python SDK）','跨等待与重启的工作流',
'一个研发任务可能先执行外部 Activity，再等维护者决定；等待跨越 worker 重启或新版本上线。',
'SDK 在激活时读取 replay 标记及历史逻辑标记，分组处理 signal、update 等事件；示例通过 workflow.wait_condition 等待 signal 改变状态，也可设超时。Replayer 能用已有 history 检查新 workflow 实现。',
'业务实现决定谁可发 signal、何时超时、如何重试外部操作；编排层可保存决定并继续，而非一直占用一个模型请求。',
'用持久工作流表达等待、取消、重试和升级，历史回放可成为平台变更的一项兼容性检查。',
'基于 Python SDK 的证据不能直接外推所有语言。重复外部副作用是否受控，取决于 Activity 和下游的幂等设计；未运行 Temporal 服务或测试历史。',
'1.36.1 对未记录逻辑标记 2 的工作流默认关闭 single-batch 激活，以维持旧 signal/条件等待/取消的行为；已记录标记 2 的 history 继续使用该语义。',
'工作流版本升级必须尊重在途实例的事件历史。评估 harness 时应把跨版本恢复与外部副作用区分开。',
'录制“发出请求→等待 signal→取消”不同先后次序的 histories，在两个 SDK 版本上回放；另对重复 Activity 注入幂等键，分别记录兼容性与外部写入次数。',
('temporalio/worker/_workflow_instance.py L480–545、4264–4271：replay、逻辑标记与激活分组','README 的 Workflow Replay、wait_condition、signal 超时示例','1.36.1 Notable Changes 对 flag 2 的兼容规则')),
('D11','jenkins','Jenkins Pipeline Input Step','人在回路中的授权与拒绝',
'生产发布抵达 Jenkins Pipeline 的 input 步骤时，需要指定值班组或人员确认，或由有权人员中止。',
'InputStepExecution 在 POST 端点做 preSubmissionCheck，检查是否已经处理、是否可提交；未指定 submitter 用 Job.BUILD 权限，指定时按用户/组匹配并保留管理员特例。submitterParameter 可记录提交者，abort 向流水线传播中断。',
'配置者设定可提交人员或组；经授权的账号确认、填写参数或拒绝。管理员特例需进入组织自己的职责分离检查。',
'平台用同一输入步骤表达例外升级；能统计等待时长、决策者与处理结果，为减少无价值等待提供样本。',
'该插件不自动判断审批者当时看到哪个 commit 或产物，也不能仅凭一次确认断言双人分权成立；构建参数另需绑定具体交付内容。',
'560.v56198a_642157 为 Pipeline Graph View 复用 input 对话框增加资源文件，使另一界面复用交互。此项属于呈现与集成变更。',
'审批事件至少应能关联可执行产物与决策者。等待点可以复用 Jenkins，证据绑定仍须在上层实现。',
'用普通构建者、指定组成员和管理员分别提交或拒绝同一输入，记录结果、提交者字段及重复提交响应；更新构建版本后检查旧批准能否被复用。',
('InputStepExecution.java L284–311、336–346、372–396：批准/拒绝、处理状态、人员与组','README L23–39：submitter 与 submitterParameter','560.v56198a_642157 的 Pipeline Graph View 对话框 #258'))]
def build():
 cases=[];manifest={}
 for row in rows:
  id,k,name,category,scenario,mech,human,org,limits,change,ins,exp,detail=row
  d=json.loads((ROOT/(k+'.index.json')).read_text(encoding='utf-8')); release=json.loads((ROOT/(k+'.release.json')).read_text(encoding='utf-8'))
  docs=[s for s in d['sources'] if 'repo_path' in s]
  assert len(docs)==2
  primary=docs+[release['source']]; sources=[]
  for s,note in zip(primary,detail):
   url='https://github.com/'+d['repo']+'/blob/'+d['sha']+'/'+s['repo_path'] if 'repo_path' in s else s['url']
   sources.append(dict(url=url,path=s['path'],detail=note,date=s['date']))
  for s in d['sources']+[release['source']]:
   p=BASE/s['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];manifest[s['path']]=s
  case=dict(id=id,name=name,category=category,scenario=scenario,mechanism=mech,human=human,org=org,limits=limits,change=f"{release['source']['date']} UTC，"+change,insight=ins,experiment=exp,sources=sources,source_commit=d['sha'],evidence='源码与版本说明复核；'+('本地 CLI 三个输入已验证' if k=='conftest' else '配置范围函数四个输入已验证' if k=='pragent' else '未做产品运行实验'))
  if k=='conftest':case['runtime_record']='lanes/delivery/experiment/conftest-v0.71.0.json'
  if k=='pragent':case['runtime_record']='lanes/delivery/experiment/pragent-config-scope.json'
  cases.append(case)
 (ROOT/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'manifest.json').write_text(json.dumps(list(manifest.values()),ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'{len(cases)} cases; {len(manifest)} unique source snapshots hash-verified')
if __name__=='__main__': build()


