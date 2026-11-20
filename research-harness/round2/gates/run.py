"""All scheduled candidates receive all three gates, even if an earlier gate fails."""
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from xml.etree import ElementTree as ET
from candidates import P,O,read,write,checkout,apply
def counter(xml):
    out=Counter()
    if xml.exists():
        for item in ET.parse(xml).findall(".//testcase"):
            state="passed"
            for child in item:
                if child.tag in ("error","failure","skipped"):
                    state="xfail" if "xfail" in child.get("type","") else child.tag;break
            out[state]+=1
    return dict(out)
def command(args,cwd,env,log,timeout):
    begin=time.monotonic()
    try:
        r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,encoding="utf8",errors="replace",timeout=timeout);code=r.returncode;stdout=r.stdout+r.stderr
    except subprocess.TimeoutExpired as e:
        code=124;stdout=(e.stdout or b"").decode(errors="replace")+"\nTIMEOUT\n"
    log.write_text(stdout,encoding="utf8")
    return {"exit":code,"elapsed_seconds":round(time.monotonic()-begin,3),"stdout":log.name}
def run_case(args):
    meta,en,exe,dest,env=args;key=meta["instance_id"];root=checkout(meta,False);pre=read(O/"runs"/key/"outcomes.json")
    working=dest/key;working.mkdir()
    expected_files={x["path"] for x in en["changes"]};outputs=[]
    checks=[("base",None),("gold",None)]+[(x["id"],x) for x in sorted(en["changes"],key=lambda r:r["id"]) if x["selected"]]
    fields=pre["phases"]["regression_on_gold"]["selected"]; nodes=[n for v in fields.values() for n in v["nodes"]]
    full=pre["src_test_paths"];cached={}
    for ident,edit in checks:
        leaf=working/ident;leaf.mkdir()
        if ident=="gold":
            apply(root,O/"raw"/key/"patch.diff");cached={p:(root/p).read_bytes() for p in expected_files}
        if edit:
            for p,b in cached.items():(root/p).write_bytes(b)
            patch=P/"patches"/key/(ident+".diff");assert hashlib.sha256(patch.read_bytes()).hexdigest()==edit["diff_sha256"]
            apply(root,patch)
            import ast
            cur=ast.dump(ast.parse((root/edit["path"]).read_text("utf8")),include_attributes=False)
            assert hashlib.sha256(cur.encode()).hexdigest()==edit["ast_sha256"]
        r={"case":key,"id":ident,"labels":[],"modules":[]}
        if ident!="base":
            for level,tests in [("labels",[nodes]),("modules",[[m] for m in full])]:
                for z,spec in enumerate(tests):
                    log=leaf/(level+str(z)+".txt");xml=leaf/(level+str(z)+".xml")
                    cmd=[exe,"-m","pytest","-q","-p","no:cacheprovider","--disable-warnings","--tb=short","--color=no","--junitxml="+str(xml),*spec]
                    obs=command(cmd,root,env,log,480)
                    r[level].append(obs|{"states":counter(xml),"xml":xml.name if xml.exists() else None})
        prop=leaf/"property.json";obs=command([exe,str(P/"properties.py"),key.split("-")[-1],str(prop)],root,env,leaf/"property.log",300)
        r["property"]=obs|{"observations":prop.name if prop.exists() else None}
        outputs.append(r);write(working/"summary.json",outputs)
        print(key,ident,[x["exit"] for x in r["labels"]],[x["exit"] for x in r["modules"]],obs["exit"],flush=True)
    return outputs
def main(exe,dest):
    begin=time.monotonic();dest=dest.resolve()
    if dest.exists() and any(dest.iterdir()):raise FileExistsError(dest)
    dest.mkdir(exist_ok=True,parents=True)
    env=dict(os.environ);env.update({"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0","MPLBACKEND":"Agg","PYTHONIOENCODING":"utf-8"})
    for k in list(env):
        if any(w in k.upper() for w in ("TOKEN","OPENAI","ANTHROPIC","PASSWORD","SECRET","API_KEY")):env.pop(k)
    cases=read(O/"cohort.json")["selected"];enum=read(P/"candidates.json")
    version=subprocess.check_output([exe,"-c","import sys;print(sys.version)"],text=True,env=env)
    libs=subprocess.check_output([exe,"-m","pip","freeze"],env=env,text=True)
    (dest/"environment.txt").write_text(version+libs,encoding="utf8")
    lock={k:hashlib.sha256((P/k).read_bytes()).hexdigest() for k in ("protocol.md","candidates.json","properties.py")}
    write(dest/"lock.json",lock)
    with ThreadPoolExecutor(2) as pool:records=[r for group in pool.map(run_case,[(a,b,exe,dest,env) for a,b in zip(cases,enum)]) for r in group]
    write(dest/"observations.json",{"wall_seconds":round(time.monotonic()-begin,3),"observations":records})
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--python",required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args();main(a.python,a.out)
