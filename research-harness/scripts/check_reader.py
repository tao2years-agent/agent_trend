"""Open both standalone reports in Chrome offline, check navigation, filtering and narrow layout."""
import base64,json,os,subprocess,tempfile,time,urllib.request
from pathlib import Path
import websocket
R=Path(__file__).resolve().parents[1]
exe=Path(os.environ["ProgramFiles"])/"Google/Chrome/Application/chrome.exe"
local=urllib.request.build_opener(urllib.request.ProxyHandler({}))
report={};errors=[]; requests=[]
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
    p=subprocess.Popen([str(exe),"--headless=new","--disable-gpu","--disable-extensions","--no-first-run","--disable-background-networking","--remote-allow-origins=*","--remote-debugging-port=0","--user-data-dir="+profile,"about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        for _ in range(120):
            port=Path(profile)/"DevToolsActivePort"
            if port.exists():break
            time.sleep(.1)
        tab=json.load(local.open("http://127.0.0.1:"+port.read_text().splitlines()[0]+"/json/list"))[0]
        ws=websocket.create_connection(tab["webSocketDebuggerUrl"],suppress_origin=True,http_no_proxy=["127.0.0.1","localhost"])
        seq=0
        def call(method,params=None):
            global seq
            seq+=1;ws.send(json.dumps(dict(id=seq,method=method,params=params or {})))
            while True:
                msg=json.loads(ws.recv())
                if msg.get("method")=="Runtime.exceptionThrown":errors.append(str(msg["params"])[:100])
                if msg.get("method")=="Network.requestWillBeSent":requests.append(msg["params"]["request"]["url"])
                if msg.get("id")==seq:
                    if "error" in msg:raise ValueError(msg)
                    return msg["result"]
        def ev(expr):return call("Runtime.evaluate",{"expression":expr,"returnByValue":True})["result"].get("value")
        call("Page.enable");call("Runtime.enable");call("Network.enable")
        call("Network.emulateNetworkConditions",dict(offline=True,latency=0,downloadThroughput=0,uploadThroughput=0))
        for file in ["insights","deep-report"]:
            for tag,w,h in [("desktop",1440,900),("phone",390,844)]:
                call("Emulation.setDeviceMetricsOverride",dict(width=w,height=h,deviceScaleFactor=1,mobile=False))
                url=(R/f"outputs/{file}.html").as_uri()
                call("Page.navigate",{"url":url})
                for _ in range(100):
                    if ev("document.readyState==='complete' && !!document.querySelector('#count') && document.querySelector('#count').textContent==='92 项'"):break
                    time.sleep(.05)
                status=ev("({title:document.title,width:document.documentElement.scrollWidth,records:document.querySelectorAll('.record').length,anchors:[...document.querySelectorAll('a[href^=\"#\"]')].every(a=>!!document.getElementById(decodeURIComponent(a.hash.slice(1))))})")
                assert status["width"]<=w and status["anchors"] and status["records"]==92,status
                if file=="insights":
                    snap=call("Page.captureScreenshot",dict(format="png",captureBeyondViewport=False))
                    (R/f"state/{file}-{tag}.png").write_bytes(base64.b64decode(snap["data"]))
                ev("scope.value='商业工作流';scope.dispatchEvent(new Event('change'))")
                assert ev("count.textContent")=="7 项"
                ev("q.value='Jules';q.dispatchEvent(new Event('input'))")
                assert ev("!document.querySelector('#M03').hidden")
                ev("q.value='__no_match__';q.dispatchEvent(new Event('input'))")
                assert ev("count.textContent")=="0 项"
                ev("document.querySelector('article a[href=\"#P01\"]').click()")
                assert ev("document.querySelector('#P01').open && !document.querySelector('#P01').hidden && location.hash==='#P01'")
                ev("document.querySelector('#P01 summary').click()")
                assert not ev("document.querySelector('#P01').open")
                report[f"{file}-{tag}"]=status
        ws.close()
    finally:
        p.terminate();p.wait(timeout=12)
report.update(offline=True,javascript_errors=errors,external_asset_requests=[u for u in requests if u.startswith(("http:","https:"))])
assert not errors and not report["external_asset_requests"]
(R/"state/reader-check.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print(report)
