"""Recompute published transition sets. Native attempts and inferred repeated workflow runs remain separate."""
import ast,collections,csv,gzip,hashlib,io,json,math,os
from pathlib import Path
import requests
csv.field_size_limit(32*1024*1024)
P=Path(__file__).resolve().parent
SHA="080aa9edd5f54c4e9dc5675ea75bc0f545c37ff3"
CACHE=Path(os.getenv("CI_CROSS_CACHE",str(Path(os.getenv("TEMP","/tmp"))/"gha-cross-20261120")))/"huangdata"
files={"native":{"name":"dataframe_job_rerun_distinct_with_conclusion.csv.gz","sha256":"d91f6179d8cabdbbc94130b96eacdcaf49155a8f159d42a3bd751708238939d4","blob":"5c2e0e4ab05c728cb2d1c5e2329645a1812be164"},"inferred":{"name":"dataframe_workflow_rerun_distinct.csv.gz","sha256":"c50cddaf68e2cdfb1dc715ad17f36d0f605748ea54855437222710d67c4ea904","blob":"7fad2da5cebc9df8e581e8da8dc5cea31cda8111"}}
def write(f,x):(P/f).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf8")
def fetch(f):
    CACHE.mkdir(parents=True,exist_ok=True);dst=CACHE/f["name"]
    url=f"https://raw.githubusercontent.com/jiangnanpro/Reruns-of-GHA-workflow/{SHA}/data/dataframes/{f['name']}"
    if not dst.exists():
        r=requests.get(url,timeout=35);r.raise_for_status();dst.write_bytes(r.content)
    b=dst.read_bytes();assert hashlib.sha256(b).hexdigest()==f["sha256"] and hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()==f["blob"]
    return dst
def values(kind):
    sets={};ground=collections.Counter();expected=collections.Counter()
    with gzip.open(fetch(files[kind]),"rt",encoding="utf8",newline="") as src:
        for row in csv.DictReader(src):
            ids,out,ns,fs=map(ast.literal_eval,(row["reruns ids"],row["rerun conclusion"],row["reruns"],row["last rerun's conclusion"]))
            assert len(ids)==len(out)==len(ns)==len(fs)
            ground["group_rows"]+=1
            for rid,seq,num,last in zip(ids,out,ns,fs):
                k=rid if kind=="native" else tuple(rid)
                entry=(row["repo path"],tuple(seq),num,last)
                if k in sets:assert entry==sets[k];ground["dup_records"]+=1
                sets[k]=entry;ground["sets_rows"]+=1
                ground["published_final_success"]+=last=="success"
                expected[str(last)]+=1
    return sets,dict(ground),dict(expected)
def describe(kind,sets,ground,expected):
    first=collections.Counter();second=collections.Counter();last=collections.Counter();finalinfo=collections.Counter()
    repo=collections.defaultdict(list);q=collections.Counter();trans=collections.Counter();num_attempts=collections.Counter()
    for k,(org,seq,expected_retries,cached_last) in sets.items():
        finalinfo[str(cached_last)]+=1;num_attempts[str(expected_retries+1)]+=1
        q["outcome_length_mismatch"]+=len(seq)!=expected_retries+1
        q["nonempty_final_disagrees"]+=bool(seq) and cached_last!=seq[-1]
        q["missing_sequence"]+=not seq
        if not seq:continue
        first[str(seq[0])]+=1
        for a,b in zip(seq,seq[1:]):trans[str(a)+"->"+str(b)]+=1
        if len(seq)<2:continue
        q["start_success_second_failure"]+=seq[0]=="success" and seq[1]=="failure"
        q["observed_at_least_two"]+=1
        if seq[0]!="failure":continue
        q["start_failure"]+=1;second[str(seq[1])]+=1;last[str(seq[-1])]+=1
        q["first_red_ever_green"]+="success" in seq[1:]
        q["first_two_red_then_green"]+=seq[1]=="failure" and "success" in seq[2:]
        q["second_green_but_last_not_green"]+=seq[1]=="success" and seq[-1]!="success"
        if seq[1] in ("success","failure"):repo[org].append(int(seq[1]=="success"))
    return {"kind":kind,"groups_and_original_sets":ground,"published_final_states":expected,"unique_sets":len(sets),"unique_repos":len({v[0] for v in sets.values()}),"unique_final_states":dict(finalinfo),"initial_observed":dict(first),"all_observed_adjacent_transitions":dict(trans),"next_given_initial_failure":dict(second),"last_given_initial_failure":dict(last),"counts":dict(q),"nominal_length_histogram":dict(sorted(num_attempts.items(),key=lambda a:int(a[0]))),"macro_red_to_next_green":sum(sum(v)/len(v) for v in repo.values())/len(repo),"macro_repos":len(repo)}
def targets(sets,strict=False):
    return sorted((rid,org,s[1]=="success") for rid,(org,s,n,last) in sets.items() if len(s)>=2 and s[0]=="failure" and s[1] in ("success","failure") and (not strict or (len(s)==n+1 and s[-1]==last)))
def hold(eligible):
    n=len(eligible);a=n*6//10;b=n*8//10;train,dev,test=eligible[:a],eligible[a:b],eligible[b:]
    history=collections.defaultdict(list)
    for _,repo,val in train:history[repo].append(val)
    prior=sum(v for _,_,v in train)/len(train)
    scores={r:(sum(v)+20*prior)/(len(v)+20) for r,v in history.items()}
    out=[]
    def score(rows):return [(scores.get(r,prior),v) for _,r,v in rows]
    d=score(dev);t=score(test);devgreen=sum(y for _,y in d);testgreen=sum(y for _,y in t)
    for target in (0.90,.95,.99,1):
        threshold=0.0
        if target!=1:
            for cut in sorted(set(s for s,_ in d),reverse=True):
                if sum(y for s,y in d if s>=cut)/devgreen>=target:threshold=cut;break
        sent=[y for s,y in t if s>=threshold];skipped=[y for s,y in t if s<threshold]
        out.append({"target":target,"threshold":threshold,"dev_dispatched":sum(s>=threshold for s,_ in d),"dev_green_recall":sum(y for s,y in d if s>=threshold)/devgreen,"test_dispatched":len(sent),"saved_retries":len(skipped),"missed_green":sum(skipped),"avoided_red":len(skipped)-sum(skipped),"retained_green":sum(sent),"green_recall":sum(sent)/testgreen,"break_even_loss_over_cost":len(skipped)/sum(skipped) if sum(skipped) else None})
    return {"eligible":n,"train":len(train),"dev":len(dev),"test":len(test),"train_green":sum(v for _,_,v in train),"dev_green":devgreen,"test_green":testgreen,"holdout_repos":len({r for _,r,_ in test}),"cold_test":sum(r not in scores for _,r,_ in test),"train_repo_count":len(scores),"test_red":len(test)-testgreen,"policies":out}
def main():
    c={};holdouts={}
    for k in files:
        v,ground,last=values(k);c[k]=describe(k,v,ground,last)
        if k=="native":holdouts={"registered":hold(targets(v)),"complete_sequence_only":hold(targets(v,True))}
    write("transitions.json",c);write("holdout.json",holdouts)
    print([(k,r["unique_sets"],r["counts"]) for k,r in c.items()])
    print(holdouts["registered"])
if __name__=="__main__":main()
