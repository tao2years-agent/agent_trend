"""Read-only access to the official conference program's public 'show paper' form."""
from pathlib import Path
import sys, requests, time, json, csv
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from hashlib import sha256
BASE=Path(__file__).resolve().parent
FRAME=BASE.parent/'venue-frame'
sys.path.insert(0,str(FRAME))
from frame import tsv, normal

def readframe():
    return list(csv.DictReader((FRAME/'frame.tsv').open(encoding='utf8'),delimiter='\t'))

def getform(venue):
    s=BeautifulSoup((FRAME/'raw'/f'{venue}.html').read_bytes(),'html.parser')
    form=s.select_one('#load-modal-action').find_parent('form')
    params={i['name']:i.get('value','') for i in form.select('input')}
    params[form.select_one('[submitid]')['submitid']]='1'
    params['__ajax_runtime_request__']='event-modal-loader'
    return form['action'],form.select_one('.event-id-input')['name'],params

def capturepaper(row,forms):
    url,key,template=forms[row['venue']]
    params={**template,key:row['id']}
    dest=BASE/'raw'/f"{row['id']}.json"
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():
        for trial in range(7):
            try:
                sess=requests.Session();sess.trust_env=False
                response=sess.post(url,data=params,timeout=(10,16))
                response.raise_for_status()
                assert row['id'] in response.text
                response.json()
                dest.write_bytes(response.content)
                break
            except (ValueError,AssertionError,requests.RequestException):
                if trial==6: raise
                time.sleep(.6*(trial+1))
    doc=json.loads(dest.read_bytes())
    el=BeautifulSoup(next(v['value'] for v in doc if v['action']=='append'),'html.parser')
    body=el.select_one('.event-description')
    abstract=' '.join(p.get_text(' ',strip=True) for p in body.select(':scope > p') if p.get_text(strip=True)) if body else ''
    links=[a for a in el.select('a[href]') if a['href'].startswith('http')]
    detail=next((a['href'] for a in links if '/details/' in a['href']),'')
    pdf=list(dict.fromkeys(a['href'].strip() for a in links if any(k in a['href'] for k in ('arxiv.org','doi.org','pdf','zenodo.org','github.com','ssrn.com'))))
    title=el.select_one('.event-title h4 strong') or el.select_one('.event-title h4')
    groups=' | '.join(a.get_text(' ',strip=True) for a in el.select('.event-description .row a[href*="/profile/"]'))
    return dict(id=row['id'],venue=row['venue'],title=row['title'],authors=row['authors'],author_affiliations=groups,rules=row['rules'],modal_title=title.get_text(' ',strip=True) if title else '',abstract=abstract,url=detail,paper_links=' | '.join(pdf),path=dest.relative_to(BASE).as_posix(),sha256=sha256(dest.read_bytes()).hexdigest())

if __name__=='__main__':
    rows=[r for r in readframe() if r['rules']]
    forms={v:getform(v) for v in sorted({r['venue'] for r in rows})}
    with ThreadPoolExecutor(7) as pool: results=list(pool.map(lambda row:capturepaper(row,forms),rows))
    tsv(BASE/'abstracts.tsv',results)
    print(len(results),sum(bool(r['abstract']) for r in results),sum(bool(r['url']) for r in results))
