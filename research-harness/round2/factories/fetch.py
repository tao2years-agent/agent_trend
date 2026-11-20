"""Reuse the published snapshot method; also extract the editorial HTML as reading derivatives."""
import sys,csv,json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'labs'))
import fetch as archive
# Python launched as a file can have its own directory later than the inserted labs directory.
archive.R=R
with (R/'targets.tsv').open(encoding='utf8') as fp:seeds=list(csv.DictReader(fp,delimiter='\t'))
with ThreadPoolExecutor(5) as pool:items=list(pool.map(archive.guarded,seeds))
for row in items:
    if not row.get('path'):continue
    h=BeautifulSoup((R/row['path']).read_bytes(),'html.parser')
    article=h.select_one('article') or h.select_one('main') or h
    (R/(row['id']+'.txt')).write_text(article.get_text('\n',strip=True),'utf8')
(R/'sources.json').write_text(json.dumps(items,indent=2,ensure_ascii=False),'utf8')
print([(r['id'],r.get('size',r.get('error'))) for r in items])

