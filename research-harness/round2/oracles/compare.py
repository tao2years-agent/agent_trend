from collections import Counter
import json
from pathlib import Path
P=Path(__file__).resolve().parent
def read(p):return json.loads((P/p).read_bytes())
def compare():
    full=read("full311/all.json")
    cases={r["instance_id"]:r for r in read("cohort.json")["selected"]}
    nodes=read("outcomes.json");partial=read("sensitivity.json")
    rows_by_phase={}
    outcomes={}
    signatures={}
    for r in full["runs"]:
        case,phase=r["case"],r["phase"]
        tests={}
        for n in r["tests"]:
            k=r["module"]+"::"+n["class"]+"::"+n["name"]
            if k in tests:raise ValueError("duplicate full test id "+k)
            tests[k]=n
        rows_by_phase.setdefault((case,phase),[]).append(r)
        outcomes.setdefault((case,phase),{}).update(tests)
        signatures.setdefault(phase,Counter()).update(n["outcome"] for n in tests.values())
    bycase=[]
    for key,meta in cases.items():
        fixed=set(meta['FAIL_TO_PASS'])
        limited=set(next(r for r in nodes if r["instance_id"]==key)["phases"]["regression_on_gold"]["selected"])
        gold=outcomes[key,"regression_on_gold"]
        def delta(phase):
            src=outcomes[key,phase]
            shared=src.keys() & gold.keys()
            contrasts=[{"node":k,"name":src[k]["name"],"from":src[k]["outcome"],"gold":gold[k]["outcome"],"is_ftp":src[k]["name"] in fixed,"is_in_small_oracle":src[k]["name"] in limited} for k in sorted(shared) if src[k]["outcome"]!=gold[k]["outcome"]]
            missing=sorted(gold.keys()-src.keys());added=sorted(src.keys()-gold.keys())
            rows=rows_by_phase[key,phase];ec=[r["exit"] for r in rows]
            return {"contrasts":contrasts,"missing_from_candidate":missing,"additional_on_candidate":added,"module_codes":ec,"timeouts":sum(i==124 for i in ec),"number_shared":len(shared),"sum_seconds":round(sum(r["seconds"] for r in rows),3)}
        main=delta("regression_on_base")
        benign=delta("original")
        variants=[{"omit":item["omit"],"short_exit3_12":item["exit"],**delta("without-"+str(item["omit"]))} for item in partial if item["case"]==key]
        bycase.append({"case":key,"module_count":len(rows_by_phase[key,"regression_on_gold"]),"gold_statuses":dict(Counter(i["outcome"] for i in gold.values())),"gold_nonpass":[{"node":k,"outcome":n["outcome"],"reason":n["reason"]} for k,n in gold.items() if n["outcome"]!="passed"],"original_to_gold":benign,"same_tests_base_to_gold":main,"variants":variants})
    return {"whole":{"wall_seconds":full["wall_seconds"],"n_subprocesses":len(full["runs"]),"elapsed_subprocess_seconds":round(sum(r["seconds"] for r in full["runs"]),3),"status_counts_by_phase":signatures,"by_case":bycase}}
if __name__=="__main__":
    res=compare()
    (P/"comparison.json").write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding="utf8")
    for r in res["whole"]["by_case"]:
        d=r["same_tests_base_to_gold"];print(r["case"],r["gold_statuses"],Counter((c["from"],c["gold"],c["is_ftp"]) for c in d["contrasts"]),[(v["omit"],len(v["contrasts"]),len(v["missing_from_candidate"])) for v in r["variants"]])
