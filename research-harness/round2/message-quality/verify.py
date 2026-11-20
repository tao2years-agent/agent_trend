from pathlib import Path
import csv,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
def load(name):return json.loads((R/name).read_text('utf8'))
for s in load('sources.json'):
    if s.get('path','').startswith('raw/'):assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
for s in load('swe-sources.json'):assert hashlib.sha256((R/'raw'/s['path']).read_bytes()).hexdigest()==s['sha256']
for s in ['recompute.py','swe_join.py','cards.py']:subprocess.run([sys.executable,str(R/s)],stdout=subprocess.DEVNULL,check=True)
a=load('swe-joined.json');base=[v for v in a if v['scope']=='unresolved' and not v['agent'].startswith('audit')]
assert sum(v['n'] for v in base)==369 and sum(v['pbt_failed'] for v in base)==191 and sum(v['resolved_but_pbt_fails'] for v in base)==32
c=load('card-replay.json')
assert [x['top3_hit'] for x in c]==[63,64,77,18,48,99,100,112,19,48]
assert all(x['all_good']+x['has_failure']==297 for x in c)
print('40 task means, 5 upstream submissions, 1,485 joined patch/issue pairs, 10 three-card scenarios checked.')
