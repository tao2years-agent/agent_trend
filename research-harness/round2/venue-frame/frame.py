from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import csv
import json
from pathlib import Path
import re
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE=Path(__file__).resolve().parent
VENUES=json.loads((BASE/'venues.json').read_text(encoding='utf8'))
RULES={k:re.compile(v,re.I) for k,v in json.loads((BASE/'rules.json').read_text(encoding='utf8')).items()}
def normal(s):return re.sub(r'[^a-z0-9]+',' ',s.casefold()).strip()
def capture(url,dest):
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        for attempt in range(6):
            try:
                sess=requests.Session()
                sess.trust_env=False
                r=sess.get(url,timeout=(12,30),headers={'User-Agent':'Mozilla/5.0 scholarly index verification'})
                r.raise_for_status()
                dest.write_bytes(r.content)
                break
            except requests.RequestException:
                if attempt==5:raise
                time.sleep(.5)
    return dest.read_bytes()

def tsv(p,rows):
    if not rows:return
    with p.open('w',encoding='utf8',newline='') as f:
        out=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n')
        out.writeheader()
        out.writerows(rows)

def run(venue):
    track=VENUES[venue]
    url=f'https://conf.researchr.org/track/{venue}/{track}'
    dest=BASE/'raw'/f'{venue}.html'
    raw=capture(url,dest)
    soup=BeautifulSoup(raw,'html.parser')
    scope=soup.select_one('#event-overview')
    print(venue,'overview',scope.h3.get_text(' ',strip=True) if scope and scope.h3 else '-',
          'rows',len(scope.select('tr')) if scope else 0,'detail links',
          len({a['href'] for a in soup.select('a[href]') if f'/details/{venue}/{track}/' in a['href']}),flush=True)
    href_by_event={}
    for row in soup.select('[data-event-star]'):
        tr=row.find_parent('tr')
        if tr:
            link=next((a['href'] for a in tr.select('a[href]') if f'/details/{venue}/{track}/' in a['href']),None)
            if link:href_by_event[row['data-event-star']]=link
    docs=[]
    if scope:
        for tr in scope.select('tr'):
            a=tr.select_one('a[data-event-modal]')
            if not a:continue
            uid=a['data-event-modal']
            for badge in a.select('.pull-right,.label'):
                badge.decompose()
            title=a.get_text(' ',strip=True)
            doi=next((link for link in tr.select('.publication-link[href]') if 'doi.org/' in link['href']),None)
            authors=tr.select_one('.performers')
            label=tr.select_one('.prog-track')
            tests=','.join(k for k,rgx in RULES.items() if rgx.search(re.sub(r'[-–—‐‑]',' ',title)))
            explicit=re.search(r'\((Experience Paper|Replicability Study|Technical Research Paper)\)\s*$',title,re.I)
            subtype='title annotated: '+explicit.group(1) if explicit else 'unknown'
            docs.append(dict(id=uid,venue=venue,title=title,track=label.get_text(' ',strip=True) if label else 'unknown',subtype=subtype,
                             doi=doi['href'].strip() if doi else '',url=href_by_event.get(uid,''),
                             authors=authors.get_text(' ',strip=True) if authors else '',rules=tests,
                             screening='rule-hit' if tests else 'rule-miss'))
    return docs,dict(venue=venue,url=url,path=dest.relative_to(BASE).as_posix(),sha256=sha256(raw).hexdigest(),
                     heading=scope.h3.get_text(' ',strip=True) if scope and scope.h3 else '',rows=len(docs))

if __name__=='__main__':
    with ThreadPoolExecutor(8) as pool:results=list(pool.map(run,VENUES))
    rows=[r for items,_ in results for r in items]
    assert len(rows)==len({r['id'] for r in rows}), 'duplicate event UUID'
    tsv(BASE/'frame.tsv',rows)
    manifest=BASE/'manifest.json'
    if not manifest.exists():manifest.write_text(json.dumps(dict(captured=datetime.now(timezone.utc).isoformat(),sources=[r for _,r in results]),indent=2),encoding='utf8')
