"""GET-only queries for a deterministic paired sample of public dated references. Persist only allowlisted fields."""
import requests,re,json,hashlib
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from extract import BASE,CACHE
def get(url):
    try:
        r=requests.get(url,timeout=(8,20),headers={'Accept':'application/json'})
        obs={'http':r.status_code,'media':r.headers.get('Content-Type'),'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()}
        if r.status_code!=200 or 'json' not in (r.headers.get('Content-Type') or '').lower():return obs,None
        obj=json.loads(r.content[5:] if r.content.startswith(b")]}\'") else r.content)
        return obs,obj
    except Exception as e:return {'error':type(e).__name__},None
def check(row):
    ret={k:row[k] for k in ['id','roster','same_job','request_time']}
    uuids=[row['prior_uuid'],row['current_uuid']]
    for name,uid in zip(['prior','current'],uuids):
        endpoint='https://zuul.opendev.org/api/tenant/openstack/build/'+uid
        stat,obj=get(endpoint)
        known=isinstance(obj,dict) and obj.get('uuid')==uid
        ret[name]={'official_url':endpoint,'query':stat,'matched':known}
        if known:
            ret[name].update({k:obj.get(k) for k in ['start_time','end_time','job_name','result','voting']})
            ref=obj.get('ref') or obj
            ret[name]['patch_matched']=str(ref.get('change'))==str(row['change']) and str(ref.get('patchset'))==str(row['patch'])
    url='https://review.opendev.org/changes/'+str(row['change'])+'/messages'
    stat,objs=get(url)
    ret['gerrit']={'query':stat,'official_url':url,'patch_messages':None,'prior_reports':[],'current_reports':[],'request_posts':[],'start_notices_between_request_and_report':[]}
    if isinstance(objs,list):
        sub=[(m.get('date',''),m.get('message','')) for m in objs if str(m.get('_revision_number'))==str(row['patch'])]
        g=ret['gerrit'];g['patch_messages']=len(sub);req=row['request_time']
        for t,msg in sub:
            if t[:19]==req[:19] and re.search(r'\brecheck\b',msg,re.I):g['request_posts'].append(t)
            for uid,side in zip(uuids,['prior_reports','current_reports']):
                if uid in msg:g[side].append(t)
        t_end=min(g['current_reports'],default='')
        if t_end:
            for t,msg in sub:
                if req<=t<t_end and re.search(r'\bbuild(?:s|set)? (?:has )?started\b|\bstarting (?:the )?build\b',msg,re.I):
                    g['start_notices_between_request_and_report'].append(t)
    return ret
def main():
    probes=json.loads((CACHE/'probes.json').read_text());selected=[]
    for typ in ['same','changed']:
        group=sorted((p for p in probes if p['roster']==typ),key=lambda r:r['request_time'],reverse=True)[:8]
        selected.extend(group)
    with ThreadPoolExecutor(max_workers=3) as pool:r=list(pool.map(check,selected))
    control='https://zuul.opendev.org/api/tenant/openstack/builds?limit=1'
    stat,ls=get(control)
    obj={'queried_at_utc':datetime.now(timezone.utc).isoformat(),'available_monthly_candidates':len(probes),'sample_rule':'one lowest case hash per month and roster status, two build UUIDs present; latest eight months per status among candidates','current_api_control':{'url':control,'query':stat,'current_list_has_start_end':isinstance(ls,list) and bool(ls) and all(ls[0].get(k) for k in ['start_time','end_time'])},'cases':r}
    (BASE/'clock-evidence.json').write_text(json.dumps(obj,indent=2),'utf8')
    print('cases',len(r),'build clocks found',sum(x[s]['matched'] for x in r for s in ['prior','current']),'Gerrit correlated pairs',sum(bool(x['gerrit']['prior_reports'] and x['gerrit']['current_reports'] and x['gerrit']['request_posts']) for x in r),flush=True)
if __name__=='__main__':main()
