from pathlib import Path
from urllib.parse import quote
import requests,hashlib,json,concurrent.futures,time,datetime
R=Path(__file__).resolve().parent;B=R.parent.parent
def get_case(pair):
 k,f=pair;ix=json.loads((R/(k+'-index.json')).read_text());assert f in ix['paths'];u=ix['repo'][:-4];sha=ix['sha'];name=u.split('.com/')[1]
 if 'gitlab.' in u:
  url=f'{u}/-/raw/{sha}/{f}';alt=f'https://gitlab.com/api/v4/projects/{quote(name,safe="")}/repository/files/{quote(f,safe="")}/raw?ref={sha}';page=f'{u}/-/blob/{sha}/{f}'
 else:url=f'https://raw.githubusercontent.com/{name}/{sha}/{f}';alt=url;page=f'{u}/blob/{sha}/{f}'
 if (R/'sources.json').exists():
  for s in json.loads((R/'sources.json').read_text()):
   if s['url']==page and s.get('sha256')==hashlib.sha256((B/s['path']).read_bytes()).hexdigest():return s
 for i in range(6):
  try:
   ses=requests.Session();ses.trust_env=False;p=ses.get(alt if i%2 else url,timeout=(7,25));p.raise_for_status();raw=p.content
   assert not raw.lstrip()[:40].lower().startswith(b'<!doctype html') and len(raw)>70;break
  except Exception as err:
   if i==5:raise IOError(k,f,err)
   time.sleep(.4+i*.3)
 h=hashlib.sha256(raw).hexdigest();loc=R/'raw'/(k+'-'+h[:12]+'-'+f.split('/')[-1]);loc.write_bytes(raw) if not loc.exists() else None
 return dict(id=k+':'+f,url=page,raw_url=p.url,commit=sha,repo_path=f,path=loc.relative_to(B).as_posix(),sha256=h,lines=len(raw.decode('utf-8',errors='replace').splitlines()),retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
if __name__=='__main__':
 rows=[l.split('|') for l in (R/'targets.txt').read_text(encoding='utf-8-sig').splitlines() if l]
 with concurrent.futures.ThreadPoolExecutor(max_workers=11) as e:v=list(e.map(get_case,rows))
 (R/'sources.json').write_text(json.dumps(v,indent=2),encoding='utf-8');print(len(v),'source files')
