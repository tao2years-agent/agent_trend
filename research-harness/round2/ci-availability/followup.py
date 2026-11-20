"""Purposeful follow-up: prior and current both contain a link to the same voting job, while overall reported roster changed."""
from clocks import check,BASE,CACHE
from buildsets import query
from concurrent.futures import ThreadPoolExecutor
import json
seen={i['id'] for i in json.loads((BASE/'clock-evidence.json').read_text())['cases']}
private=json.loads((CACHE/'probes.json').read_text())
pool=sorted([i for i in private if i['id'] not in seen and i['roster']=='changed' and i['same_job']],key=lambda i:i['request_time'],reverse=True)
with ThreadPoolExecutor(3) as t:public=list(t.map(check,pool))
valid=[i for i in public if i['prior']['matched'] and i['current']['matched']]
with ThreadPoolExecutor(3) as t:pairs=list(t.map(query,valid))
(BASE/'clock-followup.json').write_text(json.dumps(dict(sampling='remaining monthly minimum-case-hash, changed complete reported roster, same voting job with UUID on both sides',n=len(pool),linked_cases=public,buildsets=pairs),indent=2),'utf8')
for i in pairs:print(i['id'],i['prior'].get('pipeline'),i['current'].get('pipeline'),i['current'].get('request_to_event_seconds'),i.get('actual_voting_name_set_changed'))
