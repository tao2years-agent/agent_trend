from pathlib import Path
import sys, json, re, csv
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
BASE=Path(__file__).resolve().parent; FRAME=BASE.parent/'venue-frame'
sys.path.insert(0,str(BASE.parent/'venue-review'))
import fetch
from frame import normal, tsv

def load(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t'))
if __name__=='__main__':
    rules={k:re.compile(s,re.I) for k,s in json.loads((BASE/'rules.json').read_text(encoding='utf8')).items()}
    rs=fetch.readframe(); samples={r['id'] for r in load(FRAME/'sample-review.tsv')}
    known={normal(r['name']) for r in load(FRAME/'prior-recall.tsv')} | {normal(r['title']) for r in load(BASE.parent/'papers'/'results.tsv')}
    articles=[]; byid={r['id']:r for r in rs}
    for r in rs:
        rank=''; seen=[]
        if r['rules']:seen.append('V1 hit/full abstract')
        if r['id'] in samples:seen.append('V1 audited')
        if normal(r['title']) in known:seen.append('prior known paper')
        title=re.sub(r'[-–—‐‑]',' ',r['title'])
        hit=','.join(q for q,rg in rules.items() if rg.search(title))
        stratum='excluded' if seen else ('new-hit' if hit else 'still-miss')
        if not seen:rank=sha256(('v2-blind-20261120|'+r['id']).encode()).hexdigest()
        articles.append(dict(uuid=r['id'],venue=r['venue'],title=r['title'],v1=r['rules'],v2=hit,excluded_for='; '.join(seen),stratum=stratum,hash=rank,sampled='no'))
    sample=[]
    for venue in dict.fromkeys(r['venue'] for r in rs):
        for stratum in ['new-hit','still-miss']:
            select=sorted([r for r in articles if r['venue']==venue and r['stratum']==stratum],key=lambda r:r['hash'])[:8]
            for r in select:r['sampled']='yes'
            sample+=select
    tsv(BASE/'ledger.tsv',articles)
    print('strata',Counter(r['stratum'] for r in articles),len(sample),flush=True)
    fetch.BASE=BASE
    forms={v:fetch.getform(v) for v in {r['venue'] for r in sample}}
    with ThreadPoolExecutor(7) as pool:data=list(pool.map(lambda r:fetch.capturepaper(byid[r['uuid']],forms),sample))
    merged=[dict(sample_id=f'V{i:03}',stratum=r['stratum'],v2=r['v2'],**d) for i,(r,d) in enumerate(zip(sample,data),1)]
    assert len({r['id'] for r in merged})==len(merged) and all(r['title']==r['modal_title'] for r in merged)
    tsv(BASE/'abstracts.tsv',merged)
    print(len(merged),sum(bool(r['abstract']) for r in merged))
