"""Analyze a paired, cluster-randomized pilot with complete observation windows. No external dependencies."""
import argparse
import csv
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as fp:
        rows=list(csv.DictReader(fp))
    if any(r['window_complete']!='yes' for r in rows):
        raise ValueError('Wait for all pre-registered observation windows to close.')
    groups=defaultdict(dict)
    seen=set()
    for r in rows:
        arm, key, unit = r['arm'], r['pair'], r['cluster']
        if not key or not unit or arm not in ('existing','new') or arm in groups[key] or unit in seen:
            raise ValueError('Each cluster must appear once, with exactly two different arms per pair.')
        seen.add(unit)
        for k in ('eligible','accepted','serious_regressions'):
            r[k]=int(r[k])
        for k in ('operator_minutes','owner_minutes','review_minutes'):
            r[k]=float(r[k])
        if not 0<=r['accepted']<=r['eligible'] or r['eligible']==0 or r['serious_regressions']<0:
            raise ValueError('Invalid denominator or outcome.')
        if any(not math.isfinite(r[k]) or r[k]<0 for k in ('operator_minutes','owner_minutes','review_minutes')):
            raise ValueError('Role minutes must be finite and nonnegative.')
        r['total_minutes']=sum(r[k] for k in ('operator_minutes','owner_minutes','review_minutes'))
        groups[key][arm]=r
    if not groups or any(len(g)!=2 for g in groups.values()):
        raise ValueError('Incomplete matched pairs.')
    return [g for _,g in sorted(groups.items())]

def randomization(delta):
    observed=abs(sum(delta))
    def as_extreme(signs):
        return abs(sum(a*b for a,b in zip(delta,signs)))+1e-10>=observed
    if len(delta)<=18:
        draws=list(itertools.product((-1,1),repeat=len(delta)))
        return {'method':'exact within-pair label swaps','draws':len(draws),'two_sided_p':sum(map(as_extreme,draws))/len(draws)}
    rng=random.Random(20261120)
    n=20000
    hits=sum(as_extreme(rng.choices((-1,1),k=len(delta))) for _ in range(n))
    return {'method':'fixed-seed random label swaps with +1 correction','draws':n,'two_sided_p':(hits+1)/(n+1)}

def compare(groups):
    arms={}
    for arm in ('existing','new'):
        units=[g[arm] for g in groups]
        totals={k:sum(x[k] for x in units) for k in ('eligible','accepted','operator_minutes','owner_minutes','review_minutes','total_minutes','serious_regressions')}
        totals['accepted_fraction']=totals['accepted']/totals['eligible']
        arms[arm]=totals
    relative=lambda r,k:r[k]/r['eligible']
    deltas={k:[relative(g['new'],k)-relative(g['existing'],k) for g in groups] for k in ('accepted','total_minutes','owner_minutes')}
    return {'pairs':len(groups),'arm_totals':arms,'primary_mean_pair_difference_in_accepted_fraction':mean(deltas['accepted']),
        'pooled_difference_in_accepted_fraction':arms['new']['accepted_fraction']-arms['existing']['accepted_fraction'],
        'mean_pair_difference_in_total_minutes_per_eligible':mean(deltas['total_minutes']),
        'mean_pair_difference_in_owner_minutes_per_eligible':mean(deltas['owner_minutes']),
        'primary_sharp_null_test':randomization(deltas['accepted'])}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv',type=Path)
    args=p.parse_args()
    print(json.dumps(compare(load(args.csv)),ensure_ascii=False,indent=2))
