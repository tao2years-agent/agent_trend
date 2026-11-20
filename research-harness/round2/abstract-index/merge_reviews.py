"""Join never-overwritten first-pass labels, then quantify independent model-reviewer disagreement."""
import csv,json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
def table(path):
    with (R/path).open(encoding='utf-8-sig',newline='') as fp:return list(csv.DictReader(fp,delimiter='\t'))
def write(path,records):
    with (R/path).open('w',encoding='utf8',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=list(records[0]),delimiter='\t');writer.writeheader();writer.writerows(records)
source=table('audit-selection.tsv')
notes=table('early-notes.tsv')+table('late-notes.tsv')
assert len(source)==len(notes)==len({n['uuid'] for n in notes})==32
src={r['uuid']:r for r in source}
out=[]
for n in notes:
    s=src[n['uuid']];out.append({k:s[k] for k in ['uuid','venue','reason','title','url']}|{k:n[k] for k in ['decision','evidence_level','finding','decision_test']})
write('adjudications.tsv',out)
peer=table('second-review.tsv')
if len(peer)!=32:
    print('Primary 32 saved; secondary panel still in progress:',len(peer));raise SystemExit(0)
sv={r['uuid']:r for r in peer};assert len(set(sv)&set(src))==32
votes=[]
for r in out:
    p=sv[r['uuid']];other='relevant' if p['verdict']=='direct' else p['verdict']
    assert other in ['relevant','adjacent','off-topic','unknown']
    votes.append(dict(uuid=r['uuid'],venue=r['venue'],title=r['title'],first=r['decision'],second=other,comment=p['rationale_zh'],url=r['url']))
write('paired-decisions.tsv',votes)
n=len(votes);v=Counter(r['first'] for r in votes);w=Counter(r['second'] for r in votes)
agree=sum(r['first']==r['second'] for r in votes)
po=agree/n;pe=sum(v[k]*w[k] for k in set(v)|set(w))/n**2
results=dict(n=n,exact=agree,primary=v,second=w,expected_from_marginals=pe,unweighted_kappa=(po-pe)/(1-pe),both_direct=sum(r['first']==r['second']=='relevant' for r in votes),confusion={a+' / '+b:c for (a,b),c in Counter((r['first'],r['second']) for r in votes).items()})
(R/'review-agreement.json').write_text(json.dumps(results,indent=2),'utf8');print(results)

