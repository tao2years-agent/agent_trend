from pathlib import Path
import hashlib,json,sys,requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'cowork'))
from fetch import capture as borrowed
import fetch as source
source.R=R
paths=[
 ('ramp-official-feed.xml','https://builders.ramp.com/feed.xml'),
 ('symphony-spec-revision.json','https://api.github.com/repos/openai/symphony/commits?path=SPEC.md&per_page=1&until=2026-11-20T04:00:00Z')]
with ThreadPoolExecutor(2) as ex:items=list(ex.map(borrowed,paths))
rev=json.loads((R/items[1]['path']).read_bytes())[0]['sha']
items.append(borrowed(('symphony-spec.md','https://raw.githubusercontent.com/openai/symphony/'+rev+'/SPEC.md')))
root=ElementTree.fromstring((R/items[0]['path']).read_bytes())
for node in root.iter('item'):
    title=node.findtext('title','')
    if not any(t in title.lower() for t in ['building llm judges','why we built our own background agent']):continue
    vals=[(len(n.text or ''),n.text) for n in node if n.text]
    content=BeautifulSoup(max(vals)[1],'html.parser').get_text('\n',strip=True)
    key='judge' if 'judge' in title.lower() else 'inspect'
    (R/('ramp-'+key+'.txt')).write_text(title+'\n'+node.findtext('pubDate','')+'\n'+content,'utf8')
print([(p.name,p.stat().st_size) for p in R.glob('ramp-*.txt')])
(R/'additional-sources.json').write_text(json.dumps(items,indent=2),'utf8')

