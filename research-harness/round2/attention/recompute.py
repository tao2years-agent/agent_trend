"""Recompute published aggregate counts, visible task completions, and annotation times (no author code)."""
import csv,hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
def rows(name):
    with (B/'raw'/name).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main():
    src=json.loads((B/'sources.json').read_text('utf8'));assert len(src)==9
    for o in src:assert hashlib.file_digest((B/o['local']).open('rb'),'sha256').hexdigest()==o['sha256']
    f=rows('A05-Fig4-counts.csv');numeric=['effective','disruptive','ignored','total']
    for r in f:assert sum(int(r[k]) for k in numeric[:3])==int(r['total'])
    def aggregate(rr):return {k:sum(int(r[k]) for r in rr) for k in numeric}
    all_events=aggregate(f);obscure=aggregate([r for r in f if r['trigger'] in ['User idle','User select code']]);retained={k:all_events[k]-obscure[k] for k in numeric}
    assert list(all_events.values())==[212,48,138,398]
    t=rows('A02-Table3-counts.csv');games=['Tetris','Pacman','SpaceInvaders'];comps=[sum(int(r[k]) for k in games) for r in t]
    assert comps==[7,7,4];cue_n=sum(int(r['n_exposures']) for r in t[:2]);notes_n=int(t[2]['n_exposures']);p=sum(comps[:2])/cue_n;q=comps[2]/notes_n
    time=rows('A07-public-minute-projection.csv');arms={r['arm'] for r in time};timings={a:[int(r['annotated_main_minutes']) for r in time if r['arm']==a] for a in arms}
    out=dict(A05_all=all_events,A05_idle_select=obscure,A05_others=retained,A05_observed_share_of_disruption_in_idle_select=obscure['disruptive']/all_events['disruptive'],A05_observed_share_of_engagement_in_idle_select=obscure['effective']/all_events['effective'],A02_history_success=sum(comps[:2]),A02_history_exposures=cue_n,A02_notes_success=comps[2],A02_notes_exposures=notes_n,A02_descriptive_risk_difference=p-q,A02_descriptive_risk_ratio=p/q,A07_annotated_arm_counts={a:len(g) for a,g in timings.items()},A07_difference_minutes=sum(timings['AI'])/len(timings['AI'])-sum(timings['No-AI'])/len(timings['No-AI']),A04_accept_shown_literal=33523/168807,A01_reduction_based_on_rounded_means=(4.1-2.2)/4.1)
    assert len(time)==52 and out['A02_descriptive_risk_ratio']==1.75
    (B/'recalculated.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
if __name__=='__main__':main()
