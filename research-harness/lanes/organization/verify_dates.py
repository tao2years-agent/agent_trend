"""Resolve the date displayed on each individual release page independently of Atom's update time."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
import time
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from collect import BASE, CACHE

CHOICES={'backstage':2,'devlake':1,'otel':0,'langfuse':0,'phoenix':0,'promptfoo':0,
         'flagd':1,'openfga':2,'alertmanager':2,'k6':1,'conftest':1,'opencost':6}


def collect(item):
    product,index=item
    entry=json.loads((CACHE/(product+'.releases.json')).read_text(encoding='utf8'))[index]
    dest=BASE/'raw'/product/('release-'+unquote(entry['url'].split('/tag/')[-1]).replace('/','-')+'.html')
    if not dest.exists():
        for i in range(5):
            try:
                session=requests.Session()
                session.trust_env=False
                response=session.get(entry['url'],timeout=18)
                response.raise_for_status()
                dest.write_bytes(response.content)
                break
            except requests.RequestException:
                if i==4: raise
                time.sleep(1)
    soup=BeautifulSoup(dest.read_bytes(),'html.parser')
    times=[dict(time=t.get('datetime'),parent=' '.join(t.parent.parent.stripped_strings)[:220])
           for t in soup.select('relative-time[datetime]')]
    released=next((t['time'] for t in times if 'released' in t['parent'].lower()), None)
    print(product,released,times[:2],flush=True)
    return dict(id=product,url=entry['url'],date=released,atom_updated=entry['updated'],
                path=dest.relative_to(BASE.parent.parent).as_posix(),sha256=sha256(dest.read_bytes()).hexdigest())


if __name__=='__main__':
    with ThreadPoolExecutor(6) as pool:
        records=list(pool.map(collect,CHOICES.items()))
    dest=BASE/'raw'/'release-pages.json'
    if not dest.exists():
        dest.write_text(json.dumps(dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),files=records),indent=2),encoding='utf8')
