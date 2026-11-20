"""Reconstruct the observable historical minimum on the PRIOR voting roster at the request second.
Use whole relevant BSON member only. One-run and rerun histories are assembled before decision time.
"""
from scan import BASE,CACHE
from bson_sample import val
from extract import feature_table,key
from array import array
from datetime import datetime,timezone
from collections import Counter
import numpy as np,pandas as pd
import struct,zlib,json,hashlib
from sklearn.metrics import roc_auc_score,average_precision_score
def documents(meta):
    stream=zlib.decompressobj(-15);remain=b'';crc=0;size=0
    path=CACHE/'jobs-occurrences.deflate'
    with path.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==meta['compressed_sha256']
    with path.open('rb') as f:
        while block:=f.read(512*1024):
            out=stream.decompress(block);crc=zlib.crc32(out,crc);size+=len(out)
            dat=remain+out;i=0
            while len(dat)-i>=4:
                n=struct.unpack_from('<i',dat,i)[0]
                if not 5<=n<=16000000:raise ValueError('invalid BSON length')
                if n>len(dat)-i:break
                yield val(dat[i:i+n])[1]
                i+=n
            remain=dat[i:]
    assert stream.eof and crc==meta['zip_crc32'] and size==meta['uncompressed']
    yield {'eof_metadata':dict(verified_uncompressed_bytes=size,crc32=crc,remaining_incomplete_document_bytes=len(remain))}
