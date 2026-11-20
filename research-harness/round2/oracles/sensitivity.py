from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,tarfile,tempfile
from xml.etree import ElementTree as ET
from ingest import P,RAW,CACHE
from run import apply,filetests
def split_patch(text):
    files=[]
    for chunk in re.split(r"(?=^diff --git )",text,flags=re.M):
        if not chunk:continue
        sections=re.split(r"(?=^@@ )",chunk,flags=re.M)
        name=re.search(r"^diff --git a/(\S+)",chunk)[1]
        files.append((name,sections[0],sections[1:]))
    return files
def process(row):
    key=row["instance_id"];metadata=RAW/key;gold=(metadata/"patch.diff").read_text(encoding="utf8")
    files=split_patch(gold);total=sum(len(hunks) for _,_,hunks in files)
    if total<2:return []
    out=P/"sensitivity"/key;out.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix=key+"-partial-"))
    archive=CACHE/(row["base_commit"]+".tar.gz");assert hashlib.sha256(archive.read_bytes()).hexdigest()==row["archive_sha256"]
    with tarfile.open(archive) as tar:tar.extractall(tmp,filter="data")
    checkout=tmp/("sympy-"+row["base_commit"])
    apply(checkout,metadata/"test_patch.diff")
    affected={name:(checkout/name).read_bytes() for name,_,_ in files}
    main=json.loads((P/"runs"/key/"outcomes.json").read_bytes())
    names=main["phases"]["regression_on_gold"]["selected"]
    nodes=[i for v in names.values() for i in v["nodes"]]
    env=os.environ.copy()
    env.update({"PYTEST_DISABLE_PLUGIN_AUTOLOAD":"1","PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0","MPLBACKEND":"Agg","PYTHONIOENCODING":"utf-8"})
    for k in list(env):
        if any(w in k.upper() for w in ("TOKEN","OPENAI","ANTHROPIC","PASSWORD","SECRET","API_KEY")):env.pop(k)
    results=[]
    for omitted in range(total):
        for name,b in affected.items():(checkout/name).write_bytes(b)
        idx=0;parts=[];omitted_ref=None
        for name,header,hunks in files:
            used=[]
            for h in hunks:
                if idx==omitted:omitted_ref=name+" "+h.splitlines()[0]
                else:used.append(h)
                idx+=1
            if used:parts.append(header+"".join(used))
        f=out/f"without-{omitted+1}.diff";f.write_bytes("".join(parts).encode())
        item={"case":key,"omit":omitted+1,"omitted_hunk":omitted_ref,"patch_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"nodes":[]}
        try:apply(checkout,f)
        except subprocess.CalledProcessError as e:
            item["error"]=e.stderr.decode(errors="replace");results.append(item);continue
        xml=out/f"without-{omitted+1}.xml"
        cmd=[sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--tb=short","--disable-warnings","--color=no","--junitxml="+str(xml),*nodes]
        p=subprocess.run(cmd,cwd=checkout,env=env,timeout=160,capture_output=True,encoding="utf8",errors="replace")
        (out/f"without-{omitted+1}.txt").write_text(p.stdout+p.stderr,encoding="utf8");item["exit"]=p.returncode
        if xml.exists():
            for case in ET.parse(xml).findall(".//testcase"):
                n=case.get("name");tag=next((c.tag for c in list(case) if c.tag in ("failure","error","skipped")),"passed")
                item["nodes"].append({"name":n,"class":case.get("classname"),"role":names.get(n,{}).get("role","unknown"),"outcome":tag})
        results.append(item)
    return results
if __name__=="__main__":
    cases=json.loads((P/"cohort.json").read_bytes())["selected"]
    with ThreadPoolExecutor(2) as e: records=[r for rs in e.map(process,cases) for r in rs]
    (P/"sensitivity.json").write_text(json.dumps(records,indent=2),encoding="utf8")
    print([(r["case"],r["omit"],r.get("exit"),sum(i["outcome"]!="passed" for i in r["nodes"])) for r in records])
