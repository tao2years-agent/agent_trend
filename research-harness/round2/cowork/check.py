"""Recalculate public task denominators and the size of macro vs. micro weighting effects."""
from pathlib import Path
import hashlib,json,csv
import pandas as pd
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_bytes())
def main():
    mf=load(R/'raw/release/MANIFEST.json')
    t=pd.read_parquet(R/'raw/data/tasks.parquet').set_index('row')
    rows=[]
    for r in mf['tasks']:
        row=r['row']; idx=t.loc[row]; assert idx.task_id==r['task_id'] and idx.task_path==r['path'] and idx.task_version==r['task_version']
        f=R/'raw/release'/r['path']/'tests/config.json'
        conf=load(f); assert hashlib.sha256(f.read_bytes()).hexdigest()==r['files']['tests/config.json']
        for kind in ['f2p','p2p']:
            x=conf[kind+'_node_ids'];assert len(set(x))==len(x) and set(x)==set(r[kind+'_nodes']) and all(x)
        assert not set(conf['f2p_node_ids'])&set(conf['p2p_node_ids'])
        rows.append(dict(row=row,new_nodes=len(conf['f2p_node_ids']),regression_nodes=len(conf['p2p_node_ids']),budget_seconds=int(idx.budget_seconds)))
    frame=pd.DataFrame(rows).sort_values('row');assert len(frame)==len(t)==len(set(frame.row))==101
    frame.to_csv(R/'task-counts.csv',index=False)
    dist={}
    for col in ['new_nodes','regression_nodes']:
        x=frame[col]; dist[col]=dict(sum=int(x.sum()),min=int(x.min()),median=float(x.median()),max=int(x.max()),largest_10_tasks=int(x.nlargest(10).sum()),smallest_10_tasks=int(x.nsmallest(10).sum()),zeros=int((x==0).sum()))
    paths=[x['rfilename'] for x in load(R/'raw/release-files.json')['siblings']]
    out=dict(task_count=len(frame),revision='529b67ddf03ff6efd74658b4b2a436abf371c5cf',budget_seconds=sorted(set(frame.budget_seconds)),release=dist,
    paper_table2=dict(new_nodes=2699,regression_nodes=562,tasks=101),same_per_task_manifest_config=True,listed_files=len(paths),
    campaign_status_files=sum(p.lower().endswith('/status.json') and '/jobs/' in p.lower() for p in paths),exact_statistics_files=sum(p.endswith('/statistics.json') for p in paths))
    (R/'audit.json').write_text(json.dumps(out,indent=2),'utf8');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

