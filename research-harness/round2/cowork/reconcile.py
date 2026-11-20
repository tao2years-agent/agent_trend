"""Compare the scored task-index with the release manifest and summarized validation declarations."""
import json,collections
from fetch import R,BASE,capture
from concurrent.futures import ThreadPoolExecutor
ps=['release/MANIFEST.json','release/docs/STATUS.md','release/validation/REPAIR_COHORT.json','release/validation/INTEGRATION_SMOKE.json','release/docs/RELEASE_HOLDS.md','release/README.md']
with ThreadPoolExecutor(4) as ex:rows=list(ex.map(capture,[(x,BASE+x) for x in ps]))
(R/'release-sources.json').write_text(json.dumps(rows,indent=2),'utf8')
for key in ps:
    if not key.endswith('json'):continue
    d=json.loads((R/'raw'/key).read_bytes());print(key,[(k,type(v).__name__,len(v) if isinstance(v,(list,dict)) else None) for k,v in d.items()][:15])

