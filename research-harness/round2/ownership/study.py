"""Strict temporal split. No login, repo id, PR id, or reviewer pseudonym leaves memory."""
from pathlib import Path
from collections import Counter,defaultdict
from bisect import bisect_left
from functools import lru_cache
import hashlib,json,sys
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/"empirical"))
from ingest import parquet,CACHE
RAW=P.parent/"empirical"/"raw"
SHA="b8dc67df93e7c11f6f20c84129db7232eb1ec253"
LOCK="b514ce21f168eff137a3099f6f6ce61c101f2e4095332e12c9c31a62ca6db10e"
DAY=86400*1_000_000_000
C0=pd.Timestamp("2026-02-01",tz="UTC").value
C1=pd.Timestamp("2026-03-01",tz="UTC").value
RULES=["F","R","P","G","B"]
def write(name,obj):
    (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf8")
def labeltime(series):
    return pd.to_datetime(series,utc=True,format="mixed",errors="raise").astype("datetime64[ns, UTC]").astype("int64")
@lru_cache(None)
def opaque(login):
    return int.from_bytes(hashlib.sha256(("ownership-v1|"+login).encode()).digest()[:12],"big")
def load():
    assert hashlib.sha256((P/"protocol.md").read_bytes()).hexdigest()==LOCK
    lock=json.loads((RAW/"ranges.json").read_bytes());assert lock["revision"]==SHA
    cols={"pull_request":["id","repo_id","created_at"],"pr_reviews":["id","pr_id","user","user_type","state","submitted_at"]}
    manifest=[r for r in lock["ranges"] if r["column"] in cols.get(r["table"],[])]
    for r in manifest:
        assert hashlib.sha256((CACHE/r["table"]/f"{r['start']}-{r['end']}.bin").read_bytes()).hexdigest()==r["sha256"]
    p=parquet("pull_request",manifest).read(columns=cols["pull_request"]).to_pandas().drop_duplicates()
    assert not p.id.duplicated().any() and p[["id","repo_id","created_at"]].notna().all().all()
    p["t"]=labeltime(p.created_at)
    tests=p[p.t.between(C0,C1,inclusive="left")][["t","id","repo_id"]].sort_values(["t","id"]);assert tests.t.max()+30*DAY < pd.Timestamp("2026-04-01",tz="UTC").value
    reviews=parquet("pr_reviews",manifest).read(columns=cols["pr_reviews"]).to_pandas().drop_duplicates();assert not reviews.id.duplicated().any()
    count=len(reviews);login=reviews.user.fillna("").str.casefold()
    flags=reviews.user_type.fillna("").str.casefold().eq("user")&login.ne("")&~login.str.contains(r"\[bot\]$|(?:^|[-_])(?:bot|automation)(?:$|[-_])",regex=True)&~login.isin(["claude","claude-code","cursor-agent","devin-ai","devin-ai-integration","copilot","openai-codex","google-labs-jules"])
    reviews=reviews[flags & reviews.state.str.upper().isin(["APPROVED","CHANGES_REQUESTED"]) & reviews.submitted_at.notna()].copy()
    reviews["u"]=[opaque(u.casefold()) for u in reviews.user]
    reviews["t"]=labeltime(reviews.submitted_at);left=reviews.merge(p[["id","repo_id","t"]].rename(columns={"id":"pr_id","t":"opened"}),on="pr_id",how="inner",validate="many_to_one")
    data=left[left.t>=left.opened].sort_values(["t","id"])
    obs=list(data[["t","id","pr_id","repo_id","u"]].itertuples(index=False,name=None))
    return list(tests.itertuples(index=False,name=None)),obs,{"source_prs":len(p),"source_review_rows":count,"usable_joined_formal_person_events_all_snapshot":len(data),"unmatched_formal_rows":len(reviews)-len(left),"invalid_before_open":len(left)-len(data),"data_column_ranges_checked":len(manifest),"data_column_bytes":sum(r["end"]-r["start"]+1 for r in manifest)}

class Repo:
    def __init__(self):
        self.users={};self.prs=set();self.seen=set();self._ranks=None
    def observe(self,t,p,u):
        first=p not in self.prs;self.prs.add(p)
        a=self.users.setdefault(u,[0,0,0,0])
        if (p,u) not in self.seen:self.seen.add((p,u));a[0]+=1
        a[1]=t
        if first:a[2]+=1;a[3]=t
        self._ranks=None
    def ranks(self):
        if self._ranks is None:
            d=self.users
            f=sorted(d,key=lambda u:(-d[u][0],-d[u][1],u))
            r=sorted(d,key=lambda u:(-d[u][1],-d[u][0],u))
            p=sorted((u for u in d if d[u][2]),key=lambda u:(-d[u][2],-d[u][3],u))
            g=[u for u in f if d[u][0]>=2]
            self._ranks=(f[:3],r[:3],p[:3],g)
        return self._ranks
def predict(tests,events,mode):
    repos={};index=0;recommend=[];day=None;load=Counter();max_peak=0
    history_bounds=[]
    for t,p,repo in tests:
        cutoff=C0 if mode=="frozen" else t
        while index<len(events) and events[index][0]<cutoff:
            et,_,ep,er,u=events[index]
            obj=repos.get(er)
            if obj is None:repos[er]=obj=Repo()
            obj.observe(et,ep,u);index+=1
        assert not index or events[index-1][0]<cutoff
        assert index==len(events) or events[index][0]>=cutoff
        if t//DAY!=day:load.clear();day=t//DAY
        o=repos.get(repo)
        if o:
            f,r,first,g=o.ranks()
            b=[]
            for u in g:
                if load[u]<3:b.append(u)
                if len(b)==3:break
            if b:load[b[0]]+=1;max_peak=max(max_peak,load[b[0]])
            preds=(tuple(f),tuple(r),tuple(first),tuple(g[:3]),tuple(b))
        else:preds=((),)*5
        recommend.append((len(o.prs) if o else 0,preds))
    assert max_peak<=3
    return recommend,{"train_events_before_final_prediction":index,"last_eligible_event_utc":pd.Timestamp(events[index-1][0],tz="UTC").isoformat(),"historical_repos_at_last_score":len(repos),"historical_accounts_at_last_score":len(set(u for r in repos.values() for u in r.users)),"historical_distinct_prs_at_last_score":sum(len(r.prs) for r in repos.values()),"budget_max_charged_in_day":max_peak}
def truth(tests,events):
    expected={p:t for t,p,_ in tests};labels={};amb=defaultdict(set)
    # Deliberately called after all predictions and budget ledgers have been constructed.
    for et,rid,p,repo,u in events:
        if p not in expected or et>expected[p]+30*DAY:continue
        if p not in labels:labels[p]=(et,u)
        if labels[p][0]==et:amb[p].add(u)
    return labels,amb
def evaluate(mode,tests,events,pred,labels,tie):
    # Build (repo,account)->earliest submission time to diagnose candidate reachability; no label enters predictions.
    earlier={}
    for et,_,_,repo,u in events:earlier.setdefault((repo,u),et)
    frames=[];daily=[]
    for ix,rule in enumerate(RULES):
        items=[]
        for (t,p,repo),(nh,ranks) in zip(tests,pred):
            rank=ranks[ix];lab=labels.get(p);target=lab[1] if lab else None
            sett=tie[p] if lab else set();cut=C0 if mode=="frozen" else t
            items.append((repo,int((t-C0)//DAY)+1,nh,1 if rank else 0,rank[0] if rank else -1,int(bool(lab)),int(bool(lab and lab[0]<=t+7*DAY)),int(bool(rank and target==rank[0])),int(target in rank),int(bool(lab and earlier.get((repo,target),10**30)<cut)),int(bool(sett.intersection(rank))),int(len(sett)>1),int(bool(rank and rank[0] in sett))))
        d=pd.DataFrame(items,columns=["repo","day","nh","routed","top","label","label7","hit1","hit3","reachable","hit3_ties","tie","hit1_ties"])
        for subset,q in [("all",d),("hist1",d[d.nh>=1]),("hist3",d[d.nh>=3]),("hist10",d[d.nh>=10])]:
            for horizon in ([30,7] if subset=="all" else [30]):
                a=q[q.label.eq(1) if horizon==30 else q.label7.eq(1)]
                b=a[a.routed.eq(1)]
                per=a.groupby("repo")[["hit1","hit3"]].mean()
                loads=q.loc[q.routed.eq(1)].groupby("top").size().sort_values(ascending=False)
                onday=q[q.routed.eq(1)].groupby(["day","top"]).size()
                metrics={"mode":mode,"policy":rule,"subset":subset,"horizon":horizon,"N":len(q),"R":q.repo.nunique(),"L":len(a),"U":len(q)-len(a),"LR":a.repo.nunique(),"routed":int(q.routed.sum()),"routed_labeled":len(b),"hits1":int(a.hit1.sum()),"hits3":int(a.hit3.sum()),"top1":a.hit1.mean(),"top3":a.hit3.mean(),"top1_cond":b.hit1.mean(),"top3_cond":b.hit3.mean(),"macro1":per.hit1.mean(),"macro3":per.hit3.mean(),"top10_share":loads.head(10).sum()/loads.sum(),"unique_recommended":len(loads),"peak_daily":int(onday.max()),"hhi":float(((loads/loads.sum())**2).sum()),"cold_prs":int(q.nh.eq(0).sum()),"cold_label":int(a.nh.eq(0).sum()),"reachable_label":int(a.reachable.sum()),"ties":int(a.tie.sum()),"tie_inclusive_1":int(a.hit1_ties.sum()),"tie_inclusive_3":int(a.hit3_ties.sum())}
                frames.append(metrics)
        for day,daily_frame in d.groupby("day"):
            a=daily_frame[daily_frame.label.eq(1)];daily.append(dict(mode=mode,policy=rule,day=day,prs=len(daily_frame),routed=int(daily_frame.routed.sum()),labeled=len(a),hits1=int(a.hit1.sum()),hits3=int(a.hit3.sum())))
    return frames,daily
def main():
    tests,events,source=load();predictions={};boundary={}
    for mode in ("frozen","rolling"):
        predictions[mode],boundary[mode]=predict(tests,events,mode)
    labels,tie=truth(tests,events)
    rows=[];daily=[]
    for mode in predictions:
        a,b=evaluate(mode,tests,events,predictions[mode],labels,tie);rows.extend(a);daily.extend(b)
    write("results.json",rows);write("by-day.json",daily)
    first=next(r for r in rows if r["mode"]=="frozen" and r["policy"]=="F" and r["subset"]=="all" and r["horizon"]==30)
    source.update({"revision":SHA,"protocol_sha256":LOCK,"n_prs":len(tests),"n_repos":len(set(t[2] for t in tests)),"n_label30":len(labels),"n_label7":sum(1 for t,p,_ in tests if p in labels and labels[p][0]<=t+7*DAY),"n_ambiguous_first_timestamp":sum(len(x)>1 for x in tie.values()),"bounds":boundary,"cold_repos":len({t[2] for t,(n,_) in zip(tests,predictions['frozen']) if n==0}),"jointly_cold_prs":first["cold_prs"]})
    write("coverage.json",source)
    print(source,flush=True)
if __name__=="__main__":main()
