from collections import Counter
import json
from pathlib import Path
P=Path(__file__).resolve().parent
def read(p):return json.loads((P/p).read_bytes())
def collect():
    accu={"runs":Counter(),"jobs":Counter()};groups={"runs":set(),"jobs":set()};ranges=[];cells=Counter()
    for f in (P/"aggregates").glob("*/*.json"):
        r=json.loads(f.read_bytes());t=r["table"];assert r["group"] not in groups[t];groups[t].add(r["group"]);assert sum(x["count_all"] for x in r["frequencies"])==r["rows"]
        ranges.extend(r["ranges"])
        for q in r["frequencies"]:
            a=q.get("run_attempt");con=(q["conclusion"] or "unknown").lower();s=(q["status"] or "unknown").lower();n=q["count_all"]
            accu[t]["all"]+=n;accu[t]["status/"+s]+=n;accu[t]["conclusion/"+con]+=n
            if t=="runs":
                group="attempt_1" if a==1 else "attempt_gt_1" if a is not None and a>1 else "invalid_attempt"
                accu[t][group]+=n;accu[t][group+"/"+con]+=n
                if s=="completed":accu[t]["completed/"+group+"/"+con]+=n
                cells[str(a)]+=n
    assert [len(groups[k]) for k in ("runs","jobs")]==[139,222]
    assert accu["runs"]["all"]==130338516 and accu["jobs"]["all"]==221534997
    o={"coverage":{"tables":{k:{"groups":len(v),"rows":accu[k]["all"]} for k,v in groups.items()},"locked_column_ranges":len(ranges),"compressed_selected_bytes":sum(r["end"]-r["start"]+1 for r in ranges)},"runs":dict(accu["runs"]),"jobs":dict(accu["jobs"]),"attempt_frequency":dict(cells)}
    (P/"census.json").write_text(json.dumps(o,indent=2),encoding="utf8")
    return o
if __name__=="__main__":
    o=collect();print(o["coverage"])
    print({k:v for k,v in o["runs"].items() if k in ("attempt_1","attempt_gt_1","attempt_1/failure","attempt_gt_1/failure","attempt_gt_1/success","conclusion/failure","status/completed","invalid_attempt")})
    print({k:v for k,v in o["jobs"].items() if k.startswith("conclusion/")})
