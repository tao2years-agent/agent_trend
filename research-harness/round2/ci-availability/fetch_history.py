"""Download exactly one relevant ZIP member. Resume contiguous compressed bytes and honor HTTP 429."""
from remote_index import url,BASE,size,Tail
from scan import CACHE
import json,zipfile,hashlib,time,requests
def range_get(start,end,suffix):
    for attempt in range(5):
        with requests.get('https://zenodo.org/records/15559526/files/dataset.zip?download=1&ci_availability='+suffix,headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},timeout=(12,60),stream=True) as r:
            if r.status_code==429:
                delay=int(r.headers.get('Retry-After','60')) if r.headers.get('Retry-After','60').isdigit() else 60
                print('rate limited; waiting',delay,'seconds',flush=True);time.sleep(max(60,delay));continue
            assert r.status_code==206 and r.headers.get('Content-Range')==f'bytes {start}-{end}/{size}',(r.status_code,r.headers.get('Content-Range'))
            data=r.raw.read(end-start+2);assert len(data)==end-start+1
            return data
    raise RuntimeError('range unavailable')
def main():
    data=range_get(size-131072,size-1,'central-directory')
    with zipfile.ZipFile(Tail(data,size-131072)) as z:
        info=z.getinfo('dataset/recheck_builds_helper_years_20/jobs_occurrences.bson')
    meta=next(x for x in json.loads((BASE/'bson-samples.json').read_text()) if x['member']==info.filename)
    start=info.header_offset+meta['header_bytes'];n=info.compress_size
    dest=CACHE/'jobs-occurrences.deflate';done=dest.stat().st_size if dest.exists() else 0
    assert 0<=done<=n
    while done<n:
        end=min(n,done+64*1024*1024)-1
        buf=range_get(start+done,start+end,str(done))
        with dest.open('ab') as f:f.write(buf)
        done=end+1
    with open(dest,'rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    (BASE/'history-member.json').write_text(json.dumps(dict(official=url,member=info.filename,archive_size=size,compressed_size=n,uncompressed=info.file_size,zip_crc32=info.CRC,compressed_sha256=sha,absolute_compressed_offset=start),indent=2),'utf8')
if __name__=='__main__':main()
