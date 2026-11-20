"""Exercise both offline readers in Chromium, print the same brief HTML to PDF, verify its text."""
import base64,json,os,subprocess,tempfile,time,urllib.request
from pathlib import Path
import websocket
R=Path(__file__).resolve().parent
P=R.parent
report={}; errors=[]; external=[]
chrome=Path(os.environ['ProgramFiles'])/'Google/Chrome/Application/chrome.exe'
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
    p=subprocess.Popen([str(chrome),'--headless=new','--disable-gpu','--disable-extensions','--no-first-run','--disable-background-networking','--remote-allow-origins=*','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        port=Path(profile)/'DevToolsActivePort'
        for _ in range(160):
            if port.exists():break
            time.sleep(.1)
        local=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        tab=json.load(local.open('http://127.0.0.1:'+port.read_text().splitlines()[0]+'/json/list'))[0]
        ws=websocket.create_connection(tab['webSocketDebuggerUrl'],suppress_origin=True,http_no_proxy=['127.0.0.1','localhost'])
        seq=0
        def call(method,params=None):
            global seq
            seq+=1
            ws.send(json.dumps(dict(id=seq,method=method,params=params or {})))
            while True:
                msg=json.loads(ws.recv())
                kind=msg.get('method')
                if kind=='Runtime.exceptionThrown':errors.append(str(msg['params'])[:120])
                if kind=='Network.requestWillBeSent':
                    url=msg['params']['request']['url']
                    if url.startswith(('http:','https:')):external.append(url)
                if msg.get('id')==seq:
                    assert 'error' not in msg,msg
                    return msg['result']
        def ev(js):return call('Runtime.evaluate',{'expression':js,'returnByValue':True})['result'].get('value')
        for n in ['Page','Network','Runtime']:call(n+'.enable')
        downloads=Path(profile)/'reader-downloads';downloads.mkdir()
        call('Browser.setDownloadBehavior',dict(behavior='allow',downloadPath=str(downloads)))
        call('Network.emulateNetworkConditions',dict(offline=True,latency=0,downloadThroughput=0,uploadThroughput=0))
        for name in ['insights-decision','deep-report-v2']:
            for tag,width,height in [('desktop',1440,900),('phone',390,844)]:
                call('Emulation.setDeviceMetricsOverride',dict(width=width,height=height,deviceScaleFactor=1,mobile=False))
                url=(P/f'outputs/{name}.html').as_uri()
                call('Page.navigate',{'url':url})
                for _ in range(100):
                    if ev("document.readyState==='complete' && document.URL==="+json.dumps(url)+" && !!document.querySelector('article .chapter')"):break
                    time.sleep(.1)
                st=ev("""({title:document.title,width:document.documentElement.scrollWidth,sections:document.querySelectorAll('.chapter').length,nav:[...document.querySelectorAll('nav a')].every(a=>document.querySelector(a.hash)),anchors:[...document.querySelectorAll('a[href^="#"]:not([data-attachment])')].every(a=>document.getElementById(a.hash.slice(1))),attached:document.querySelectorAll('[data-attachment]').length})""")
                assert st['width']<=width and st['nav'] and st['anchors'],st
                snap=call('Page.captureScreenshot',dict(format='png',captureBeyondViewport=False))
                (R/f'state/{name}-{tag}.png').write_bytes(base64.b64decode(snap['data']))
                if name.startswith('deep'):
                    ev("document.querySelector('details.navgroup:not([open]) summary').click()")
                    assert ev("document.querySelectorAll('details.navgroup[open]').length>=3")
                    assert ev("document.querySelector('#matches').textContent")=='35 项'
                    ev("const q=document.querySelector('#search');q.value='Aider';q.dispatchEvent(new Event('input'));")
                    assert ev("Array.from(document.querySelectorAll('.record:not([hidden])')).some(d=>d.textContent.includes('Aider'))")
                    ev("q.value='____absent____';q.dispatchEvent(new Event('input'));")
                    assert ev("document.querySelector('#matches').textContent")=='0 项'
                    ev("q.value='';q.dispatchEvent(new Event('input'));document.querySelectorAll('.record')[0].querySelector('summary').click()")
                    assert ev("document.querySelector('.record').open")
                    assert ev("Object.values(files).length>0 && [...document.querySelectorAll('[data-attachment]')].every(e=>!!files[e.dataset.attachment] && atob(files[e.dataset.attachment].b).length>0)")
                    if tag=='desktop':
                        item=ev("(()=>{let a=document.querySelector('[data-attachment]'); const f=files[a.dataset.attachment];a.click();return [f.n,f.b]})()")
                        download=downloads/item[0]
                        for _ in range(100):
                            if download.is_file():break
                            time.sleep(.05)
                        assert download.read_bytes()==base64.b64decode(item[1])
                        st['embedded_download_verified']=True
                else:
                    assert st['sections']==4
                    if tag=='desktop':
                        pdf=call('Page.printToPDF',dict(preferCSSPageSize=True,printBackground=True,displayHeaderFooter=False))
                        (P/'outputs/insights-decision.pdf').write_bytes(base64.b64decode(pdf['data']))
                report[name+'-'+tag]=st
        ws.close()
    finally:
        p.terminate();p.wait(timeout=15)
assert not errors and not external,(errors,external)
import pymupdf
with pymupdf.open(P/'outputs/insights-decision.pdf') as pdf:
    pages=[]
    for i,page in enumerate(pdf):
        content=''.join(page.get_text().split())
        assert len(content)>300,(i,len(content))
        page.get_pixmap(matrix=pymupdf.Matrix(.68,.68)).save(R/f'state/pdf-page-{i+1}.png')
        pages.append(dict(characters=len(content),links=len(page.get_links()),last=content[-14:]))
    assert len(pages)==4,pages
report.update(pdf=pages,external_requests=external,js_errors=errors)
(R/'state/readers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(report,ensure_ascii=False))
