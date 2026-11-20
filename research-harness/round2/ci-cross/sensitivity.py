from collections import Counter,defaultdict
from huang import values,targets,hold,write
import numpy as np
src=targets(values("native")[0]);n=len(src);a=n*6//10;b=n*8//10;train,dev,test=src[:a],src[a:b],src[b:]
stats=hold(src);k=next(x['threshold'] for x in stats['policies'] if x['target']==.95)
pr=sum(v for _,_,v in train)/len(train);tr=defaultdict(list)
for _,r,v in train:tr[r].append(v)
row=defaultdict(lambda:[0,0,0,0]);grp=defaultdict(Counter)
for _,r,y in test:
    prior=(sum(tr[r])+20*pr)/(len(tr[r])+20) if r in tr else pr
    skip=prior<k;d=row[r];d[0]+=1;d[1]+=int(y);d[2]+=int(skip);d[3]+=int(skip and y)
    z="cold" if r not in tr else "warm";g=grp[z];g["runs"]+=1;g["green"]+=int(y);g["suppressed"]+=int(skip);g["missed_green"]+=int(skip and y)
vec=np.array([v for k,v in sorted(row.items())]);g=np.random.default_rng(20261120);ests=[]
for _ in range(2000):
 z=vec[g.integers(0,len(vec),len(vec))].sum(axis=0)
 if z[3]:ests.append(z[2]/z[3])
out={"heldout_repositories":len(row),"repositories_with_at_least_one_suppression":sum(x[2]>0 for x in row.values()),"repositories_with_at_least_one_missed_green":sum(x[3]>0 for x in row.values()),"cold":grp["cold"],"warm":grp["warm"],"max_single_repo_share_of_missed_greens":max(x[3] for x in row.values())/vec[:,3].sum(),"repo_bootstrap_fixed_model_break_even_L_over_C":{"draws":2000,"finite_draws":len(ests),"p025":float(np.quantile(ests,.025)),"p975":float(np.quantile(ests,.975))}}
major=max(row.values(),key=lambda z:z[3]);out["max_missed_repo_no_identity"]={"runs":major[0],"would_skip":major[2],"missed_green":major[3]};out["without_this_repo_no_refit"]={"runs":int(vec[:,0].sum()-major[0]),"would_skip":int(vec[:,2].sum()-major[2]),"missed_green":int(vec[:,3].sum()-major[3])};write("heldout-sensitivity.json",out);print(out)
