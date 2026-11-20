"""Capture rendered public articles when the server response is an empty application shell."""
from pathlib import Path
import os,tempfile,subprocess,json,hashlib
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
def render(row):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        chrome=Path(os.environ['ProgramFiles'])/'Google/Chrome/Application/chrome.exe'
        raw=subprocess.run([str(chrome),'--headless=new','--no-first-run','--disable-extensions','--disable-gpu','--user-data-dir='+profile,'--virtual-time-budget=9500','--dump-dom',row['url']],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=75).stdout
    digest=hashlib.sha256(raw).hexdigest();dest=R/'raw'/(row['id']+'-render-'+digest[:16]+'.html')
    if not dest.exists():dest.write_bytes(raw)
    soup=BeautifulSoup(raw,'html.parser');main=soup.select_one('article') or soup.select_one('main') or soup
    body=main.get_text('\n',strip=True)
    (R/(row['id']+'-render.txt')).write_text(body,'utf8')
    return dict(id=row['id'],url=row['url'],path=dest.relative_to(R).as_posix(),sha256=digest,body_chars=len(body),when=datetime.now(timezone.utc).isoformat())
with ThreadPoolExecutor(2) as ex:result=list(ex.map(render,[r for r in json.loads((R/'sources.json').read_bytes()) if r['id'] in ['F03','F05']]))
(R/'rendered-sources.json').write_text(json.dumps(result,indent=2),'utf8');print(result)

