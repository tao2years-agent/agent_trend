from pathlib import Path
import requests,sys,json
p=Path(__file__).resolve().parent
def get(u,**kwargs):
 for n in range(4):
  try:
   s=requests.Session();s.trust_env=False if n%2==0 else True
   resp=s.get(u,timeout=25,**kwargs);resp.raise_for_status();return resp
  except Exception:
   if n==3:raise
if __name__=="__main__":
 d=get('https://huggingface.co/api/datasets/hao-li/AIDev/revision/b8dc67df93e7c11f6f20c84129db7232eb1ec253').json()
 sha=d['sha'];print(sha)
 tree=get(f'https://huggingface.co/api/datasets/hao-li/AIDev/tree/{sha}?limit=100').json()
 print([(row['path'],int(row['size']/1e6))for row in tree])
 (p/'raw'/'tree.json').write_text(json.dumps({'revision':sha,'files':tree},ensure_ascii=False,indent=2),'utf8')
 b=get(f'https://huggingface.co/datasets/hao-li/AIDev/raw/{sha}/README.md').content
 (p/'raw'/'README.upstream.md').write_bytes(b)
