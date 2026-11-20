from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import csv,hashlib,json,requests
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
def fetch(q):
    k,u=q.values();prior=next((r for r in old if r['key']==k and r['url']==u and 'path' in r),None)
    if prior:
        assert hashlib.sha256((R/prior['path']).read_bytes()).hexdigest()==prior['sha256'];return prior
    s=requests.Session();s.trust_env=False;r={'key':k,'url':u,'retrieved':datetime.now(timezone.utc).isoformat()}
    try:
        q=s.get(u,timeout=(8,25),headers={'User-Agent':'Mozilla/5.0'});q.raise_for_status();b=q.content
        if u.endswith('.pdf'):
            assert b[:4]==b'%PDF';title='Atlassian FY26 Annual Report'
        else:
            d=BeautifulSoup(b,'html.parser');title=d.title.get_text(' ',strip=True) if d.title else ''
        if not b or 'just a moment' in title.lower():raise ValueError('no article returned')
        h=hashlib.sha256(b).hexdigest();p='raw/'+k+'-'+h[:14]+('.pdf' if u.endswith('.pdf') else '.html');(R/p).write_bytes(b)
        r.update(path=p,sha256=h,bytes=len(b),title=title,resolved=q.url)
    except Exception as e:r['error']=str(e)
    return r
if __name__=='__main__':
    p=R/'sources.json';old=json.loads(p.read_text('utf8')) if p.exists() else []
    rows=list(csv.DictReader((R/'targets.tsv').open(encoding='utf-8-sig'),delimiter='\t'))
    with ThreadPoolExecutor(8) as e:out=list(e.map(fetch,rows))
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
    for x in out:print(x['key'],x.get('title',x.get('error',''))[:125])

