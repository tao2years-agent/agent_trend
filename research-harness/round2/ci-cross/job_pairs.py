from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
import bisect,hashlib,json
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from range_counts import RAW,P,metas,parse,ranges,fetch,Fragments,dump
def fields(t,g):
    m=metas[t];j=m.schema.names.index("check_suite_id");col=m.row_group(g).column(j);a=col.dictionary_page_offset if col.has_dictionary_page else col.data_page_offset
    return int(col.statistics.min),int(col.statistics.max),[a,a+col.total_compressed_size-1,["check_suite_id"]]
def selected(t,g,bands):
    lo,hi,part=fields(t,g)
    key=fetch(t,g,part)
    parts=[key]+[fetch(t,g,r) for r in ranges(t,g)]
    tab=pq.ParquetFile(Fragments(t,parts),metadata=metas[t],pre_buffer=False).read_row_group(g,columns=["check_suite_id","conclusion"]+(["run_attempt"] if t=="runs" else []))
    keys=tab["check_suite_id"];cond=None
    for a,b in bands:
        ok=pc.and_(pc.greater_equal(keys,a),pc.less_equal(keys,b));cond=ok if cond is None else pc.or_(cond,ok)
    return key,tab.filter(cond).to_pylist()
def main():
    for t in ("runs","jobs"):metas[t]=parse(t)
    spans=[fields("runs",g) for g in range(metas["runs"].num_row_groups)]
    low=min(a for a,b,r in spans);high=max(b for a,b,r in spans);bands=[(low+(high-low)*k//10,low+(high-low)*k//10+999999) for k in (1,5,9)]
    runs={};jobs=defaultdict(Counter);dups=set();refs=[];c=Counter()
    todo=[]
    for t,md in metas.items():
        for g in range(md.num_row_groups):
            a,b,_=fields(t,g)
            if any(a<=y and b>=x for x,y in bands):todo.append((t,g))
    with ThreadPoolExecutor(5) as ex:
        fs={ex.submit(selected,t,g,bands):(t,g) for t,g in todo}
        for f in as_completed(fs):
            t,g=fs[f];key,rows=f.result();refs.append(key);c[t+"_rows"]+=len(rows)
            for row in rows:
                suite=int(row["check_suite_id"]);con=(row["conclusion"] or "NULL").lower()
                if t=="jobs":jobs[suite][con]+=1
                else:
                    if suite in runs:dups.add(suite)
                    runs[suite]=(con,row["run_attempt"])
    def count_band(lo,hi):
        stats=Counter();cube=defaultdict(Counter);jcount=Counter();unmatched=Counter()
        for suite,(con,att) in runs.items():
            if not lo<=suite<=hi:continue
            stats["run_suites"]+=1
            if suite in dups:stats["excluded_ambiguous"]+=1;continue
            jj=jobs.get(suite)
            if not jj:stats["run_without_job"]+=1;unmatched[con]+=1;continue
            stats["matched_runs"]+=1;stats["matched_job_rows"]+=sum(jj.values());jcount.update(jj)
            for key in ("all",("retried" if att and att>1 else "first_only")+"/"+con,con):
                cube[key]["runs"]+=1;cube[key]["job_rows"]+=sum(jj.values());cube[key]["with_failed_job"]+=bool(jj["failure"])
                cube[key]["with_success_job"]+=bool(jj["success"]);cube[key]["with_both_failed_and_success_jobs"]+=bool(jj["failure"] and jj["success"]);cube[key]["all_jobs_failed"]+=sum(jj.values())==jj["failure"]
        stats["job_suites_without_run"]=sum(1 for s in jobs if lo<=s<=hi and s not in runs)
        return {"coverage":dict(stats),"by_workflow_final_state":dict(cube),"matched_job_conclusions":dict(jcount),"run_without_job_states":dict(unmatched)}
    result={"bands":bands,"new_groups":len(todo),"checked_key_bytes":sum(r["end"]-r["start"]+1 for r in refs),"rows_scanned_within_bands":dict(c),"total":count_band(low,high),"by_band":[count_band(a,b) for a,b in bands]}
    dump(P/"job-pairs.json",result);dump(RAW/"suite-id-range-hashes.json",sorted(refs,key=lambda x:(x["table"],x["group"])))
    print(result['total'],flush=True)
if __name__=="__main__":main()
