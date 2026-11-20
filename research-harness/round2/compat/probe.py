"""All requests stay in-process. Check endpoint reachability separately from framework test clients."""
import asyncio,sys,json,warnings
family=sys.argv[1]
out={}
def step(k,func):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try: value=func();out[k]=dict(ok=True,value=value)
        except Exception as e:out[k]=dict(ok=False,error=type(e).__name__+': '+str(e))
        out[k]['warnings']=sorted(set(type(w.message).__name__+': '+str(w.message) for w in caught))
def build():
    global app
    if family=='Flask':
        from flask import Flask
        app=Flask(__name__)
        @app.get('/')
        def index():return 'ready'
    else:
        from starlette.applications import Starlette
        from starlette.responses import PlainTextResponse
        from starlette.routing import Route
        async def index(request):return PlainTextResponse('ready')
        app=Starlette(routes=[Route('/',index)])
def direct():
    if family=='Flask':
        from werkzeug.test import Client
        answer=Client(app).get('/').get_data(as_text=True)
    else:
        scope={'type':'http','asgi':{'version':'3.0'},'http_version':'1.1','scheme':'http','method':'GET','path':'/','raw_path':b'/','query_string':b'','headers':[],'server':('test',80),'client':('local',1),'root_path':''}
        messages=[]
        async def send(msg):messages.append(msg)
        async def receive():return {'type':'http.request','body':b'','more_body':False}
        asyncio.run(app(scope,receive,send))
        answer=b''.join(m['body'] for m in messages if m['type']=='http.response.body').decode()
    assert answer=='ready';return answer
def testclient():
    if family=='Flask':
        answer=app.test_client().get('/').get_data(as_text=True)
    else:
        from starlette.testclient import TestClient
        with TestClient(app) as c:answer=c.get('/').text
    assert answer=='ready';return answer
step('import_and_build',build)
if out['import_and_build']['ok']:
    step('wsgi_asgi_request',direct);step('framework_testclient',testclient)
print(json.dumps(out,ensure_ascii=True))
