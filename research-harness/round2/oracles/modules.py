"""Execute whole upstream pytest modules in a second isolated interpreter."""
import argparse,hashlib,json,os,pathlib,re,subprocess,sys,tarfile,tempfile,time
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET
from ingest import P,CACHE,RAW
from run import apply

def rows(xml):
    if not xml.exists():return []
    out=[]
    for n in ET.parse(xml).findall(".//testcase"):
        outcome="passed";reason=""
        for child in n:
            if child.tag in ("failure","error","skipped"):
                outcome=child.tag;reason=child.get("message","");kind=child.get("type","")
                if "xfail" in kind:outcome="xfail"
                break
        out.append({"class":n.get("classname",""),"name":n.get("name",""),"outcome":outcome,"reason":reason[:400]})
    return out

def execute(args):
    meta,exe,reportdir,env=args
    key=meta["instance_id"];repo=RAW/key
    fixed=json.loads((P/"runs"/key/"outcomes.json").read_bytes())
    modules=fixed["src_test_paths"]
    sens=[r for r in json.loads((P/"sensitivity.json").read_bytes()) if r["case"]==key]
    tmp=pathlib.Path(tempfile.mkdtemp(prefix=key+"-full311-"))
    archive=CACHE/(meta["base_commit"]+".tar.gz");assert hashlib.sha256(archive.read_bytes()).hexdigest()==meta["archive_sha256"]
    with tarfile.open(archive) as tar:tar.extractall(tmp,filter="data")
    root=tmp/("sympy-"+meta["base_commit"]);dest=reportdir/key;dest.mkdir(parents=True,exist_ok=True)
    prov=subprocess.run([exe,"-c","import sympy; print(sympy.__file__)"],cwd=root,env=env,capture_output=True,text=True)
    if prov.returncode or str(root).lower() not in prov.stdout.lower():raise RuntimeError(prov.stderr)
    gold=(repo/"patch.diff").read_text(encoding="utf8")
    modified=re.findall(r"^diff --git a/(\S+)",gold,re.M)
    base={p:(root/p).read_bytes() for p in modified}
    outcomes=[]
    for phase in ["original","regression_on_base","regression_on_gold"]+[f"without-{r['omit']}" for r in sens]:
        err=None
        try:
            if phase=="regression_on_base":apply(root,repo/"test_patch.diff")
            if phase=="regression_on_gold":apply(root,repo/"patch.diff")
            if phase.startswith("without"):
                for path,b in base.items():(root/path).write_bytes(b)
                apply(root,P/"sensitivity"/key/(phase+".diff"))
        except subprocess.CalledProcessError as e:
            err=e.stderr.decode(errors="replace")
        for i,module in enumerate(modules):
            tag=f"{phase}_m{i+1}"
            xml=dest/(tag+".xml");log=dest/(tag+".txt")
            cmd=[exe,"-m","pytest","-q","-p","no:cacheprovider","--tb=short","--disable-warnings","--color=no","--junitxml="+str(xml),module]
            began=time.monotonic()
            if err:code=127;stdout="GIT APPLY FAILED: "+err
            else:
                try:
                    r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding="utf8",errors="replace",timeout=480)
                    code=r.returncode;stdout=r.stdout+r.stderr
                except subprocess.TimeoutExpired as e:
                    code=124;stdout=(e.stdout or b"").decode(errors="replace")+"\nTIMEOUT 480s"
            log.write_text(stdout,encoding="utf8")
            result={"case":key,"phase":phase,"module":module,"exit":code,"seconds":round(time.monotonic()-began,3),"xml":xml.name if xml.exists() else None,"log":log.name,"tests":rows(xml) if xml.exists() else []}
            outcomes.append(result)
            (dest/"outcomes.json").write_text(json.dumps(outcomes,indent=2),encoding="utf8")
            print(key,tag,code,len(result["tests"]),result["seconds"],flush=True)
    return outcomes

def main(exe,dest):
    start=time.monotonic()
    dest=dest.resolve()
    if dest.exists() and any(dest.iterdir()):raise FileExistsError(dest)
    dest.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ);env.update({"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0","MPLBACKEND":"Agg","PYTHONIOENCODING":"utf-8"})
    for k in list(env):
        if any(w in k.upper() for w in ("TOKEN","OPENAI","ANTHROPIC","PASSWORD","SECRET","API_KEY")):env.pop(k)
    version=subprocess.check_output([exe,"-c","import sys;print(sys.version)"],env=env,text=True).strip()
    freeze=subprocess.check_output([exe,"-m","pip","freeze"],env=env,text=True)
    (dest/"environment.txt").write_text(version+"\n"+freeze,encoding="utf8")
    cases=json.loads((P/"cohort.json").read_bytes())["selected"]
    with ThreadPoolExecutor(2) as ex:runs=[item for row in ex.map(execute,[(c,exe,dest,env) for c in cases]) for item in row]
    (dest/"all.json").write_text(json.dumps({"wall_seconds":round(time.monotonic()-start,3),"timeout_per_module":480,"max_concurrent":2,"version":version,"runs":runs},indent=2),encoding="utf8")
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--python",required=True);ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args();main(a.python,a.out)
