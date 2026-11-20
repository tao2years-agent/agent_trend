"""Fetch one release page per candidate and keep its source/stated changes separately from sampled HEAD."""
import json,re
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from fetch import ROOT,get,save
tags={'runner':'v2.338.2','buildkite':'v4.12.0','tekton':'v1.18.0','argocd':'v3.6.2','rollouts':'v1.11.0-rc1','renovate':'44.253.4','pragent':'v0.50.0','atlantis':'v0.49.0','conftest':'v0.71.0','temporal':'1.36.1','jenkins':'560.v56198a_642157'}
def run(kv):
 id,tag=kv
 d=json.loads((ROOT/(id+'.index.json')).read_text(encoding='utf-8'))
 entry=next(e for e in d['releases'] if e['url'].endswith('/'+tag));r=get(entry['url']); soup=BeautifulSoup(r.content,'html.parser')
 dt=[t.get('datetime') for t in soup.select('relative-time') if t.get('datetime')]
 s=save(id,entry['url'],r,(dt[0] if dt else entry['updated'])[:10],tag+'.html')
 summary=dict(source=s,tag=tag,dates=dt,feed_updated=entry['updated'])
 (ROOT/(id+'.release.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(id,dt[:3],flush=True)
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(run,tags.items()))
