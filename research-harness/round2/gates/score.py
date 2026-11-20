"""Pair each independent input with both the golden response and mutated response."""
import json,statistics
from collections import Counter,defaultdict
from pathlib import Path
from candidates import P,read,write
def good(entries):return bool(entries) and all(r["exit"]==0 and sum(r["states"].values())>0 for r in entries)
def prop(base,obs):
    return {t["id"]:t for t in read(base/obs["property"]["observations"])} if obs["property"]["observations"] else {}
def main():
    src=read(P/"runs"/"observations.json");univ=read(P/"candidates.json");by={r["id"]:r for c in univ for r in c["changes"]}
    grouped=defaultdict(list)
    for x in src["observations"]:grouped[x["case"]].append(x)
    cases=[];mut=[];cost=defaultdict(list)
    for key,runs in grouped.items():
        lookup={r["id"]:r for r in runs};folder=P/"runs"/key
        gold=prop(folder/"gold",lookup["gold"]);base=prop(folder/"base",lookup["base"])
        gpassed={k for k,x in gold.items() if x["ok"]};need={k for k,x in gold.items() if not x["ok"]}
        assert set(gold)==set(base) and gold
        assert good(lookup["gold"]["labels"]) and good(lookup["gold"]["modules"])
        before={k for k,n in base.items() if not n["ok"]}
        ex=next(c for c in univ if c["case"]==key);xs=[]
        for r in runs:
            pid=r["id"]
            for lvl in ("labels","modules"):cost[lvl]+=[v["elapsed_seconds"] for v in r[lvl]]
            cost["property"].append(r["property"]["elapsed_seconds"])
            if pid in ("base","gold"):continue
            a=prop(folder/pid,r);t=good(r["labels"]);m=good(r["modules"])
            ok=bool(a) and set(a)==set(gold) and r["property"]["exit"]==0
            broken=sorted(k for k in gpassed if ok and not a[k]["ok"])
            repaired=sorted(k for k in need if ok and a[k]["ok"])
            srcmut=by[pid]
            item={"id":pid,"case":key,"operator":srcmut["operator"],"labels_pass":t,"modules_pass":m,"both_pass":t and m,"property_executed":ok,"newly_failing_count":len(broken),"restored_gold_failures":len(repaired),"first_counterexample":a[broken[0]] if broken else None, "comparison_valid":ok}
            if broken:item["counterexample_ids"]=broken
            if repaired:item["restored_ids"]=repaired
            xs.append(item);mut.append(item)
        cases.append({"case":key,"enumerated":len(ex["changes"]),"selected":len(xs),"labels_ok":sum(x["labels_pass"] for x in xs),"mods_ok":sum(x["modules_pass"] for x in xs),"both_ok":sum(x["both_pass"] for x in xs),"both_executed_I":sum(x["both_pass"] and x["property_executed"] for x in xs),"grey_killed":sum(x["both_pass"] and x["newly_failing_count"]>0 for x in xs),"gold_inputs":len(gold),"baseline_failures":len(before),"gold_failures":len(need),"gold_introduced_witnesses":[gold[k] for k in sorted(need-before)],"gold_repaired_count":len(before-need),"gold_preexisting_fail_count":len(need&before)})
    stats={}
    for l,ts in cost.items():
        q=statistics.quantiles(ts,n=4,method="inclusive")
        stats[l]={"processes":len(ts),"sum":round(sum(ts),3),"q1":round(q[0],3),"median":round(statistics.median(ts),3),"q3":round(q[2],3),"max":max(ts)}
    write(P/"scores.json",{"wall_seconds":src["wall_seconds"],"cases":cases,"candidates":mut,"cost":stats})
    print([(q["case"],q["selected"],q["both_ok"],q["grey_killed"],q["gold_inputs"],q["gold_failures"]) for q in cases])
if __name__=="__main__":main()
