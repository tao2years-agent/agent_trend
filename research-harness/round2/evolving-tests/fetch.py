"""Lock paper PDFs and the author's source ledger for the three earlier recall misses."""
from pathlib import Path
import csv,json,sys
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'labs'));import fetch as arch
arch.R=R
with (R/'targets.tsv').open(encoding='utf8') as f:seeds=list(csv.DictReader(f,delimiter='\t'))
with ThreadPoolExecutor(4) as pool:items=list(pool.map(arch.guarded,seeds))
rev='f8c5a072f7a8da9c7c42dd358868606d480eb648'
items.append(arch.guarded(dict(id='X08',group='ISSTA',url='https://github.com/shiwen-song/GUIRevive/commit/'+rev+'.patch')))
for i,source in enumerate(['All_cases.csv','README.md']):
    v=arch.guarded(dict(id='X0'+str(i+6),group='ISSTA',url='https://raw.githubusercontent.com/shiwen-song/GUIRevive/'+rev+'/'+source));items.append(v)
(R/'sources.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),'utf8');print([(x['id'],x.get('size',x.get('error'))) for x in items])

