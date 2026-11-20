from pathlib import Path
import requests,datetime,hashlib,json,concurrent.futures
from bs4 import BeautifulSoup
base=Path(__file__).resolve().parent
urls={'pr-8870':'https://github.com/apache/devlake/pull/8870','pr-8890-patch':'https://github.com/apache/devlake/pull/8890.patch','pr-8890':'https://github.com/apache/devlake/pull/8890','release-beta13':'https://github.com/apache/devlake/releases/tag/v1.0.3-beta13','release-beta19':'https://github.com/apache/devlake/releases/tag/v1.0.3-beta19'}
urls.update({'merge-8890-legacy':'https://raw.githubusercontent.com/apache/devlake/92fbab8c02a73178e4eb639b1f584191f522f61a/grafana/dashboards/DORADetails-ChangeFailureRate.json'})
for engine in ('mysql','postgresql'):
    urls['merge-8870-'+engine]='https://raw.githubusercontent.com/apache/devlake/31ea5303835512af67b39221b1cec350b143cf4d/grafana/dashboards/'+engine+'/dora-details-change-failure-rate.json'
def fetch(item):
    key,url=item
    session=requests.Session();session.trust_env=False
    res=session.get(url,timeout=25);res.raise_for_status()
    digest=hashlib.sha256(res.content).hexdigest()
    file=base/'independent-assets'/(digest[:12]+'-'+key+('.patch' if key.endswith('patch') else '.json' if key.startswith('merge-') else '.html'))
    if not file.exists():file.write_bytes(res.content)
    if 'html' in file.suffix:
        soup=BeautifulSoup(res.content,'html.parser')
        print(key,[t.get('datetime') for t in soup.find_all('relative-time')][:12],[(a.get_text(strip=True)[:180],a.get('href')) for a in soup.select('a[href*="8890"]') if a.get_text(strip=True)][:10])
    return dict(id=key,url=res.url,path=file.relative_to(base).as_posix(),sha256=digest,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:items=list(pool.map(fetch,urls.items()))
(base/'independent-history-sources.json').write_text(json.dumps(items,indent=2),encoding='utf8')
