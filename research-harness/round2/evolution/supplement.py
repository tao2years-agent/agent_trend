from pathlib import Path
import concurrent.futures,json
from ingest import R,B,save,old,registry
targets=[('pr-project-config','https://github.com/The-PR-Agent/pr-agent/pull/2463.diff'),('argo-abort','https://github.com/argoproj/argo-rollouts/pull/4919.diff'),('pr-unused','https://github.com/The-PR-Agent/pr-agent/pull/4598.diff'),('atlantis-policy','https://github.com/runatlantis/atlantis/pull/6271.diff')]
reuse=[('src-cloud-office','https://sourcegraph.com/changelog/2026-11-09','round2/workflows/sources.json'),('src-preview','https://raw.githubusercontent.com/sourcegraph/src-cli/f2901d14d2db58c4f25d0f73736805e01b14f502/cmd/src/batch_preview.go','round2/workflows/sources.json'),('src-apply','https://raw.githubusercontent.com/sourcegraph/src-cli/f2901d14d2db58c4f25d0f73736805e01b14f502/cmd/src/batch_apply.go','round2/workflows/sources.json'),('jules-plan','https://jules.google/docs/review-plan/','lanes/managed/manifest.json'),('devin-access','https://docs.devin.ai/work-with-devin/bots/access-and-security.md','lanes/managed/manifest.json')]
primary_pr=[('pr-5098','https://github.com/argoproj/argo-rollouts/pull/5098.diff'),('pr-6533','https://github.com/runatlantis/atlantis/pull/6533.diff'),('pr-3712','https://github.com/The-PR-Agent/pr-agent/pull/3712.diff'),('pr-1381','https://github.com/sourcegraph/src-cli/pull/1381.diff')]
def fetch(pair):
 key,url=pair;d,s=save(url,'diff',key);print(key,len(d),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:list(e.map(fetch,primary_pr))
 (R/'diff-sources.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False),encoding='utf-8')
 registry.clear()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(fetch,targets))
 for k,u,f in reuse:old(k,u,f)
 (R/'supplement-sources.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False),encoding='utf-8')
