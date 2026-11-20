"""Fetch immutable official MLflow distributions and extract readable implementation sections."""
import requests,hashlib,json,zipfile,io
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
B=Path(__file__).resolve().parent;raw=B/'raw';raw.mkdir(exist_ok=True)
def one(name):
    url=f'https://pypi.org/pypi/{name}/3.18.0/json';m=requests.get(url,timeout=25).json();a=next(d for d in m['urls'] if d['filename'].endswith('.whl'))
    path=raw/a['filename']
    if not path.exists():
        r=requests.get(a['url'],timeout=50);r.raise_for_status();buf=r.content
        assert hashlib.sha256(buf).hexdigest()==a['digests']['sha256'];path.write_bytes(buf)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==a['digests']['sha256']
    with zipfile.ZipFile(path) as z:
        items=[k for k in z.namelist() if 'prompt' in k.lower() and k.endswith('.py') and ('registry' in k or 'cache' in k)]
        if name=='mlflow-skinny':
            for k in z.namelist():
                if k in ['mlflow/genai/prompts/__init__.py','mlflow/store/model_registry/sqlalchemy_store.py','mlflow/tracking/_model_registry/client.py','mlflow/tracking/_model_registry/fluent.py','mlflow/entities/model_registry/prompt_version.py','mlflow/prompt/registry_utils.py','mlflow/store/model_registry/abstract_store.py','mlflow/tracking/client.py'] or ('prompt' in k and 'cache' in k and k.endswith('.py')):
                    out=raw/(k.replace('/','__')+'.txt');out.write_bytes(z.read(k))
    return dict(package=name,version='3.18.0',pypi=url,source=a['url'],file=path.relative_to(B).as_posix(),sha256=a['digests']['sha256'],release_utc=a['upload_time_iso_8601'],registry_modules=items)
if __name__=='__main__':
    with ThreadPoolExecutor(3) as pool:res=list(pool.map(one,['mlflow','mlflow-skinny','mlflow-tracing']))
    (B/'sources.json').write_text(json.dumps(res,indent=2),'utf8');print([(a['package'],len(a['registry_modules'])) for a in res])
