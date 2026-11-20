from pathlib import Path
import requests,json,hashlib,subprocess,concurrent.futures,datetime,re,tempfile
R=Path(__file__).resolve().parent;A=R/'independent-assets';base='apache/incubator-devlake'
refs={v.strip().removesuffix('^{}'):k for k,v in (l.split() for l in (A/'git-tag-refs.txt').read_text().splitlines())}
head=[l.split()[0] for l in (A/'git-head-refs.txt').read_text().splitlines() if l.endswith('refs/heads/main')][0]
labels=[f'v1.0.3-beta{i}' for i in range(12,20)]+['v1.0.3','v1.0.4-alpha','main']
tree={}
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
 def git(*args):return subprocess.check_output(['git','-C',t,'-c','http.proxy=','-c','http.version=HTTP/1.1',*args],text=True,stderr=subprocess.DEVNULL)
 h=lambda s: head if s=='main' else refs['refs/tags/'+s]
 git('init','--bare');git('fetch','--depth=1','--no-tags','--filter=blob:none','https://github.com/'+base+'.git',*[h(s) for s in labels])
 for label in labels:
  sha=h(label);tree[label]={'sha':sha,'date':git('show','-s','--format=%cI',sha).strip(),'paths':[p for p in git('ls-tree','-r','--name-only',sha).splitlines() if (('grafana/' in p.lower() and ('dora' in p.lower() or 'four-key' in p.lower())) or ('backend/plugins/dora/tasks/' in p and 'incident' in p.lower())) or any(w in p.lower() for w in ('incident_commit','deployment_commit','incident_deployment','deployment_incident'))]}
(A/'tree-locators.json').write_text(json.dumps(tree,indent=2),encoding='utf8')
work=[]
for lab,v in tree.items():
 for p in v['paths']:
  if p.endswith('dora-details-change-failure-rate.json') or (lab in ('main','v1.0.3-beta13') and p.endswith(('dora.json','incident_commit.go','deployment_commit.go','incident_deployment.go','deployment_incident.go','project_incident_deployment_relationship.go','project_incident_deployment_relationships.csv','incident_deployment_connection.go','incident_deployment_connection_test.go','four-key-metrics.json','four-keys.json','dora-by-team.json'))):
   url=f'https://raw.githubusercontent.com/{base}/{v["sha"]}/{p}';work.append((f'{lab}:{p}',url,p,v['sha'],v['date']))
def capture(row):
 k,url,path,sha,date=row
 olds=R/'independent-sources.json'
 if olds.exists():
  for doc in json.loads(olds.read_text(encoding='utf8')):
   if doc['id']==k:return doc
 s=requests.Session();s.trust_env=False;r=s.get(url,timeout=22);r.raise_for_status();v=r.content;h=hashlib.sha256(v).hexdigest();f=A/(h[:12]+'-'+Path(path).name)
 if not f.exists():f.write_bytes(v)
 return dict(id=k,url=url,source_path=path,sha=sha,commit_date=date,sha256=h,path=f.relative_to(R).as_posix(),retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:out=list(ex.map(capture,work))
(R/'independent-sources.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print([(k,v['date'],len(v['paths'])) for k,v in tree.items()]);print('beta13',tree['v1.0.3-beta13']['paths'])
