from pathlib import Path
import hashlib,json,datetime,csv
from concurrent.futures import ThreadPoolExecutor
import requests,subprocess
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
def fetch(row):
    p=R/'raw'/(row['id']+'.html');p.parent.mkdir(exist_ok=True)
    if not p.exists():
        for direct in [False,True,False]:
            try:
                s=requests.Session();s.trust_env=not direct
                res=s.get(row['url'],timeout=20);res.raise_for_status()
                assert len(res.content)>3000
                p.write_bytes(res.content);break
            except (AssertionError,requests.RequestException):continue
    if not p.exists():return dict(row,status='not captured')
    raw=p.read_bytes()
    soup=BeautifulSoup(raw,'html.parser')
    for node in soup.select('style,script,nav,footer'):node.decompose()
    article=soup.select_one('.post-main') or soup.select_one('article') or soup.select_one('main') or soup
    lines='\n'.join(' '.join(a.split()) for a in article.stripped_strings if a.strip())
    (R/'raw'/(row['id']+'.txt')).write_text(lines,'utf8')
    return dict(row,status='captured',path='raw/'+p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),fetched_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),heading=soup.title.get_text(strip=True) if soup.title else '')
with ThreadPoolExecutor(6) as ex:records=list(ex.map(fetch,list(csv.DictReader((R/'targets.tsv').read_text('utf8').splitlines(),delimiter='\t'))))
(R/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),'utf8')
print([(x['id'],x['status'],x.get('heading','')[:33]) for x in records])
