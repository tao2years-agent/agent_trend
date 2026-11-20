import json,csv,hashlib,sys,subprocess,datetime,requests,os,tempfile
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version,InvalidVersion
from pathlib import Path
R=Path(__file__).resolve().parent
D=R/'raw';D.mkdir(exist_ok=True)
CACHE=Path(tempfile.gettempdir())/'dongcha-sympy-releases';CACHE.mkdir(exist_ok=True)
cut='2026-11-20T04:50:00'
def get_index(pkg):
    p=D/(pkg+'.json')
    if not p.exists():
        res=requests.get('https://pypi.org/pypi/'+pkg+'/json',timeout=60);res.raise_for_status();p.write_bytes(res.content)
    return json.loads(p.read_bytes()),dict(pkg=pkg,url='https://pypi.org/pypi/'+pkg+'/json',path='raw/'+p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),local_snapshot_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat())
idx,src=get_index('sympy'); mp,ms=get_index('mpmath')
def allowed(files):
    return [x for x in files if not x['yanked'] and x['filename'].endswith('none-any.whl') and x['upload_time']<=cut]
vs={}
for name,files in idx['releases'].items():
    try:v=Version(name)
    except InvalidVersion:continue
    if v.major==1 and v.minor>=9 and not(v.is_prerelease or v.is_devrelease) and allowed(files):vs.setdefault(v.minor,[]).append(v)
choices=sorted({item for values in vs.values() for item in [min(values),max(values)]})
def fetch(row):
    f=CACHE/row['filename']
    if not f.exists():
        r=requests.get(row['url'],timeout=60);r.raise_for_status();f.write_bytes(r.content)
    assert hashlib.sha256(f.read_bytes()).hexdigest()==row['digests']['sha256']
    return f
m=allowed(mp['releases']['1.3.0'])[0];mpf=fetch(m)
def run(v):
    row=allowed(idx['releases'][str(v)])[0];sf=fetch(row)
    r=subprocess.run(['py','-3.11','-I','-S',str(R/'probe.py'),str(sf),str(mpf)],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=90)
    base=dict(version=str(v),date=row['upload_time_iso_8601'],wheel=row['filename'],url=row['url'],sha256=row['digests']['sha256'],exit=r.returncode)
    if r.returncode:return base|dict(observations=[],error=r.stderr[-900:].replace(str(CACHE),'[cache]'))
    doc=json.loads(r.stdout);assert doc['version']==str(v) and doc['mpmath']=='1.3.0'
    return base|dict(observations=doc['runs'])
with ThreadPoolExecutor(3) as pool:results=list(pool.map(run,choices))
(R/'sources.json').write_text(json.dumps(dict(snapshot=[src,ms],fixed_mpmath=dict(url=m['url'],sha256=m['digests']['sha256']),selected=[v['version'] for v in results]),indent=2),'utf8')
(R/'checks.json').write_text(json.dumps(results,indent=2),'utf8')
print([(r['version'],r['exit'],[v['probe'] for v in r['observations'] if not v['ok']],r.get('error','')[-100:]) for r in results])

