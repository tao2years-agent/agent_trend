import hashlib,io,json,re,tarfile
from datetime import datetime,timezone
from ingest import P,RAW,CACHE,freeze,sha,HF
from pathlib import Path
def main():
    c=json.loads((P/"cohort.json").read_bytes()); rows=[]
    def index(case,path,url,role,location=None):
        rows.append({"case":case,"path":str(path.relative_to(P)).replace(chr(92),"/"),"url":url,"role":role,"sha256":sha(path.read_bytes()),"location":location})
    index("cohort",RAW/"verified.parquet",c["source"],"official 500-row release")
    index("cohort",RAW/"dataset-card.md",f"https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/raw/{HF}/README.md","official dataset card")
    for r in c["selected"]:
        key=r["instance_id"];d=RAW/key;commit=r["base_commit"];f=d/"pr-body.json"; pr=json.loads(f.read_bytes());nums=pr["issue_references_in_closing_phrases"];assert len(nums)==1
        index(key,f,r["pull_request_url"],"upstream PR closing-issue statement")
        index(key,d/"problem_statement.md","https://github.com/sympy/sympy/issues/"+str(nums[0]),"benchmark problem statement mapped to upstream issue",r["row_index_zero_based"])
        for n in ("patch.diff","test_patch.diff"):index(key,d/n,c["source"],n,r["row_index_zero_based"])
        patchpaths=set(re.findall(r"^diff --git a/(\S+)",(d/"patch.diff").read_text(encoding="utf8")+(d/"test_patch.diff").read_text(encoding="utf8"),re.M))
        archive=CACHE/(commit+".tar.gz")
        assert sha(archive.read_bytes())==r["archive_sha256"]
        with tarfile.open(archive) as t:
            for path in sorted(patchpaths):
                try:src=t.extractfile("sympy-"+commit+"/"+path)
                except KeyError:continue
                dest=d/"base"/path;freeze(dest,src.read())
                index(key,dest,f"https://github.com/sympy/sympy/blob/{commit}/{path}","unmodified base file")
    (P/"sources.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding="utf8")
    print(len(rows),"sources")
if __name__=="__main__":main()
