from pathlib import Path
import collections,gzip,json
R=Path(__file__).resolve().parent
def main():
    d=json.loads(gzip.decompress((R/'raw/author-score-labels.json.gz').read_bytes()))
    agents=sorted(a for a in d['labels'] if not a.startswith('audit_'))
    issues=sorted(d['labels'][agents[0]]);assert len(issues)==297 and len(agents)==5
    outcomes={}
    for a in agents:
        j=json.loads((R/'raw'/('verified-'+a+'.json')).read_text('utf8'));resolved=set(j['resolved']) if 'resolved' in j else {i for i,v in j.items() if v['resolved']}
        outcomes[a]={i:(not d['labels'][a][i][0],i not in resolved) for i in issues}
    report=[]
    for col,judge in enumerate(['PBT_failed','SWE_unresolved']):
        for cue,abstain in [('archive-order',False),('original',False),('audit',False),('original',True),('audit',True)]:
            tally=collections.Counter();ranks=[]
            for i in issues:
                scores={a:d['failure_votes'][('audit_' if cue=='audit' else '')+a][i] for a in agents}
                order=sorted(agents,key=lambda a:-scores[a]) if cue!='archive-order' else agents
                cards=[a for a in order if not abstain or scores[a]>=3][:3]
                bad={a for a in agents if outcomes[a][i][col]};tally['eligible']+=1;tally['has_failure']+=bool(bad);tally['all_good']+=not bad;tally['shown_cards']+=len(cards);tally['any_cards']+=bool(cards)
                tally['called_on_all_good']+=not bad and bool(cards)
                if bad:
                    tally['top1_hit']+=bool(cards and cards[0] in bad);tally['top3_hit']+=bool(bad.intersection(cards));tally['abstain_with_failure']+=not cards
            report.append(dict(judge=judge,cue=cue,threshold='votes>=3' if abstain else 'all',**tally))
    (R/'card-replay.json').write_text(json.dumps(report,indent=2),'utf8')
    for x in report:print(x['judge'],x['cue'],x['threshold'],x['has_failure'],x['top1_hit'],x['top3_hit'],x['called_on_all_good'],x['shown_cards'],x['abstain_with_failure'])
if __name__=='__main__':main()
