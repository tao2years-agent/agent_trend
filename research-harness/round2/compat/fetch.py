"""Download specified 3.11 Windows wheels and upstream source releases using PyPI's release hashes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,sys
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'migration'))
from acquire import grab
families=dict(Flask=['2.2.2','2.3.3','3.0.0'],Werkzeug=['2.2.3','2.3.8','3.0.0'],Starlette=['0.36.3','0.37.2','0.38.6'],httpx=['0.26.0','0.27.2','0.28.1'])
pins=dict(Jinja2='3.1.4',MarkupSafe='2.1.5',itsdangerous='2.1.2',click='8.1.7',blinker='1.8.2',colorama='0.4.6',anyio='4.5.2',certifi='2024.8.30',httpcore='1.0.7',idna='3.10',sniffio='1.3.1',h11='0.14.0',typing_extensions='4.12.2',pytest='8.3.3',iniconfig='2.0.0',packaging='24.1',pluggy='1.5.0',trio='0.27.0',attrs='24.2.0',sortedcontainers='2.4.0',outcome='1.3.0.post0',exceptiongroup='1.2.2')
pins.update(cffi='1.17.1',pycparser='2.22')
def task(item):
    name,version=item
    url=f'https://pypi.org/pypi/{name}/{version}/json'
    data=json.loads(grab(url))
    files=[x for x in data['urls'] if x['filename'].endswith('none-any.whl') or ('cp311-cp311-win_amd64.whl' in x['filename'])]
    assert len(files)>=1,(name,version)
    selected=[files[0]]
    if name in ('Flask','Starlette'):
        selected.append(next(x for x in data['urls'] if x['packagetype']=='sdist'))
    records=[]
    for f in selected:
        p=R/'raw'/f['filename'];p.parent.mkdir(exist_ok=True)
        if not p.exists():p.write_bytes(grab(f['url']))
        assert hashlib.sha256(p.read_bytes()).hexdigest()==f['digests']['sha256']
        records.append(dict(name=name,version=version,path='raw/'+p.name,url=f['url'],metadata=url,sha256=f['digests']['sha256'],kind=f['packagetype'],uploaded=f['upload_time_iso_8601']))
    return records
if __name__=='__main__':
    work=[(n,v) for n,vs in families.items() for v in vs]+list(pins.items())
    with ThreadPoolExecutor(8) as pool:out=[row for group in pool.map(task,work) for row in group]
    (R/'sources.json').write_text(json.dumps(out,indent=2),'utf8');print(len(out))
