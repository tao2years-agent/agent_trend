"""Exercise the exact upstream function ASTs without importing provider clients or running any agents."""
from pathlib import Path
import ast,contextlib,hashlib,io,json,tempfile
P=Path(__file__).resolve().parent
sources=json.loads((P/'sources.json').read_text('utf8'))
def functions(suffix,names,globals_):
 r=next(r for r in sources if r['path'].endswith(suffix))
 f=P/r['path']; data=f.read_bytes(); assert hashlib.sha256(data).hexdigest()==r['sha256']
 tree=ast.parse(data,filename=str(f)); selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in selected}==set(names)
 exec(compile(ast.Module(body=selected,type_ignores=[]),str(f),'exec'),globals_)
 return {n:globals_[n]for n in names}
rows=[]
with tempfile.TemporaryDirectory() as scratch:
 f=Path(scratch)/'frontier_val.json'
 frontier=functions('terminal_bench_2/meta_harness.py',['update_frontier','compute_pass_rates'],{'json':json,'FRONTIER_VAL':f})
 for name,A,B,expected,expected_B in [('baseline',[1,1],[0,0],'baseline','baseline'),('tied_mean',[1,0],[1,0],'baseline','tied_mean'),('worse_mean',[0,0],[1,0],'baseline','tied_mean'),('better_mean',[1,1],[1,0],'better_mean','tied_mean')]:
  per,avg=frontier['compute_pass_rates']({'A':A,'B':B});frontier['update_frontier']({name:(per,avg)})
  state=json.loads(f.read_text());assert (state['_best']['agent'],state['B']['best_agent'])==(expected,expected_B)
  rows.append({'case':'Meta-Harness '+name,'trial_rewards':{'A':A,'B':B},'avg':avg,'overall':state['_best']['agent'],'best_by_task':{n:state[n]['best_agent']for n in ['A','B']}})
winner=functions('ahe/182ea06e578df7b1d503eca537503c1e4c5a8a58/evolve.py',['select_variant_winner'],{})['select_variant_winner']
for desc,variants,base,idx,warning in [('lower_than_baseline',[(0,.50,0),(1,.60,1)],.80,1,True),('tie_exception',[(0,.80,2),(1,.80,0)],.80,1,False),('equal_rate_exception_ordered',[(0,.80,0),(1,.80,0)],.80,0,False)]:
 vr=[{'idx':i,'stats':{'pass_rate':r,'n_exception':e}}for i,r,e in variants]
 with contextlib.redirect_stdout(io.StringIO())as log:actual=winner(vr,{'pass_rate':base})
 w='Warning:' in log.getvalue();assert(actual,w)==(idx,warning)
 rows.append({'case':'AHE '+desc,'base':base,'variants':vr,'selected':actual,'warned':w})
evaluate=functions('scripts/verify_manifest.py',['evaluate_predictions'],{})['evaluate_predictions']
for label,passed,failed,at_risk,expected in [('declared_risk',['intended'],['r1'],['r1'],'revert'),('unlisted_failures',['intended'],['r1','r2'],[],'keep'),('missing_observations',[],[],[],'partial'),('intended_not_fixed',[],['intended'],[],'revert')]:
 change=[{'predicted_impact':{'expected_fixes':['intended'],'at_risk_regressions':at_risk}}]; rr=evaluate(change,{'passed':passed,'failed':failed});assert rr['verdict']==expected
 rows.append({'case':'AHE manifest '+label,'changes':change,'passed':passed,'failed':failed,'verdict':rr['verdict']})
(P/'probe-results.json').write_text(json.dumps(rows,indent=2),'utf8')
print('Passed',len(rows),'no-model/no-service scenarios against four original functions')
