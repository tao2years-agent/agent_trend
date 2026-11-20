"""Recalculate summary totals from the small de-identified cohort; no network or account."""
from pathlib import Path
import csv,collections,json,hashlib
P=Path(__file__).resolve().parent;t=P/'tables'
def load(name):
 with (t/name).open(encoding='utf8',newline='')as f:return list(csv.DictReader(f))
lines=load('sample-minimal.csv');expected=json.loads((P/'audit.json').read_text('utf8'))
for horizon in ('7','30'):
 rows=[r for r in lines if r['window_days']==horizon]
 assert len(set(r['pr_key']for r in rows))==len(rows)==expected['sampled']
 assert set(r['outcome']for r in rows)<=set(['merged','closed_unmerged','no_terminal_by_horizon'])
 agent_rows=load('agent-'+horizon+'d.csv')
 for agent in agent_rows:
  sample=[r for r in rows if r['agent']==agent['agent']]
  assert len(sample)==int(agent['n'])
  for f in expected['windows'][horizon]['totals']:
   assert sum(int(r[f])for r in sample)==int(agent[f])
  assert sum(int(agent[f]) for f in ('merged','closed_unmerged','no_terminal_by_horizon'))==len(sample)
 for k,v in expected['windows'][horizon]['totals'].items():
  assert sum(int(r[k])for r in rows)==v,(k,v)
 for k,v in expected['windows'][horizon]['weighted_percent'].items():
  est=100*sum(int(r[k])/int(r['n'])*int(r['eligible']) for r in agent_rows)/sum(int(r['eligible']) for r in agent_rows)
  assert abs(est-v)<1e-8
 for r in rows:
  assert int(r['personal_decision'])==int(bool(int(r['approve'])or int(r['request_changes'])))
  assert int(r['both_decisions'])==int(bool(int(r['approve'])and int(r['request_changes'])))
print("Verified sample keys, 7/30-day outcomes, reviewer overlaps, per-agent totals and weighted estimates.")
