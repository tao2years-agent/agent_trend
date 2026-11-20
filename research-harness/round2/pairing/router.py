from pathlib import Path
import hashlib,pandas as pd
R=Path(__file__).resolve().parent
df=pd.read_csv(R/'scores.csv')
agents=sorted(df.columns[2:])
def best(data):return data[agents].sum().idxmax()
results=[]
for seed in range(20):
    fold=df.instance_id.map(lambda v:int(hashlib.sha256((str(seed)+'|'+v).encode()).hexdigest(),16)%5)
    scores=dict(global_train=0,repository_route=0,uses_repository=0)
    for f in range(5):
        train=df[fold!=f];test=df[fold==f]
        base=best(train)
        scores['global_train']+=int(test[base].sum())
        for repo,batch in test.groupby('repo'):
            local=train[train.repo==repo]
            use=best(local) if len(local)>=10 else base
            scores['uses_repository']+=len(batch) if use!=base else 0
            scores['repository_route']+=int(batch[use].sum())
    results.append(dict(seed=seed,**scores))
pd.DataFrame(results).to_csv(R/'router.csv',index=False)
hold=[]
for repo,group in df.groupby('repo'):
    base=best(df[df.repo!=repo])
    hold.append(dict(repo=repo,n=len(group),selected=base,passed=int(group[base].sum())))
pd.DataFrame(hold).to_csv(R/'new-repo.csv',index=False)
print(pd.DataFrame(results).describe().round(2).to_string());print('unseen repo',sum(r['passed'] for r in hold))
