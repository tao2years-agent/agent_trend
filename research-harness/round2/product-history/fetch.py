"""Read-only retrieval, content-addressed files; skips unchanged snapshots when replayed."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import csv,json,hashlib,requests
R=Path(__file__).resolve().parent
def capture(row):
    s=requests.Session();s.trust_env=False
    ident,url=row.values()
    old=next((x for x in prior if x['key']==ident and x['url']==url and x.get('path')),None)
    if old:return old
    res={'key':ident,'url':url,'fetched_utc':datetime.now(timezone.utc).isoformat()}
    try:
        req=s.get(url,timeout=(7,45),headers={'User-Agent':'Mozilla/5.0 research snapshot'});req.raise_for_status()
        b=req.content;h=hashlib.sha256(b).hexdigest();p=Path('round2/product-history/raw')/(ident+'-'+h[:16]+('.md' if ident=='claude' else '.html'));o=R.parent.parent/p
        if o.exists():assert o.read_bytes()==b
        else:o.write_bytes(b)
        res.update(sha256=h,path=p.as_posix(),resolved=req.url)
    except Exception as e:res['error']=str(e)
    return res
if __name__=='__main__':
    f=R/'fresh.json';prior=json.loads(f.read_text('utf8')) if f.exists() else []
    rows=list(csv.DictReader((R/'targets.tsv').open(encoding='utf-8-sig'),delimiter='\t'))
    with ThreadPoolExecutor(8) as pool:out=list(pool.map(capture,rows))
    f.write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
    for x in out:print(x['key'],x.get('path',x.get('error','')))
