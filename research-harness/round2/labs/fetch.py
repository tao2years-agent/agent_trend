"""Save immutable HTTP response bytes and registered derivatives, with explicit active revision."""
import csv,datetime,hashlib,json,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit
import requests,pymupdf
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
def get(v):
    r=requests.get(v['url'],timeout=60,headers={'User-Agent':'Mozilla/5.0 (compatible; Research Evidence Archive/1.0)'});r.raise_for_status()
    raw=r.content
    typ='pdf' if raw.startswith(b'%PDF') else ('json' if 'json' in r.headers.get('Content-Type','') else 'html')
    digest=hashlib.sha256(raw).hexdigest()
    path=R/'raw'/(v['id']+'-'+digest[:16]+'.'+typ);path.parent.mkdir(exist_ok=True)
    if not path.is_file():path.write_bytes(raw)
    if typ=='pdf':
        with pymupdf.open(stream=raw,filetype='pdf') as d:
            (R/(v['id']+'.txt')).write_text('\n'.join('PAGE '+str(i+1)+'\n'+page.get_text() for i,page in enumerate(d)),'utf8')
    return v|dict(path=path.relative_to(R).as_posix(),sha256=digest,acquired_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),final_url=r.url,content_type=typ,size=len(raw))
def guarded(v):
    try:return get(v)
    except Exception as e:return v|dict(error=str(e))
if __name__=='__main__':
    with (R/'targets.tsv').open(encoding='utf8') as f:targets=list(csv.DictReader(f,delimiter='\t'))
    with ThreadPoolExecutor(5) as pool:result=list(pool.map(guarded,targets))
    print([(r['id'],r.get('size',r.get('error'))) for r in result])
    (R/'sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')

