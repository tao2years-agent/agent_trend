"""Verify the largest divergent stratum with unchanged upstream token goldens."""
import csv,hashlib,json,os,subprocess,sys,tarfile,tempfile,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
from replay import R,material,manifest,tools
meta=json.loads((R/"golden-source.json").read_text("utf8"))
pkg=next(x for x in manifest if x["name"]=="Pygments" and x["version"]=="2.19.1")
result={}
with tempfile.TemporaryDirectory(prefix="round2-golden-") as temp:
    base=Path(temp)
    with tarfile.open(R/meta["path"]) as t:
        for m in t:
            if not m.isfile():continue
            parts=Path(m.name).parts
            if parts[1:3] not in (("tests","examplefiles"),("tests","snippets")) and parts[1:]!=("tests","conftest.py"):continue
            rel=Path(*parts[1:]);assert not rel.is_absolute() and ".." not in rel.parts
            dest=base/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.extractfile(m).read())
    original=base/"original";original.mkdir();material(pkg,original)
    variant=base/"flynt";variant.mkdir();material(pkg,variant)
    env=dict(os.environ,PYTHONUTF8="1",PYTHONPATH=str(tools["flynt"]))
    subprocess.run([sys.executable,"-m","flynt","--no-tp",str(variant)],cwd=base,env=env,stdout=subprocess.DEVNULL,check=True)
    for name,src in [("original",original),("flynt",variant)]:
        env=dict(os.environ,PYTHONPATH=str(src),PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONUTF8="1")
        v=subprocess.check_output([sys.executable,"-c","import pygments;print(pygments.__version__,pygments.__file__)"],cwd=base,env=env).decode()
        assert str(src).lower() in v.lower(),v
        path=base/(name+".xml")
        p=subprocess.run([sys.executable,"-m","pytest","tests/examplefiles","tests/snippets","-q","--disable-warnings","-o","python_files=__not_a_python_test__.py","--junitxml",str(path)],cwd=base,env=env,timeout=1500,capture_output=True)
        if not path.exists():raise RuntimeError(p.stdout.decode(errors="replace")[-800:])
        tests=ET.parse(path).find(".//testsuite")
        cases=[(x.get("classname","")+"/"+x.get("name",""),"failed" if x.find("failure") is not None or x.find("error") is not None else "skipped" if x.find("skipped") is not None else "passed") for x in tests.iter("testcase")]
        (R/("goldens-"+name+".csv")).write_text("case,status\n"+"\n".join('"'+n.replace('"','""')+'",'+a for n,a in cases),encoding="utf-8-sig")
        result[name]=dict(version=v.split()[0],code=p.returncode,tests=int(tests.get("tests")),errors=int(tests.get("errors")),skipped=int(tests.get("skipped")),failed=int(tests.get("failures")),seconds=float(tests.get("time")),failed_cases=[n for n,s in cases if s=="failed"][:30])
        print(name,result[name],flush=True)
(R/"goldens.json").write_text(json.dumps(result,indent=2),encoding="utf8")
