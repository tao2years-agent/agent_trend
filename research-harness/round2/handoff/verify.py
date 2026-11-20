"""Offline verification, using only stdlib and the evidence previously saved."""
from pathlib import Path
import hashlib
import json
from itertools import product
ROOT=Path(__file__).resolve().parent
read=lambda p: json.loads((ROOT/p).read_bytes())
def main():
    sources=read("sources.json")
    for s in sources:
        if "path" in s:assert hashlib.sha256((ROOT/s["path"]).read_bytes()).hexdigest()==s["sha256"]
    primary=read("evidence/observations.json")
    def verify(rows):
        cells={}
        for row in rows:
            engine,case,guard=key=(row["engine"],row["scenario"],row["guarded"])
            assert key not in cells
            want="held_stale" if guard and case=="stale" else "held_request" if guard and case=="duplicate" else "published"
            count=0 if want!="published" else 2 if case=="lost" and not guard else 1
            assert row["effects"]==(["v2"] if case=="stale" and not guard else ["v1"]*count)
            assert row["status"]==want
            inv=row["invocations"]
            if case=="lost":
                assert [i["verdict"] for i in inv]==["insert","reuse" if guard else "insert"]
                assert len({i["pid"] for i in inv})==2
            if engine=="temporal":
                workers=row["runtime_worker_pids"]
                assert len(set(workers))==len(workers)==2+(case=="lost")
                assert all(x["pid"] in workers[1:] for x in inv)
                if case=="lost":
                    assert [e["attempt"] for e in row["history"] if "attempt" in e]==[2]
            else:
                assert len(set(e["pid"] for e in row["steps"]))==len(row["steps"])
                assert row["steps"][0]["state"]["interrupts"][0]["request"]=="R1"
            cells[key]=(row["status"],row["effects"])
        assert set(cells)==set(product(("langgraph","temporal"),("resume","duplicate","stale","lost"),(True,False)))
        return cells
    a=verify(primary["runs"])
    repeat=read("evidence/repeat/observations.json")
    assert repeat.get("finished_utc") and verify(repeat["runs"])==a
    n=read("evidence/native.json")
    assert n["langgraph"]["R1"]!=n["langgraph"]["R2"]
    assert n["langgraph"]["duplicate_old_interrupt"]["interrupt_ids"]==[n["langgraph"]["R2"]]
    assert n["temporal"]["gate_after_repeat"]==2 and len(n["temporal"]["signal_event_ids"])==2
    assert all(v["before_valid_R2"]["effects"]==[] and v["target"]["effects"]==["v1"] for v in n.values())
    print("16 matrix cells x 2 fresh runs plus 2 native controls; 9 raw source hashes verified.")
if __name__=="__main__": main()
