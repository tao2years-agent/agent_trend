"""Check all row-group closure identities and independently recomputed small-table claims."""
import hashlib,json,os,re
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n):return json.loads((P/n).read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert sha(P/"protocol.md")=="f5f83448e4d29415b7207684f9a84068324746a480a562a63981ebc06116cb4a"
    for src in read("sources.json"):
        if src.get("path"):assert sha(P/src["path"])==src["sha256"]
    t=read("transitions.json");sql=read("sql-check.json");h=read("holdout.json")["registered"];c=read("census.json");j=read("job-pairs.json")
    for k,row in t.items():
        z=sql[k];assert row["unique_sets"]==z["unique_sets"] and row["counts"]["missing_sequence"]==z["missing_sequences"] and row["next_given_initial_failure"]["success"]==z["red_green_next"] and row["next_given_initial_failure"]["failure"]==z["red_red_next"] and row["last_given_initial_failure"]["success"]==z["red_green_last"]
    for row in h["policies"]:
        assert h["test"]==row["test_dispatched"]+row["saved_retries"]
        assert row["saved_retries"]==row["avoided_red"]+row["missed_green"]
        assert h["test_green"]==row["retained_green"]+row["missed_green"]
    assert sum(h[k] for k in ("train","dev","test"))==h["eligible"]==7358
    assert c["runs"]["all"]==c["runs"]["attempt_1"]+c["runs"]["attempt_gt_1"]==130338516 and c["jobs"]["all"]==221534997
    assert c["runs"]["attempt_1/failure"]+c["runs"]["attempt_gt_1/failure"]==c["runs"]["conclusion/failure"]==12566611
    manifest=[];groups={"runs":set(),"jobs":set()};freq={"runs":Counter(),"jobs":Counter()}
    for f in (P/"aggregates").glob("*/*.json"):
        z=json.loads(f.read_bytes());g=z["group"];k=z["table"];assert g not in groups[k];groups[k].add(g);manifest.extend(z["ranges"])
        assert sum(v["count_all"] for v in z["frequencies"])==z["rows"]
        for r in z["frequencies"]:freq[k][(r['conclusion'] or 'unknown').lower()]+=r["count_all"]
    for k in groups:
        assert len(groups[k])==c['coverage']['tables'][k]['groups']
        for con,n in freq[k].items():assert n==c[k]['conclusion/'+con]
    assert len(manifest)==500; manifest+=read("raw/suite-id-range-hashes.json");assert len(manifest)==601
    cache=Path(os.getenv("CI_CROSS_CACHE",str(Path(os.getenv("TEMP","/tmp"))/"gha-cross-20261120")))/"columns"
    verified=0
    for r in manifest:
        f=cache/r["table"]/f"{r['start']}-{r['end']}.bin"
        if f.is_file():assert f.stat().st_size==r["end"]-r["start"]+1 and sha(f)==r["sha256"];verified+=1
    assert sum(x["coverage"]["matched_runs"] for x in j["by_band"])==j["total"]["coverage"]["matched_runs"]==3416
    assert j["total"]["by_workflow_final_state"]["failure"]["with_both_failed_and_success_jobs"]==119
    assert sum(x["coverage"]["matched_job_rows"] for x in j["by_band"])==12977
    for u in re.findall(r"\]\(([^)]+)\)",(P/"result.md").read_text("utf8")):assert u.startswith("https://") or (P/u).exists(),u
    print("361 row groups; 130,338,516 runs, 221,534,997 jobs; 601 hashed source ranges, "+str(verified)+" cache blocks verified; independent SQLite counts, holdout, joins, sources and links checked.")
if __name__=="__main__":main()
