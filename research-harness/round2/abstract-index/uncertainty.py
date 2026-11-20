"""Sensitivity: stratified paired bootstrap on the 128 held-out labels; no hyperparameter selection."""
import numpy as np,pandas as pd,json
from pathlib import Path
from sklearn.metrics import average_precision_score
R=Path(__file__).resolve().parent
df=pd.read_csv(R/'holdout.csv')
a=df.query("model=='title'").set_index('uuid').sort_index()
b=df.query("model=='title_and_abstract'").set_index('uuid').sort_index()
assert a.index.equals(b.index) and (a.truth==b.truth).all()
strata=list(a.groupby(['venue','stratum']).indices.values())
assert all(len(x)==8 for x in strata)
y=a.truth.to_numpy(dtype=bool);t=a.score.to_numpy();u=b.score.to_numpy()
def stats(i):
    return average_precision_score(y[i],u[i])-average_precision_score(y[i],t[i])
rng=np.random.default_rng(20261120)
dist=[stats(np.concatenate([rng.choice(d,len(d),replace=True) for d in strata])) for _ in range(2000)]
q=np.quantile(dist,[.025,.5,.975])
out=dict(n=128,groups=len(strata),predefined_target='same balanced 16 strata, conditional on these labels',iterations=len(dist),seed=20261120,
delta_ap=stats(np.arange(len(y))),bootstrap_percentile_95=q.tolist(),bootstrap_nonpositive=int((np.array(dist)<=0).sum()))
(R/'uncertainty.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
false=b[b.truth].sort_values('score').head(10).join(pd.read_csv(R.parent/'recall/review.tsv',sep='\t').set_index('uuid')[['title','rationale','url']]);false.to_csv(R/'low-ranked-relevant.csv')
print(false[['venue','score','title']].head(5).to_string(index=False))

