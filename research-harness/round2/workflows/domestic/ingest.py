from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor
import requests,json,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent; BASE=ROOT.parents[2]
rows=[
('CN21','Qoder','https://docs.qoder.com/qoder/plan-driven','新版 Qoder 可审计划执行流、计划变更与确认。',''),
('CN22','Qoder','https://docs.qoder.com/qoder/review-and-commit','新版 Qoder review/commit/push 及代码提交范围。',''),
('CN01','Qoder','https://docs.qoder.com/release-notes/quest-retirement-notice','Quest 下线、滚动关闭、Editor 保留、导入与手机重连','2026-10-15'),
('CN02','Qoder','https://docs.qoder.com/zh/user-guide/quest/overview','旧 Quest 的 diff、拒绝单文件、push 与创建 PR',''),
('CN03','Qoder','https://docs.qoder.com/user-guide/quest/task-management','旧 Quest 任务暂停与继续、分支管理',''),
('CN04','Qoder','https://docs.qoder.com/qoder/approval-and-sandbox','新 Qoder 权限预设，工作区内改写与其它操作的差别',''),
('CN05','腾讯 CodeBuddy Code','https://www.codebuddy.cn/docs/cli/agent-teams','领导、成员、计划批准、任务依赖、关停和已知限制',''),
('CN06','腾讯 CodeBuddy Code','https://www.codebuddy.cn/docs/cli/release-notes/v2.95.0','v2.95.0 Plan 审批和关停握手与默认超时',''),
('CN07','腾讯 CodeBuddy Code','https://www.codebuddy.cn/docs/cli/release-notes/v2.140.0','v2.140.0 的团队停止作用域修复',''),
('CN08','腾讯 CodeBuddy Code','https://www.codebuddy.cn/docs/cli/gitlab-ci-cd','GitLab CI 触发、凭据、MR 交付和分支保护',''),
('CN09','华为云码道','https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0005.html','IDE 规范开发模式、spec 与文件差异和运行策略',''),
('CN10','华为云码道','https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0070.html','/goal 限制、暂停当前迭代、验证语义',''),
('CN11','华为云码道','https://support.huaweicloud.com/bestpractice-codeartsagent/codeartsagent_bp_0019.html','CodeArts Repo 创建 MR、Committer 审核合入示例',''),
('CN12','华为云码道','https://support.huaweicloud.com/usermanual-codeartsmobile/mobile_0009.html','小程序退出而云端继续、跨端任务可见性',''),
('CN13','华为云码道','https://support.huaweicloud.com/usermanual-enterprise/codeartsagent_enterprise_0000.html','控制台企业套餐成员管控与资源',''),
('CN14','阿里云云效','https://help.aliyun.com/zh/yunxiao/user-guide/ai-intelligent-code-review','触发方式、评审报告、评审记忆与权限',''),
('CN15','阿里云云效','https://help.aliyun.com/zh/yunxiao/user-guide/using-merge-requests','评论、人工表态，以及自动化检查卡点',''),
('CN16','阿里云云效','https://help.aliyun.com/zh/yunxiao/user-guide/using-the-code-detection-service','门禁阈值与保护分支的双重设置',''),
('CN17','TRAE','https://docs.trae.cn/work_changelog','2026-06-09 SOLO 升级为 TraeWork，桌面及网页、企业账号','2026-06-09'),
('CN18','TRAE','https://docs.trae.cn/work_traework-to-traecode-data-migration','TraeWork 与 TraeCode 融合升级至 TRAE、历史迁移',''),
('CN19','TRAE','https://docs.trae.cn/ide_handoff?lang=zh','接续的在途限制、检查和重试、GitHub 权限，未自动回退',''),
('CN20','TRAE','https://docs.trae.cn/enterprise_github-integration','企业 TraeWork GitHub 连接与断开，支持界面及专属域名限制','')]
def fetch(row):
 id,prod,url,loc,date=row
 for trust in (True,False,True,False):
  try:
   s=requests.Session();s.trust_env=trust;r=s.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36','Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8'},timeout=14);r.raise_for_status(); assert b'Security Verification</title>' not in r.content; break
  except (requests.RequestException,AssertionError) as e:err=e
 else: print('FAIL',id,str(err)[:140]);return
 blob=r.content;h=sha256(blob).hexdigest();p=ROOT/'raw'/f'{id}-{h[:12]}.html';p.parent.mkdir(exist_ok=True)
 if not p.exists():p.write_bytes(blob)
 doc=BeautifulSoup(blob,'html.parser');title=doc.title.get_text(' ',strip=True) if doc.title else '';txt=(doc.select_one('main') or doc.select_one('article') or doc).get_text(' ',strip=True)
 print(id,len(blob),len(txt),title[:50],flush=True)
 return dict(id=id,product=prod,url=url,resolved_url=r.url,locator=loc,event_date=date,retrieved=datetime.now(timezone.utc).isoformat(),sha256=h,bytes=len(blob),path=p.relative_to(BASE).as_posix(),title=title)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=10) as ex:data=[s for s in ex.map(fetch,rows) if s]
 (ROOT/'sources.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


