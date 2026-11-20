"""Inspect fields of bounded BSON range samples, without deserializing object types or retaining values."""
from remote_index import fetch,url,BASE
import json,zlib,struct
def val(doc):
    i=4;allkeys=[];limited={}
    while i<len(doc) and doc[i]:
        t=doc[i];i+=1;j=doc.index(0,i);k=doc[i:j].decode();i=j+1;allkeys.append(k)
        if t in (2,13,14):
            n=struct.unpack_from('<i',doc,i)[0];value=doc[i+4:i+3+n].decode(errors='replace');i+=4+n
        elif t in (3,4):
            n=struct.unpack_from('<i',doc,i)[0];value=None;i+=n
        elif t in (1,9,17,18):value=None;i+=8
        elif t==7:value=None;i+=12
        elif t==8:value=bool(doc[i]);i+=1
        elif t==10:value=None
        elif t==16:value=struct.unpack_from('<i',doc,i)[0];i+=4
        elif t==5:n=struct.unpack_from('<i',doc,i)[0];i+=5+n;value=None
        else:raise ValueError('unknown BSON type '+str(t))
        if k in ['date_before','feature_key','bot_id','job_name','status','num_success_occurences','num_all_occurences','voting']:limited[k]=value
    return sorted(allkeys),limited
def main():
    members=json.loads((BASE/'mongo-directory.json').read_text())['members'];out=[]
    patterns=['recheck_builds_common/messages_filtered.bson','recheck_builds_common/all_10_years_detailed_info.bson','recheck_builds_common/recheck_builds.bson','recheck_builds_helper_years_20/jobs_occurrences.bson']
    for sf in patterns:
        m=next(x for x in members if x['member'].endswith(sf));start=m['offset'];size=131072
        data,stat=fetch(url+'?range_start='+str(start),start,start+size-1)
        row={'member':m['member'],'range':stat};out.append(row)
        if data is None:continue
        assert data[:4]==b'PK\x03\x04'
        a,b=struct.unpack_from('<HH',data,26);plen=30+a+b;raw=zlib.decompressobj(-15).decompress(data[plen:],3000000)
        i=0;keys=set();observed=0
        while len(raw)-i>=4:
            n=struct.unpack_from('<i',raw,i)[0]
            if n<5 or len(raw)-i<n:break
            cur,lim=val(raw[i:i+n]);keys.update(cur);i+=n;observed+=1
        row.update({'complete_prefix_records':observed,'observed_top_level_keys':sorted(keys),'header_bytes':plen})
    (BASE/'bson-samples.json').write_text(json.dumps(out,indent=2),'utf8')
    print(out)
if __name__=='__main__':main()
