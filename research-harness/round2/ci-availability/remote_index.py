"""Read just the hosted ZIP central directory and fixed-size slices. Ignore payloads."""
import struct,zipfile,requests,io,json,datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent
url='https://zenodo.org/api/records/15559526/files/dataset.zip/content'
size=7037207133
def fetch(url,start,end):
    with requests.get(url,headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},timeout=(10,45),stream=True) as r:
        if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/{size}':
            return None,{'http':r.status_code,'content_range':r.headers.get('Content-Range'),'media':r.headers.get('Content-Type')}
        data=r.raw.read(end-start+2);assert len(data)==end-start+1
        return data,{'http':r.status_code,'content_range':r.headers.get('Content-Range'),'media':r.headers.get('Content-Type')}
class Tail(io.RawIOBase):
    def __init__(self,data,start): self.data=data;self.start=start;self.pos=start
    def seek(self,off,whence=0):
        self.pos=(self.pos if whence==1 else size if whence==2 else 0)+off
        return self.pos
    def tell(self):return self.pos
    def seekable(self):return True
    def read(self,n=-1):
        assert self.pos>=self.start
        data=self.data[self.pos-self.start:] if n<0 else self.data[self.pos-self.start:self.pos-self.start+n]
        self.pos+=len(data);return data
def main():
    out={'source':url,'size':size,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    for u in [url,'https://zenodo.org/records/15559526/files/dataset.zip?download=1']:
        try:
            n=131072;data,resp=fetch(u,size-n,size-1);out.setdefault('attempts',[]).append([u,resp])
            if data is None:continue
            with zipfile.ZipFile(Tail(data,size-n)) as z:
                out['members']=[dict(member=i.filename,compressed_size=i.compress_size,file_size=i.file_size,offset=i.header_offset) for i in z.infolist()]
            out['retrieved_bytes']=len(data);break
        except Exception as e:out.setdefault('errors',[]).append(type(e).__name__+': '+str(e)[:200])
    (BASE/'mongo-directory.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
if __name__=='__main__':main()
