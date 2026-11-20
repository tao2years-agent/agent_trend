from pathlib import Path
import os,subprocess,tempfile,concurrent.futures,time,json
R=Path(__file__).resolve().parent
repos={
'GITLAB':'https://gitlab.com/gitlab-org/modelops/applied-ml/code-suggestions/ai-assist.git',
'SEER':'https://github.com/getsentry/seer.git','SENTRY':'https://github.com/getsentry/sentry.git','SONAR':'https://github.com/SonarSource/sonarqube.git',
'AIDER':'https://github.com/Aider-AI/aider.git','ARGO':'https://github.com/argoproj/argo-rollouts.git','REN':'https://github.com/renovatebot/renovate.git',
'MOD':'https://github.com/openrewrite/rewrite.git','TRAE':'https://github.com/bytedance/trae-agent.git',
'MERGIFY':'https://github.com/Mergifyio/mergify.git','SNYK':'https://github.com/snyk/cli.git','SPACE':'https://github.com/spacelift-io/terraform-provider-spacelift.git',
'LAUNCH':'https://github.com/launchdarkly/go-server-sdk.git','INC':'https://github.com/incident-io/terraform-provider-incident.git','ROOTLY':'https://github.com/rootlyhq/terraform-provider-rootly.git','DD':'https://github.com/DataDog/terraform-provider-datadog.git','GOOSE':'https://github.com/aaif-goose/goose.git'}
repos.update({'GHSDK': 'https://github.com/github/copilot-sdk.git', 'CODEBUDDY': 'https://github.com/TencentCloudBase/CloudBase-AI-ToolKit.git', 'DEVIN': 'https://github.com/CognitionAI/plugin-template.git', 'CLAUDE': 'https://github.com/anthropics/claude-code.git', 'FACTORY': 'https://github.com/Factory-AI/factory-plugins.git', 'CIRCLE': 'https://github.com/CircleCI-Public/circleci-cli.git'})
repos.update({k:'https://github.com/'+v+'.git' for k,v in {'AWSEX':'aws-samples/aws-transform-custom-samples','QODEREX':'QoderAI/qoder-agent-sdk-samples','CBEX':'coderabbitai/skills','ADK':'google/adk-python','ALI':'aliyun/alibabacloud-devops-mcp-server'}.items()})
def cap(k,item):
 ix=R/(k+'-index.json')
 if ix.exists():return
 env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='Never')
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
  def git(*args):
   for i in range(3):
    p=subprocess.run(['git','-C',tmp,'-c','http.proxy=','-c','credential.helper=','-c','http.version=HTTP/1.1',*args],capture_output=True,timeout=90,env=env)
    if not p.returncode:return p.stdout
    if b'not read Username' in p.stderr or b'not found' in p.stderr:break
   raise RuntimeError(p.stderr[-280:].decode(errors='replace'))
  try:
   git('init','--bare');git('fetch','--depth=1','--filter=blob:none','--no-tags',item,'HEAD');sha=git('rev-parse','FETCH_HEAD^{commit}').decode().strip();lst=git('ls-tree','-r','--name-only',sha).decode().splitlines();d=dict(repo=item,sha=sha,paths=lst);print(k,sha[:9],len(lst),flush=True)
  except Exception as ex:
   print(k,'unavailable',str(ex)[:110],flush=True);d=dict(repo=item,error=str(ex))
  ix.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(lambda kv:cap(*kv),repos.items()))
