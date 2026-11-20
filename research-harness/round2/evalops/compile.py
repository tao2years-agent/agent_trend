import csv,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent.parent
sources=json.loads((R/'sources.json').read_text(encoding='utf-8'));reg={s['id']:s for s in sources};assert len(reg)==len(sources)==len({i['path'] for i in sources})
for s in reg.values():assert hashlib.sha256((B/s['path']).read_bytes()).hexdigest()==s['sha256']
lines=(R/'matrix.txt').read_text(encoding='utf-8-sig').splitlines();rows=list(csv.DictReader(lines,delimiter='|'));assert len(rows)==6
for r in rows:
 ids=r['evidence'].split();assert set(ids)<=reg.keys() and len(ids)>=8
 assert all(x for x in r.values())
with (R/'matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
results=json.loads((R/'probe-results.json').read_text());assert len(results['per_case_agreement'])==18 and results['per_split']['candidate']['blind']==[2,4] and results['opik_candidate_all_assertions']==.5 and results['opik_candidate_omit_both_failed_assertions']==1
print(len(rows),len(sources),sum('raw.githubusercontent' in s['url'] for s in sources),'code / license sources; 18 matching scores')
