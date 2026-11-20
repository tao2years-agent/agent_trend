from pathlib import Path
import requests,hashlib,json,datetime,concurrent.futures
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent;A=R/'independent-assets';T=json.loads((A/'tree-locators.json').read_text());sha=T['v1.0.3-beta13']['sha']
tree=(A/'e2e-beta13-tree.txt').read_text().splitlines()
urls=[]
for f in tree:
 if ('/connect_incident_to_deployment/' in f or f.endswith('connect_incident_to_deploy_test.go') or '/prev_success_deployment_commit/' in f and f.endswith(('after.csv','before.csv','project_mapping.csv')) or '/e2e/raw_tables/' in f and f.endswith(('/incidents.csv','/cicd_deployment_commits_before_enrich.csv','/issues.csv','/project_mapping.csv'))):
  urls.append((f,'https://raw.githubusercontent.com/apache/devlake/'+sha+'/'+f))
for f in ['backend/plugins/dora/tasks/incident_deploy_connector.go','grafana/dashboards/mysql/dora-details-change-failure-rate.json','grafana/dashboards/postgresql/dora-details-change-failure-rate.json']:
 if not any(f==a for a,b in urls):urls.append((f,'https://raw.githubusercontent.com/apache/devlake/'+sha+'/'+f))
for tag in ('v1.0.3-beta12','v1.0.3','v1.0.4-alpha'):
 for f in T[tag]['paths']:
  if f.endswith('DORADetails-ChangeFailureRate.json'):urls.append((tag+':'+f,'https://raw.githubusercontent.com/apache/devlake/'+T[tag]['sha']+'/'+f))
for k,u in [('docs-CFR-stable','https://devlake.apache.org/docs/v1.0/Metrics/CFR/'),('docs-CFR-default','https://devlake.apache.org/docs/Metrics/CFR/')]:urls.append((k,u))
def cap(row):
 k,u=row;s=requests.Session();s.trust_env=False;resp=s.get(u,timeout=25);resp.raise_for_status();h=hashlib.sha256(resp.content).hexdigest();base=Path(k).name if not k.startswith('docs-') else k+'.html';p=A/(h[:12]+'-'+base)
 if not p.exists():p.write_bytes(resp.content)
 return dict(id=k,url=resp.url,path=p.relative_to(R).as_posix(),sha256=h,retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:out=list(e.map(cap,urls))
(R/'independent-fixture-sources.json').write_text(json.dumps(out,indent=2),encoding='utf8')
for d in out:
 if 'connect_incident_to_deploy' in d['id']:print(d['id'],d['path'])
