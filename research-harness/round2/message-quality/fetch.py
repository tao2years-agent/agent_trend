from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime,timezone
import requests,hashlib,json,tempfile
R=Path(__file__).resolve().parent
urls={
'gfm.pdf':'https://dl.acm.org/doi/pdf/10.1145/3832783.3837473','gfm.html':'https://dl.acm.org/doi/full/10.1145/3832783.3837473','author.html':'https://minghua-ma.github.io/','gfm-crossref.json':'https://api.crossref.org/works/10.1145/3832783.3837473','gfm-openalex.json':'https://api.openalex.org/works/https://doi.org/10.1145/3832783.3837473',
'explain.pdf':'https://arxiv.org/pdf/2607.26451','explain.html':'https://arxiv.org/html/2607.26451v1','zenodo.json':'https://zenodo.org/api/records/19230708','artifact-readme.md':'https://zenodo.org/records/19230708/files/README.md?download=1','artifact.zip':'https://zenodo.org/records/19230708/files/artifact.zip?download=1'}
urls.update({
'author-publications.yml':'https://minghua-ma.github.io/data/publications.yml',
'gfm-msr.html':'https://www.microsoft.com/en-us/research/publication/when-does-ai-actually-help-in-incident-response-identifying-good-first-messages-in-cloud-service-incidents/',
'gfm-semanticscholar.json':'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3832783.3837473?fields=title,openAccessPdf,externalIds,url',
'gfm-dblp.xml':'https://dblp.org/rec/conf/kbse/MaWBRDZ26.xml',
'gfm-unpaywall.json':'https://api.unpaywall.org/v2/10.1145/3832783.3837473?email=research@localhost.example',
'gfm-doi.html':'https://doi.org/10.1145/3832783.3837473',
})
def run(item):
 k,u=item; f=(Path(tempfile.gettempdir())/'ase26-explainbench-19230708.zip' if k=='artifact.zip' else R/'raw'/k)
 if k in old and 'sha256' in old[k] and f.exists():
  assert hashlib.sha256(f.read_bytes()).hexdigest()==old[k]['sha256'];return old[k]
 s=requests.Session();s.trust_env=False
 r=dict(key=k,url=u,retrieved=datetime.now(timezone.utc).isoformat())
 try:
  q=s.get(u,timeout=(8,50),headers={'User-Agent':'Mozilla/5.0'});q.raise_for_status();b=q.content
  if k.endswith('.pdf'):assert b[:4]==b'%PDF',b[:55]
  if k.endswith('.zip'):assert b[:2]==b'PK',b[:55]
  f.write_bytes(b);r.update(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),path='TEMP/ase26-explainbench-19230708.zip' if k=='artifact.zip' else 'raw/'+k)
 except Exception as e:r['error']=str(e)
 return r
if __name__=='__main__':
 p=R/'sources.json';old={s['key']:s for s in json.loads(p.read_text('utf8'))} if p.exists() else {}
 with ThreadPoolExecutor(9) as e:l=list(e.map(run,urls.items()))
 p.write_text(json.dumps(l,ensure_ascii=False,indent=2),'utf8')
 for s in l:print(s['key'],s.get('bytes',s.get('error')))

