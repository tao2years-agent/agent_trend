from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,requests
from candidates import O,P
def fetch(u):
    for i in range(4):
        try:
            with requests.Session() as s:
                s.trust_env=i%2==0
                r=s.get(u,timeout=27);r.raise_for_status();return r.content
        except requests.RequestException:
            if i==3:raise
def get(row):
    name,u=row;b=fetch(u);sha=hashlib.sha256(b).hexdigest()
    f=P/"raw"/(sha[:12]+"-"+name+".html");f.parent.mkdir(exist_ok=True)
    if not f.exists():f.write_bytes(b)
    assert hashlib.sha256(f.read_bytes()).hexdigest()==sha
    return {"purpose":name,"url":u,"path":f.relative_to(P).as_posix(),"sha256":sha,"retrieved_utc":datetime.now(timezone.utc).isoformat(),"role":"background documentation; never substitutes for the exact historical source"}
if __name__=="__main__":
    urls=[("python-3.11-expressions","https://docs.python.org/3.11/reference/expressions.html"),("points","https://docs.sympy.org/latest/modules/geometry/points.html"),("normalforms","https://docs.sympy.org/latest/modules/matrices/normalforms.html"),("lambdify","https://docs.sympy.org/latest/modules/utilities/lambdify.html")]
    with ThreadPoolExecutor(4) as ex:rows=list(ex.map(get,urls))
    f=O/"sources.json";rows.append({"purpose":"fixed original PRs, official benchmark rows, historical implementation and tests","path":"../oracles/sources.json","url":"https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/tree/c104f840cc67f8b6eec6f759ebc8b2693d585d4a","sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"count":len(json.loads(f.read_bytes()))})
    (P/"sources.json").write_text(json.dumps(rows,indent=2),encoding="utf8");print(len(rows))
