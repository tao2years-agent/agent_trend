"""Read-only audit of the candidate universe, patches, gates, witnesses and source hashes."""
import hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from xml.etree import ElementTree as E
P=Path(__file__).resolve().parent
def read(f):return json.loads((P/f).read_bytes())
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
def main():
    lock=read("runs/lock.json")
    for p,d in lock.items():assert sha(p)==d
    for ref in read("sources.json"):assert sha(ref["path"])==ref["sha256"]
    en=read("candidates.json");src=read("runs/observations.json");score=read("scores.json")
    selected={v["id"]:v for c in en for v in c["changes"] if v["selected"]}
    assert len(selected)==49 and sum(len(c["changes"]) for c in en)==64
    seen=set()
    for c in en:
        assert len({(r['path'],r['ast_sha256']) for r in c['changes']})==len(c['changes'])
        for r in c["changes"]:
            assert r["line"] in c["gold_added_lines"][r["path"]] and "/tests/" not in r["path"]
            assert r["id"] not in seen;seen.add(r["id"])
            if r["selected"]:assert sha(f"patches/{c['case']}/{r['id']}.diff")==r["diff_sha256"]
    assert {r["id"] for r in src["observations"] if r["id"] not in ("gold","base")}==set(selected)
    golds={};cases=defaultdict(list)
    for r in src["observations"]:
        leaf=P/"runs"/r["case"]/r["id"]
        for grp in ("labels","modules"):
            for g in r[grp]:
                if g["xml"]:assert len(E.parse(leaf/g["xml"]).findall(".//testcase"))==sum(g["states"].values())
        if r["id"]=="gold":golds[r["case"]]={x["id"]:x["ok"] for x in json.loads((leaf/r["property"]["observations"]).read_bytes())}
        if r["id"] not in ("gold","base"):cases[r["case"]].append(r)
    memo={r["id"]:r for r in score["candidates"]}
    for case,runs in cases.items():
        for r in runs:
            ids=r["id"];q=memo[ids];f=r["property"]["observations"]
            if f:
                data=json.loads((P/"runs"/case/ids/f).read_bytes());assert {x["id"] for x in data}==set(golds[case])
                mismatch=[x["id"] for x in data if golds[case][x["id"]] and not x["ok"]]
                assert len(mismatch)==q["newly_failing_count"]
    with_id=memo["Ve63126860e55"];assert with_id["both_pass"] and with_id["newly_failing_count"]==16
    evidence=read("witnesses.json");assert [r["observation"]["result"] for r in evidence]==["rejected","accepted","returned","error"]
    ext={r["version"]:r["results"] for r in read("extension-results.json")}
    for k in ("positive","integer","real","nonnegative"):
        assert ext["gold"][k]["explicit_assumptions"]==[True]*4
        assert ext["V168a02a26183"][k]["explicit_assumptions"]==[None]*4
    assert ext["gold"]["positive"]["sqrt_square_equals_self"]==[True]*4
    assert ext["V168a02a26183"]["positive"]["sqrt_square_equals_self"]==[False]*4
    assert ext["gold"]["control"]==ext["V168a02a26183"]["control"]
    jp=read("package-runs/observations.json")
    for row in jp["rows"]:
        xml=P/"package-runs"/row["case"]/row["id"]/"all.xml"
        if xml.exists():assert len(E.parse(xml).findall(".//testcase"))==sum(row["states"].values())
    for link in re.findall(r"\]\(([^)]+)\)",(P/"result.md").read_text("utf8")):
        assert link.startswith("https://") or (P/link).exists(),link
    print("8 historic golds; 64 eligible, 49 selected candidate patches; main XML, independent inputs, two-version witnesses, package XML, source hashes and report links checked.")
if __name__=="__main__":main()
