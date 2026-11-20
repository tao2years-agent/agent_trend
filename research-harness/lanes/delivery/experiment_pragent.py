"""Run the snapshot's pure PR-Agent repository-setting predicate on benign scope examples."""
from pathlib import Path
import json, hashlib, importlib.util, sys, datetime
from fetch import ROOT,BASE
src=json.loads((ROOT/'pragent.index.json').read_text(encoding='utf-8'))
s=next(s for s in src['sources'] if s.get('repo_path')=='pr_agent/config_security.py')
p=BASE/s['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pragent_scope_check',p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=[]
for section,key,expected in [('config','enable_auto_approval',True),('config','num_retries',True),('skills','max_skills_tokens',False),('skills','enabled',False)]:
 observed=mod.is_repo_host_only_key(section,key);assert observed==expected
 rows.append(dict(section=section,key=key,expected_host_only=expected,observed_host_only=observed))
out=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),commit=src['sha'],source=s['path'],sha256=s['sha256'],entrypoint='is_repo_host_only_key',cases=rows)
dest=ROOT/'experiment/pragent-config-scope.json'
if not dest.exists():dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(rows)
