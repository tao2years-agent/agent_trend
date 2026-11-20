"""Verify product release artifacts against registry integrity records; do not install packages."""
from pathlib import Path
import requests,json,hashlib,base64,zipfile,tarfile,tempfile,io,time,importlib.util
R=Path(__file__).resolve().parent
def get(url):
 for i in range(5):
  try:
   ss=requests.Session();ss.trust_env=False;r=ss.get(url,timeout=35);r.raise_for_status();return r.content
  except Exception:
   if i==4:raise
   time.sleep(.3+i*.25)
purl='https://pypi.org/pypi/langsmith/0.2.11/json';mm=json.loads(get(purl));pkg=next(w for w in mm['urls'] if w['filename'].endswith('.whl'));wheel=get(pkg['url']);assert hashlib.sha256(wheel).hexdigest()==pkg['digests']['sha256']
with zipfile.ZipFile(io.BytesIO(wheel)) as z:code=z.read('langsmith/evaluation/_runner.py')
# Windows installers may normalize line endings.
actual=Path(importlib.util.find_spec('langsmith.evaluation._runner').origin).read_bytes();assert actual.replace(b'\r\n',b'\n')==code.replace(b'\r\n',b'\n')
version='0.126.0';url='https://registry.npmjs.org/promptfoo/'+version;npm=json.loads(get(url));turl=npm['dist']['tarball'];tmp=Path(tempfile.gettempdir())/('dongcha-promptfoo-'+version+'.tgz');a=tmp.read_bytes() if tmp.exists() else get(turl);assert 'sha512-'+base64.b64encode(hashlib.sha512(a).digest()).decode()==npm['dist']['integrity']
with tarfile.open(fileobj=io.BytesIO(a),mode='r:gz') as t:
 f=json.loads(t.extractfile('package/package.json').read());assert f['version']==version
out={'langsmith':dict(version='0.2.11',source=purl,url=pkg['url'],sha256=pkg['digests']['sha256'],uploaded=pkg['upload_time_iso_8601'],wheel_runner_sha256=hashlib.sha256(code).hexdigest(),installed_runner_sha256=hashlib.sha256(actual).hexdigest(),normalized_runner_matches=True),'promptfoo':dict(version=version,source=url,url=turl,integrity=npm['dist']['integrity'],cli_entry=f['bin'],archive_verified=True,execution='This archive verified release metadata only. Probe runs pinned upstream TypeScript sources directly.')}
(R/'runtime-versions.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('Verified installed LangSmith evaluator and Promptfoo release metadata.')
