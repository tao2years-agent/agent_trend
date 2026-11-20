"""Archive the exact official publication and the original JSON replies for replay."""
from pathlib import Path
import base64, datetime, gzip, hashlib, io, json, tarfile
import requests
R=Path(__file__).resolve().parent
raw=R/'raw'
def sha(b):return hashlib.sha256(b).hexdigest()
def archive(name,data):
    p=raw/name
    if p.exists() and p.read_bytes()!=data:raise ValueError('Immutable snapshot already exists: '+name)
    if not p.exists():p.write_bytes(data)
    return p
def main():
    s=requests.Session();s.trust_env=False
    rows=[]
    def get(url):
        reply=s.get(url,timeout=45);reply.raise_for_status();return reply.content
    url='https://registry.npmjs.org/renovate/44.256.0'
    meta=json.loads((raw/'npm-renovate-44.256.0.json').read_bytes())
    tgz=get(meta['dist']['tarball'])
    assert 'sha512-'+base64.b64encode(hashlib.sha512(tgz).digest()).decode()==meta['dist']['integrity']
    archive('renovate-44.256.0.tgz',tgz)
    rows.append({'url':url,'file':'npm-renovate-44.256.0.json','sha256':sha((raw/'npm-renovate-44.256.0.json').read_bytes())})
    rows.append(dict(url=meta['dist']['tarball'],file='renovate-44.256.0.tgz',sha256=sha(tgz),integrity=meta['dist']['integrity']))
    with tarfile.open(fileobj=io.BytesIO(tgz)) as tar:
        for p in sorted(raw.glob('package--*')):
            member=p.name.replace('--','/')
            assert tar.extractfile(member).read()==p.read_bytes()
            rows.append(dict(url=meta['dist']['tarball'],member=member,file=p.name,sha256=sha(p.read_bytes())))
    for name in ['starlette','httpx','flask','werkzeug']:
        url=f'https://pypi.org/pypi/{name}/json'
        p=raw/f'{name}.json.gz'
        data=gzip.decompress(p.read_bytes()) if p.exists() else get(url)
        if not p.exists():archive(p.name,gzip.compress(data,mtime=0))
        rows.append(dict(url=url,file=p.name,sha256=sha(p.read_bytes()),decoded_sha256=sha(data),release_keys=len(json.loads(data)['releases'])))
    (R/'sources.json').write_text(json.dumps({'snapshot_date':'2026-11-20','files':rows},indent=2),'utf8')
if __name__=='__main__':main()
