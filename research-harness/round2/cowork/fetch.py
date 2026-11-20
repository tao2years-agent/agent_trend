"""Only retrieve public benchmark metadata and scorer source. Never execute code from the bundle."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,requests,time
R=Path(__file__).resolve().parent
SHA='529b67ddf03ff6efd74658b4b2a436abf371c5cf'
BASE='https://huggingface.co/datasets/Tokenwave-AI/swe-cowork/resolve/'+SHA+'/'
def capture(task):
    name,url=task
    path=R/'raw'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    meta=path.with_name(path.name+'.capture.json')
    if path.exists() and meta.exists():
        m=json.loads(meta.read_bytes())
        assert hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256']
        return m
    for i in range(3):
        try:
            res=requests.get(url,timeout=(12,80));res.raise_for_status();break
        except requests.RequestException:
            if i==2:raise
            time.sleep(1+i*3)
    raw=res.content
    assert not (path.is_file() and path.read_bytes()!=raw)
    path.write_bytes(raw)
    m=dict(artifact=name,url=url,path=path.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),captured=datetime.now(timezone.utc).isoformat())
    meta.write_text(json.dumps(m,indent=2),'utf8');return m
if __name__=='__main__':
    listing=capture(('release-files.json','https://huggingface.co/api/datasets/Tokenwave-AI/swe-cowork/revision/'+SHA+'?blobs=true'))
    package=json.loads((R/listing['path']).read_bytes());assert package['sha']==SHA
    files=['data/tasks.parquet','eval-kit/analysis/cowork-skill/scripts/check_paper_numbers.py','eval-kit/scoring/score_campaign.py','README.md','docs/RUNNING_EVAL.zh.md']
    with ThreadPoolExecutor(4) as ex:result=list(ex.map(capture,[(x,BASE+x) for x in files]))
    (R/'sources.json').write_text(json.dumps([listing]+result,indent=2),'utf8')
    import pyarrow.parquet as pq
    d=pq.read_table(R/'raw/data/tasks.parquet');print(d.num_rows,d.column_names);print([x['rfilename'] for x in package['siblings'] if x['rfilename'].startswith(('eval-kit/scoring','eval-kit/workplace'))][:100])
    task=next(x['rfilename'].split('/')[2] for x in package['siblings'] if x['rfilename'].startswith('release/tasks/') and len(x['rfilename'].split('/'))>3)
    print([x['rfilename'] for x in package['siblings'] if x['rfilename'].startswith('release/tasks/'+task+'/') and len(x['rfilename'].split('/'))<=5][:60])

