"""Verify published counts without loading private identifiers or the column cache."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
def read(n):return json.loads((P/n).read_bytes())
for ref in read("sources.json"):assert hashlib.sha256((P/ref["path"]).read_bytes()).hexdigest()==ref["sha256"]
c=read("coverage.json");d=read("results.json");daily=read("by-day.json");sql=read("sql-check.json")["exact_match"]
assert hashlib.sha256((P/"protocol.md").read_bytes()).hexdigest()==c["protocol_sha256"]
assert len(d)==2*5*(4+1) and len(daily)==2*5*28
assert c["n_prs"]==67327 and c["n_repos"]==8700 and c["n_label30"]==15203
for r in d:
    assert 0<=r["hits1"]<=r["hits3"]<=r["routed_labeled"]<=r["L"]<=r["N"]
    assert 0<=r["hits3"]<=r["reachable_label"]<=r["L"] and r["N"]==r["L"]+r["U"]
    assert r["top1"]==r["hits1"]/r["L"] and r["top3"]==r["hits3"]/r["L"]
    if r["policy"]=="B":assert r["peak_daily"]<=3
    if r["subset"]=="all" and r["horizon"]==30:
        subset=[s for s in daily if s["mode"]==r["mode"] and s["policy"]==r["policy"]]
        for src,dst in (("prs","N"),("labeled","L"),("routed","routed"),("hits1","hits1"),("hits3","hits3")):assert sum(i[src] for i in subset)==r[dst]
    assert r["tie_inclusive_1"]==r["hits1"] and r["tie_inclusive_3"]==r["hits3"]
assert sql=={'eligible':67327,'labeled':15203,'routed':36476,'hit1':4827,'hit3':7310,'cold_prs':30851,'seen_reviewer':9165}
assert c["bounds"]["frozen"]["last_eligible_event_utc"]<"2026-02-01"
audit=read("request-field-audit.json");assert audit["non_null_assignee"]==0 and audit["requested_events"]==56954
for url in re.findall(r"\]\(([^)]+)\)",(P/"result.md").read_text(encoding="utf8")):
    assert url.startswith("https://") or (P/url).exists()
print("Verified 50 result cells, 280 day/policy groups, independent SQL count match, primary evidence links and capacity.")
