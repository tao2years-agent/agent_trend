from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
here=Path(__file__).resolve().parent;root=here.parents[1]
refs=json.loads((here/'sources.json').read_text('utf8'))
d={
'symphony':['SPEC 核对调度边界、并发、重复尝试与独立工作目录。','maybe_dispatch、reconcile_issue_state、handle_info retry token。','样例的 Human Review、Merging 与 Rework 约定。','v0.0.3 的认证与发行更新；Atom 条目 updated UTC 日期。'],
'ghaw':['process_safe_outputs 调用独立 manager 并避免将 handler stdout/stderr 打包。','2026-10-14 Proposed ADR，对照 staged 权限和私有仓库过滤器。','早期 changeset 对 staged 不配置写权限的预期。','2026-10-28 正式 GA，默认权限、运行器和预算预测。','2026-02-13 技术预览说明，追溯只读及 safe outputs。','safe_output_handler_manager 的 effectiveAuthorization、授权规则选择、batchDigest、stagedFor 与按类型 dispatch。'],
'tessl':['Prove a skill works using evaluation；baseline、variant、plugin 根路径和场景。','2026-10-30 周更中 Skill activation for more agents；区分加载与完成。','2026-02-17 Task Evals 发布说明及当时 repo evals 的阶段。'],
'routines':['现行 Scheduled tasks 文档，核对旧名、触发、个人归属、权限与暂停。','2026-04-14 产品发布页，核对历史命名和发行时间。'],
'sandbox':['OpenSandbox 仓库用途、平台及后端。','evaluate_idle 所有条件分支与未知状态的 tombstone 意义。','v1.2.0+、Fast Sandbox、网关流量和 Redis 前置条件、唤醒超时。','1.3.0-rc.2 发布记录，续期与删除竞争及正常退出的状态问题。']}
for k,ls in d.items():
 for v,desc in zip(refs[k],ls):v['detail']=desc
p=here/'raw/symphony/report-20260427/web-excerpt.json';url='https://openai.com/index/open-source-codex-orchestration-symphony/'
if not any(v['url']==url for v in refs['symphony']):
 refs['symphony'].append(dict(url=url,download_url=url,kind='report',path=p.relative_to(root).as_posix(),date='2026-04-27',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat(),detail='厂商内部实践与公开规范的网页摘录；非完整页面。'))
out=[]
for line in (here/'notes.txt').read_text('utf-8-sig').splitlines():
 row=line.split('|')
 if len(row)==5:
  k,id,name,cat,plat=row;c=dict(id=id,name=name,category=cat,platform=plat,sources=refs[k]);out.append(c)
 else:c[row[0]]=row[1]
for case in out:
 for f in 'scenario mechanism human org limits change insight experiment'.split():assert case[f]
 for i in case['sources']:assert i['detail'] and hashlib.sha256((root/i['path']).read_bytes()).hexdigest()==i['sha256']
(here/'cases.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
(here/'sources.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),'utf8')
print('verified',len(out),sum(len(c['sources'])for c in out))
