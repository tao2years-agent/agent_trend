"""Pin author data, repack only raw QA scores and discrete pass labels, and recompute tables."""
from pathlib import Path
import argparse,collections,gzip,hashlib,json,math,statistics,subprocess
R=Path(__file__).resolve().parent
SHA='6f105fe50db34e9364375333a2ec8691e1d7c63b'
TASKS=['e2e_intent','e2e_effect','local_intent','local_effect']
def get(p):return json.loads(p.read_text('utf8'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf8')
def collect(repo):
    assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==SHA
    refs=[];scores={};labels={};stats={};failure_votes={}
    def load(p):
        b=p.read_bytes();rel=p.relative_to(repo).as_posix()
        refs.append(dict(path=rel,sha256=hashlib.sha256(b).hexdigest(),url='https://github.com/pan2013e/explainbench/blob/'+SHA+'/'+rel))
        return json.loads(b)
    for task in TASKS:
        for p in sorted((repo/'results/evaluation'/task).glob('*.json')):
            alg=p.stem.split('__')[0];j=load(p)
            scores[task+'/'+alg]=j['raw']
            stats[task+'/'+alg]=j['statistics']['mean']
            if task!='e2e_effect':continue
            bare=alg.removeprefix('audit_');prefix=task+'__'+bare+'.json'
            gt=load(repo/'dataset/ground_truths'/prefix);ctx=load(repo/'dataset/context'/prefix);pred=load(repo/'results/generation'/task/p.name)['predictions'];records={}
            for key,t in gt.items():
                choices=ctx[key]['choices'];pass_i=[i for i,c in enumerate(choices) if 'test passed' in c.lower()];assert len(pass_i)==1
                letter=chr(ord('a')+pass_i[0]);gold=t['after_answer'].lower()==letter
                seq=[(s.get('after_selection') or '').lower().strip()[:1]==letter if isinstance(s,dict) else False for s in pred.get(key,[])]
                assert len(seq)==5
                records[key]=[gold,seq]
                fail_letters={chr(ord('a')+i) for i,c in enumerate(choices) if 'test failed' in c.lower()}
                assert fail_letters
                failure_votes.setdefault(alg,{})[key]=sum(isinstance(s,dict) and (s.get('after_selection') or '').lower().strip()[:1] in fail_letters for s in pred[key])
            labels[alg]=records
    compact=dict(commit=SHA,scores=scores,labels=labels,failure_votes=failure_votes,author_means=stats)
    data=json.dumps(compact,separators=(',',':')).encode();(R/'raw/author-score-labels.json.gz').write_bytes(gzip.compress(data,mtime=0))
    put(R/'artifact-sources.json',list({s['path']:s for s in refs}.values()))
def analyze():
    p=R/'raw/author-score-labels.json.gz';d=json.loads(gzip.decompress(p.read_bytes()));scores=d['scores'];agents=sorted(d['labels']); table=[]
    for agg in agents:
        dat=d['labels'][agg]
        neg=[seq for gold,seq in dat.values() if not gold];row=dict(agent=agg,n=len(dat),pbt_fail=len(neg),fail_pred_pass_first=sum(s[0] for s in neg),fail_pred_pass_majority=sum(sum(s)>=3 for s in neg),fail_pred_pass_all_five=sum(all(s) for s in neg),fail_pred_pass_any_five=sum(any(s) for s in neg),fail_pred_pass_all_draws=sum(sum(s) for s in neg),draws=len(neg)*5)
        task_scores={}
        for t in TASKS:
            key=t+'/'+agg;results=scores[key]
            assert set(results)==set(dat) and all(len(v)==5 for v in results.values())
            mean=statistics.mean(v for arr in results.values() for v in arr)
            assert math.isclose(mean,d['author_means'][key],abs_tol=1e-12),(key,mean,d['author_means'][key])
            task_scores[t]=mean
        row.update(task_scores);row['explanation_score']=statistics.mean(task_scores.values());table.append(row)
    put(R/'recomputed.json',table)
    for a in table:print(a['agent'][:30],round(a['explanation_score'],4),a['pbt_fail'],a['fail_pred_pass_first'],a['fail_pred_pass_majority'],round(a['fail_pred_pass_all_draws']/a['draws'],4))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);args=ap.parse_args()
    if args.repo:collect(args.repo)
    analyze()
