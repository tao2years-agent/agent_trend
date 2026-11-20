"""Retry only the timed-out follow-up case and check a completed-build API control."""
from buildsets import BASE,query,get
import json
f=json.loads((BASE/'clock-followup.json').read_text())
rows=[r for r in f['buildsets'] if any((r[side].get('query') or {}).get('error') for side in ['prior','current'])]
new=[query(next(c for c in f['linked_cases'] if c['id']==r['id'])) for r in rows]
u='https://zuul.opendev.org/api/tenant/openstack/builds?complete=true&limit=1'
s,obj=get(u);ok=isinstance(obj,list) and bool(obj) and all(obj[0].get(k) for k in ['start_time','end_time'])
(BASE/'clock-retries.json').write_text(json.dumps(dict(followup_retry=new,completed_control=dict(url=u,request=s,has_start_end=ok)),indent=2),'utf8')