def main():
    meta=json.loads((BASE/'history-member.json').read_text())
    df=feature_table()
    pairs=pd.read_csv(CACHE/'paired.tsv.gz',sep='\t',usecols=['row','time_agrees','previous_failure','before','nprev','seqgap','npost']).set_index('row')
    df=df.join(pairs);dt=pd.to_datetime(df.date_of_recheck)
    order=df.sort_values(['date_of_recheck','key']).index;cut1=dt[order[int(.6*len(df))]];cut2=dt[order[int(.8*len(df))]]
    gap=pd.Timedelta(days=7);tr=dt<cut1-gap;dv=(dt>=cut1)&(dt<cut2-gap);te=dt>=cut2
    safe=(df.before.eq(1)&df.time_agrees.eq(1)&df.previous_failure.eq(1)&df.nprev.gt(0))
    prior_ix={};curr_ix={};obs={};prior_rosters={};positive_control={};runs=0;voting=0;excluded=0
    for i in df.index[dv|te]:
        cp,p,s=key(df.key[i]);curr_ix[str((cp,p,s))]=i
        if safe[i]:
            k=str((cp,p,s-int(df.seqgap[i])));assert k not in prior_ix;prior_ix[k]=i
    jobcode={};authors_last={};bad_prefix=set();last_code=None;min_ts=2**32;max_ts=0
    for doc in documents(meta):
        if 'eof_metadata' in doc:verification=doc['eof_metadata'];break
        runs+=1
        if not doc['voting']:excluded+=1;continue
        voting+=1;pair=(doc['bot_id'],doc['job_name']);code=jobcode.setdefault(pair,len(jobcode));fk=doc['feature_key']
        if code not in obs:obs[code]=array('q')
        sec=int(datetime.fromisoformat(doc['date_before']).replace(tzinfo=timezone.utc).timestamp());min_ts=min(min_ts,sec);max_ts=max(max_ts,sec)
        if len(obs[code])!=doc['num_all_occurences']:bad_prefix.add(code)
        obs[code].append(2*sec+int(doc['status']=='success'));last_code=code
        authors_last[code]=max(doc['num_all_occurences'],authors_last.get(code,0))
        ix=prior_ix.get(fk)
        if ix is not None:prior_rosters.setdefault(ix,{})[code]=max(sec,prior_rosters.get(ix,{}).get(code,0))
        ix=curr_ix.get(fk)
        if ix is not None:
            nums=positive_control.setdefault(ix,{})
            total=doc['num_all_occurences']
            nums[code]=doc['num_success_occurences']/total if total else float('nan')
    hist={};suspect=set(bad_prefix);extra=set()
    if verification['remaining_incomplete_document_bytes']:suspect.add(last_code)
    for c,records in obs.items():
        enc=np.array(records);enc.sort();hist[c]=(enc//2,np.cumsum(enc%2,dtype=np.int32))
        if authors_last[c]+1>len(enc):suspect.add(c)
        if authors_last[c]+1<len(enc):extra.add(c)
    # All dates must fall inside the author's 20-year window; otherwise implement two-sided subtraction.
    assert max_ts-min_ts<20*365*86400
    base=df.loc[tr,'label'].mean()
    proj=df[tr].groupby('project').label.agg(['sum','size']);proj=(proj['sum']+20*base)/(proj['size']+20)
    project=df.project.map(proj).fillna(base).to_numpy();scores=project.copy()
    observed=pd.Series(False,index=df.index);reasons=Counter();check=Counter()
    def prior_counts(cut,c):
        ts,counts=hist[c];j=ts.searchsorted(cut,side='left')
        return counts[j-1]/j if j else None
    for i in df.index[dv|te]:
        z=positive_control.get(i,{});pub=df.jobs_success_ratio[i]
        if len(z)==df.npost[i] and z and all(np.isfinite(x) for x in z.values()) and np.isfinite(pub):
            check['finite_full_current_roster']+=1
            if abs(min(z.values())-pub)<1e-8:check['published_min_reproduced']+=1
        if not safe[i]:reason='prior_empty_or_unavailable'
        else:
            roster=prior_rosters.get(i,{})
            sec=int(dt[i].to_pydatetime().replace(tzinfo=timezone.utc).timestamp())
            if len(roster)!=df.nprev[i]:reason='prior_count_mismatch'
            elif any(c in suspect or c in extra for c in roster):reason='incomplete_job_history'
            elif any(s>=sec for s in roster.values()):reason='prior_report_not_before_request'
            else:
                vals=[prior_counts(sec,c) for c in roster]
                if None in vals:reason='no_prior_job_history'
                else:reason='observable_roster_with_asof_history';scores[i]=min(vals);observed[i]=True
        reasons[('validation' if dv[i] else 'test',reason)]+=1
    truth=df.label.to_numpy(bool)
    pos=np.sort(scores[dv&truth]);threshold=float(pos[int(np.floor((1-.95)*len(pos)))])
    results=[]
    for nm,group in [('all_test',te),('asof_reconstructed_test',te&observed),('project_fallback_test',te&~observed)]:
        y=truth[group];s=scores[group];k=s>=threshold
        results.append(dict(cohort=nm,n=len(y),green=int(y.sum()),rerun=int(k.sum()),missed_green=int((~k&y).sum()),avoided_red=int((~k&~y).sum()),auc=roc_auc_score(y,s) if len(set(y))>1 else None,ap=average_precision_score(y,s) if y.any() else None))
    selected=te&observed; peers=[]
    pub=df.jobs_success_ratio.where(df.jobs_success_ratio.between(0,1),base).fillna(base).to_numpy()
    for tag,signal in [('project',project),('published_retrospective',pub),('prior_asof',scores)]:
        positives=np.sort(signal[dv&truth]);qt=float(positives[int(np.floor((1-.95)*len(positives)))]);y=truth[selected];ss=signal[selected];keep=ss>=qt
        peers.append(dict(method=tag,n=len(y),green=int(y.sum()),rerun=int(keep.sum()),missed_green=int((~keep&y).sum()),avoided_red=int((~keep&~y).sum()),auc=roc_auc_score(y,ss),ap=average_precision_score(y,ss)))
    out=dict(verified=verification, same_reconstructable_cohort=peers, job_histories_with_prefix_count_disagreement=len(bad_prefix),tail_job_conservatively_excluded=bool(verification['remaining_incomplete_document_bytes']),documents=runs,voting=voting,nonvoting=excluded,distinct_jobs=len(hist),histories_with_missing_or_extra_observations=len(suspect|extra),
        min_date=datetime.fromtimestamp(min_ts,timezone.utc).isoformat(),max_date=datetime.fromtimestamp(max_ts,timezone.utc).isoformat(),positive_control=check,
        partition_counts={k:{c:n for (g,c),n in reasons.items() if g==k} for k in ['validation','test']},threshold=threshold,results=results)
    (BASE/'asof-replay.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
if __name__=='__main__':main()
