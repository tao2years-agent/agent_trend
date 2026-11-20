"""Join previously prepared features with the exact same patch/recheck events.

Writes no user identifiers, comments or URLs to the public output. Compact internal
temporary rows hold integer roster codes and numeric feature-row offsets only.
"""
from scan import *
from records import records
from collections import defaultdict
import pandas as pd
import re,csv,gzip
from datetime import timedelta
from urllib.parse import urlsplit
FEATURE='replication_package_rechecks/features_datasets/final_datasets/features_years_20.csv'

def feature_table():
    with zipfile.ZipFile(ARCHIVE) as z, z.open(FEATURE) as f:
        return pd.read_csv(f,usecols=['key','project','label','date_of_recheck','jobs_success_ratio'])

def key(s):
    fields=re.findall(r'\d+',s)
    assert len(fields) in [2,3] and not re.search(r'[A-Za-z]',s)
    return tuple(map(int,fields))

def main():
    df=feature_table()
    targets={key(k):i for i,k in enumerate(df.key)}
    assert len(df)==len(targets)==353700
    previous_hist=defaultdict(lambda:[0,0]);codebook={};stats=Counter();out_examples={};clock_probes={}; tech=re.compile(r'^(?:openstack|tox|gate|tempest|zuul|neutron|nova|devstack|devstack-gate|build|unit|check)[a-z0-9_.:-]{1,105}$')
    cut=(pd.Timestamp('2018-01-15 08:04:32')-pd.Timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    def members(round_doc):
        jobs=defaultdict(list);obs=[];bots=set();samples={};links={};all_count=0
        for bot,info in round_doc.items():
            if bot in ('recheck_number','status','') or not isinstance(info,dict):continue
            bots.add(bot)
            if info.get('started_at'):obs.append(info['started_at'])
            for j in info.get('jobs',[]):
                all_count+=1
                if not j.get('voting') or not j.get('name'):continue
                n=j['name'];pair=(bot,n)
                if pair not in codebook:codebook[pair]=len(codebook)+1
                cid=codebook[pair];jobs[cid].append(j.get('status')=='success')
                if tech.fullmatch(n):samples[cid]=n
                m=re.search(r'/build/([0-9a-f]{32})(?:/|\b)',str(j.get('link','')))
                if m:links[cid]=m.group(1)
        return jobs,obs,bots,samples,links,all_count
    header=['row','label_agrees','time_agrees','previous_failure','seqgap','before','after','both_empty','changed','bot_changed','name_changed','nprev','npost','added','removed','prev_success','prev_failed','prev_posts','post_posts','prev_to_request_s','request_to_post_s','prior_codes']
    seen=set()
    with gzip.open(CACHE/'paired.tsv.gz','wt',encoding='utf8',newline='') as fout:
        w=csv.DictWriter(fout,fieldnames=header,delimiter='\t',lineterminator='\n');w.writeheader()
        for doc in records():
            stats['patch_records']+=1
            patch=key(doc['key'])
            req={int(v['recheck_number']):v['created_at'] for v in doc.get('rerun_requestors',[]) if v.get('created_at')}
            rounds=doc.get('bot') or []
            for index in range(1,len(rounds)):
                current=rounds[index];prev=rounds[index-1];seq=int(current['recheck_number']);ix=targets.get((*patch,seq))
                if ix is None:continue
                if ix in seen:
                    stats['duplicate_matched_rows']+=1;continue
                seen.add(ix)
                reqtime=req.get(seq,''); prevjobs,prevobs,prevbots,pnames,plinks,_=members(prev)
                currjobs,currobs,currbots,cnames,clinks,_=members(current)
                pset=set(prevjobs);cset=set(currjobs)
                prior_t=max(prevobs,default='');next_t=min(currobs,default='')
                prior_ok=bool(prior_t and reqtime and prior_t<reqtime);after=bool(next_t and reqtime and next_t>reqtime)
                req_match=reqtime==df.date_of_recheck.iat[ix]
                previous_failure=(prev.get('status')=='failure')
                label_agrees=int(current.get('status')=='success')==int(df.label.iat[ix])
                delta=lambda l,h:int((pd.Timestamp(h)-pd.Timestamp(l)).total_seconds()) if l and h else ''
                ids=' '.join(map(str,sorted(pset))) if prior_ok and req_match and previous_failure else ''
                row=dict(row=ix,label_agrees=int(label_agrees),time_agrees=int(req_match),previous_failure=int(previous_failure),seqgap=seq-int(prev['recheck_number']),before=int(prior_ok),after=int(after),both_empty=int(not pset and not cset),changed=int(pset!=cset),bot_changed=int(prevbots!=currbots),name_changed=0,nprev=len(pset),npost=len(cset),added=len(cset-pset),removed=len(pset-cset),prev_success=sum(sum(a) for a in prevjobs.values()),prev_failed=sum(len(a)-sum(a) for a in prevjobs.values()),prev_posts=len(prevobs),post_posts=len(currobs),prev_to_request_s=delta(prior_t,reqtime),request_to_post_s=delta(reqtime,next_t),prior_codes=ids)
                bare=lambda d:{j['name'] for b,info in d.items() if b not in ('recheck_number','status','') and isinstance(info,dict) for j in info.get('jobs',[]) if j.get('voting') and j.get('name')}
                row['name_changed']=int(bare(prev)!=bare(current))
                w.writerow(row)
                if prior_ok and req_match and previous_failure and reqtime<cut:
                    for code,flags in prevjobs.items():
                        previous_hist[code][0]+=sum(flags);previous_hist[code][1]+=len(flags)
                if prior_ok and after and req_match and previous_failure and label_agrees and pset and cset:
                    typ='changed' if pset!=cset else 'same';tag=(typ,reqtime[:4])
                    pid=hashlib.sha256(('recheck-availability|'+str((*patch,seq))).encode()).hexdigest()[:20]
                    if tag not in out_examples or pid<out_examples[tag][0]:
                        added=sorted({cnames[c] for c in cset-pset if c in cnames})[:6]
                        removed=sorted({pnames[c] for c in pset-cset if c in pnames})[:6]
                        common=sorted({pnames[c] for c in pset&cset if c in pnames})[:6]
                        if (typ=='same' and common) or (typ=='changed' and (added or removed)):
                            out_examples[tag]=(pid,dict(case=pid,roster=typ,request_time=reqtime,latest_recorded_prior_bot_comment=prior_t,earliest_recorded_next_bot_comment=next_t,previous_size=len(pset),new_size=len(cset),added_sample=added,removed_sample=removed,common_sample=common,outcome=int(df.label.iat[ix])))
                    if reqtime>='2022-01-01' and plinks and clinks:
                        anchor=(typ,reqtime[:7]); shared=sorted(plinks.keys() & clinks.keys()); c=shared[0] if shared else None;old=plinks[c] if c else min(plinks.values());new=clinks[c] if c else min(clinks.values())
                        if anchor not in clock_probes or pid<clock_probes[anchor]['id']:
                            clock_probes[anchor]=dict(id=pid,roster=typ,request_time=reqtime,change=patch[0],patch=patch[1],same_job=bool(c),prior_uuid=old,current_uuid=new)
            if stats['patch_records']%50000==0:print('patches',stats['patch_records'],'matched',len(seen),flush=True)
    (CACHE/'hist.json').write_text(json.dumps(previous_hist),encoding='utf8')
    (CACHE/'probes.json').write_text(json.dumps(list(clock_probes.values())),encoding='utf8')
    (BASE/'examples.json').write_text(json.dumps([q[1] for _,q in sorted(out_examples.items())],indent=2),encoding='utf8')
    stats['n_matched']=len(seen);stats['n_model_rows']=len(df);stats['n_unmatched']=len(df)-len(seen);stats['distinct_sampled_bot_job_pairs']=len(codebook)
    (BASE/'join.json').write_text(json.dumps(stats,indent=2),encoding='utf8');print(stats)
if __name__=='__main__':main()
