"""Fetch fixed public benchmark shard and the predeclared SymPy cases."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,io,json,os,pathlib,re,tarfile,tempfile,time
import pyarrow.parquet as pq
import requests
P=pathlib.Path(__file__).resolve().parent
RAW=P/"raw"
CACHE=pathlib.Path(os.environ.get("ORACLE_CACHE",str(pathlib.Path(tempfile.gettempdir())/"verified-sympy-20261120")))
HF="c104f840cc67f8b6eec6f759ebc8b2693d585d4a"
SHARD_SHA="a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd"
URL=f"https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/resolve/{HF}/data/test-00000-of-00001.parquet"
def sha(b):return hashlib.sha256(b).hexdigest()
def get(url):
    for i in range(6):
        try:
            with requests.Session() as s:
                s.trust_env=(i%2==0)
                resp=s.get(url,timeout=65);resp.raise_for_status();return resp.content
        except requests.RequestException:
            if i==5:raise
def freeze(path,b):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():assert path.read_bytes()==b,path
    else:path.write_bytes(b)
def obtain(row):
    commit=row["base_commit"]; key=row["instance_id"]; path=CACHE/f"{commit}.tar.gz"
    url=f"https://codeload.github.com/sympy/sympy/tar.gz/{commit}"
    if path.exists():archive=path.read_bytes()
    else:
        archive=get(url);freeze(path,archive)
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as t:
        members=t.getmembers()
        assert all(m.name.split("/")[0]=="sympy-"+commit for m in members)
    case=RAW/key
    for field in ("patch","test_patch","problem_statement"):
        freeze(case/(field+(".diff" if "patch" in field else ".md")),row[field].encode())
    rowidx=row.pop("row_index")
    info={k:row[k] for k in ("instance_id","repo","base_commit","environment_setup_commit","version","created_at","difficulty")}
    for k in ("FAIL_TO_PASS","PASS_TO_PASS"):info[k]=json.loads(row[k])
    info.update({"row_index_zero_based":rowidx,"archive_url":url,"archive_sha256":sha(archive),"archive_bytes":len(archive),"issue_url":row.get("issue_url"),"pull_request_url":f"https://github.com/sympy/sympy/pull/{key.split('-')[-1]}","base_url":f"https://github.com/sympy/sympy/tree/{commit}"})
    freeze(case/"metadata.json",json.dumps(info,indent=2).encode())
    return info
def main():
    RAW.mkdir(exist_ok=True);CACHE.mkdir(exist_ok=True)
    f=RAW/"verified.parquet";b=f.read_bytes() if f.exists() else get(URL)
    assert sha(b)==SHARD_SHA;freeze(f,b)
    rows=pq.read_table(io.BytesIO(b)).to_pylist()
    for i,r in enumerate(rows):r["row_index"]=i
    sym=[r for r in rows if r["repo"]=="sympy/sympy"]
    eligible=[r for r in sym if tuple(map(int,r["version"].split(".")[:2]))>=(1,10) and r["patch"] and r["test_patch"] and json.loads(r["FAIL_TO_PASS"]) and json.loads(r["PASS_TO_PASS"])]
    selected=sorted(eligible,key=lambda r:int(r["instance_id"].split("-")[-1]))[:8]
    assert len(selected)==8
    with ThreadPoolExecutor(4) as ex: cases=list(ex.map(obtain,selected))
    doc={"source":URL,"hf_revision":HF,"dataset_sha256":SHARD_SHA,"dataset_rows":len(rows),"sympy_rows":len(sym),"version_and_fields_eligible":len(eligible),"selected":cases,"method_sha256":sha((P/"preregister.md").read_bytes())}
    freeze(P/"cohort.json",json.dumps(doc,indent=2).encode())
    print([(x["instance_id"],x["archive_bytes"]) for x in cases])
if __name__=="__main__":main()
