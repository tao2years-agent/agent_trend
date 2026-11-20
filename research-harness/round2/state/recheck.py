"""Execute existing independent evidence validators and register their actual exit status."""
import hashlib,datetime,sys,subprocess,json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
R=Path(__file__).resolve().parent.parent
paths=['empirical/verify.py','handoff/verify.py','ownership/verify.py','oracles/verify.py','gates/verify.py','ci-cross/verify.py','ci-availability/verify.py','dependency-bot/verify.py','cowork/check.py','message-quality/verify.py','eng-intel-vendors/verify.py','promotion-replay/validate.py','devlake/independent-check.py']
def check(name):
    f=R/name
    run=subprocess.run([sys.executable,'-X','utf8',str(f)],capture_output=True,text=True,encoding='utf8',timeout=120)
    return dict(script=name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),exit=run.returncode,stdout=run.stdout.strip(),error=run.stderr.strip())
with ThreadPoolExecutor(3) as pool:items=list(pool.map(check,paths))
report=dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),validators=items)
(R/'state/independent-checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8')
print([(r['script'],r['exit']) for r in items]);assert all(r['exit']==0 for r in items)

