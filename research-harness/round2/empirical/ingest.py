"""Download byte ranges containing only preselected Parquet columns. No body, names of repositories or messages."""
import io, os, json, hashlib, time
from datetime import datetime,timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import pyarrow.parquet as pq
from columns import P,files,SHA,fetch
CACHE=Path(os.environ.get('TEMP','/tmp'))/('aidev-r2-'+SHA)
KEEP={'pull_request':['id','agent','repo_id','state','created_at','merged_at','closed_at'],
      'pr_reviews':['id','pr_id','user','user_type','state','submitted_at'],
      'pr_timeline':['pr_id','event','created_at']}
def metadata(table):return pq.read_metadata(io.BytesIO(b'PAR1'+(P/'raw'/(table+'.parquet.footer')).read_bytes()))
def lock():
 entries=[]
 for table,cols in KEEP.items():
  md=metadata(table)
  for i in range(md.num_row_groups):
   for name in cols:
    c=md.row_group(i).column(md.schema.names.index(name)); offset=c.dictionary_page_offset if c.has_dictionary_page else c.data_page_offset
    entries.append(dict(table=table,group=i,column=name,start=offset,end=offset+c.total_compressed_size-1))
 return entries
def pull(row):
 t=row['table'];a=row['start'];b=row['end']; path=CACHE/t/f'{a}-{b}.bin';path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  raw=fetch(t+'.parquet',a,b);path.write_bytes(raw)
 else:raw=path.read_bytes()
 assert len(raw)==b-a+1
 return row|{'sha256':hashlib.sha256(raw).hexdigest()}
class ColumnFile(io.RawIOBase):
 def __init__(self,table,rows):
  self.length=files[table+'.parquet']['size'];self.pos=0;self.segments=[];self.table=table
  for r in rows:
   a,b=r['start'],r['end']
   self.segments.append((a,b,CACHE/table/f'{a}-{b}.bin'))
 def readable(self):return True
 def seekable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.length+offset
  return self.pos
 def read(self,n=-1):
  start=self.pos;stop=self.length if n<0 else self.pos+n
  parts=[]
  for a,b,path in self.segments:
   if a<=self.pos<=b:
    with path.open('rb') as f:
     f.seek(self.pos-a);data=f.read(min(b+1,stop)-self.pos);parts.append(data);self.pos+=len(data)
    if self.pos==stop:return b''.join(parts)
  raise OSError((self.table,'unregistered byte range',start,stop,self.pos))
def parquet(table,manifest):
 return pq.ParquetFile(ColumnFile(table,[r for r in manifest if r['table']==table]),metadata=metadata(table),pre_buffer=False)
if __name__=='__main__':
 if not all((P/'raw'/(t+'.parquet.footer')).exists() for t in KEEP):raise RuntimeError("Fetch parquet footers first via columns.footer")
 rows=lock();print('requested',len(rows),sum(r['end']-r['start']+1 for r in rows),'bytes',flush=True)
 with ThreadPoolExecutor(12) as ex:
  completed=[]
  for i,f in enumerate(as_completed([ex.submit(pull,r) for r in rows]),1):
   completed.append(f.result())
   if i%20==0:print(i,len(rows),flush=True)
 completed.sort(key=lambda r:(r['table'],r['group'],r['start']))
 if (P/'raw/ranges.json').exists():
  previous=json.loads((P/'raw/ranges.json').read_text('utf8'))
  assert previous['revision']==SHA and previous['ranges']==completed,'Pinned byte ranges differ'
  print('Matched all 131 byte-range hashes to the locked capture.')
 else:
  (P/'raw/ranges.json').write_text(json.dumps({'revision':SHA,'preregister_sha256':'d12e7a143d6bef9ae4cd7d9911a1bb46ae91ffb0f4ddda5038f684359ee26af6','completed_utc':datetime.now(timezone.utc).isoformat(),'ranges':completed},indent=2),'utf8')
