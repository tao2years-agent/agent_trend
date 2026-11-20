"""Offline lint, evidence hashes, link/reference integrity, and a reproducible first-pass search ledger."""
import csv, hashlib, json, re, unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import pymupdf
R=Path(__file__).resolve().parents[1]
def rd(p):return (R/p).read_text(encoding="utf-8-sig")
def load(p):return json.loads(rd(p))
def write(p,obj):(R/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
def normalized(s):return " ".join(re.findall("[a-z0-9]+",unicodedata.normalize("NFKD",s.lower())))
c=load("state/coverage.json")
entities=sum([load("corpus/"+n+".json") for n in ("products","papers","field")],[])
ids={x["id"] for x in entities};assert len(ids)==92
sources=load("corpus/sources.json");seen={}
for s in sources:
    p=R/s["path"];assert p.is_file() and p.stat().st_size
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    assert h==s["sha256"] and s["entity"] in ids
    if re.match(r"^\d{4}-\d{2}-\d{2}$",s["date"]):assert s["date"]<="2026-11-20",s
    seen[s["path"]]=h
for case in load("corpus/products.json"):
    assert all(case.get(k) for k in ("scenario","mechanism","limits","human","change","insight","experiment"))
    assert len(case["sources"])>=2
for doc in [R/"outputs/deep-report.md",*sorted((R/"wiki").glob("*.md"))]:
    for target in re.findall(r"\]\(([^)\s]+)\)",doc.read_text("utf8")):
        if not target.startswith(("http","#","mailto:")):assert (doc.parent/unquote(target)).exists(),(doc,target)
for p in ("outputs/deep-report.html","outputs/insights.html"):
    soup=BeautifulSoup(rd(p),"lxml");record_ids={x["id"] for x in soup.select("details.record")}
    assert record_ids==ids and "{{" not in soup.get_text()
    anchors=[x["id"] for x in soup.select("[id]")];assert len(anchors)==len(set(anchors))
    for a in soup.select('a[href^="#"]'):assert a["href"][1:] in set(anchors)
with pymupdf.open(R/"outputs/insights.pdf") as pdf:
    pdfstats={"pages":len(pdf),"linked_sources":sum(len(p.get_links()) for p in pdf),"pages_with_text":sum(len(p.get_text())>250 for p in pdf)}
    assert pdfstats["pages"]==pdfstats["pages_with_text"]==4 and pdfstats["linked_sources"]>15
for item in load("corpus/papers.json"):
    if item["level"]=="正文定点复核":
        p=next(s["path"] for s in item["sources"] if s["path"].endswith(".pdf"))
        with pymupdf.open(R/p) as doc:assert len(doc)>2 and doc[0].get_text().strip()
# Each first-pass disposition is deliberately mechanical. Manual retained readings live in paper-notes/field-notes/cases.
pool={}
for f in sorted((R/"raw/web").glob("discovery-*.txt")):
    for l in f.read_text("utf8").splitlines():
        m=re.match(r"^(.{2,400}?) \((https?://[^ )]+)\)\s*$",l)
        if not m:continue
        name,url=m.groups();parts=urlsplit(url);uid=parts.netloc.lower()+unquote(parts.path).rstrip("/")
        row=pool.setdefault(uid,dict(title=name,url=url,found_in=[]))
        row["found_in"].append(f.name)
for v in pool.values():
    u=v["url"].split("?")[0].rstrip("/").lower();t=normalized(v["title"]);matches=[]
    for e in entities:
        urls=[z["url"].split("?")[0].rstrip("/").lower() for z in e["sources"]]
        n=normalized(e.get("name") or e["title"])
        if u in urls or (len(n)>24 and n in t):matches.append(e["id"])
    v["matches"]=matches
    v["stage"]="已与本期案例或来源匹配" if matches else ("目录/会议项目表，用于发现" if "/track/" in u or "/program/" in u else "仅发现，未以本条支撑结论")
write("corpus/discovery-ledger.json",list(pool.values()))
result=dict(source_pointers=len(sources),unique_paths=len(seen),entity_ids=len(ids),search_hits_deduplicated=len(pool),discovery_stages=dict(Counter(x["stage"] for x in pool.values())),pdf=pdfstats,html=load("state/reader-check.json"),status="通过")
write("state/audit.json",result);print(result)
