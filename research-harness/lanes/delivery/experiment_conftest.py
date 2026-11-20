"""Verify an official Windows conftest release, run a disposable policy gate, record stdout and status."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, subprocess, zipfile, shutil, datetime
from fetch import get
base='https://github.com/open-policy-agent/conftest/releases/download/v0.71.0/'
asset='conftest_0.71.0_Windows_x86_64.zip'
out=Path(__file__).resolve().parent/'experiment'
out.mkdir(exist_ok=True)
with TemporaryDirectory() as tmp:
 d=Path(tmp); z=d/asset
 sums=get(base+'checksums.txt').content
 z.write_bytes(get(base+asset).content)
 digest=hashlib.sha256(z.read_bytes()).hexdigest()
 assert any(line.split()==[digest,asset] for line in sums.decode().splitlines())
 with zipfile.ZipFile(z) as arc:
  name=next(f for f in arc.namelist() if Path(f).name.lower()=='conftest.exe')
  with arc.open(name) as source,(d/'conftest.exe').open('wb') as dest: shutil.copyfileobj(source,dest)
 policy='package main\n\ndeny contains "production needs an owner" if {\n  input.environment == "prod"\n  not input.owner\n}\n'
 (d/'rule.rego').write_text(policy,encoding='utf-8')
 records=[]
 for nm,inp in [('owned',{'environment':'prod','owner':'payments'}),('unowned',{'environment':'prod'}),('development',{'environment':'dev'})]:
  (d/'manifest.json').write_text(json.dumps(inp),encoding='utf-8')
  proc=subprocess.run([str(d/'conftest.exe'),'test','manifest.json','--policy','rule.rego','--output','json'],capture_output=True,encoding='utf-8',cwd=d,timeout=20)
  records.append(dict(name=nm,input=inp,exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
 assert [r['exit'] for r in records]==[0,1,0],records
 report=dict(version='v0.71.0',asset_url=base+asset,sha256=digest,checksums_url=base+'checksums.txt',policy=policy,command='conftest test manifest.json --policy rule.rego --output json',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),cases=records)
 p=out/'conftest-v0.71.0.json'; 
 if not p.exists(): p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print([(r['name'],r['exit']) for r in records],digest)
