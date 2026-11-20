import json,os,hashlib,struct,sys,time,concurrent.futures as CF,io
from pathlib import Path
import pyarrow.parquet as pq
from discover import get
P=Path(__file__).resolve().parent
tree=json.loads((P/'raw/tree.json').read_text('utf8'));SHA=tree['revision']; files={x['path']:x for x in tree['files']}
def fetch(name,start,end):
 url=f'https://huggingface.co/datasets/hao-li/AIDev/resolve/{SHA}/{name}?download=true&part={start}-{end}'
 r=get(url,headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},stream=True)
 if r.status_code!=206 or r.headers.get('Content-Range','').split('/')[0]!=f'bytes {start}-{end}':
  r.close();raise ValueError((name,start,end,r.status_code,r.headers.get('Content-Range')))
 b=r.content;assert len(b)==end-start+1
 return b
def footer(name):
 size=files[name]['size'];b=fetch(name,size-65536,size-1);n=int.from_bytes(b[-8:-4],'little');assert b[-4:]==b'PAR1'
 if n+8>len(b):b=fetch(name,size-n-8,size-1)
 foot=b[-8-n:];p=P/'raw'/(name+'.footer');p.write_bytes(foot)
 md=pq.read_metadata(io.BytesIO(b'PAR1'+foot))
 print(name,md.num_rows,md.num_row_groups,md.schema.names,flush=True)
 return md
if __name__=='__main__':
 with CF.ThreadPoolExecutor(2) as ex:list(ex.map(footer,['pull_request.parquet','pr_reviews.parquet','pr_timeline.parquet']))
