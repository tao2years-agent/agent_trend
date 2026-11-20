from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
from bs4 import BeautifulSoup
import re,requests,json
ROOT=Path(__file__).resolve().parent; BASE=ROOT.parent.parent
sources={
'M01':[('plan','https://docs.factory.com/missions/planning.md'),('run','https://docs.factory.com/missions/running-cli.md'),('log','https://docs.factory.com/changelog/release-notes.md')],
'M02':[('launch','https://devin.ai/blog/introducing-devin-bots'),('bot','https://docs.devin.ai/work-with-devin/bots.md'),('access','https://docs.devin.ai/work-with-devin/bots/access-and-security.md'),('log','https://docs.devin.ai/release-notes/2026.md')],
'M03':[('log','https://jules.google/docs/changelog/'),('schedule','https://jules.google/docs/scheduled-tasks/'),('plan','https://jules.google/docs/review-plan/')],
'M04':[('automations','https://docs.gitlab.com/user/duo_agent_platform/automations/'),('new','https://about.gitlab.com/blog/gitlab-scheduled-automations/'),('triggers','https://docs.gitlab.com/user/duo_agent_platform/triggers/'),('flow','https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/'),('sessions','https://docs.gitlab.com/user/duo_agent_platform/sessions/'),('log','https://about.gitlab.com/press/releases/2026-07-16-gitlab-19-2-brings-governed-agentic-automation/'),('catalog','https://docs.gitlab.com/user/duo_agent_platform/flows/')],
'M05':[('checks','https://docs.coderabbit.ai/pr-reviews/pre-merge-checks'),('custom','https://docs.coderabbit.ai/pr-reviews/custom-checks'),('log','https://www.coderabbit.ai/blog/pre-merge-checks-built-in-and-custom-pr-enforced')],
'M06':[('home','https://graphite.com/'),('queue','https://graphite.com/docs/merge-queue-optimizations.md'),('setup','https://graphite.com/docs/set-up-merge-queue.md'),('status','https://status.graphite.com/history/1'),('log','https://cursor.com/blog/graphite')],
'M07':[('review','https://antigravity.google/docs/artifact-review'),('artifacts','https://antigravity.google/docs/artifacts'),('log','https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/')]
}
def ingest(entry):
 id,key,url=entry
 for trust in (True,False,True,False):
  try:
   session=requests.Session();session.trust_env=trust;r=session.get(url,timeout=14);r.raise_for_status();break
  except requests.RequestException as e: ex=e
 else: print('FAIL',id,key,str(ex)[:180]);return
 h=sha256(r.content).hexdigest()
 ishtml='text/html' in r.headers.get('Content-Type','') or '<html' in r.text[:250].lower()
 path=ROOT/'raw'/id/(h[:12]+'-'+key+('.html' if ishtml else '.md'));path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():path.write_bytes(r.content)
 rec=dict(id=id,key=key,url=url,resolved_url=r.url,path=path.relative_to(BASE).as_posix(),bytes=len(r.content),sha256=h,retrieved=datetime.now(timezone.utc).isoformat())
 print(id,key,len(r.content),r.url,flush=True)
 return rec
def extract(s):
 p=BASE/s['path']
 if p.suffix!='.html':return p.read_text(encoding='utf-8-sig')
 doc=BeautifulSoup(p.read_bytes(),'html.parser'); node=doc.find('main') or doc.find('article') or doc;return '\n'.join(ln.strip() for ln in node.get_text('\n',strip=True).splitlines() if ln.strip())
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=12) as ex: rows=list(ex.map(ingest,[(id,k,url) for id,records in sources.items() for k,url in records]))
 assert all(rows);(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')



