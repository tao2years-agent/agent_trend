"""Fetch only public categorical Parquet column ranges, no logs, paths, names, or code."""
import argparse,hashlib,io,json,os,random,threading,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import pyarrow.parquet as pq
import requests
P=Path(__file__).resolve().parent
RAW=P/"raw";CACHE=Path(os.environ.get("CI_CROSS_CACHE",str(Path(os.environ.get("TEMP","/tmp"))/"gha-cross-20261120")))/"columns"
record=json.loads((RAW/"gharuns-zenodo.json").read_bytes());sources={r["key"].split(".")[0]:r for r in record["files"] if r["key"].endswith(".parquet")}
locks={};metas={};local=threading.local()
def digest(b):return hashlib.sha256(b).hexdigest()
def dump(f,j):f.write_text(json.dumps(j,indent=2),encoding="utf8")
def parse(table):return pq.read_metadata(io.BytesIO(b'PAR1'+(RAW/(table+".parquet.footer")).read_bytes()))
def ranges(table,group):
    md=metas[table];names=["status","conclusion"]+ (["run_attempt"] if table=="runs" else [])
    pairs=[]
    for n in names:
        c=md.row_group(group).column(md.schema.names.index(n));a=c.dictionary_page_offset if c.has_dictionary_page else c.data_page_offset
        pairs.append([a,a+c.total_compressed_size-1,[n]])
    pairs.sort()
    merged=[]
    for a,b,cols in pairs:
        if merged and merged[-1][1]+1==a:merged[-1][1]=b;merged[-1][2]+=cols
        else:merged.append([a,b,cols])
    return merged
def fetch(table,group,r):
    a,b,cols=r;f=CACHE/table/f"{a}-{b}.bin";f.parent.mkdir(parents=True,exist_ok=True)
    if not f.exists():
        u=sources[table]["links"]["self"]+f"?slice={a}-{b}"
        for attempt in range(7):
            try:
                k=attempt%2
                if not hasattr(local,"sessions"):local.sessions={}
                if k not in local.sessions:local.sessions[k]=requests.Session();local.sessions[k].trust_env=k==0
                s=local.sessions[k]
                with s.get(u,headers={"Range":f"bytes={a}-{b}","Accept-Encoding":"identity"},stream=True,timeout=(12,35)) as resp:
                    if resp.status_code in (429,503):
                        time.sleep(min(55,float(resp.headers.get("Retry-After","3"))) if resp.headers.get("Retry-After","3").isdigit() else 3);resp.raise_for_status()
                    assert resp.status_code==206 and resp.headers["Content-Range"]==f"bytes {a}-{b}/{sources[table]['size']}",(resp.status_code,resp.headers.get("Content-Range"))
                    body=resp.content
                assert len(body)==b-a+1;f.write_bytes(body);break
            except Exception:
                if attempt==6:raise
                time.sleep(min(8,1+attempt))
    raw=f.read_bytes();assert len(raw)==b-a+1
    return {"table":table,"group":group,"columns":cols,"start":a,"end":b,"sha256":digest(raw)}
class Fragments(io.RawIOBase):
    def __init__(self,table,available):self.table=table;self.rs=available;self.pos=0;self.size=sources[table]['size']
    def readable(self):return True
    def seekable(self):return True
    def tell(self):return self.pos
    def seek(self,off,whence=0):
        self.pos=off if whence==0 else self.pos+off if whence==1 else self.size+off;return self.pos
    def read(self,n=-1):
        a=self.pos;end=a+n
        for r in self.rs:
            if r["start"]<=a and end-1<=r["end"]:
                with open(CACHE/self.table/f"{r['start']}-{r['end']}.bin","rb") as f:
                    f.seek(a-r["start"]);b=f.read(n)
                self.pos+=len(b);return b
        raise IOError(("Read outside locked categorical columns",self.table,a,n))
def aggregate(table,g):
    locked=[fetch(table,g,r) for r in ranges(table,g)]
    pf=pq.ParquetFile(Fragments(table,locked),metadata=metas[table],pre_buffer=False)
    cols=["status","conclusion"]+(["run_attempt"] if table=="runs" else [])
    tab=pf.read_row_group(g,columns=cols,use_threads=False)
    h=tab.group_by(cols,use_threads=False).aggregate([([],"count_all")]).to_pylist()
    assert sum(i["count_all"] for i in h)==metas[table].row_group(g).num_rows
    return {"table":table,"group":g,"rows":tab.num_rows,"frequencies":h,"ranges":locked}
def main():
    for table in ["runs","jobs"]:metas[table]=parse(table)
    a=[];b=[]
    for t,m in metas.items():
        ids=sorted(range(m.num_row_groups),key=lambda n:digest(f"CI-CROSS-20261120|{t}|{n}".encode()))
        a += [(t,g) for g in ids[:24]];b += [(t,g) for g in ids[24:]]
    for label,items in [("pilot",a),("all-rest",b)]:
        rows=[];target=P/"aggregates"/label;target.mkdir(parents=True,exist_ok=True)
        with ThreadPoolExecutor(8) as ex:
            tasks={ex.submit(aggregate,t,g):(t,g) for t,g in items}
            for v in as_completed(tasks):
                t,g=tasks[v]
                try:
                    o=v.result();dump(target/f"{t}-{g}.json",o);rows.append(o)
                except Exception as e:
                    print("FAILED",t,g,repr(e)[:150],flush=True);continue
                if len(rows)%30==0:print(label,len(rows),len(items),flush=True)
        print("phase",label,len(rows),len(items),flush=True)
if __name__=="__main__":main()
