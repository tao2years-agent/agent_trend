"""Freeze a numeric, privacy-minimized projection of the researchers' fixed public annotation archive."""
from pathlib import Path
import io,zipfile,json,hashlib,requests,csv,re,datetime
from statistics import mean,median
B=Path(__file__).resolve().parent
commit='bae6eab7b80ab652d612ff9a9ee2d72dddd754aa'
repo='safety-research/how-ai-impacts-skill-formation'
u=f'https://codeload.github.com/{repo}/zip/{commit}'
def main():
    r=requests.get(u,timeout=30);r.raise_for_status();data=r.content;rows=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in sorted(z.namelist()):
            if not re.search(r'/annotated_transcripts/p[0-9]+\.json$',name):continue
            raw=z.read(name);x=json.loads(raw);assert isinstance(x['main_task_minutes'],(int,float))
            rows.append(dict(source_file=name.split('/')[-1],arm=x['condition'],annotated_main_minutes=x['main_task_minutes'],annotated_warmup_minutes=x['warmup_task_minutes'],source_sha256=hashlib.sha256(raw).hexdigest()))
    with (B/'raw'/'A07-public-minute-projection.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    groups={arm:[r['annotated_main_minutes'] for r in rows if r['arm']==arm] for arm in sorted({r['arm'] for r in rows})}
    out=dict(repo=repo,commit=commit,archive_url=u,archive_sha256=hashlib.sha256(data).hexdigest(),retrieval_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),n=len(rows),numeric_coverage={a:dict(n=len(g),mean=mean(g),median=median(g),min=min(g),max=max(g)) for a,g in groups.items()},annotation_difference_minutes=None)
    labels=list(groups);other=next(k for k in labels if k!='AI');out['annotation_difference_minutes']=mean(groups['AI'])-mean(groups[other])
    (B/'A07-recalculated.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
if __name__=='__main__':main()
