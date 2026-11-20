"""Publication-level screening experiment; never equate predicted relevance with human review."""
import csv,json,hashlib,sys
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score,roc_auc_score
R=Path(__file__).resolve().parent
def tab(p):return pd.read_csv(p,sep='\t',dtype=str,keep_default_na=False)
a=tab(R.parent/'venue-review'/'review.tsv');b=tab(R.parent/'recall'/'review.tsv')
assert len(a)==142 and len(b)==128 and not set(a.uuid)&set(b.uuid)
# The already-adjudicated abstracts suffice for train/test even when extending the offline corpus.
source=R/('partial.jsonl' if '--partial' in sys.argv else 'abstracts.jsonl')
if source.exists():
    frame=pd.DataFrame([json.loads(l) for l in source.read_text('utf8').splitlines()])
else:
    frame=pd.concat([tab(R.parent/n/'abstracts.tsv') for n in ['venue-review','recall']]).drop_duplicates('id')
frame=frame.set_index('id')
metrics=[];predictions=[];novel=[]
for treatment in ['title','title_and_abstract']:
    x=frame.title if treatment=='title' else frame.title+' '+frame.abstract
    model=make_pipeline(TfidfVectorizer(strip_accents='unicode',lowercase=True,ngram_range=(1,2),sublinear_tf=True,min_df=1),LogisticRegression(C=1,max_iter=1000,solver='liblinear',random_state=0))
    model.fit(x.loc[a.uuid],a.decision.eq('relevant'))
    preds=pd.DataFrame(dict(uuid=b.uuid,venue=b.venue,stratum=b.stratum,truth=b.decision.eq('relevant'),score=model.predict_proba(x.loc[b.uuid])[:,1]))
    preds['model']=treatment;predictions.append(preds)
    for name,group in [('all',preds),*list(preds.groupby('venue')),*list(preds.groupby('stratum'))]:
        t=group.sort_values(['score','uuid'],ascending=[False,True]);n=len(t);y=t.truth
        metrics.append(dict(model=treatment,group=name,n=n,relevant=int(y.sum()),ap=average_precision_score(y,t.score),auc=roc_auc_score(y,t.score) if y.nunique()==2 else None,top20=int(y.head(min(n,20)).sum()),top40=int(y.head(min(n,40)).sum())))
    if treatment=='title_and_abstract':
        known=set(a.uuid)|set(b.uuid)|set(tab(R.parent/'venue-frame/sample-review.tsv').id)
        prior=set(tab(R.parent/'venue-frame/prior-recall.tsv').name.str.lower())
        pool=frame[~frame.index.isin(known)&~frame.title.str.lower().isin(prior)&frame.abstract.str.len().gt(0)].copy()
        if len(pool):
            pool['score']=model.predict_proba(x.loc[pool.index])[:,1]
            pool=pool.sort_values('score',ascending=False)
            seen=tab(R.parent/'recall/ledger.tsv').set_index('uuid')
            for idx,v in pool.iterrows():
                novel.append(dict(uuid=idx,score=v.score,venue=v.venue,title=v.title,url=v.url,stratum=seen.at[idx,'stratum'],abstract=v.abstract))
pd.DataFrame(metrics).to_csv(R/'model-metrics.csv',index=False)
pd.concat(predictions).to_csv(R/'holdout.csv',index=False)
if novel:pd.DataFrame(novel).to_csv(R/('partial-queue.csv' if '--partial' in sys.argv else 'queue.csv'),index=False)
print(pd.DataFrame(metrics).query("group=='all'").round(3).to_string(index=False))
