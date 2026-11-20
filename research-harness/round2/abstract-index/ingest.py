"""Archive each public program detail once, resume interrupted sessions, preserve source hashes."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import csv,datetime,hashlib,json,sys,time,threading
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'venue-review'))
import fetch
def tab(p):
    with p.open(encoding='utf8',newline='') as fp:return list(csv.DictReader(fp,delimiter='\t'))
frame=fetch.readframe()
known={}
for d in ['venue-review','recall']:
    for v in tab(R.parent/d/'abstracts.tsv'):
        known[v['id']]=dict(id=v['id'],venue=v['venue'],title=v['title'],abstract=v['abstract'],url=v['url'],path='../'+d+'/'+v['path'],sha256=v['sha256'])
# Include already captured public full pages used for the first random holdout.
for v in tab(R.parent/'venue-frame/sample-review.tsv'):
    ident=v['id'];dest=R.parent/'venue-frame'/v['path']
    if ident not in known and dest.is_file() and v.get('abstract'):
        row=next(x for x in frame if x['id']==ident)
        known[ident]=dict(id=ident,venue=row['venue'],title=row['title'],abstract=v['abstract'],url=v['url'],path='../venue-frame/'+v['path'],sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
fetch.BASE=R
forms={v:fetch.getform(v) for v in set(row['venue'] for row in frame)}
start_lock=threading.Lock();last=0
def capture(row):
    global last
    v=known.get(row['id'])
    if v is not None:return v
    try:
        # Throttle new public detail requests only. No wait for cached replays.
        if not (R/'raw'/(row['id']+'.json')).exists():
            with start_lock:
                now=time.monotonic();time.sleep(max(0,.7-(now-last)));last=time.monotonic()
        d=fetch.capturepaper(row,forms)
        assert d['title']==d['modal_title'],(row['id'],d['title'],d['modal_title'])
        return {k:d[k] for k in ['id','venue','title','abstract','url','path','sha256']}
    except Exception as e:
        return dict(id=row['id'],venue=row['venue'],title=row['title'],url=row['url'],abstract='',path='',sha256='',error=str(e)[:250])
if __name__=='__main__':
    out={}
    with ThreadPoolExecutor(2) as pool:
        jobs={pool.submit(capture,row):row for row in frame}
        for f in as_completed(jobs):
            row=f.result();out[row['id']]=row
            if len(out)%100==0:
                print(len(out),'/',len(frame),flush=True)
                (R/'ingest-progress.json').write_text(json.dumps(dict(records=len(out),cached_before=len(known),with_abstract=sum(bool(v['abstract']) for v in out.values())),indent=2),'utf8')
    vals=[out[v['id']] for v in frame]
    for record in vals:
        if record['path']:
            stat=(R/record['path']).stat()
            record['snapshot_written_utc']=datetime.datetime.fromtimestamp(stat.st_mtime,datetime.timezone.utc).isoformat()
            record['snapshot_bytes']=stat.st_size
    (R/'abstracts.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in vals),'utf8')
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (R/'ingest-progress.json').write_text(json.dumps(dict(records=len(vals),cached_before=len(known),with_abstract=sum(bool(v['abstract']) for v in vals),finished=True),indent=2),'utf8')
    (R/'audit.json').write_text(json.dumps(dict(total=len(vals),with_abstract=sum(bool(v['abstract']) for v in vals),reused=len(known),ended_utc=stamp,errors=[v for v in vals if 'error' in v]),indent=2),'utf8')
