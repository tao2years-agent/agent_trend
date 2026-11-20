"""Capture official public documents for commercial comparators."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import time
import requests
from bs4 import BeautifulSoup

BASE=pathlib.Path(__file__).resolve().parent


def fetch(task):
    item,index,url=task
    name=f"{index+1:02}-20261120"+('.pdf' if url.endswith('.pdf') else '.html')
    dest=BASE/'raw'/item/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        for trial in range(4):
            try:
                session=requests.Session()
                session.trust_env=False
                response=session.get(url,headers={'User-Agent':'Mozilla/5.0 research evidence capture'},timeout=(10,25))
                response.raise_for_status()
                if url.endswith('.pdf'): assert response.content.startswith(b'%PDF')
                else: assert len(response.content)>1024
                dest.write_bytes(response.content)
                break
            except (requests.RequestException,AssertionError) as err:
                if trial==3:
                    print(item,index,'FAIL',str(err)[:150],flush=True)
                    return None
                time.sleep(1)
    body=dest.read_bytes()
    print(item,index,len(body),flush=True)
    return dict(id=item,url=url,path=dest.relative_to(BASE.parent.parent).as_posix(),sha256=hashlib.sha256(body).hexdigest(),bytes=len(body))


if __name__=='__main__':
    sources=json.loads((BASE/'sources.json').read_text(encoding='utf8'))
    tasks=[(item,i,url) for item,urls in sources.items() for i,url in enumerate(urls)]
    with concurrent.futures.ThreadPoolExecutor(13) as pool: rows=list(pool.map(fetch,tasks))
    dest=BASE/'manifest.json'
    if dest.exists() and all(rows) and len(json.loads(dest.read_text(encoding='utf8'))['files'])!=len(rows):
        dest=BASE/f'manifest-{len(rows)}.json'
    if all(rows) and not dest.exists():
        dest.write_text(json.dumps(dict(retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=rows),indent=2),encoding='utf8')
