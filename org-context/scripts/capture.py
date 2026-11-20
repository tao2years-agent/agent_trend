"""Fetch immutable public evidence and resolve bibliographic records."""
import concurrent.futures as cf
import csv
import difflib
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "raw" / "sources" / "2026-11-18"
BASE.mkdir(parents=True, exist_ok=True)

def get(id, url, ext):
    path = BASE / (id + "." + ext)
    if not path.exists():
        buf = subprocess.check_output(["curl.exe", "--noproxy", "*", "--max-time", "28", "-A", "Research/1.0 (public research evidence)", "-fsSL", url], stderr=subprocess.DEVNULL)
        if not buf: raise ValueError("empty response")
        path.write_bytes(buf)
        path.with_suffix(path.suffix + ".json").write_text(json.dumps({"url":url, "fetched_utc":datetime.now(timezone.utc).isoformat(), "sha256":hashlib.sha256(buf).hexdigest()}, indent=2), encoding="utf8")
    return path

def normalized(s): return " ".join(re.findall(r"[a-z0-9]+", s.lower()))

def paper(row):
    id, key = row["id"], row["key"]
    if re.fullmatch(r"\d{4}\.\d+", key):
        url = "https://arxiv.org/abs/" + key
        path = get(id,url,"html")
        soup = BeautifulSoup(path.read_bytes(), "html.parser")
        title = soup.select_one('meta[name="citation_title"]')["content"]
        date = soup.select_one('meta[name="citation_date"]')["content"].replace("/", "-")
        return dict(row,title=title,url=url,first_public=date,date_kind="arXiv v1",snapshot=path.relative_to(ROOT).as_posix(),status="纳入")
    url = "https://api.crossref.org/works?" + urlencode({"query.bibliographic":key,"rows":5})
    path = get(id,url,"json")
    items = json.loads(path.read_bytes())["message"]["items"]
    score,item = max(((difflib.SequenceMatcher(None, normalized(key), normalized(x.get("title",[""])[0])).ratio(),x) for x in items), key=lambda a:a[0])
    title = item["title"][0]
    date = "-".join(str(n).zfill(2) for n in item["published"]["date-parts"][0])
    return dict(row,title=title,url=item["URL"],first_public=date,date_kind="Crossref 出版；更早预印本未定",snapshot=path.relative_to(ROOT).as_posix(),status="纳入" if score>=0.77 else "待核",match=round(score,3),venue=" / ".join(item.get("container-title",[])))

def capture(row):
    path=get(row["id"],row["url"],row.get("ext","html"))
    return dict(row,snapshot=path.relative_to(ROOT).as_posix(),status="已抓取")

if __name__=="__main__":
    mode=sys.argv[1]
    src=ROOT / "corpus" / (mode+".tsv")
    rows=list(csv.DictReader(src.open(encoding="utf8"),delimiter="\t"))
    def run(row):
        try: return (paper if mode=="papers" else capture)(row)
        except Exception as e: return dict(row,status="抓取失败",error=str(e))
    with cf.ThreadPoolExecutor(max_workers=14) as pool: result=list(pool.map(run,rows))
    (src.with_suffix(".json")).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf8")
    print([(x["id"],x["status"]) for x in result if x["status"] not in ("纳入","已抓取")])
