"""Recheck the project where an explicit Python 3.8 target conflicts with its metadata."""
import tempfile,subprocess,json,zipfile
from pathlib import Path
from replay import R,tools,manifest,material,readtree
with tempfile.TemporaryDirectory() as t:
    root=Path(t);src=root/"django";src.mkdir();spec=next(s for s in manifest if s["name"]=="Django" and s["version"]=="5.2.1")
    material(spec,src)
    with zipfile.ZipFile(tools["ruff"]) as z:(root/"ruff.exe").write_bytes(z.read(next(n for n in z.namelist() if n.endswith("/ruff.exe"))))
    a=readtree(src);r=subprocess.run([str(root/"ruff.exe"),"check","--isolated","--no-cache","--select","UP032","--fix","--target-version","py310",str(src)],capture_output=True)
    b=readtree(src);out=dict(code=r.returncode,calls_before=sum(x[1] or 0 for x in a.values()),calls_after=sum(x[1] or 0 for x in b.values()),changed_files=sum(a[k][0]!=b[k][0] for k in a))
(R/"sensitivity.json").write_text(json.dumps(out,indent=2),encoding="utf8");print(out)
