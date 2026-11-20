from pathlib import Path
import requests,json,hashlib,datetime,concurrent.futures,time,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
locks=json.loads((R/'repository-locks.json').read_text())
targets=[('JUL','https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/','2025-07-10'),('FEB','https://metr.org/blog/2026-02-24-uplift-update/','2026-02-24'),('VERS','https://arxiv.org/abs/2507.09089','2025-07-25'),('PAPER','https://arxiv.org/html/2507.09089v2','2025-07-25'),('INDEX','https://metr.org/research/','')]
for k,v in locks.items():
 for path in v['files']:targets.append((k+'-'+path,'https://raw.githubusercontent.com/'+v['repo']+'/'+v['sha']+'/'+path,v['date']))
extras=R/'extra-targets.json'
if extras.is_file():targets.extend(json.loads(extras.read_text(encoding='utf8')))
def one(row):
 k,url,date=row
 if (R/'sources.json').exists():
  for d in json.loads((R/'sources.json').read_text(encoding='utf8')):
   if d['id']==k:return d
 for i in range(3):
  try:
   s=requests.Session();s.trust_env=False;res=s.get(url,timeout=(8,30),headers={'User-Agent':'Mozilla/5.0'});res.raise_for_status();raw=res.content;assert len(raw)>100;break
  except Exception as e:
   if i==2:print('ERROR',k,str(e),flush=True);return
   time.sleep(1)
 h=hashlib.sha256(raw).hexdigest();ext=Path(k).suffix or ('.pdf' if raw.startswith(b'%PDF') else '.html')
 file=R/'raw'/(k+'-'+h[:12]+ext)
 if not file.is_file():file.write_bytes(raw)
 textpath=''
 if ext=='.html':
  soup=BeautifulSoup(raw,'html.parser')
  for tag in soup.find_all(['script','style','nav','header','footer','svg']):tag.decompose()
  root=soup.find('article') or soup.find('main') or soup
  plain=file.with_suffix('.txt');plain.write_text('\n'.join(root.stripped_strings),encoding='utf8');textpath=plain.relative_to(R).as_posix()
 print(k,len(raw),flush=True)
 return dict(id=k,url=res.url,path=file.relative_to(R).as_posix(),text=textpath,sha256=h,source_date=date,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as e:d=[a for a in e.map(one,targets) if a]
(R/'sources.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
