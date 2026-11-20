import ast,hashlib,json,os,pathlib,re,shutil,subprocess,sys,tarfile,tempfile,time
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET
from ingest import P,RAW,CACHE
PHASES=("original","regression_on_base","regression_on_gold")
def filetests(paths,root):
    by_name={}
    for path in paths:
        f=root/path
        if not f.exists():continue
        tree=ast.parse(f.read_bytes(),filename=str(f))
        for fn in tree.body:
            if isinstance(fn,(ast.FunctionDef,ast.AsyncFunctionDef)) and fn.name.startswith("test_"):
                by_name.setdefault(fn.name,[]).append(path+"::"+fn.name)
            elif isinstance(fn,ast.ClassDef):
                for m in fn.body:
                    if isinstance(m,ast.FunctionDef) and m.name.startswith("test_"):by_name.setdefault(m.name,[]).append(path+"::"+fn.name+"::"+m.name)
    return by_name
def apply(root,path):
    subprocess.run(["git","apply","--whitespace=nowarn",str(path)],cwd=root,check=True,capture_output=True)
def case_run(meta):
    key=meta["instance_id"]; src=RAW/key; phases={}
    work=pathlib.Path(tempfile.mkdtemp(prefix=key+"-"))
    tarpath=CACHE/(meta["base_commit"]+".tar.gz")
    assert hashlib.sha256(tarpath.read_bytes()).hexdigest()==meta["archive_sha256"]
    with tarfile.open(tarpath) as t:t.extractall(work,filter="data")
    root=work/("sympy-"+meta["base_commit"])
    paths=list(dict.fromkeys(re.findall(r"^\+\+\+ b/([^\t\r\n]+)",(src/"test_patch.diff").read_text(encoding="utf8"),re.M)))
    names={**{n:"FTP" for n in meta["FAIL_TO_PASS"]},**{n:"PTP" for n in sorted(set(meta["PASS_TO_PASS"]))[:5]}}
    assert len(names)==len(set(meta["FAIL_TO_PASS"]))+min(5,len(set(meta["PASS_TO_PASS"])))
    audit=P/"runs"/key;audit.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.update({"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0","MPLBACKEND":"Agg","PYTHONIOENCODING":"utf-8"})
    # Local imports use the checkout at cwd. No private service/LLM credentials needed.
    for k in list(env):
        if any(w in k.upper() for w in ("TOKEN","OPENAI","ANTHROPIC","PASSWORD","SECRET","API_KEY")):env.pop(k)
    origin=subprocess.check_output([sys.executable,"-c","import sympy; print(sympy.__file__)"],cwd=root,env=env,text=True,stderr=subprocess.STDOUT).strip()
    if str(root).lower() not in origin.lower():raise ValueError("sympy did not load from checkout: "+origin)
    for phase in PHASES:
        if phase=="regression_on_base":apply(root,src/"test_patch.diff")
        if phase=="regression_on_gold":apply(root,src/"patch.diff")
        available=filetests(paths,root)
        status={n:{"role":r,"nodes":available.get(n,[]),"outcome":"missing" if n not in available else "unknown"} for n,r in names.items()}
        nodes=[i for n in names for i in available.get(n,[])]
        xml=audit/(phase+".xml");report=audit/(phase+".txt")
        cmd=[sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--tb=short","--disable-warnings","--color=no","--junitxml="+str(xml),*nodes]
        start=time.monotonic()
        if nodes:
            try:
                run=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding="utf8",errors="replace",timeout=160)
                code=run.returncode;stdout=run.stdout+run.stderr
            except subprocess.TimeoutExpired as e:
                code=124;stdout=(e.stdout or b"").decode("utf8",errors="replace")+"\nTIMEOUT 160s"
        else:code=5;stdout="No runnable names in this phase."
        report.write_text(stdout,encoding="utf8")
        if code!=124 and xml.exists():
            tree=ET.parse(xml); matches={}
            for el in tree.findall(".//testcase"):
                n=el.attrib.get("name","")
                if n not in names:continue
                outcome=("failure" if el.find("failure") is not None else "error" if el.find("error") is not None else "skipped" if el.find("skipped") is not None else "passed")
                matches.setdefault(n,[]).append(outcome)
            for n,values in matches.items():
                status[n]["observations"]=values
                if len(values)==len(status[n]["nodes"]):
                    status[n]["outcome"]=values[0] if len(set(values))==1 else "mixed"
        phases[phase]={"selected":status,"exit":code,"seconds":round(time.monotonic()-start,2),"xml":xml.name if xml.exists() else None,"stdout":report.name}
        print(key,phase,code,[(k,v["outcome"]) for k,v in status.items() if v['role']=="FTP"],flush=True)
    result={"instance_id":key,"src_test_paths":paths,"upstream_import":origin,"phases":phases}
    (audit/"outcomes.json").write_text(json.dumps(result,indent=2),encoding="utf8")
    return result
if __name__=="__main__":
    cohort=json.loads((P/"cohort.json").read_bytes())
    with ThreadPoolExecutor(4) as executor: rows=list(executor.map(case_run,cohort["selected"]))
    (P/"outcomes.json").write_text(json.dumps(rows,indent=2),encoding="utf8")
