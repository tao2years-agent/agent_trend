from pathlib import Path
import hashlib,json,tarfile
from acquire import grab,R
j=json.loads((R/"raw/Pygments-2.19.1.json").read_text("utf8"))
u=next(x for x in j["urls"] if x["packagetype"]=="sdist")
p=R/"raw"/u["filename"]
if not p.exists():
    data=grab(u["url"]);assert hashlib.sha256(data).hexdigest()==u["digests"]["sha256"];p.write_bytes(data)
assert hashlib.sha256(p.read_bytes()).hexdigest()==u["digests"]["sha256"]
(R/"golden-source.json").write_text(json.dumps(dict(path="raw/"+p.name,url=u["url"],sha256=u["digests"]["sha256"],version="2.19.1"),indent=2),encoding="utf8")
with tarfile.open(p) as t:
    fs=[n for n in t.getnames() if '/tests/' in n]
    print(len(fs),fs[:18]);print([n for n in fs if 'test_' in n and n.endswith('.py') and n.count('/')<4][:60])
    for n in fs:
        if n.endswith(("/test_examplefiles.py","/test_snippets.py")):
            print(t.extractfile(n).read().decode("utf8")[:3900])
