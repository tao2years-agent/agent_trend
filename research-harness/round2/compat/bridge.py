from pathlib import Path
import itertools,json,sys
from concurrent.futures import ThreadPoolExecutor
from fetch import task
from run import run,sources
R=Path(__file__).resolve().parent
extra=task(('Flask','2.2.5'))
sources.extend(extra)
(R/'bridge-sources.json').write_text(json.dumps(extra,indent=2),'utf8')
with ThreadPoolExecutor(2) as pool:
    result=list(pool.map(run,[('Flask','2.2.5','Werkzeug',w) for w in ['2.2.3','2.3.8','3.0.0']]))
(R/'bridge.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),'utf8')
print([(r['provider'],r.get('upstream')) for r in result])
