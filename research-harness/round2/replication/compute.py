"""Independent calculations from selected columns in the author's archived data."""
from pathlib import Path
import hashlib,json,os,sys,tempfile,zipfile
import numpy as np,pandas as pd,scipy
from scipy.stats import mannwhitneyu, false_discovery_control
R=Path(__file__).resolve().parent
arc=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.gettempdir())/'esem2026-20442228-study.zip'
with arc.open('rb') as f: has=hashlib.file_digest(f,'md5').hexdigest()
assert has=='51ed9a445c45e1f96d294a882288a57d'
records=[]; manifest=[]
with zipfile.ZipFile(arc) as z:
    def load(name,cols):
        src='ai-complacency-study/CSV_files/'+name+'.csv'
        with z.open(src) as f: frame=pd.read_csv(f,usecols=cols)
        with z.open(src) as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
        manifest.append(dict(path=src,sha256=sha,rows=len(frame),columns=cols))
        return frame
    matched=load('matched_pairs',['treat_repo','ctrl_repo'])
    pools={}
    for label,tag in [('treat','human'),('ctrl','control')]:
        code=load(tag+'_prs_enriched',['author','repo','period','additions','deletions','changed_files','commits','body_length'])
        code['pr_size']=code.additions.fillna(0)+code.deletions.fillna(0)
        for c in ['pr_size','changed_files','commits','body_length']:
            s=code[c].fillna(0);q1,q3=s.quantile([.25,.75]);code[c]=s.clip(q1-3*(q3-q1),q3+3*(q3-q1))
        test=load(('control_' if label=='ctrl' else '')+'rq2_files',['author','repo','period','test_ratio','co_change','has_prod'])
        review=load('control_rq3_reviews' if label=='ctrl' else 'rq3_reviews_proper',['reviewer','repo','pr_period','submitted_at','pr_created_at','review_state','inline_comments']).rename(columns={'reviewer':'author','pr_period':'period'})
        ts=lambda c:pd.to_datetime(review[c],utc=True,format='mixed')
        review['turnaround']=(ts('submitted_at')-ts('pr_created_at')).dt.total_seconds()/3600
        review=review[review.turnaround.between(0,720)].copy()
        review['requested']=review.review_state.eq('CHANGES_REQUESTED')
        review['approved']=review.review_state.eq('APPROVED')
        pools[label]=[code,test,test[test.has_prod.astype(bool)],review]
    defs=[('pr_size',0,'pr_size','median'),('files_changed',0,'changed_files','median'),('commits',0,'commits','median'),('description',0,'body_length','median'),('test_ratio',1,'test_ratio','median'),('cochange',1,'co_change','mean'),('prod_cochange',2,'co_change','mean'),('inline',3,'inline_comments','median'),('review_hours',3,'turnaround','median'),('changes_requested',3,'requested','mean'),('approval',3,'approved','mean')]
    for control in ('all','matched'):
        for unit in ('person','person_repo'):
            cur=[]
            for metric,table,col,fn in defs:
                groups=[]
                for key in ('treat','ctrl'):
                    data=pools[key][table]
                    if control=='matched' and key=='ctrl':data=data[data.repo.isin(matched.ctrl_repo)]
                    keys=['author']+(['repo'] if unit=='person_repo' else [])+['period']
                    g=data.groupby(keys)[col].agg(fn).unstack().dropna(subset=['before','after'])
                    groups.append(g.after-g.before)
                a,b=groups
                stat,p=mannwhitneyu(a,b,alternative='two-sided')
                cur.append(dict(control=control,unit=unit,metric=metric,n_treat=len(a),n_control=len(b),median_treat=a.median(),median_control=b.median(),difference=a.median()-b.median(),p=p,rank_biserial=1-2*stat/(len(a)*len(b))))
            adjusted=false_discovery_control([row['p'] for row in cur],method='bh')
            records.extend(dict(**r,p_adj=v) for r,v in zip(cur,adjusted))
pd.DataFrame(records).to_csv(R/'sensitivity.csv',index=False)
(R/'manifest.json').write_text(json.dumps(dict(url='https://zenodo.org/records/20442228/files/ai-complacency-study.zip?download=1',md5=has,bytes=arc.stat().st_size,columns=manifest,scipy=scipy.__version__,pandas=pd.__version__),indent=2),'utf8')
