"""Sensitivity of comparisons to reweighting entire repositories; no identity outputs."""
import numpy as np
from collections import defaultdict
from study import load,predict,truth,write
tests,events,_=load();f,_=predict(tests,events,"frozen");r,_=predict(tests,events,"rolling")
labels,_=truth(tests,events)
values=defaultdict(lambda:np.zeros(6,dtype=int))
for (t,p,repo),(_,rf),(_,rr) in zip(tests,f,r):
    if p not in labels:continue
    u=labels[p][1];a=values[repo];a[0]+=1
    a[1]+=int(bool(rf[0]) and rf[0][0]==u);a[2]+=int(bool(rf[1]) and rf[1][0]==u)
    a[3]+=int(bool(rf[2]) and rf[2][0]==u);a[4]+=int(bool(rr[0]) and rr[0][0]==u)
    a[5]+=int(bool(rf[4]) and rf[4][0]==u)
arr=np.stack([values[k] for k in sorted(values)]);g=np.random.default_rng(20261120)
pairs=[(1,2,"frozen_frequency_minus_recency"),(1,3,"frozen_frequency_minus_first_frequency"),(4,1,"rolling_frequency_minus_frozen"),(1,5,"frozen_frequency_minus_budget")]
intervals=[[] for p in pairs]
for _ in range(2000):
    a=arr[g.integers(0,len(arr),len(arr))].sum(axis=0)
    for i,(x,y,n) in enumerate(pairs):intervals[i].append((a[x]-a[y])/a[0])
records=[]
for i,(x,y,n) in enumerate(pairs):
    sums=arr.sum(axis=0)
    records.append({"contrast":n,"micro_top1_diff":(sums[x]-sums[y])/sums[0],"resampling_p025":float(np.quantile(intervals[i],.025)),"resampling_p975":float(np.quantile(intervals[i],.975)),"replicates":2000,"label_repositories":len(arr)})
write("paired-robustness.json",records);print(records)
