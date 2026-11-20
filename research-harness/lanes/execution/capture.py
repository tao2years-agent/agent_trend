import os, subprocess, pathlib as P, json, hashlib, concurrent.futures as CF, time
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
import requests
HERE=P.Path(__file__).resolve().parent
CACHE=P.Path(os.environ.get("TEMP","."))/"eng-research-20261120"
SETTINGS={
 "openhands":("OpenHands/software-agent-sdk",0,["openhands-sdk/openhands/sdk/security/confirmation_policy.py","tests/sdk/conversation/local/test_confirmation_mode.py"]),
 "sweagent":("SWE-agent/SWE-agent",2,["sweagent/agent/agents.py","sweagent/agent/reviewer.py"]),
 "goose":("aaif-goose/goose",6,["crates/goose/src/scheduler/full.rs","crates/goose/src/agents/state_machine/tool_approval.rs"]),
 "aider":("Aider-AI/aider",5,["aider/coders/base_coder.py","aider/commands.py","HISTORY.md"]),
 "codex":("openai/codex",2,["codex-rs/core/src/tools/approvals.rs","codex-rs/core/tests/suite/auto_review.rs"]),
 "gemini":("google-gemini/gemini-cli",2,["packages/core/src/policy/policy-engine.ts","docs/reference/policy-engine.md"]),
 "cline":("cline/cline",5,["sdk/packages/core/src/session/checkpoint-restore.ts","docs/core-workflows/checkpoints.mdx"]),
 "opencode":("anomalyco/opencode",4,["packages/core/src/session/subagent-completion.ts","packages/core/src/session/subagent-job.ts"]),
 "claude":("anthropics/claude-agent-sdk-python",6,["src/claude_agent_sdk/_internal/query.py","src/claude_agent_sdk/types.py","CHANGELOG.md"]),
 "langgraph":("langchain-ai/langgraph",0,["libs/langgraph/langgraph/types.py","libs/langgraph/langgraph/pregel/_loop.py"]),
 "mini":("SWE-agent/mini-swe-agent",0,["src/minisweagent/agents/default.py","src/minisweagent/environments/local.py"])
}
def request(url):
 for attempt in range(6):
  try:
   with requests.Session() as sess:
    sess.trust_env=False
    r=sess.get(url,timeout=25); r.raise_for_status();return r.content
  except requests.RequestException:
   if attempt==5:raise
   time.sleep(attempt+0.3)
def store(k,tag,filename,data):
 p=HERE/"raw"/k/tag/filename
 p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():
  assert p.read_bytes()==data,p
 else:p.write_bytes(data)
 return p.relative_to(HERE.parents[1]).as_posix()
def collect(item):
 k,(repo,idx,files)=item; cache=CACHE/k
 def git(*args):return subprocess.check_output(['git','-C',str(cache),*args]).decode().strip()
 sha=git('rev-parse','HEAD')
 date=git('log','-1','--format=%cI')
 records=[]
 for fname in ["README.md",*files]:
  url=f'https://raw.githubusercontent.com/{repo}/{sha}/{fname}'
  gid=git('rev-parse',f'{sha}:{fname}')
  data=request(url)
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==gid
  dst=store(k,sha,fname,data)
  records.append(dict(url=f'https://github.com/{repo}/blob/{sha}/{fname}',download_url=url,path=dst,date=date[:10],sha256=hashlib.sha256(data).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat(),kind='source' if fname!='README.md' else 'documentation'))
 atom=(CACHE/(k+'.atom')).read_bytes()
 e=ET.fromstring(atom).findall('{*}entry')[idx]
 href=e.find('{*}link').attrib['href']; updated=e.findtext('{*}updated')
 dst=store(k,hashlib.sha256(atom).hexdigest()[:16],"releases.atom",atom)
 records.append(dict(url=href,download_url=f'https://github.com/{repo}/releases.atom',path=dst,date=updated[:10],sha256=hashlib.sha256(atom).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat(),kind='release',detail=e.findtext('{*}title')))
 print(k,len(records),flush=True)
 return k, records
if __name__=='__main__':
 if (HERE/'sources.json').exists():
  meta=json.loads((HERE/'sources.json').read_text('utf8'))
  for items in meta.values():
   for item in items:
    p=HERE.parents[1]/item['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
  print('All local snapshots verified')
 else:
  with CF.ThreadPoolExecutor(7) as ex: rows=dict(ex.map(collect,SETTINGS.items()))
  (HERE/'sources.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
