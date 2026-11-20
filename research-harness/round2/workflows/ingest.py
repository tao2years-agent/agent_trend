from pathlib import Path
import requests,json,hashlib,datetime,re,csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
new=[
('W01','Factory','https://docs.factory.com/workstreams/automations.md','Where runs go and where they run；暂停、运行历史及事件。',''),
('W02','Factory','https://docs.factory.com/droid-cli/cli-reference.md','CreateAutomation 的首次运行、投递到已有会话及服务身份。',''),
('W03','Devin','https://docs.devin.ai/product-guides/automations.md','Who automations run as、Schedule、权限及隐私。',''),
('W04','Devin','https://docs.devin.ai/product-guides/scheduled-sessions.md','Legacy schedules 与新建 automation 的区分。',''),
('W05','Antigravity','https://antigravity.google/docs/commands/automation','后台新会话无上次记忆，建立后暂停，采集权限及无人值守自动拒绝。',''),
('W06','Copilot','https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-automations','适用仓库、创建者权限、动作、事件、审核或暂停。',''),
('W07','Copilot','https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/copilot-surfaces/copilot-on-github','cloud agent 仓库与分支/PR 边界，读取上下文和写权限分别说明。',''),
('W08','Copilot','https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/','上线时的适用仓库范围、触发和工具配置。','2026-06-02'),
('W09','Sourcegraph','https://sourcegraph.com/docs/batch-changes/faq','重跑 spec 后的变化、移出范围、归档与只读 changeset。',''),
('W10','Sourcegraph','https://sourcegraph.com/docs/admin/config/batch-changes','Rollout windows 的节流范围；批量 merge 不受窗口限制。',''),
('W11','Sourcegraph','https://sourcegraph.com/changelog/2026-11-09','在对话中确认 merge、移交线程与身份、权限和空闲条件。','2026-11-09'),
('W12','Sourcegraph','https://sourcegraph.com/changelog/agentic-batch-changes-workspace-continuation','后台执行期间可继续聊天、单独调查失败以及当时 Cloud-only 限制。','2026-11-02'),
('W13','Sourcegraph','https://sourcegraph.com/pricing','Enterprise 方案包含 Batch Changes；普通 Batch Changes 不等于每项 Agentic 能力都可用于同一部署。',''),
('W14','Sourcegraph','https://sourcegraph.com/docs/agentic-batch-changes/configuration','功能权限、访问控制、审计和部署要求。',''),
('W15','Graphite','https://graphite.com/docs/get-started-merge-queue.md','入队与失败路径、如何移出队列。',''),
('W16','CodeRabbit','https://kb.coderabbit.ai/articles/1442026547-troubleshoot-why-coderabbit-reviews-might-not-trigger','按条件排查评审未启动，手动触发增量/完整评审。',''),
('W17','GitLab','https://docs.gitlab.com/user/duo_agent_platform/composite_identity/','源用户、服务账号、成员关系与动态权限边界。',''),
('W21','Copilot','https://github.blog/changelog/2026-10-28-work-from-anywhere-with-a-new-connected-copilot-cloud-experience/','cloud sandbox 从预览到 GA、跨入口的会话连续性。','2026-10-28'),
('W18','Jules','https://jules.google/docs/changelog/2026-10-29','独立的只读与退场公告、导出范围。','2026-10-29')]
def request(url):
 for trust in [True,False,True,False]:
  try:
   a=requests.Session();a.trust_env=trust;r=a.get(url,timeout=16);r.raise_for_status();return r
  except requests.RequestException as e:err=e
 raise err
def ingest(row):
 id,product,u,loc,dt=row
 try:
  r=request(u); raw=r.content; digest=hashlib.sha256(raw).hexdigest(); suf='.html' if 'text/html' in r.headers.get('Content-Type','') else ('.xml' if '<feed' in r.text[:220] else '.md')
  if u.endswith('.go'):suf='.go'
  p=ROOT/'raw'/(id+'-'+digest[:12]+suf);p.parent.mkdir(exist_ok=True)
  if not p.exists():p.write_bytes(raw)
  print(id,r.status_code,r.url,len(raw),flush=True)
  return dict(id=id,product=product,url=u,resolved_url=r.url,locator=loc,event_date=dt,path=p.relative_to(BASE).as_posix(),sha256=digest,bytes=len(raw),retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat(),origin='R2')
 except Exception as ex: print(id,'FAIL',str(ex)[:190],flush=True);return None
def readable(s):
 p=BASE/s['path'];t=p.read_text(encoding='utf-8-sig',errors='replace')
 if p.suffix!='.html':return t
 b=BeautifulSoup(t,'html.parser');sel=b.select_one('main') or b.select_one('article') or b
 return '\n'.join(l for l in sel.stripped_strings)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=12) as ex: data=[s for s in ex.map(ingest,new) if s]
 feed=ingest(('W19','Sourcegraph','https://github.com/sourcegraph/src-cli/commits/main.atom','官方 CLI 的提交列表，用以固定基线版本。',''))
 if feed:
  ns={'a':'http://www.w3.org/2005/Atom'}; entries=ET.parse(BASE/feed['path']).getroot().findall('a:entry',ns)
  head=next(e for e in entries if e.findtext('a:updated','',ns)<='2026-11-20T16:00:00Z');sha=head.findtext('a:id','',ns).split('/')[-1];data.append(feed);s=ingest(('W20','Sourcegraph','https://raw.githubusercontent.com/sourcegraph/src-cli/'+sha+'/cmd/src/batch_apply.go','固定提交的 CLI applyCommand 调用点；不代表 Agentic Cloud 后端源码。',head.findtext('a:updated','',ns)[:10]));data.append(s)
  for evidence_id,filename,locator in [('W22','batch_preview.go','CLI preview 入口把 applyBatchSpec 设置为 false。'),('W23','batch_common.go','共用执行路径按 applyBatchSpec 标志选择返回或应用。')]:
   data.append(ingest((evidence_id,'Sourcegraph','https://raw.githubusercontent.com/sourcegraph/src-cli/'+sha+'/cmd/src/'+filename,locator,head.findtext('a:updated','',ns)[:10])))
 assert len(data)==23 and all(data)
 (ROOT/'fresh.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

