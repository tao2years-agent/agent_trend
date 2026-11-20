import argparse,hashlib,json,os,subprocess,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as E
from candidates import P,O,read,write,apply,checkout
from run import command,counter
def module_results(xml):
    x={}
    if xml.exists():
        for n in E.parse(xml).findall(".//testcase"):
            k=n.get('classname','')+"::"+n.get('name','')
            state="passed"
            for child in n:
                if child.tag in ("error","failure","skipped"):
                    state="xfail" if "xfail" in child.get("type","") else child.tag;break
            x[k]=state
    return x
def group(args):
    meta,items,exe,dest,env=args;key=meta["instance_id"];root=checkout(meta)
    module={"sympy__sympy-22714":"sympy/geometry/tests","sympy__sympy-23413":"sympy/polys/matrices/tests"}[key]
    gold=None;out=[]
    by={m["id"]:m for c in read(P/"candidates.json") if c["case"]==key for m in c["changes"]}
    pristine={r["path"]:(root/r["path"]).read_bytes() for r in by.values()}
    for ident in ["gold"]+items:
        leaf=dest/key/ident;leaf.mkdir(parents=True)
        if ident!="gold":
            for n,b in pristine.items():(root/n).write_bytes(b)
            apply(root,P/"patches"/key/(ident+".diff"))
        xml=leaf/"all.xml"
        cmd=[exe,"-m","pytest","-q","-p","no:cacheprovider","--tb=short","--disable-warnings","--color=no","--junitxml="+str(xml),module]
        st=command(cmd,root,env,leaf/"all.txt",480);d=module_results(xml)
        if ident=="gold":gold=d
        contrasts=[{"node":k,"candidate":d[k],"gold":gold[k]} for k in d.keys() & gold.keys() if d[k]!=gold[k]]
        r=st|{"case":key,"id":ident,"package":module,"states":counter(xml),"compared":len(d.keys()&gold.keys()),"missing_in_candidate":sorted(gold.keys()-d.keys()),"consumed":len(d),"contrasts":sorted(contrasts,key=lambda v:v["node"])}
        print(key,ident,r["exit"],r["states"],r["elapsed_seconds"],flush=True)
        out.append(r);write(leaf/"result.json",r)
    return out
def main(exe,dest):
    dest=dest.resolve();dest.mkdir(parents=True,exist_ok=False);data=read(P/"scores.json")["candidates"]; cases=read(O/"cohort.json")["selected"]
    config=[];env=dict(os.environ);env.update({"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0","MPLBACKEND":"Agg","PYTHONIOENCODING":"utf-8"})
    for k in list(env):
        if any(w in k.upper() for w in ("TOKEN","OPENAI","ANTHROPIC","PASSWORD","SECRET","API_KEY")):env.pop(k)
    for c in cases:
        if c["instance_id"].split("-")[-1] not in ("22714","23413"):continue
        choices=sorted([r for r in data if r["case"]==c["instance_id"] and r["both_pass"] and r["property_executed"]],key=lambda r:(r["newly_failing_count"]==0,r["id"]))
        config.append((c,[r["id"] for r in choices[:2]],exe,dest,env))
    begin=time.monotonic()
    with ThreadPoolExecutor(2) as ex:rows=[i for batch in ex.map(group,config) for i in batch]
    write(dest/"observations.json",{"rows":rows,"wall_seconds":round(time.monotonic()-begin,3)})
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--python",required=True);ap.add_argument("--out",type=Path,required=True);v=ap.parse_args();main(v.python,v.out)
