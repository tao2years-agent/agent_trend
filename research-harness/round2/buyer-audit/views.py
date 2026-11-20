from pathlib import Path
from bs4 import BeautifulSoup
from hashlib import sha256
import re,json,html,csv,sys
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
SRC={s['id']:s for s in json.loads((ROOT/'round2/buyers/sources.json').read_text(encoding='utf8'))}
LEDGER=list(csv.DictReader((ROOT/'round2/buyers/ledger.csv').open(encoding='utf-8-sig')))

def get(sid):
    source=SRC[sid];p=ROOT/source['path'];data=p.read_bytes()
    assert sha256(data).hexdigest()==source['sha256']
    raw=data.decode('utf8',errors='replace')
    if p.suffix=='.html':
        soup=BeautifulSoup(data,'html.parser')
        for t in soup.select('script,style,nav,footer,aside,header,template,noscript,svg,[role="navigation"]'):t.decompose()
        main=soup.find('main') or soup.find('article') or soup.body or soup
        lines=[x.strip() for x in main.get_text('\n',strip=True).splitlines() if x.strip()]
    elif p.suffix=='.atom':
        soup=BeautifulSoup(raw,'xml'); lines=[]
        for entry in soup.find_all('entry'):
            lines.extend([entry.title.get_text(),entry.updated.get_text()])
            if entry.content:lines+=BeautifulSoup(entry.content.get_text(),'html.parser').get_text('\n',strip=True).splitlines()
    else:lines=raw.splitlines()
    return lines

def lookup(query,maxhits=3):
    sid,pattern=query.split('=',1);lines=get(sid);found=[i for i,l in enumerate(lines) if re.search(pattern,l,re.I)]
    print(sid,pattern,'n',len(found))
    for i in found[:maxhits]:print(str(i+1)+': '+' '.join(lines[max(0,i-1):i+3])[:265])

if __name__=='__main__':
    for q in sys.argv[1:]:lookup(q)
