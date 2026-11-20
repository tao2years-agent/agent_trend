"""Run the upstream test module against unchanged frozen source files in a temporary working tree."""
from pathlib import Path
import importlib.util, re
import hashlib, json, os, shutil, subprocess, sys, tempfile, importlib.metadata
R=Path(__file__).resolve().parent
manifest=json.loads((R/'sources.json').read_text())
target='tests/duo_workflow_service/checkpointer/test_node_lifecycle.py'
files=[target,'duo_workflow_service/checkpointer/node_lifecycle.py','duo_workflow_service/agent_platform/node_naming.py','duo_workflow_service/agent_platform/constants.py']
with tempfile.TemporaryDirectory() as tmp:
    work=Path(tmp)
    for file in files:
        doc=next(s for s in manifest if s['id']=='GITLAB:'+file)
        incoming=R.parent.parent/doc['path']
        assert hashlib.sha256(incoming.read_bytes()).hexdigest()==doc['sha256']
        dst=work/file
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(incoming,dst)
    env=dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', LANGCHAIN_TRACING_V2='false', LANGSMITH_TRACING='false')
    driver="""import asyncio, inspect, runpy, sys, traceback
tests=runpy.run_path(sys.argv[1])
failed=0
for name, case in sorted(tests.items()):
    if not name.startswith('test_'):
        continue
    try:
        result=case()
        if inspect.isawaitable(result):
            asyncio.run(result)
        print('PASS',name)
    except Exception:
        failed+=1
        print('FAIL',name)
        traceback.print_exc()
sys.exit(bool(failed))
"""
    profile=('locked-direct' if '--direct' in sys.argv else 'locked') if '--locked' in sys.argv else 'ambient'
    command=[sys.executable,'-c',driver,target]
    if profile.startswith('locked'):
        import tomllib
        lockdoc=next(s for s in manifest if s['id']=='GITLAB:poetry.lock')
        lock=tomllib.loads((R.parent.parent/lockdoc['path']).read_text(encoding='utf8'))
        expected={d['name']:d['version'] for d in lock['package'] if d['name'] in ('langgraph','langchain-core','langgraph-checkpoint','langgraph-prebuilt','langgraph-sdk','pytest','pytest-asyncio')}
        assert all(importlib.metadata.version(n)==v for n,v in expected.items())
        if profile=='locked':
            command=[sys.executable,'-m','pytest','-p','pytest_asyncio.plugin','--asyncio-mode=auto','-v','--tb=short',target]
    run=subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,errors='replace')
    report={'commit':doc['commit'],'packages':{name:importlib.metadata.version(name) for name in (expected if profile.startswith('locked') else ('langgraph','langchain-core','pytest'))},'driver':'pytest + pytest-asyncio' if profile=='locked' else 'Python direct invocation of all upstream test functions, asyncio.run for awaitables','files':files,'exit':run.returncode,'stdout':run.stdout.replace(str(work),'<isolated-worktree>'),'stderr':run.stderr.replace(str(work),'<isolated-worktree>')}
    (R/('gitlab-test-'+profile+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(run.stdout,run.stderr)
    sys.exit(run.returncode)
