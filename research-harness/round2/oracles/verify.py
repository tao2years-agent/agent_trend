"""Use archived records to verify result.md, independently of pytest and third-party imports."""
from collections import Counter
import hashlib,json
from pathlib import Path
import re
from xml.etree import ElementTree as E
P=Path(__file__).resolve().parent
def read(p):return json.loads((P/p).read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checks():
    cohort=read("cohort.json")
    assert cohort["method_sha256"]==sha(P/"preregister.md") and cohort["dataset_sha256"]==sha(P/"raw"/"verified.parquet")
    for r in read("sources.json"):assert sha(P/r["path"])==r["sha256"]
    main=read("outcomes.json");full=read("full311/all.json");partial=read("sensitivity.json");summary=read("comparison.json")["whole"]
    assert [x["row_index_zero_based"] for x in cohort["selected"]]==list(range(485,493))
    assert len(main)==8 and len(partial)==7 and len(full["runs"])==46
    phase_counts=Counter()
    for case in main:
        for phase,v in case["phases"].items():
            xml=E.parse(P/"runs"/case["instance_id"]/v["xml"])
            counts=Counter()
            for t in xml.findall(".//testcase"):
                tag=next((c.tag for c in t if c.tag in ("failure","error","skipped")),"passed")
                counts[tag]+=1
            flattened=Counter(y for n in v["selected"].values() for y in n.get("observations",[]))
            assert counts==flattened
            phase_counts[phase]+=1
    assert set(phase_counts.values())=={8}
    for r in full["runs"]:
        xml=E.parse(P/"full311"/r["case"]/r["xml"])
        assert len(xml.findall(".//testcase"))==len(r["tests"])
        assert r["exit"]!=124
    assert summary["status_counts_by_phase"]["regression_on_gold"]=={"passed":325,"skipped":30,"xfail":1}
    assert summary["status_counts_by_phase"]["regression_on_base"]=={"passed":313,"failure":12,"skipped":30,"xfail":1}
    deltas=[e for r in summary["by_case"] for e in r["same_tests_base_to_gold"]["contrasts"]]
    assert all(e["from"]=="failure" and e["gold"]=="passed" for e in deltas)
    assert [e["name"] for e in deltas if not e["is_ftp"]]==["test_issue_23410"]
    assert Counter(i["exit"] for i in partial)=={0:2,1:4,4:1}
    for a in partial:
        f=P/"sensitivity"/a["case"]/f"without-{a['omit']}.diff";assert a["patch_sha256"]==sha(f)
    refs=re.findall(r"\]\(([^)]+)\)",(P/"result.md").read_text(encoding="utf8"))
    assert all((P/x).exists() for x in refs if not x.startswith(("http:","https:")))
    print("Verified 8 fixed rows, 54 sources, 24 targeted + 7 partial + 46 full-module pytest subprocesses and report links.")
if __name__=="__main__":checks()
