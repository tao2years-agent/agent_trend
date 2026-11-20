"""Validate evidence integrity, local references, time windows, and compiled outputs."""
import hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
def rd(p):return p.read_text(encoding="utf8")
meta_n=0
for p in (R/"raw/sources").rglob("*.json"):
    row=json.loads(rd(p))
    if "sha256" not in row:continue
    data=p.with_suffix("")
    assert data.exists() and hashlib.sha256(data.read_bytes()).hexdigest()==row["sha256"],p
    meta_n+=1
links=0
for p in [*(R/"wiki").glob("*.md"),R/"outputs/report.md",R/"state/checkpoint.md"]:
    body=rd(p)
    assert not re.search(r"\{\{[ADCGJV]\d+",body),p
    for href in re.findall(r"\]\(([^)]+)\)",body):
        if href.startswith(("http:","https:","#")):continue
        target=(p.parent/href.split("#")[0]).resolve()
        assert target.exists(),(p,href)
        links+=1
papers=json.loads(rd(R/"corpus/screened-papers.json"))
inc=[p for p in papers if p["status"]=="纳入"]
assert len({p["id"] for p in papers})==len(papers)
assert len({p["url"] for p in inc})==len(inc)
assert all(p["first_public"]<="2026-11-18" for p in inc)
report=rd(R/"outputs/report.md")
html=BeautifulSoup(rd(R/"outputs/report.html"),"html.parser").get_text(" ",strip=True)
for name in ["E1　单仓多人","E2　跨仓接口","E3　零知识库","E4　初始化 Skill","O16","11.6%","V04","J02","34.34%","2026-08-13"]:
    assert name in report and name in html,name
out={"snapshot_hashes_checked":meta_n,"local_link_occurrences_checked":links,"source_dates_within_cutoff":True,"paper_ids_unique":True,"paper_urls_unique":True,"selected_cross_output_checks":10,"browser_qa":json.loads(rd(R/"state/reader-check.json"))}
(R/"state/lint.json").write_text(json.dumps(out,indent=2),encoding="utf8")
print(out)
