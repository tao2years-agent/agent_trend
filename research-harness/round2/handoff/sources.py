"""Snapshot official version metadata, wheel sources and exact CLI binary provenance."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib
from importlib.metadata import distribution
import io
import json
from pathlib import Path
import re
import zipfile
import requests

P=Path(__file__).resolve().parent
DOCS={"langgraph-interrupts":"https://docs.langchain.com/oss/python/langgraph/interrupts.md",
      "temporal-retry":"https://docs.temporal.io/encyclopedia/retry-policies.md",
      "temporal-checksums":"https://github.com/temporalio/cli/releases/download/v1.10.1/checksums.txt"}
def fetch(url):
    for i in range(4):
        try:
            with requests.Session() as s:
                s.trust_env=bool(i%2)
                r=s.get(url,timeout=45);r.raise_for_status();return r.content
        except requests.RequestException:
            if i==3:raise
def snapshot(name,b,url,kind):
    sha=hashlib.sha256(b).hexdigest()
    dst=P/"raw"/(sha[:12]+"-"+name)
    dst.parent.mkdir(exist_ok=True)
    if dst.exists():assert dst.read_bytes()==b
    else:dst.write_bytes(b)
    return {"path":dst.relative_to(P).as_posix(),"url":url,"sha256":sha,"kind":kind,"retrieved_utc":datetime.now(timezone.utc).isoformat()}
def source(spec):
    package,path=spec
    d=distribution(package)
    u=f"https://pypi.org/pypi/{package}/{d.version}/json"
    b=fetch(u)
    pub=json.loads(b)
    record=next(r for r in d.files if str(r)==path)
    source=record.read_binary()
    sha=hashlib.sha256(source).digest()
    assert base64.urlsafe_b64encode(sha).decode().rstrip("=")==record.hash.value
    return [snapshot(package+".json",b,u,"published-version-metadata"),snapshot(path.replace("/","-"),source,f"https://pypi.org/project/{package}/{d.version}/","installed-implementation-verified-by-wheel-RECORD")]
def document(kv):
    name,url=kv
    return snapshot(name+".txt",fetch(url),url,"official-document")
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--temporal",type=Path,required=True);args=ap.parse_args()
    with ThreadPoolExecutor(6) as pool:
        rows=list(pool.map(document,DOCS.items()))
        for part in pool.map(source,[("langgraph","langgraph/types.py"),("langgraph-checkpoint-sqlite","langgraph/checkpoint/sqlite/__init__.py"),("temporalio","temporalio/worker/_activity.py")]):rows.extend(part)
    checksum=next(x for x in rows if "checksums" in x["path"])
    lines=(P/checksum["path"]).read_text().splitlines()
    expected=next(line.split()[0] for line in lines if "windows_amd64.zip" in line)
    u="https://temporal.download/cli/archive/v1.10.1?platform=windows&arch=amd64"
    z=fetch(u);assert hashlib.sha256(z).hexdigest()==expected
    with zipfile.ZipFile(io.BytesIO(z)) as archive:
        binary=archive.read(next(n for n in archive.namelist() if n.endswith("temporal.exe")))
    assert binary==args.temporal.read_bytes()
    rows.append({"kind":"installed-binary-verified-against-checksummed-release","url":u,"archive_sha256":expected,"executable_sha256":hashlib.sha256(binary).hexdigest(),"retrieved_utc":datetime.now(timezone.utc).isoformat()})
    (P/"sources.json").write_text(json.dumps(rows,indent=2),encoding="utf8")
    print("verified",len(rows),"provenance records")
