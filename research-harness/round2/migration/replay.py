"""Paired, local, original-wheel replay. Execute only the hand-written behavioral fixtures."""
import ast,csv,difflib,hashlib,io,json,os,re,subprocess,sys,tempfile,tokenize,warnings,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent
manifest=json.loads((R/"sources.json").read_text("utf8"))
tools={v["name"]:R/"raw"/v["file"] for v in manifest if v["role"]=="tool"}
probes={
    "simple":"return 'value={}'.format(42)",
    "keywords":"return '{team}/{id}'.format(team='infra', id=17)",
    "precision":"return '{:.2f}'.format(2.345)",
    "escaped_braces":"return '{{{}}}'.format(5)",
    "repeat_position":"return '{0}:{0}'.format(next_value('a'))",
    "reorder_args":"return '{1}:{0}'.format(next_value('a'),next_value('b'))",
    "unused_arg":"return '{0}'.format(next_value('a'),next_value('b'))",
    "format_side_effect":"return '{} {}'.format(mark('a'),mark('b'))",
    "same_object_twice":"return '{0}-{0}'.format(mark('a'))",
    "nested_width":"return '{num:{width}}'.format(num=2,width=4)",
    "missing_key":"return '{absent}'.format(present=3)",
    "spread_list":"return '{}/{}'.format(*[next_value('a'),next_value('b')])"}
common="""log=[]
def next_value(x):
    log.append('eval:'+x)
    return x
class V:
    def __init__(self,x):self.x=x
    def __format__(self,s):
        log.append('format:'+self.x)
        return self.x
def mark(x):return V(next_value(x))
def go():
    """
def material(scope,tar):
    if scope is None:
        for name,expr in probes.items():(tar/(name+".py")).write_text(common+expr+"\n",encoding="utf8")
        return
    with zipfile.ZipFile(R/"raw"/scope["file"]) as z:
        for fn in z.namelist():
            p=Path(fn)
            if p.suffix!=".py" or p.is_absolute() or ".." in p.parts:continue
            dest=tar/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(fn))
def state(p):
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    try:
        t=b.decode(tokenize.detect_encoding(io.BytesIO(b).readline)[0]);a=ast.parse(t)
        count=sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="format" and isinstance(n.func.value,ast.Constant) and isinstance(n.func.value.value,str) for n in ast.walk(a))
        compile(a,str(p),"exec");return h,count,t
    except (UnicodeError,SyntaxError,ValueError):return h,None,""
def behavior(t):
    ns={};exec(compile(t,"<authored fixture>","exec"),ns)
    try:r=ns["go"]();result=["value",repr(r)]
    except Exception as ex:result=["exception",type(ex).__name__,str(ex)]
    return [result,ns["log"]]
def readtree(root):return {p.relative_to(root).as_posix():state(p) for p in root.rglob("*.py")}
def store_csv(path,rows):
    with (R/path).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run():
    files=[];fixture=[];picks=[];summ=[];logs=[];warnings.simplefilter("ignore",SyntaxWarning)
    with tempfile.TemporaryDirectory(prefix="harness-paired-") as work:
        base=Path(work);binary=base/"ruff.exe"
        with zipfile.ZipFile(tools["ruff"]) as z:binary.write_bytes(z.read(next(n for n in z.namelist() if n.endswith("/ruff.exe"))))
        env=dict(os.environ,PYTHONPATH=str(tools["flynt"]),PYTHONUTF8="1",PYTHONWARNINGS="ignore::SyntaxWarning",RUFF_NO_CACHE="1")
        for scope in [None]+[s for s in manifest if s["role"]=="project"]:
            project,version=(scope["name"],scope["version"]) if scope else ("fixtures","1")
            for tool in ("ruff","flynt"):
                root=base/project/version/tool;root.mkdir(parents=True)
                material(scope,root);original=readtree(root)
                cmd=[str(binary),"check","--isolated","--no-cache","--select","UP032","--fix","--target-version","py38","--ignore-noqa",str(root)] if tool=="ruff" else [sys.executable,"-m","flynt","--no-tp",str(root)]
                # Respect suppressions in product sources for both default non-aggressive modes.
                if "--ignore-noqa" in cmd:cmd.remove("--ignore-noqa")
                first=subprocess.run(cmd,capture_output=True,cwd=base,env=env,timeout=420);changed=readtree(root)
                second=subprocess.run(cmd,capture_output=True,cwd=base,env=env,timeout=420);twice=readtree(root)
                logs.append(dict(project=project,version=version,tool=tool,first=first.returncode,second=second.returncode,stdout=first.stdout.decode("utf8","replace")[-1400:].replace(str(base),"<tmp>"),stderr=first.stderr.decode("utf8","replace")[-1400:].replace(str(base),"<tmp>")))
                assert first.returncode in (0,1) and second.returncode in (0,1),logs[-1]
                assert original.keys()==changed.keys()==twice.keys()
                sample=[]
                for f,(h,n,t) in original.items():
                    h1,n1,t1=changed[f]
                    row=dict(project=project,version=version,tool=tool,file=f,tests=int(any(i in ("test","tests") for i in Path(f).parts) or Path(f).name.startswith("test_")),before=n,after=n1,changed=int(h!=h1),second_change=int(h1!=twice[f][0]),original_sha=h,first_sha=h1)
                    if not scope:
                        a,b=behavior(t),behavior(t1)
                        fixture.append(dict(name=f,tool=tool,changed=row["changed"],behavior_matches=a==b,before=a,after=b,transformed=t1.split("def go():")[-1].strip(),second_change=row["second_change"]))
                    else:
                        files.append(row)
                        if row["changed"] and n and n1 is not None:
                            sample.append((hashlib.sha256((f+version).encode()).hexdigest(),dict(project=project,version=version,tool=tool,file=f,diff="\n".join(list(difflib.unified_diff(t.splitlines(),t1.splitlines(),n=2,lineterm=""))[:30]))))
                picks.extend(s[1] for s in sorted(sample,key=lambda x:x[0])[:3])
                if scope:
                    rows=[x for x in files if x["tool"]==tool and x["project"]==project and x["version"]==version]
                    summ.append(dict(project=project,version=version,tool=tool,files=len(rows),before=sum(x["before"] or 0 for x in rows),after=sum(x["after"] or 0 for x in rows),changed_files=sum(x["changed"] for x in rows),before_parse_errors=sum(x["before"] is None for x in rows),new_parse_errors=sum(x["after"] is None and x["before"] is not None for x in rows),second_changes=sum(x["second_change"] for x in rows)))
                print(project,version,tool,flush=True)
    store_csv("files.csv",files);store_csv("summary.csv",summ)
    for name,x in [("probes",fixture),("diff-sample",picks),("run-log",logs)]:(R/(name+".json")).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf8")
if __name__=="__main__":run()
