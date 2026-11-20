from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,tempfile,xml.etree.ElementTree as ET,tarfile,hashlib,itertools,os,sys
R=Path(__file__).resolve().parent
# Platform-independent temporary test isolation; release files are never edited.
from fetch import families,pins
sources=json.loads((R/'sources.json').read_text('utf8'))
for row in sources:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
def cmd(args,**kw):
    return subprocess.run(args,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180,env={**os.environ,'PYTHONUTF8':'1','PIP_DISABLE_PIP_VERSION_CHECK':'1','PYTHONDONTWRITEBYTECODE':'1'},**kw)
def run(cell):
    f,v,dp,dv=cell;tag=f+'-'+v+'_'+dp+'-'+dv
    evidence=R/'results'/tag;evidence.mkdir(exist_ok=True,parents=True)
    with tempfile.TemporaryDirectory(prefix='compat-harness-',ignore_cleanup_errors=True) as root:
        tmp=Path(root);venv=tmp/'env'
        cmd(['py','-3.11','-m','venv','--without-pip',str(venv)]).check_returncode()
        py=str(venv/'Scripts/python.exe')
        req=[f+'=='+v,dp+'=='+dv]+[k+'=='+val for k,val in pins.items()]
        install=cmd(['py','-3.11','-m','pip','--python',py,'install','--no-index','--find-links',str(R/'raw'),*req])
        (evidence/'install.log').write_text((install.stdout+install.stderr).replace(str(tmp),'<TEMP>'),'utf8')
        record=dict(family=f,consumer=v,dependency=dp,provider=dv,installed=install.returncode==0)
        if install.returncode:return record
        probe=cmd([py,str(R/'probe.py'),f]);probe.check_returncode()
        record.update(json.loads(probe.stdout))
        s=next(x for x in sources if x['name']==f and x['version']==v and x['kind']=='sdist')
        with tarfile.open(R/s['path']) as t:
            for m in t.getmembers():
                parts=Path(m.name).parts
                if len(parts)<3 or parts[1]!='tests' or not m.isfile() or '..' in parts:continue
                to=tmp.joinpath(*parts[1:]);to.parent.mkdir(parents=True,exist_ok=True);to.write_bytes(t.extractfile(m).read())
        target='tests/test_testing.py' if f=='Flask' else 'tests/test_testclient.py'
        xml=evidence/'pytest.xml'
        test=cmd([py,'-m','pytest',target,'-q','--disable-warnings','--tb=line','--junitxml',str(xml)],cwd=tmp)
        (evidence/'tests.log').write_text((test.stdout+test.stderr).replace(str(tmp),'<TEMP>'),'utf8')
        rec=dict(exit_code=test.returncode,module=target)
        if xml.exists():
            node=ET.parse(xml).getroot().find('testsuite')
            rec.update({k:int(node.attrib[k]) for k in ('tests','failures','errors','skipped')})
        record['upstream']=rec
        return record
if __name__=='__main__':
    cells=[(f,x,d,y) for f,d in [('Flask','Werkzeug'),('Starlette','httpx')] for x,y in itertools.product(families[f],families[d])]
    with ThreadPoolExecutor(2) as pool:result=list(pool.map(run,cells))
    (R/'matrix.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')
    print([(r['family'],r['consumer'],r['provider'],r['installed'],r.get('upstream')) for r in result])
