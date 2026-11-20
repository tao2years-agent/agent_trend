import os,zipfile,json,hashlib,tempfile
from pathlib import Path
import numpy as np,pandas as pd
R=Path(__file__).resolve().parent
au=json.loads((R/'audit.json').read_text('utf8'));z=zipfile.ZipFile(Path(tempfile.gettempdir())/'ase25-rechecks-15559526.zip')
with z.open(au['input']) as f:assert hashlib.file_digest(f,'sha256').hexdigest()==au['input_sha256']
with z.open(au['input']) as f:df=pd.read_csv(f,usecols=['project','date_of_recheck','label'],parse_dates=['date_of_recheck'])
df=df.sort_values('date_of_recheck');date=df.date_of_recheck
cut=pd.Timestamp(au['splits']['7']['cut2'])
first=cut.to_period('M');last=date.max().to_period('M');out=[]
def rates(train,sample):
    avg=train.label.mean();g=train.groupby('project').label.agg(['size','sum'])
    return sample.project.map((g['sum']+20*avg)/(g['size']+20)).fillna(avg).to_numpy()
for month in pd.period_range(first,last,freq='M'):
    start=month.start_time;end=month.end_time
    valid_start=start-pd.DateOffset(months=7);valid_end=start-pd.DateOffset(months=1)
    vtrain=df[(date>=valid_start-pd.DateOffset(months=25))&(date<valid_start-pd.Timedelta(days=30))]
    valid=df[(date>=valid_start)&(date<valid_end)&(date<start-pd.Timedelta(days=30))]
    train=df[(date>=start-pd.DateOffset(months=25))&(date<start-pd.Timedelta(days=30))]
    test=df[(date>=max(start,cut))&(date<=end)]
    if len(test)==0:continue
    dv=rates(vtrain,valid);score=rates(train,test)
    for target in [.90,.95,.99]:
        pos=np.sort(dv[valid.label.to_numpy()==1]);th=pos[max(0,int(np.floor((1-target)*len(pos))))]
        keep=score>=th;green=test.label.to_numpy()==1
        out.append(dict(month=str(month),target=target,threshold=th,n=len(test),green=int(green.sum()),queued=int(keep.sum()),missed_green=int((~keep&green).sum()),avoided_red=int((~keep&~green).sum()),training_n=len(train),dev_n=len(valid)))
results=pd.DataFrame(out);results.to_csv(R/'rolling.csv',index=False)
print(results.groupby('target')[['n','green','queued','missed_green','avoided_red']].sum().to_string())
