"""Archive the project's public GitHub Releases feed and summarize entries for manual screening."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import time
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from collect import REFS, BASE, CACHE


def fetch(ref):
    url = f"https://github.com/{ref['repo']}/releases.atom"
    dest = BASE/'raw'/ref['id']/'releases-20261120.atom'
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        for i in range(7):
            try:
                session = requests.Session()
                session.trust_env = False
                response = session.get(url, timeout=20)
                response.raise_for_status()
                ET.fromstring(response.content)
                dest.write_bytes(response.content)
                break
            except (requests.RequestException, ET.ParseError):
                if i == 6:
                    raise
                time.sleep(1)
    ns = '{http://www.w3.org/2005/Atom}'
    records = []
    for entry in ET.fromstring(dest.read_bytes()).findall(ns+'entry'):
        body = BeautifulSoup(entry.findtext(ns+'content') or '', 'html.parser').get_text(' ', strip=True)
        records.append(dict(title=entry.findtext(ns+'title'),url=entry.find(ns+'link').attrib['href'],
                            updated=entry.findtext(ns+'updated'),content=body))
    (CACHE/(ref['id']+'.releases.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(ref['id'],len(records),flush=True)
    return dict(id=ref['id'],url=url,path=dest.relative_to(BASE.parent.parent).as_posix(),
                size=dest.stat().st_size,sha256=sha256(dest.read_bytes()).hexdigest())


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        records=list(pool.map(fetch,REFS))
    manifest=BASE/'raw'/'release-manifest.json'
    if not manifest.exists():
        manifest.write_text(json.dumps(dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),files=records),indent=2),encoding='utf-8')
