"""Archive official PyPI wheels and their published digests for a paired corpus."""
import requests,time
import concurrent.futures as cf,datetime,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
raw=R/"raw"
raw.mkdir(exist_ok=True)
sets={"Django":["3.2.25","5.2.1"],"requests":["2.25.1","2.32.3"],"urllib3":["1.26.18","2.4.0"],"click":["7.1.2","8.2.1"],"networkx":["2.5.1","3.4.2"],"Pygments":["2.10.0","2.19.1"],"flynt":["1.0.6"],"astor":["0.8.1"],"ruff":["0.15.0"]}
def grab(url):
    for attempt in range(3):
        try:
            session=requests.Session();session.trust_env=False
            response=session.get(url,timeout=(6,35));response.raise_for_status();return response.content
        except requests.RequestException:pass
    return subprocess.check_output(["curl.exe","--noproxy","*","-fsSL","--retry","2","--connect-timeout","10","--max-time","120",url],stderr=subprocess.DEVNULL)
def item(t):
    name,version=t;url=f"https://pypi.org/pypi/{name}/{version}/json";mp=raw/f"{name}-{version}.json"
    alt=raw/f"{name}-all.json"
    if not mp.exists() and not alt.exists():
        try:mp.write_bytes(grab(url))
        except Exception:alt.write_bytes(grab(f"https://pypi.org/pypi/{name.lower()}/json"))
    if mp.exists():items=json.loads(mp.read_bytes())["urls"]
    else:
        items=json.loads(alt.read_bytes())["releases"][version];url=f"https://pypi.org/pypi/{name.lower()}/json"
    wheels=[u for u in items if u["packagetype"]=="bdist_wheel" and u["filename"].endswith(("none-any.whl","win_amd64.whl"))]
    u=wheels[0];path=raw/u["filename"]
    if not path.exists():
        b=grab(u["url"]);assert hashlib.sha256(b).hexdigest()==u["digests"]["sha256"];path.write_bytes(b)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==u["digests"]["sha256"]
    return dict(name=name,version=version,role="tool" if name in ("flynt","astor","ruff") else "project",file=path.name,sha256=u["digests"]["sha256"],uploaded=u["upload_time_iso_8601"],metadata=url,download=u["url"])
if __name__=="__main__":
    with cf.ThreadPoolExecutor(max_workers=8) as ex:ans=list(ex.map(item,[(k,v) for k,vs in sets.items() for v in vs]))
    p=R/"sources.json"
    if p.exists():assert ans==json.loads(p.read_text("utf8"))
    else:p.write_text(json.dumps(ans,ensure_ascii=False,indent=2),encoding="utf8")
    print([(x["name"],x["version"]) for x in ans])
