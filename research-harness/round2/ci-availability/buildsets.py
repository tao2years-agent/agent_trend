"""Compare the scheduler's actual buildsets against the comment-defined round for paired sampled builds."""
from clocks import BASE,get
import json,hashlib,re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
def seconds(t):return datetime.fromisoformat(t.replace('Z','').replace('+00:00',''))
def query(case):
    result={'id':case['id'],'published_roster':case['roster'],'request_time':case['request_time']}
    sets=[]
    for side in ['prior','current']:
        endpoint=case[side]['official_url'];stat,build=get(endpoint)
        if not isinstance(build,dict) or not build.get('buildset',{}).get('uuid'):result[side]={'build_query':stat};sets.append(None);continue
        bs=build['buildset']['uuid'];assert re.fullmatch('[0-9a-f]{32}',bs)
        url='https://zuul.opendev.org/api/tenant/openstack/buildset/'+bs;stat,bsdata=get(url)
        row={'official_build':endpoint,'official_buildset':url,'query':stat,'build_pipeline':build.get('pipeline'),'linked_job':build.get('job_name'),'build_event_timestamp':build.get('event_timestamp'),'job_start':build.get('start_time'),'job_end':build.get('end_time')}
        result[side]=row
        if not isinstance(bsdata,dict) or bsdata.get('uuid')!=bs:sets.append(None);continue
        jobs=bsdata.get('builds',[]);roster={j['job_name'] for j in jobs if j['voting']}
        sets.append(roster)
        event=bsdata.get('event_timestamp')
        row.update(dict(event_time=event,first_start=bsdata.get('first_build_start_time'),last_end=bsdata.get('last_build_end_time'),pipeline=bsdata.get('pipeline'),result=bsdata.get('result'),
                        buildset_ref_count=len(bsdata.get('refs',[])),build_count=len(jobs),unique_voting_jobs=len(roster),voting_names_hash=hashlib.sha256('\n'.join(sorted(roster)).encode()).hexdigest(),
                        request_to_event_seconds=int((seconds(event)-seconds(case['request_time'])).total_seconds()) if event else None))
    if all(r is not None for r in sets):
        p,c=sets;result['actual_voting_name_set_changed']=p!=c;result['added_n']=len(c-p);result['removed_n']=len(p-c)
    return result
def main():
    data=json.loads((BASE/'clock-evidence.json').read_text());sample=[p for p in data['cases'] if p['prior']['matched'] and p['current']['matched']]
    with ThreadPoolExecutor(3) as pool:items=list(pool.map(query,sample))
    (BASE/'buildsets.json').write_text(json.dumps(items,indent=2),'utf8')
    for i in items:print(i['id'],i['published_roster'],i['prior'].get('pipeline'),i['current'].get('pipeline'),i['current'].get('request_to_event_seconds'),i.get('actual_voting_name_set_changed'))
if __name__=='__main__':main()
