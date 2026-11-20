"""Minimal counterexamples against fresh checkouts in a second Python environment."""
import argparse,json,os,subprocess,sys
from pathlib import Path
from candidates import P,O,read,write,checkout,apply
CHILD=r"""
import json,os
from pathlib import Path
import sympy
assert os.path.normcase(str(Path.cwd())) in os.path.normcase(sympy.__file__)
from sympy import Point,I,Rational,lambdify
import sys
if sys.argv[1]=="point":
    try:
        p=Point(-1-2*I/3,1); observed={"result":"accepted","value":str(p)}
    except ValueError as exc:observed={"result":"rejected","exception":type(exc).__name__,"message":str(exc)}
else:
    try:
        val=lambdify([],(),modules="math")(); observed={"result":"returned","value":repr(val)}
    except SyntaxError as exc:observed={"result":"error","exception":type(exc).__name__,"generated_line":exc.text.strip() if exc.text else None,"offset":exc.offset}
print(json.dumps({"version":sys.version,"sympy_version":sympy.__version__,"observation":observed}))
"""
def main(exe):
    rows=[];env=dict(os.environ);env["PYTHONDONTWRITEBYTECODE"]="1";env["PYTHONNOUSERSITE"]="1"
    for meta in read(O/"cohort.json")["selected"]:
        key=meta["instance_id"]
        if key.endswith("-22714"):
            path=checkout(meta,True)
            versions=["gold","Ve63126860e55"];op="point"
        elif key.endswith("-23262"):
            path=checkout(meta,False);versions=["base","gold"];op="tuple"
        else:continue
        for i,ver in enumerate(versions):
            if i and ver=="gold":apply(path,O/"raw"/key/"patch.diff")
            if i and ver.startswith("V"):apply(path,P/"patches"/key/(ver+".diff"))
            output=subprocess.check_output([exe,"-c",CHILD,op],cwd=path,env=env,text=True,timeout=60);r=json.loads(output)
            rows.append({"case":key,"version":ver,"probe":op,**{"interpreter":r["version"],"sympy_version":r["sympy_version"],"observation":r["observation"]}})
    write(P/"witnesses.json",rows)
    print([(r["version"],r["observation"]) for r in rows])
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--python",default=sys.executable);a=ap.parse_args();main(a.python)
