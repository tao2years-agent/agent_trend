#!/usr/bin/env python3
"""Merge all result sources into one record per (model,row) and score them.
Priority: old-host final backup < A/B host last backup < one-problem sandbox (p1).
Excluded: placeholders, colleague-401-affected host results, p1 runs killed at ~4h (process_exit)."""
import json,tarfile,glob,os,collections,sys
B='/leixinping/cowork_runs/20261016-model-eval/backup'; P='/leixinping/cowork_runs/20261016-model-eval/p1'
A401={'kimi-k3':[72,85,88,90,91,96,97,99,100,102,103],'deepseek-v4-1-flash':[48,54,55,56,59,61,76,105,106,108,109],
 'qwen3-8-flash':[65,67,70,72,73,74,75,108,110],'qwen3-8-max':[49,69,70,78,105,106,108],'glm-5-2':[85,88,91,96,97,99],'glm-5-3':[82,102,107,108]}
SRC={'kimi-k3':[f'{B}/1018T1452/kimi-k3-v2',f'{B}/1018T1652/kimi-k3-b'],
 'glm-5-2':[f'{B}/1018T1452/glm-5-2-v2',f'{B}/1018T1652/glm-5-2-b'],
 'deepseek-v4-1-flash':[f'{B}/1018T1452/deepseek-v4-1-flash-v2',f'{B}/1018T1652/deepseek-v4-1-flash-b'],
 'qwen3-8-max':[f'{B}/1018T1452/qwen3-8-max-v2',f'{B}/1018T1652/qwen3-8-max-b'],
 'qwen3-8-flash':[f'{B}/final-1900/qwen3-8-flash',f'{B}/1018T1652/qwen3-8-flash-b'],
 'glm-5-3':[f'{B}/1018T1652/glm-5-3-b']}
def statuses(tgz,slug):
    out={}
    with tarfile.open(tgz) as t:
        for m in t:
            n=m.name
            if n.startswith(f'{slug}/jobs/') and n.endswith('-cowork/STATUS.json') and n.count('/')==3:
                out[int(n.split('/')[2][:3])]=json.load(t.extractfile(m))
    return out
def valid(st,src):
    p,r=st.get('phase'),st.get('agent_end_reason'); el=st.get('agent_elapsed_seconds') or 0
    if r in ('assigned_elsewhere','migrated_inflight'): return None
    if p=='finished' and r in ('completed','time_budget'): return 'ok'
    if p=='finished' and r=='cancelled' and el>7*3600: return 'ok'
    if p=='finished' and r=='agent_error':
        e=str(st.get('agent_error',''))
        if src=='p1' and 13000<el<16000 and 'registry_error' not in e: return 'cut4h'
        if 'registry_error' in e or 'Invalid Claude protocol' in e: return 'ok'   # model called a disallowed tool
        return 'agent_error'
    return p
res={}
for slug,srcs in SRC.items():
    for s in srcs:
        for row,st in statuses(f'{s}/r.tgz',slug).items():
            v=valid(st,'host')
            if v is None: continue
            if row in A401[slug]: v='colleague401'
            cur=res.get((slug,row))
            if cur is None or cur['v']!='ok' or v=='ok': res[(slug,row)]={'v':v,'st':st,'src':os.path.basename(s)}
for f in glob.glob(f'{P}/results/*/*/r.tgz'):
    slug=f.split('/')[-3]; row=int(f.split('/')[-2])
    st=statuses(f,slug).get(row)
    if not st: continue
    v=valid(st,'p1'); cur=res.get((slug,row))
    if v=='ok' or cur is None or cur['v']!='ok': res[(slug,row)]={'v':v,'st':st,'src':'p1'}
json.dump({f'{k[0]}:{k[1]}':{'v':x['v'],'src':x['src'],'reward':x['st'].get('reward'),'reason':x['st'].get('agent_end_reason'),
  'elapsed':x['st'].get('agent_elapsed_seconds'),'tool_calls':x['st'].get('tool_calls'),'phase':x['st'].get('phase')} for k,x in res.items()},
  open('merged.json','w'),indent=0)
def rv(rw):
    if isinstance(rw,dict): return float(rw.get('reward') or 0), (rw.get('f2p_passed'),rw.get('f2p_total'))
    return float(rw or 0),(None,None)
print(f"{'model':22s} {'valid':>5s} {'pass':>4s} {'pass@valid':>10s} {'pass/101':>8s} {'f2p avg':>7s}  issues")
for slug in SRC:
    rows=[(r,x) for (s,r),x in res.items() if s==slug]
    ok=[x for r,x in rows if x['v']=='ok']
    passes=sum(1 for x in ok if rv(x['st'].get('reward'))[0]>=1)
    f2=[a/b for x in ok for a,b in [rv(x['st'].get('reward'))[1]] if a is not None and b]
    iss=collections.Counter(x['v'] for r,x in rows if x['v']!='ok')
    missing=101-len(rows)
    nodes=[(x['st'].get('reward') or {}) for x in ok]
    pr=[float(n.get('partial')) for n in nodes if isinstance(n,dict) and n.get('partial') is not None]
    print(f"{slug:22s} {len(ok):5d} {passes:4d} {passes/max(1,len(ok)):10.1%} {passes/101:8.1%} {sum(f2)/max(1,len(f2)):7.1%}  n_f2p={len(f2)} {dict(iss)} no_result={missing}")
