from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import requests,json,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent; BASE=R.parent.parent
rows=[
('P01','CircleCI Chunk','https://circleci.com/docs/guides/toolkit/chunk-setup-and-overview/','Cloud/GitHub/Beta；失败作业、任务生命周期及 PR',''),
('P02','CircleCI Chunk','https://circleci.com/changelog/chunk-fix-job-pipelines-page-job-page/','2026-02-27 发布失败作业入口和上下文传递','2026-02-27'),
('P03','incident.io','https://incident.io/blog/introducing-ai-sre','一线事故上下文、调查触发、扫描的证据和沟通结论',''),
('P04','incident.io','https://incident.io/changelog/a-faster-smarter-incident','聊天界面更重视人工已确认发现并提供精确 PR','2026-01-15'),
('P05','Rootly AI SRE','https://docs.rootly.com/ai/ai-sre/running-an-investigation','手动/自动规则与调查生命周期；自动调查的团队凭据、Private Agent 与连接器写权限',''),
('P06','Rootly AI SRE','https://docs.rootly.com/ai/ai-sre/reading-the-result','证据包、结论等级、Blocked/Inconclusive',''),
('P07','Rootly AI SRE','https://rootly.com/ai-sre-guide/ai-sre-vs-aiops','原生工具不回滚/重启；连接器是否可写见 P05',''),
('P08','Datadog Bits Investigation','https://docs.datadoghq.com/bits_ai/bits_investigation/investigate_issues/','correlated telemetry / hypothesis tree / inconclusive，调查与修复边界',''),
('P09','Datadog Bits Investigation','https://docs.datadoghq.com/bits_ai/bits_ai_sre/help_bits_learn/','调查结束后的 feedback、memory 及管理删除',''),
('P10','Sentry Seer','https://docs.sentry.io/api/seer/start-seer-issue-fix/','异步 issue fix、停止点与 PR 输出；续跑首选 sentry_run_id，旧 run_id 兼容',''),
('P11','Sentry Seer','https://docs.sentry.io/api/seer/retrieve-seer-issue-fix-state/','状态、步骤和权限、根因方案与生成的变更；experimental',''),
('P12','Moderne Platform','https://docs.moderne.io/user-documentation/moderne-platform/getting-started/running-your-first-recipe/','按组织/recipe dry run、逐仓 diff、提交/PR',''),
('P13','Moderne Platform','https://docs.moderne.io/releases/saas-v2-changes/','SaaS v2 的 fast/slow lanes 与可选跨仓活动视图',''),
('P14','AWS Transform custom','https://docs.aws.amazon.com/transform/latest/userguide/custom.html','transformation definition、registry、验证命令、学习管理',''),
('P15','AWS Transform custom','https://aws.amazon.com/about-aws/whats-new/2025/12/transform-custom-organization-wide-modernization/','GA 日期、CLI/流水线调用以及适用迁移类别','2025-12-01'),
('P16','SonarQube Server','https://docs.sonarsource.com/sonarqube-server/2025.1/analyzing-source-code/pull-request-analysis/introduction','2025.1 LTA，Developer Edition 起，CI 集成与 PR 新代码检查边界',''),
('P17','SonarQube Server','https://docs.sonarsource.com/sonarqube-server/2025.6/devops-platform-integration/github-integration/setting-up-at-project-level','2025.6 GitHub 必检与失败阻断设置',''),
('P18','LaunchDarkly Guardian','https://launchdarkly.com/docs/home/releases/errors','Enterprise Guardian、顺序检验与退化指标诊断',''),
('P19','LaunchDarkly Guardian','https://support.launchdarkly.com/hc/en-us/articles/55384223785115-FAQ-Guarded-rollouts','流量调整、暂停与自动回退限制',''),
('P20','LaunchDarkly Guardian','https://launchdarkly.com/docs/integrations/monitoring/error-events','错误指标方向、退化条件与回退设置',''),
('P21','Mergify','https://docs.mergify.com/merge-queue/','PR 与最新 main 组合、并行队列、暂停和优先级入口',''),
('P22','Mergify','https://docs.mergify.com/merge-queue/batches/','批失败的拆分、重跑、剔除与限额','')]
rows.extend([('P23', 'Spacelift', 'https://docs.spacelift.io/concepts/run/tracked', 'Tracked run 从计划走向 unconfirmed、确认后等待 worker 到 apply 等状态', ''), ('P24', 'Spacelift', 'https://docs.spacelift.io/concepts/policy/approval-policy', '审批策略，取消及丢弃，autodeploy 的前提例外', ''), ('P25', 'Snyk Open Source', 'https://github.com/snyk/user-docs/blob/main/scan-fix-and-prevent/README.md', '维护者文档：自动修复 PR 与新依赖版本升级 PR 的触发差异。', ''), ('P26', 'Snyk Open Source', 'https://snyk.io/blog/dependency-updates-mergify-snyk/', 'Snyk 产生升级 PR、并行上限、将最终整合交给 Mergify 的组合案例。', '')])
def fetch(row):
 id,name,u,loc,date=row
 for trust in [True,False,True,False]:
  try:
   a=requests.Session();a.trust_env=trust;r=a.get(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'},timeout=14);r.raise_for_status();break
  except requests.RequestException as ex:err=ex
 else:print('FAIL',id,str(err)[:150]);return
 b=r.content;h=sha256(b).hexdigest();p=R/'raw'/f'{id}-{h[:12]}.html';p.parent.mkdir(exist_ok=True)
 if not p.exists():p.write_bytes(b)
 soup=BeautifulSoup(b,'html.parser');title=soup.title.get_text(' ',strip=True) if soup.title else ''
 text=' '.join((soup.select_one('main') or soup.select_one('article') or soup).stripped_strings);print(id,len(b),len(text),title[:60],flush=True)
 return dict(id=id,product=name,url=u,resolved_url=r.url,locator=loc,event_date=date,path=p.relative_to(BASE).as_posix(),sha256=h,retrieved=datetime.now(timezone.utc).isoformat(),bytes=len(b),title=title)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=12) as ex:data=[d for d in ex.map(fetch,rows) if d]
 (R/'fresh.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
