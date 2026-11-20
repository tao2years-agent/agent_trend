import argparse,json,os,subprocess
from pathlib import Path
from candidates import P,O,read,write,checkout,apply
CHILD=r"""
from sympy import symbols,Symbol,sqrt
import os,json
from pathlib import Path
import sympy
assert os.path.normcase(str(Path.cwd())) in os.path.normcase(sympy.__file__)
values={}
for f in ("positive","integer","real","nonnegative",None):
    opts={f:True} if f else {}
    v=symbols(("x:2","y:2"),cls=Symbol,**opts)
    flat=[s for group in v for s in group]
    values[f or "control"]={"names":[s.name for s in flat],"explicit_assumptions":[getattr(s,"is_"+f) for s in flat] if f else [],"sqrt_square_equals_self":[sqrt(s**2)==s for s in flat] if f=="positive" else []}
print(json.dumps(values))
"""
def main(exe):
    c=next(x for x in read(O/"cohort.json")["selected"] if x["instance_id"].endswith("23534"));key=c["instance_id"];root=checkout(c,False);obs=[]
    env=dict(os.environ);env["PYTHONNOUSERSITE"]="1";env["PYTHONDONTWRITEBYTECODE"]="1"
    for tag in ["base","gold","V168a02a26183"]:
        if tag=="gold":apply(root,O/"raw"/key/"patch.diff")
        elif tag.startswith("V"):apply(root,P/"patches"/key/(tag+".diff"))
        output=subprocess.check_output([exe,"-c",CHILD],cwd=root,env=env,text=True,timeout=60)
        obs.append({"version":tag,"results":json.loads(output)})
    write(P/"extension-results.json",obs)
    print([(r["version"],r["results"]["positive"]) for r in obs])
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--python",required=True);a=ap.parse_args();main(a.python)
