"""Fetch source bytes once per snapshot, with independent per-record failure reporting."""
import csv, concurrent.futures as cf, datetime as dt, difflib, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import fitz
R=Path(__file__).resolve().parents[1]
D=R/"raw"/"2026-11-20"
D.mkdir(parents=True, exist_ok=True)
def capture(key,url,ext,timeout=18):
    p=D/f"{key}.{ext}"
    if not p.exists():
        res=subprocess.run(["curl.exe","--noproxy","*","-L","-fsS","--connect-timeout","5","--max-time",str(timeout),"-A","Mozilla/5.0 (public software engineering research)",url],capture_output=True)
        if res.returncode or len(res.stdout)<100:raise ValueError(f"curl {res.returncode} {res.stderr.decode(errors='ignore')[:120]}")
        if ext=="pdf" and not res.stdout.startswith(b"%PDF"):raise ValueError("unexpected PDF signature")
        p.write_bytes(res.stdout)
        meta=dict(url=url,retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sha256=hashlib.sha256(res.stdout).hexdigest())
        p.with_suffix(p.suffix+".meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf8")
    return p
def norm(s):return " ".join(re.findall("[a-z0-9]+",s.lower()))
def field(row):
    url=row["url"]; ext="pdf" if url.endswith(".pdf") else "html"
    p=capture(row["id"],url,ext,28)
    return dict(row,artifact=p.relative_to(R).as_posix())
def paper(row):
    k=row["id"]; title=row["key"]
    q="https://api.openalex.org/works?"+urlencode({"filter":"title.search:"+re.sub("[^a-zA-Z0-9 -]"," ",title)[:140],"per_page":5})
    try:
        p=capture(k+"-oa",q,"json")
        items=json.loads(p.read_bytes())["results"]
        w=max(items,key=lambda x:difflib.SequenceMatcher(None,norm(title),norm(x["title"])).ratio())
        score=difflib.SequenceMatcher(None,norm(title),norm(w["title"])).ratio()
        if score<.79:raise ValueError("weak match")
        absmap=w.get("abstract_inverted_index") or {}
        ab=" ".join(word for _,word in sorted((pos,word) for word,positions in absmap.items() for pos in positions))
        out=dict(row,title=w["title"],date=w["publication_date"],doi=w.get("doi"),abstract=ab,record=p.relative_to(R).as_posix(),authors=[a["author"]["display_name"] for a in w["authorships"]],institutions=sorted({i["display_name"] for a in w["authorships"] for i in a["institutions"]}))
        links=[l.get("pdf_url") for l in w["locations"] if l.get("pdf_url")]
    except Exception:
        q="https://api.crossref.org/works?"+urlencode({"query.bibliographic":title,"rows":4})
        p=capture(k+"-crossref",q,"json")
        xs=json.loads(p.read_bytes())["message"]["items"]
        z=max(xs,key=lambda x:difflib.SequenceMatcher(None,norm(title),norm((x.get("title") or [""])[0])).ratio())
        if difflib.SequenceMatcher(None,norm(title),norm(z["title"][0])).ratio()<.79:raise ValueError("no precise match")
        out=dict(row,title=z["title"][0],date="-".join(map(str,z["published"]["date-parts"][0])),doi=z["URL"],record=p.relative_to(R).as_posix(),abstract=BeautifulSoup(z.get("abstract",""),"html.parser").get_text(" ",strip=True),authors=[(a.get("given","")+" "+a.get("family","")).strip() for a in z.get("author",[])])
        links=[a["URL"] for a in z.get("link",[])]
    if k=="P13":links.insert(0,"https://arxiv.org/pdf/2310.06770")
    if k=="P14":links.insert(0,"https://arxiv.org/pdf/2405.15793")
    if k=="P02":links.insert(0,"https://arxiv.org/pdf/2408.02232")
    if k=="P19":links.insert(0,"https://rebels.cs.uwaterloo.ca/papers/icse2023_nejati.pdf")
    for u in sorted(dict.fromkeys(links),key=lambda l:"arxiv" not in l)[:3]:
        try:
            p=capture(k+"-body",u,"pdf",25)
            with fitz.open(p) as doc:
                out["pages"]=len(doc);out["first_page"]=doc[0].get_text()[:350]
            out.update(pdf=p.relative_to(R).as_posix(),pdf_url=u);break
        except Exception:pass
    return out
def run(row):
    try:return (paper if "key" in row else field)(row)
    except Exception as e:return dict(row,error=str(e))
if __name__=="__main__":
    mode=sys.argv[1]
    with (R/f"corpus/{mode}-seeds.tsv").open(encoding="utf8") as f: seeds=list(csv.DictReader(f,delimiter="\t"))
    with cf.ThreadPoolExecutor(max_workers=12) as pool:results=list(pool.map(run,seeds))
    (R/f"corpus/{mode}-capture.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf8")
    print([(x["id"],x.get("error","ok"),x.get("pages")) for x in results])

