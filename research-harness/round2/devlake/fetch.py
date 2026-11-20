"""Freeze the DevLake fix, release lineage, both source revisions and the contemporary DORA definition."""
from pathlib import Path
import datetime as dt,hashlib,json,requests,sys
R=Path(__file__).resolve().parent
raw=R/'raw'
raw.mkdir(exist_ok=True)
reg=R/'sources.json'
rows=json.loads(reg.read_bytes()) if reg.exists() else []
session=requests.Session()
session.headers['User-Agent']='SoftwareDeliveryEvidenceResearch/1.0'
def freeze(key,url):
    old=next((r for r in rows if r['key']==key),None)
    if old:
        p=R/old['path'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==old['sha256'];return b
    resp=session.get(url,timeout=35)
    resp.raise_for_status();b=resp.content
    path=raw/key
    if path.exists():assert path.read_bytes()==b
    else:path.write_bytes(b)
    rows.append(dict(key=key,url=url,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(b).hexdigest(),captured_utc=dt.datetime.now(dt.timezone.utc).isoformat()))
    reg.write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf8')
    return b
dashboard='grafana/dashboards/DORADetails-ChangeFailureRate.json'
freeze('change.patch','https://github.com/apache/devlake/pull/8890.patch')
freeze('v1.0.3-beta12.json','https://raw.githubusercontent.com/apache/devlake/v1.0.3-beta12/'+dashboard)
freeze('proposed.json','https://raw.githubusercontent.com/apache/devlake/2289de9235b5010ac41f02e1f8266e4379d41c48/'+dashboard)
import io,zipfile
archive=freeze('v1.0.3-beta13.zip','https://codeload.github.com/apache/devlake/zip/refs/tags/v1.0.3-beta13')
with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
    matches=[p for p in bundle.namelist() if p.endswith('dora-details-change-failure-rate.json')]
    print(matches,flush=True)
    for path in matches:
        relative=path.split('/',1)[1]
        contents=freeze('beta13-'+'-'.join(relative.split('/')[-2:]),'https://raw.githubusercontent.com/apache/devlake/v1.0.3-beta13/'+relative)
        assert contents==bundle.read(path)
freeze('dora-guide.html','https://dora.dev/guides/dora-metrics/')
freeze('quick-check.html','https://dora.dev/insights/quickcheck-updates/')
freeze('release.html','https://github.com/apache/devlake/releases/tag/v1.0.3-beta13')
freeze('pull.html','https://github.com/apache/devlake/pull/8890')
for db in ['mysql','postgresql']:
    path='grafana/dashboards/'+db+'/dora-details-change-failure-rate.json'
    freeze('beta19-'+db+'.json','https://raw.githubusercontent.com/apache/devlake/v1.0.3-beta19/'+path)
freeze('beta19-release.html','https://github.com/apache/devlake/releases/tag/v1.0.3-beta19')

