"""Exercise the exact archived OpenSandbox pure decision function without a cluster."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
src=next((HERE/'raw/sandbox').rglob('decision.py'))
spec=importlib.util.spec_from_file_location('sandbox_decision_under_test',src)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rows=[]
for name,active,tomb,expected,create in [('recent',9500,None,'not_idle',False),('old',1000,None,'idle',False),
        ('no_signal',None,None,'unknown',True),('fresh_tombstone',None,9000,'unknown',False),
        ('expired_tombstone',None,5000,'idle',False),('recent_signal_overrides_old_tombstone',9900,0,'not_idle',False)]:
 result=module.evaluate_idle(last_active_ms=active,tombstone_ms=tomb,now_ms=10000,threshold_seconds=5)
 assert (result.verdict.value,result.create_tombstone)==(expected,create)
 rows.append(dict(case=name,last_active_ms=active,tombstone_ms=tomb,verdict=result.verdict.value,create_tombstone=create))
print(json.dumps(dict(commit='b71264afc2a32048b7d7a1fe7b876c8a07a03493',now_ms=10000,threshold_seconds=5,scope='single pure function, no Redis, ingress or cluster',trials=rows),indent=2))
