"""Only inspect whether there is a usable requested reviewer at PR-creation time."""
from pathlib import Path
import json,sys
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import pyarrow.compute as pc
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/"empirical"))
from ingest import pull,parquet,metadata
raw=P.parent/"empirical"/"raw"; manifest=json.loads((raw/"ranges.json").read_bytes())["ranges"]
md=metadata("pr_timeline");pieces=[];j=md.schema.names.index("assignee")
for i in range(md.num_row_groups):
    c=md.row_group(i).column(j);offset=c.dictionary_page_offset if c.has_dictionary_page else c.data_page_offset
    pieces.append(dict(table="pr_timeline",group=i,column="assignee",start=offset,end=offset+c.total_compressed_size-1))
with ThreadPoolExecutor(8) as ex:locked=list(ex.map(pull,pieces))
(P/"raw"/"assignee-ranges.json").write_text(json.dumps(locked,indent=2),encoding="utf8")
pr=parquet("pull_request",manifest).read(columns=["id","created_at"]).to_pandas()
pr["dt"]=pd.to_datetime(pr.created_at,utc=True,format="mixed"); eligible=pr[pr.dt.between(pd.Timestamp("2026-02-01",tz="UTC"),pd.Timestamp("2026-03-01",tz="UTC"),inclusive="left")].set_index("id").dt
pf=parquet("pr_timeline",manifest+locked)
count={k:0 for k in ("requested_events","non_null_assignee","before_creation","same_creation_time","before_or_equal_with_assignee")}
for i in range(pf.num_row_groups):
    a=pf.read_row_group(i,columns=["pr_id","event","created_at","assignee"])
    event=pc.utf8_lower(pc.cast(a["event"],"string"));mask=pc.match_substring_regex(event,"review.?requested(?:event)?$")
    x=a.filter(mask).to_pandas();x=x[x.pr_id.isin(eligible.index)]
    if not len(x):continue
    dt=pd.to_datetime(x.created_at,utc=True,format="mixed",errors="coerce");t=x.pr_id.map(eligible)
    avail=x.assignee.notna() & x.assignee.fillna("").ne("")
    count["requested_events"]+=len(x);count["non_null_assignee"]+=int(avail.sum());count["before_creation"]+=int((dt<t).sum());count["same_creation_time"]+=int((dt==t).sum());count["before_or_equal_with_assignee"]+=int((avail&(dt<=t)).sum())
count["additional_bytes"]=sum(r["end"]-r["start"]+1 for r in locked)
(P/"request-field-audit.json").write_text(json.dumps(count,indent=2),encoding="utf8")
print(count)
