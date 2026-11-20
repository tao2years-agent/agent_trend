import json,hashlib,datetime,re
from pathlib import Path
from xml.etree import ElementTree as E
HERE=Path(__file__).resolve().parent
project=HERE.parents[1]
refs=json.loads((HERE/'sources.json').read_text('utf8'))
details={
'openhands':['ConfirmationPolicyBase、ConfirmRisky；L43–61 核对阈值与 UNKNOWN。','L454–506、L656–700，模拟确认、拒绝及启用条件。'],
'sweagent':['RetryAgent.run L390–437，每次候选与最终选取的轨迹。','ScoreRetryLoop L590–654，接受数和剩余预算控制。'],
'goose':['schedule_recipe、execute_job L845–913、pause_schedule、kill_running_job。','GooseToolApproval.check L31–99，按请求 ID 处理检查器决策。'],
'aider':['run_one L924–944；编辑后 lint、自动测试与询问 L1599–1623。','raw_cmd_undo L560–634，历史及脏文件检查。','v0.86.0 的 /undo 展示变更及旧版撤销修复。'],
'codex':['request_approval_with_user_prompt L576–625；record_resolution 的决策来源。','required_model、approval_review_contributor 等自动评审测试案例；未执行。'],
'gemini':['PolicyEngine.check L771 之后匹配规则与附加检查，L1118–1119 非交互降级。','Priority system and tiers；Admin tier 数字在同页前后不一致。'],
'cline':['checkpointCapturedUntracked L337–355；applyCheckpointToWorktree L376–416 校验基线。','Compare、Restore Files、Restore Task Only 及两者同时恢复的 UI 说明。'],
'opencode':['formatBody 与 deliver L39–81：正文状态、父会话、通知 ID、未完成任务。','服务终止与显式取消的差异，见 run 的 onInterrupt 路径。'],
'claude':['L640–736，can_use_tool、上下文和响应；L1099–1106，输入管道保护。','DeferredToolUse、HookMatcher.on_failure 及权限返回类型。','0.2.177 加入 on_failure；0.1.74 明确 can_use_tool 只在 ask 触发。'],
'langgraph':['interrupt L913–1053，节点重放、检查点、响应验证与中断顺序。','PregelLoop 对待处理写入、恢复的配置与 interrupt 的调度。'],
'mini':['run/query/execute_actions L88–157，异常费用、终止、观察与保存。','LocalEnvironment.execute 以及 _run 超时后结束进程组的实现。']}
ex=HERE/'raw/codex/openai-harness-20260211/web-excerpt.json'
if ex.exists() and not any('web-excerpt' in i['path'] for i in refs['codex']):
 refs['codex'].append(dict(url='https://openai.com/index/harness-engineering/',download_url='https://openai.com/index/harness-engineering/',path=ex.relative_to(project).as_posix(),date='2026-02-11',sha256=hashlib.sha256(ex.read_bytes()).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),kind='report',detail='官方单团队实践，来自 web 工具的页面摘录，非全文快照；只支持具体流程。'))
for r in refs['claude']:
 if r['kind']=='release':
  e=next(e for e in E.fromstring((project/r['path']).read_bytes()).findall('{*}entry') if e.findtext('{*}title')=='v0.2.177')
  r.update(url=e.find('{*}link').attrib['href'],date=e.findtext('{*}updated')[:10],detail=e.findtext('{*}title'))
cases=[]
for line in (HERE/'notes.txt').read_text('utf-8-sig').splitlines():
 cells=line.split('|')
 if len(cells)==5:
  k,id,name,category,platform=cells;c=dict(id=id,name=name,category=category,platform=platform.strip(),sources=[]);cases.append(c)
  c['evidence']='静态源码、独立的版本记录；仅 E10 有本地运行时实验。'
  j=0
  for r in refs[k]:
   if '/blob/' in r['url']:
    name=Path(r['path']).name
    if name=='README.md':
     r.update(kind='documentation',detail='仓库 README 定位产品用途、平台和入口。')
    else:
     if name in ('HISTORY.md','CHANGELOG.md'):kind='changelog'
     elif name.endswith(('.md','.mdx')):kind='documentation'
     elif '/tests/' in r['url']:kind='upstream-test'
     else:kind='source'
     r.update(kind=kind,detail=details[k][j]);j+=1
   elif r['kind']=='release':
    entries=E.fromstring((project/r['path']).read_bytes()).findall('{*}entry')
    entry=next(e for e in entries if e.find('{*}link').attrib['href']==r['url'])
    r['detail']='官方 GitHub Releases Atom 内的条目 '+entry.findtext('{*}title')+'；date 为该条目 updated 的 UTC 日期。'
   elif r['url']=='https://arxiv.org/abs/2511.03690':r.update(date='2026-04-22',detail='论文摘要与版本历史：v1 为 2025-11-05，核对的是 2026-04-22 v2。')
   elif r['url']=='https://arxiv.org/abs/2405.15793':r.update(date='2024-11-11',detail='论文摘要、ACI 方法和版本历史：v1 为 2024-05-06，当前为 2024-11-11 v3，未重跑论文实验。')
   elif 'agent_improvement_loop' in r['url']:r.update(date='2026-05-12')
   c['sources'].append(r)
 elif line.strip():c[cells[0]]=cells[1]
assert len(cases)==11
for c in cases:
 for k in 'scenario mechanism human org limits change insight experiment'.split():assert c[k],(c,k)
 for r in c['sources']:assert hashlib.sha256((project/r['path']).read_bytes()).hexdigest()==r['sha256']
(HERE/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),'utf8')
(HERE/'sources.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),'utf8')
print(len(cases),sum(len(c['sources']) for c in cases))
