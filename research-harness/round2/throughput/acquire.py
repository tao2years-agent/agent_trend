"""Reuse the edition's frozen-PDF collector. Install targets locally as immutable snapshots."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent / 'papers'))
import collect
collect.base = R
with ThreadPoolExecutor(4) as pool:
    rows = list(pool.map(collect.fetch, json.loads((R / 'targets.json').read_text('utf8')).items()))
path = R / 'manifest.json'
previous = {r['id']:r for r in json.loads(path.read_text('utf8'))} if path.exists() else {}
path.write_text(json.dumps([previous.get(r['id'],r) if r.get('sha256') and r.get('sha256') == previous.get(r['id'],{}).get('sha256') else r for r in rows],ensure_ascii=False,indent=2),'utf8')
