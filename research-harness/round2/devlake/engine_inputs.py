"""Pin public, portable engines in a local cache, keeping the proprietary binary out of the share bundle."""
from pathlib import Path
import base64,datetime as dt,hashlib,json,os,tempfile
import requests
from concurrent.futures import ThreadPoolExecutor

R=Path(__file__).resolve().parent
CACHE=Path(tempfile.gettempdir())/'software-delivery-engine-inputs'
CACHE.mkdir(exist_ok=True)
def download(url,path):
    if path.is_file():return
    with requests.get(url,timeout=(15,90),stream=True) as r, path.with_suffix(path.suffix+'.partial').open('wb') as f:
        r.raise_for_status()
        for chunk in r.iter_content(1024*1024):f.write(chunk)
    path.with_suffix(path.suffix+'.partial').replace(path)
def hashfile(path,kind):
    with path.open('rb') as f:return hashlib.file_digest(f,kind)
def large_download(url,path,expected_bytes):
    if path.is_file():return
    chunks=CACHE/'mysql-verified-ranges'
    chunks.mkdir(exist_ok=True)
    size=4*1024*1024
    bounds=[(a,min(a+size,expected_bytes)-1) for a in range(0,expected_bytes,size)]
    def chunk(span):
        a,b=span
        piece=chunks/f'{a}-{b}.part'
        if piece.is_file() and piece.stat().st_size==b-a+1:return piece
        for trial in range(3):
            try:
                with requests.Session() as public:
                    public.trust_env=False
                    resp=public.get(url,headers={'Range':f'bytes={a}-{b}'},timeout=(20,60))
                assert resp.status_code==206 and resp.headers['Content-Range']==f'bytes {a}-{b}/{expected_bytes}'
                assert len(resp.content)==b-a+1
                piece.write_bytes(resp.content)
                return piece
            except (requests.RequestException,AssertionError):
                if trial==2:raise
    with ThreadPoolExecutor(4) as pool:parts=list(pool.map(chunk,bounds))
    merged=path.with_suffix('.joined')
    with merged.open('wb') as out:
        for p in parts:out.write(p.read_bytes())
    merged.replace(path)
def pin_meta(name,url):
    dest=R/'raw'/name
    if not dest.exists():download(url,dest)
    return dest
if __name__=='__main__':
    mysql='https://cdn.mysql.com/archives/mysql-8.4/mysql-8.4.5-winx64.zip'
    md5=pin_meta('mysql-8.4.5.md5',mysql+'.md5')
    pgmeta='https://registry.npmjs.org/@electric-sql/pglite/0.3.7'
    pgdoc=pin_meta('pglite-0.3.7.json',pgmeta)
    meta=json.loads(pgdoc.read_bytes())
    package=CACHE/'pglite-0.3.7.tgz'
    download(meta['dist']['tarball'],package)
    assert 'sha512-'+base64.b64encode(hashfile(package,'sha512').digest()).decode()==meta['dist']['integrity']
    binary=CACHE/'mysql-8.4.5-winx64.zip'
    large_download(mysql,binary,259799354)
    assert md5.read_text('ascii').split()[0]==hashfile(binary,'md5').hexdigest()
    records=[]
    for path,url,integrity in [(binary,mysql,md5.read_text('ascii').strip()),(package,meta['dist']['tarball'],meta['dist']['integrity'])]:
        records.append(dict(filename=path.name,url=url,bytes=path.stat().st_size,sha256=hashfile(path,'sha256').hexdigest(),official_digest=integrity))
    (R/'engine-lock.json').write_text(json.dumps(dict(checked_utc=dt.datetime.now(dt.timezone.utc).isoformat(),artifacts=records),indent=2),'utf8')
    print([(p['filename'],p['bytes']) for p in records])

