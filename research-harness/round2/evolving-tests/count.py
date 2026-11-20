"""Count obsolete mobile test examples by application and mismatch family, from the author's table."""
import json,hashlib
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parent
x=next(z for z in json.loads((R/'sources.json').read_bytes()) if z['id']=='X06')
p=R/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
d=pd.read_csv(p);by=pd.crosstab(d.App,d.Mismatch)
by['total']=by.sum(axis=1);by.to_csv(R/'android-by-app.csv');proportion=by.div(by['total'],axis=0)
metrics={col:{'case_weighted':float(by[col].sum()/len(d)),'app_equal':float(proportion[col].mean())} for col in by.columns if col!='total'}
out=dict(rows=len(d),projects=len(by),upgrade_pairs=len(d[['App','Record App','Replay App']].drop_duplicates()),duplicates=int(d[['App','Record App','Replay App','Run Count']].duplicated().sum()),largest_app=int(by.total.max()),largest_five_apps=int(by.total.nlargest(5).sum()),types=d.Mismatch.value_counts().to_dict(),weights=metrics)
(R/'android-audit.json').write_text(json.dumps(out,indent=2),'utf8');print(out)

