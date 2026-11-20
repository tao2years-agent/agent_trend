import hashlib
import json
from pathlib import Path

base=Path(__file__).resolve().parent
root=base.parent.parent
fields='id name category scenario mechanism human org limits change insight experiment'.split()
ledger=json.loads((base/'manifest-15.json').read_text(encoding='utf8'))['files']
cards=[]
for row in json.loads((base/'review.json').read_text(encoding='utf8')):
    card=dict(zip(fields,row[:-1],strict=True))
    sources=[s for s in ledger if s['id']==card['id']]
    card['sources']=[]
    for source,(date,detail) in zip(sources,row[-1],strict=True):
        assert hashlib.sha256((root/source['path']).read_bytes()).hexdigest()==source['sha256']
        card['sources'].append(dict(url=source['url'],path=source['path'],date=date,detail=detail))
    cards.append(card)
assert len(cards)==5
(base/'cases.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False),encoding='utf8')
print(len(cards),'cases;',len(ledger),'sources')
