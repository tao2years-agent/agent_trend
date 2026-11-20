from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,hashlib,os,subprocess,requests,time
P=Path(__file__).resolve().parent
sources={
 'meta':('stanford-iris-lab/meta-harness','f805ad3aa4ada290458c1e0deadbe132fbbdea4e','metaopt',[
 'README.md','reference_examples/terminal_bench_2/meta_harness.py','reference_examples/terminal_bench_2/README.md','reference_examples/terminal_bench_2/claude_wrapper.py','reference_examples/terminal_bench_2/.claude/skills/meta-harness-terminal-bench-2/SKILL.md',
 'reference_examples/text_classification/meta_harness.py','reference_examples/text_classification/config.yaml',
 'experimental/harbor_meta_harness/controller.py','experimental/harbor_meta_harness/README.md','experimental/harbor_meta_harness/tests/test_controller.py','experimental/harbor_meta_harness/suites/tb2-easy.toml']),
 'ahe':('china-qijizhifeng/agentic-harness-engineering','182ea06e578df7b1d503eca537503c1e4c5a8a58','aheopt',[
 'README.md','evolve.py','configs/base.yaml','configs/experiments/exp-simple-code-gpt54.yaml','configs/experiments/exp-simple-code-gpt54-new-adb.yaml','agents/evolve_agent/evolve_prompt.md','skills/agentic-harness-engineering/references/docs/rollback-strategy.md','skills/agentic-harness-engineering/scripts/verify_manifest.py','scripts/evolve-resume.sh','skills/agentic-harness-engineering/scripts/validate_harness.py'])}
def get_one(pair):
 k,n=pair;repo,sha,cache,_=sources[k];url=f'https://raw.githubusercontent.com/{repo}/{sha}/{n}'
 for attempt in range(5):
  try:
   with requests.Session()as s:
    s.trust_env=bool(attempt%2);r=s.get(url,timeout=15);r.raise_for_status();b=r.content
   break
  except Exception:
   if attempt==4:raise
 f=P/'raw'/k/sha/n;f.parent.mkdir(parents=True,exist_ok=True)
 if f.exists():assert f.read_bytes()==b
 else:f.write_bytes(b)
 g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 cache=Path(os.environ.get('TEMP','/tmp'))/'eng-research-20261120'/cache
 if (cache/'.git').is_dir():
  assert subprocess.check_output(['git','-C',str(cache),'rev-parse',f'{sha}:{n}']).decode().strip()==g
 return dict(case=k,path=f.relative_to(P).as_posix(),url=f'https://github.com/{repo}/blob/{sha}/{n}',download_url=url,commit=sha,git_blob=g,sha256=hashlib.sha256(b).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat())
if __name__=='__main__':
 with ThreadPoolExecutor(8) as ex:rows=list(ex.map(get_one,[(k,n)for k,v in sources.items()for n in v[3]]))
 (P/'sources.json').write_text(json.dumps(rows,indent=2),'utf8');print('verified',len(rows))
