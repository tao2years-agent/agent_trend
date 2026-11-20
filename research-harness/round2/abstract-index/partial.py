"""Materialize already complete venues without hitting the network during full-corpus capture."""
from ingest import R,known,frame,capture
from collections import Counter
import json
vals={}
for row in frame:
    if row['id'] in known:vals[row['id']]=known[row['id']]
    elif (R/'raw'/(row['id']+'.json')).is_file():
        d=capture(row)
        if d.get('abstract'):vals[row['id']]=d
actual=Counter(r['venue'] for r in vals.values());target=Counter(r['venue'] for r in frame)
done=[k for k,n in target.items() if actual[k]==n]
(R/'partial.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in vals.values()),'utf8')
(R/'complete-venues.json').write_text(json.dumps(done),'utf8')
print(actual,done)

