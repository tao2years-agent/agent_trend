from pathlib import Path
import re,json,csv,hashlib
from collections import Counter
R=Path(__file__).resolve().parent;B=R.parent.parent
def load(n):return json.loads((R/(n+'.json')).read_text(encoding='utf-8-sig'))
def out(n,rows):
 with (R/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
entries=load('release-entries')
src={m['id']:m for f in ['archive','diff-sources','tag-sources','supplement-sources'] for m in load(f)}
for s in src.values():assert hashlib.sha256((B/s['path']).read_bytes()).hexdigest()==s['sha256']
ds=load('tag-diffs')
for d in ds:assert hashlib.sha256((B/d['diff_path']).read_bytes()).hexdigest()==d['diff_sha256']
keys={
'Argo Rollouts':r'abort scale|bind local interface|dashboard should only bind|bind to 127',
'Atlantis':r'sticky policy approvals|lock backend|drift detection and remediation APIs|stale head/base plan|verified managed.plan|apply lock|plan store|plan snapshot',
'PR-Agent':r'github checks|files excluded|preserve findings across review reruns|action fails on tool errors|self.review|findings across|incomplete review|excluded from review coverage',
'Sourcegraph src-cli':r'(?:batch.changes|fix/batch|remove/batches|workspace paths|changeset hooks)',
'Devin':r'per.PR auto.review|composable set of custom rules|personal access tokens default to approval required|network.policy edits now apply|whether Devin fixes Devin Review findings|Mark done replaces Archive|preflight|automation.{0,40}already.running|stop session',
'Jules':r'wind down|read.only|turndown'}
chosen={}
for line in (R/'decisions.txt').read_text(encoding='utf-8-sig').splitlines():
 if not line or line.startswith('#'):continue
 name,key,kind,fact,imp,extra=line.split('|');chosen[name,key]=(kind,fact,imp,extra)
rows=[];tl=[];counts={}
for e in entries:
 d=e['date'];n=e['product'];v=e['version']
 if not '2026-05-01'<=d<='2026-11-20':continue
 k=(n,d if n in ('Jules','Devin') else v);hit=re.search(keys[n],e['body'],re.I|re.S);sel=chosen.get(k)
 status='进入时间线' if sel else ('候选未入选' if hit else '未命中定向主题')
 reason=('同一控制点有明确状态或版本变化' if sel else ('接近研究范围，但此单元未进入预先收窄的对照链；不能推论本版没有其他变化' if hit else '指定控制点检索未命中；未以此认定完全无关'))
 rows.append(dict(product=n,date=d,entry=v,stage=e['stage'],screen=status,reason=reason,match=hit.group(0)[:100] if hit else '',url=e['url'],snapshot=e['source']))
 if sel:
  kind,fact,imp,extra=sel
  ids=' '.join([e['source'],*extra.split()]);assert all(i in src for i in ids.split())
  tl.append(dict(product=n,date=d,entry=v,change_type=kind,fact=fact,procurement_inference=imp,evidence_ids=ids,url=e['url']))
assert len(tl)==len(chosen) and len(rows)==113 and len(ds)==4
out('screening.csv',rows);out('timeline.csv',sorted(tl,key=lambda x:(x['date'],x['product'],x['entry'])))
for n in keys:
 es=[e for e in rows if e['product']==n];c=Counter(e['screen'] for e in es);counts[n]=dict(window=len(es),narrow_candidates=sum(e['screen']!='未命中定向主题' for e in es),timeline=c['进入时间线'],adjacent=c['候选未入选'],outside=c['未命中定向主题'],pre=sum(e['stage']=='pre' for e in es),criterion=keys[n])
(R/'coverage.json').write_text(json.dumps(counts,indent=2,ensure_ascii=False),encoding='utf-8')
(R/'sources.json').write_text(json.dumps(list(src.values()),indent=2,ensure_ascii=False),encoding='utf-8')
print([(k,v['window'],v['narrow_candidates'],v['timeline'],v['pre']) for k,v in counts.items()],len(src),len(tl))
