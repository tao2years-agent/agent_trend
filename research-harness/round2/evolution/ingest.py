from pathlib import Path
import requests,hashlib,json,time,re,datetime,concurrent.futures,threading,os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
R=Path(__file__).resolve().parent;B=R.parent.parent;(R/'raw').mkdir(exist_ok=True)
START='2026-05-01';END='2026-11-20'
repo={'Argo Rollouts':'argoproj/argo-rollouts','Atlantis':'runatlantis/atlantis','PR-Agent':'The-PR-Agent/pr-agent','Sourcegraph src-cli':'sourcegraph/src-cli'}
registry=[];lock=threading.Lock()
def save(url,kind,id):
 for source_file in ('archive.json','diff-sources.json','supplement-sources.json'):
  if not (R/source_file).exists():continue
  known=json.loads((R/source_file).read_text(encoding='utf-8'))
  for rec in known:
   if rec['url']==url:
    raw=(B/rec['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==rec['sha256']
    with lock:registry.append(rec)
    return raw,rec['id']
 ss=requests.Session();ss.trust_env=False
 for i in range(5):
  try:
   resp=ss.get(url,timeout=(7,25));resp.raise_for_status();break
  except requests.RequestException:
   if i==4:raise
   time.sleep(i+1)
 raw=resp.content;dig=hashlib.sha256(raw).hexdigest();p=R/'raw'/(id+'-'+dig[:14]+'.'+kind);p.write_bytes(raw) if not p.exists() else None
 rec=dict(id=id,url=url,resolved=resp.url,path=p.relative_to(B).as_posix(),sha256=dig,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
 with lock:registry.append(rec)
 return raw,id
def old(e,url,registry_path):
 meta=json.loads((B/registry_path).read_text(encoding='utf-8'));s=next(m for m in meta if m['url']==url);p=B/s['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];registry.append(dict(s,id=e));return p.read_bytes(),e
def dated(raw):return datetime.datetime.strptime(raw,'%B %d, %Y').date().isoformat()
def releases(kv):
 name,repos=kv;slug=repos.split('/')[-1];url='https://github.com/'+repos+'/releases';data={};pages=[]
 for no in range(1,30):
  raw,sid=save(url,'html',slug+'-'+str(no));pages.append(sid);p=BeautifulSoup(raw,'html.parser');sec=p.select('section[data-release-anchor]');assert sec,(name,no)
  for a in sec:
   tag=a.get('data-release-anchor')[8:];dt=a.select_one('relative-time')['datetime'][:10];body=a.select_one('.markdown-body');tar=a.select_one('a[href*="/releases/tag/"]');assert tar
   key=(dt,tag)
   data[key]=dict(product=name,date=dt,version=tag,source=sid,url=urljoin(url,tar['href']),body=body.get_text('\n',strip=True) if body else '',stage=('pre' if 'Pre-release' in a.get_text(' ',strip=True)[:650] or re.search(r'(?:^|[-.])(rc|beta|alpha)\d*',tag,re.I) else 'published'))
  nxt=p.select_one('a.next_page[href]') or p.select_one('a[rel="next"][href]')
  if not nxt or min(d for d,t in data)<START:break
  url=urljoin(url,nxt['href'])
 else:raise ValueError('pagination cap',name)
 print(name,len(data),len(pages),min(d for d,t in data),flush=True);return list(data.values())
def load_logs():
 entries=[]
 raw,sid=old('devin-release','https://docs.devin.ai/release-notes/2026.md','lanes/managed/manifest.json');doc=raw.decode('utf-8');parts=re.split(r'(?m)^\*\*([A-Z][a-z]+ \d{1,2}, 2026)\*\*\s*$',doc)
 for i in range(1,len(parts),2):
  entries.append(dict(product='Devin',date=dated(parts[i]),version=parts[i],source=sid,url='https://docs.devin.ai/release-notes/2026',body=parts[i+1].strip(),stage='dated entry'))
 raw,sid=old('jules-release','https://jules.google/docs/changelog/','lanes/managed/manifest.json')
 for a in BeautifulSoup(raw,'html.parser').select('article.changelog-entry'):
  entries.append(dict(product='Jules',date=dated(a.select_one('header .date').get_text(strip=True)),version=a.h2.get_text(strip=True),source=sid,url='https://jules.google/docs/changelog/#'+a.h2['id'],body=a.get_text('\n',strip=True),stage='dated entry'))
 return entries
def main():
 entries=load_logs()
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exe:
  for group in exe.map(releases,repo.items()):entries.extend(group)
 assert len({(e['product'],e['date'],e['version']) for e in entries})==len(entries)
 for file,data in [('archive.json',registry),('release-entries.json',sorted(entries,key=lambda e:(e['product'],e['date'],e['version'])))]:
  (R/file).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
