"""Verify desktop, phone, and offline appendix navigation in installed Chrome."""
import json,os,subprocess,tempfile,time,urllib.request
from pathlib import Path
import websocket
R=Path(__file__).resolve().parents[1]
exe=Path(os.environ["ProgramFiles"])/"Google/Chrome/Application/chrome.exe"
fetch=urllib.request.build_opener(urllib.request.ProxyHandler({}))
out={}
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as user_data:
    proc=subprocess.Popen([str(exe),"--headless=new","--disable-gpu","--disable-extensions","--no-first-run","--disable-background-networking","--remote-allow-origins=*","--remote-debugging-port=0","--user-data-dir="+user_data,"about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        portfile=Path(user_data)/"DevToolsActivePort"
        for _ in range(80):
            if portfile.exists():break
            time.sleep(.1)
        port=portfile.read_text().splitlines()[0]
        tabs=json.load(fetch.open("http://127.0.0.1:"+port+"/json/list"))
        ws=websocket.create_connection(tabs[0]["webSocketDebuggerUrl"],suppress_origin=True,http_no_proxy=["127.0.0.1","localhost"])
        seq=0
        errors=[]
        def call(method,params=None):
            global seq
            seq+=1
            ws.send(json.dumps({"id":seq,"method":method,"params":params or {}}))
            while True:
                msg=json.loads(ws.recv())
                if msg.get("method")=="Runtime.exceptionThrown":errors.append(msg["params"])
                if msg.get("id")==seq:
                    if "error" in msg:raise RuntimeError(msg)
                    return msg["result"]
        def ev(js):return call("Runtime.evaluate",{"expression":js,"returnByValue":True})["result"].get("value")
        call("Runtime.enable");call("Network.enable")
        call("Network.emulateNetworkConditions",{"offline":True,"latency":0,"downloadThroughput":0,"uploadThroughput":0})
        for name,w,h in [("desktop",1440,960),("phone",390,844)]:
            call("Emulation.setDeviceMetricsOverride",{"width":w,"height":h,"deviceScaleFactor":1,"mobile":False})
            call("Page.navigate",{"url":(R/"outputs/report.html").as_uri()})
            for _ in range(100):
                if ev("!!document.querySelector('main details') && document.readyState==='complete'"):break
                time.sleep(.05)
            if name=="phone":
                ev("document.querySelector('button').click()")
                assert ev("getComputedStyle(document.querySelector('nav')).display!=='none'")
            assert ev("document.querySelectorAll('details').length")>=5
            ev("[...document.querySelectorAll('nav a')].find(a=>a.textContent==='产品机会清单').click()")
            info=ev("({appendix:document.querySelector(location.hash).open,count:document.querySelector(location.hash).querySelectorAll('h3').length,width:innerWidth,body:document.documentElement.scrollWidth,table:document.querySelector('table').getBoundingClientRect().width,links:[...document.querySelectorAll('nav a')].every(a=>!!document.querySelector(a.hash))})")
            assert info["appendix"] and info["count"]==16 and info["body"]<=w and info["links"],info
            ev("document.querySelector(location.hash).querySelector('summary').click()")
            assert not ev("document.querySelector(location.hash).open")
            out[name]=info
        out["runtime_errors"]=len(errors)
        assert not errors
        out["offline"]=True
        ws.close()
    finally:
        proc.terminate()
        proc.wait(timeout=10)
(R/"state/reader-check.json").write_text(json.dumps(out,indent=2),encoding="utf8")
print(out)
