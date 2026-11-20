from pathlib import Path
import json
R=Path(__file__).resolve().parent
def run(f):
    merged=[p for p in f['prs'] if p['merged']]
    humans=[p for p in merged if p['actor']!='agent']
    members=sum(f['membership_days'].values())/30
    j=[p for p in merged if p['actor']=='agent' or 'agent' in p['commits']]
    pure=[p for p in humans if 'agent' not in p['commits']]
    lb={}
    for minimum in [0.25,0.26]:
        flags={k for k,x in f['developer_days'].items() if x['accepted']/x['committed']>=minimum}
        hits=[p['id'] for p in pure if sum(c in flags for c in p['commits'])/len(p['commits'])>=0.1]
        lb[str(minimum)]={'numerator_ids':hits,'denominator_ids':[p['id'] for p in pure]}
    return dict(DX_PR_throughput={'numerator_ids':[p['id'] for p in humans],'denominator_developer_months':members,'value':len(humans)/members},Jellyfish_agent_involvement={'numerator_ids':[p['id'] for p in j],'denominator':len(merged),'value':len(j)/len(merged)},LinearB_pure_human_subset=lb)
if __name__=='__main__':
    out=run(json.loads((R/'fixture.json').read_text('utf-8-sig')))
    assert out['DX_PR_throughput']['value']==1.6 and out['Jellyfish_agent_involvement']['value']==0.4
    assert out['LinearB_pure_human_subset']['0.25']['numerator_ids']==['1','5'] and not out['LinearB_pure_human_subset']['0.26']['numerator_ids']
    (R/'fixture-results.json').write_text(json.dumps(out,indent=2),'utf8');print('fixture passed')
