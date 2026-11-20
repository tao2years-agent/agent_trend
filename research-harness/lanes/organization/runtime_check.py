"""Two local positive/negative controls, using publisher-checksummed Windows builds."""
import concurrent.futures
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import time
import zipfile
import requests

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / 'runtime'


def download(url):
    for attempt in range(6):
        try:
            session = requests.Session()
            session.trust_env = False
            r = session.get(url, timeout=(20, 60))
            r.raise_for_status()
            return r.content
        except requests.RequestException:
            if attempt == 5:
                raise
            time.sleep(1)


def run(spec):
    app, repo, tag, archive, sums = spec
    prefix = f'https://github.com/{repo}/releases/download/{tag}/'
    work = pathlib.Path(tempfile.mkdtemp(prefix='harness-probe-'))
    try:
        expected = next(line.split()[0] for line in download(prefix+sums).decode().splitlines() if line.split()[-1].lstrip('*') == archive)
        data = download(prefix+archive)
        assert expected == hashlib.sha256(data).hexdigest()
        bundle = work/'binary.zip'
        bundle.write_bytes(data)
        with zipfile.ZipFile(bundle) as z:
            member = next(n for n in z.namelist() if n.lower().split('/')[-1] == app+'.exe')
            exe = work/(app+'.exe')
            exe.write_bytes(z.read(member))
        outputs = []
        for mode in ['pass','fail']:
            if app == 'k6':
                test = work/'probe.js'
                test.write_text("import { Rate } from 'k6/metrics';\nconst ok=new Rate('accepted');\nexport const options={vus:1,iterations:4,thresholds:{accepted:['rate>=0.75']}};\nexport default function(){ok.add(" + ('true' if mode=='pass' else '__ITER===0') + ");}\n")
                args = ['run','--no-usage-report',test.name]
                inputs = {test.name:test.read_text()}
            else:
                policy=work/'policy'
                policy.mkdir(exist_ok=True)
                rule=policy/'gate.rego'
                rule.write_text('package main\nimport rego.v1\ndeny contains msg if {\n  input.owner == ""\n  msg := "owner required"\n}\n')
                payload = work/'service.json'
                payload.write_text(json.dumps({'owner':'platform' if mode=='pass' else ''}))
                args = ['test',payload.name,'--policy','policy','--output','json']
                inputs = {'policy/gate.rego':rule.read_text(),payload.name:payload.read_text()}
            cp = subprocess.run([str(exe)]+args,cwd=work,capture_output=True,encoding='utf-8',errors='replace',timeout=40,
                                env={**os.environ,'NO_COLOR':'1'})
            assert (cp.returncode == 0) == (mode == 'pass'), (app,cp.returncode,cp.stderr)
            outputs.append(dict(mode=mode,argv=[app]+args,input=inputs,returncode=cp.returncode,stdout=cp.stdout,stderr=cp.stderr))
        result=dict(app=app,version=tag,artifact=prefix+archive,checksums=prefix+sums,archive_sha256=expected,
                    tested_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),os='Windows x86_64',runs=outputs)
        OUT.mkdir(exist_ok=True)
        dest=OUT/(app+'.json')
        if not dest.exists():
            dest.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
        print(app, [o['returncode'] for o in outputs], flush=True)
    finally:
        shutil.rmtree(work)


if __name__=='__main__':
    specs=[('k6','grafana/k6','v2.4.0','k6-v2.4.0-windows-amd64.zip','k6-v2.4.0-checksums.txt'),
           ('conftest','open-policy-agent/conftest','v0.71.0','conftest_0.71.0_Windows_x86_64.zip','checksums.txt')]
    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        list(pool.map(run,specs))
