"""Hash the dated browsing excerpts; keep both discovery and successful destination URL."""
import csv, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
R = Path(__file__).resolve().parent
out = []
for name in ('seeds.tsv','additional-seeds.tsv'):
    for row in csv.DictReader((R/name).read_text('utf8').splitlines(), delimiter='\t'):
        path = R / (row['id'] + '-web.txt')
        body = path.read_bytes()
        first = body.decode('utf8').splitlines()[0]
        match = re.search(r'\((https?://.*)\)\s*$',first)
        out.append(dict(**row, path=path.name, fetched_url=match[1] if match else row['url'],
                        representation='浏览工具抽取的带行号文本，仅抓取到的窗口', bytes=len(body),
                        retrieved_file_utc=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
                        sha256=hashlib.sha256(body).hexdigest()))
(R/'sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
