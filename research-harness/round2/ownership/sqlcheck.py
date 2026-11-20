"""Independent aggregation in SQLite: raw PR/review metadata -> fixed holdout F ranks."""
import hashlib,json,re,sqlite3,sys
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/"empirical"))
from ingest import parquet
from functools import lru_cache
@lru_cache(None)
def code(user):
    return hashlib.sha256(("ownership-v1|"+user.lower()).encode()).hexdigest()[:24]
def epoch(t):
    if t is None:return None
    return int(datetime.fromisoformat(t.replace("Z","+00:00")).timestamp())
blocked={"claude","claude-code","cursor-agent","devin-ai","devin-ai-integration","copilot","openai-codex","google-labs-jules"}
pat=re.compile(r"\[bot\]$|(?:^|[-_])(?:bot|automation)(?:$|[-_])")
def select_user(u,ut,st):
    return u and ut and ut.lower()=="user" and st in {"APPROVED","CHANGES_REQUESTED"} and not pat.search(u.lower()) and u.lower() not in blocked
def main():
    man=json.loads((P.parent/"empirical/raw/ranges.json").read_bytes())["ranges"]
    con=sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE pr(id INTEGER PRIMARY KEY,repo INTEGER, created INTEGER);CREATE TABLE rv(id INTEGER PRIMARY KEY,pr_id INTEGER,u TEXT,submitted INTEGER);")
    pf=parquet("pull_request",man)
    for b in pf.iter_batches(columns=["id","repo_id","created_at"],batch_size=16000):
        a,b_,c=(x.to_pylist() for x in b.columns)
        con.executemany("INSERT INTO pr VALUES(?,?,?)",((x,y,epoch(z)) for x,y,z in zip(a,b_,c)))
    pf=parquet("pr_reviews",man)
    for batch in pf.iter_batches(columns=["id","pr_id","user","user_type","state","submitted_at"],batch_size=16000):
        cols=[x.to_pylist() for x in batch.columns]
        rows=((i,p,code(u),epoch(t)) for i,p,u,ut,st,t in zip(*cols) if t and select_user(u,ut,st))
        con.executemany("INSERT INTO rv VALUES(?,?,?,?)",rows)
    con.executescript("""
    CREATE INDEX event_pr ON rv(pr_id,submitted,id);
    CREATE TABLE h AS SELECT p.repo,r.u,COUNT(DISTINCT p.id) n,MAX(r.submitted) last_seen
      FROM rv r JOIN pr p ON r.pr_id=p.id WHERE r.submitted>=p.created AND r.submitted<unixepoch('2026-02-01') GROUP BY p.repo,r.u;
    CREATE TABLE f AS SELECT repo,u,row_number() OVER(PARTITION BY repo ORDER BY n DESC,last_seen DESC,u ASC) rank FROM h;
    CREATE INDEX f_repo ON f(repo,rank);
    CREATE TABLE test AS SELECT * FROM pr WHERE created>=unixepoch('2026-02-01') AND created<unixepoch('2026-03-01');
    CREATE TABLE truth AS SELECT p.id,p.repo,(
      SELECT u FROM rv r WHERE r.pr_id=p.id AND r.submitted BETWEEN p.created AND p.created+30*86400 ORDER BY r.submitted,r.id LIMIT 1) u FROM test p;
    """)
    names=["eligible","labeled","routed","hit1","hit3","cold_prs","seen_reviewer"]
    n=con.execute("""SELECT count(*),count(t.u),sum(exists(select 1 from f where f.repo=t.repo and rank=1)),
      sum(exists(select 1 from f where f.repo=t.repo and f.u=t.u and rank=1)),
      sum(exists(select 1 from f where f.repo=t.repo and f.u=t.u and rank<=3)),
      sum(not exists(select 1 from f where f.repo=t.repo and rank=1)),
      sum(exists(select 1 from f where f.repo=t.repo and f.u=t.u)) FROM truth t""").fetchone()
    val=dict(zip(names,n))
    frozen=next(i for i in json.loads((P/"results.json").read_bytes()) if (i["mode"],i["policy"],i["subset"],i["horizon"])==("frozen","F","all",30))
    for field,source in zip(names,["N","L","routed","hits1","hits3","cold_prs","reachable_label"]):assert val[field]==frozen[source],field
    obj={"engine":"stdlib SQLite "+sqlite3.sqlite_version,"comparison":"independent SQL window query versus Python chronological replay","exact_match":val}
    (P/"sql-check.json").write_text(json.dumps(obj,indent=2),encoding="utf8")
    print(obj)
if __name__=="__main__":main()
