"""Compare all agent pairs inside common repo-months, reusing hash-locked public columns."""
import itertools,json,re,sys
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/"empirical"))
from ingest import KEEP,parquet
locked=json.loads((R.parent/"empirical/raw/ranges.json").read_text("utf8"))["ranges"]
pr=parquet("pull_request",locked).read(columns=KEEP["pull_request"],use_threads=False).to_pandas().drop_duplicates()
assert not pr.id.duplicated().any()
for c in ["created_at","closed_at","merged_at"]:pr[c]=pd.to_datetime(pr[c],utc=True,format="mixed")
pr=pr[pr.created_at.between(pd.Timestamp("2025-12-01",tz="UTC"),pd.Timestamp("2026-03-01",tz="UTC"),inclusive="left")].set_index("id")
pr["month"]=pr.created_at.dt.strftime("%Y-%m")
end=pr.created_at+pd.Timedelta(days=30)
pr["merged"]=(pr.merged_at<=end)
pr["closed"]=(pr.closed_at<=end)&(~pr.merged)
deciders=set()
pf=parquet("pr_reviews",locked)
for i in range(pf.num_row_groups):
    rv=pf.read_row_group(i,columns=["pr_id","state","submitted_at","user","user_type"],use_threads=False).to_pandas()
    rv=rv[rv.pr_id.isin(pr.index)&rv.state.str.upper().isin(["APPROVED","CHANGES_REQUESTED"])].copy()
    name=rv.user.fillna("").str.lower()
    keep=rv.user_type.fillna("").str.casefold().eq("user")&name.ne("")&~name.str.contains(r"\[bot\]$|(?:^|[-_])(?:bot|automation)(?:$|[-_])",regex=True)&~name.isin(["claude","claude-code","cursor-agent","devin-ai","devin-ai-integration","copilot","openai-codex","google-labs-jules"])
    rv=rv[keep]
    d=(pd.to_datetime(rv.submitted_at,utc=True,format="mixed")-rv.pr_id.map(pr.created_at)).dt.total_seconds()
    deciders.update(rv.loc[d.between(0,30*24*3600),"pr_id"])
pr["decision"]=pr.index.isin(deciders)
def agg(df,keys):return df.groupby(keys).agg(n=("merged","size"),merged=("merged","sum"),closed=("closed","sum"),decision=("decision","sum"))
counts=agg(pr,["month","agent"])
counts.to_csv(R/"months.csv")
v=agg(pr,["agent","month","repo_id"])
overall=agg(pr,["agent"])
rows=[]
for a,b in itertools.combinations(sorted(pr.agent.unique()),2):
    ab=v.loc[a].join(v.loc[b],how="inner",lsuffix="_a",rsuffix="_b")
    for k in (2,5,10):
        sub=ab[(ab.n_a>=k)&(ab.n_b>=k)]
        row=dict(first=a,second=b,minimum=k,shared_repo_months=len(sub),shared_repositories=sub.index.get_level_values("repo_id").nunique(),coverage_first=sub.n_a.sum()/overall.loc[a,"n"],coverage_second=sub.n_b.sum()/overall.loc[b,"n"])
        for val in ("merged","decision"):
            row[val+"_all_pp"]=100*(overall.loc[a,val]/overall.loc[a,"n"]-overall.loc[b,val]/overall.loc[b,"n"])
            row[val+"_common_equal_pp"]=100*(sub[val+"_a"]/sub.n_a-sub[val+"_b"]/sub.n_b).mean()
        rows.append(row)
pd.DataFrame(rows).to_csv(R/"all-pairs.csv",index=False)
audit=dict(total=len(pr),repos=pr.repo_id.nunique(),merged=int(pr.merged.sum()),closed=int(pr.closed.sum()),no_terminal=int((~(pr.merged|pr.closed)).sum()),formal_observed=int(pr.decision.sum()),dec_months=counts.groupby(level=0).sum().to_dict("index"))
(R/"audit.json").write_text(json.dumps(audit,indent=2),encoding="utf8")
print(audit)
