"""Snapshot author-hosted/publisher papers, extract layout-preserved text and record failures."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
import requests
import pymupdf

base=Path(__file__).resolve().parent
def fetch(item):
    ident,url=item
    pdf=ident!='R02U'
    raw=base/'raw'/(ident+('.pdf' if pdf else '.html'))
    raw.parent.mkdir(exist_ok=True)
    error=''
    for attempt in range(4):
        if raw.exists(): break
        try:
            s=requests.Session()
            s.trust_env=False
            r=s.get(url,timeout=(12,28),headers={'User-Agent':'Mozilla/5.0'})
            r.raise_for_status()
            if pdf and not r.content.startswith(b'%PDF'): raise ValueError('non-PDF response')
            raw.write_bytes(r.content)
            break
        except (ValueError,requests.RequestException) as err:
            error=str(err)[:180]
            time.sleep(.25)
    if not raw.exists():
        print(ident,error,flush=True)
        return dict(id=ident,url=url,state='unavailable',error=error)
    extra={}
    if pdf:
        textdir=base/'text'
        textdir.mkdir(exist_ok=True)
        subprocess.run(['pdftotext','-layout','-enc','UTF-8',str(raw),str(textdir/(ident+'.txt'))],check=True)
        with pymupdf.open(raw) as doc:
            extra=dict(pages=len(doc),first_page=doc[0].get_text()[:180])
    print(ident,'retrieved',extra.get('pages'),flush=True)
    return dict(id=ident,url=url,state='captured',path=raw.relative_to(base).as_posix(),
                sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),retrieved=datetime.now(timezone.utc).isoformat(),**extra)


if __name__=='__main__':
    targets=json.loads((base/'targets.json').read_text(encoding='utf8'))
    with concurrent.futures.ThreadPoolExecutor(10) as pool: rows=list(pool.map(fetch,targets.items()))
    dest=base/'manifest.json'
    if dest.exists():
        old={x['id']:x for x in json.loads(dest.read_text(encoding='utf8'))}
        rows=[old[r['id']] if r['id'] in old and old[r['id']].get('sha256')==r.get('sha256') and r.get('sha256') else r for r in rows]
    dest.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
