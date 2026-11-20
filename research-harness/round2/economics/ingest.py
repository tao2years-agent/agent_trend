from pathlib import Path
import requests,concurrent.futures,json,hashlib,datetime,re,time
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
t=[i.split('|') for i in (R/'targets.psv').read_text(encoding='utf-8-sig').splitlines() if i]
def grab(row):
    id,url,detail=row
    if (R/'sources.json').is_file():
        old=next((d for d in json.loads((R/'sources.json').read_text(encoding='utf8')) if d['id']==id),None)
        if old and (R/old['path']).is_file():return old
    if id=='L3':
        prior=json.loads((R/'buy26-prior.json').read_text(encoding='utf8'))
        doc=next(d for d in prior['prior_sources'] if d['id']=='P19')
        original=R.parent.parent/doc['path']
        assert hashlib.sha256(original.read_bytes()).hexdigest()==doc['sha256']
        soup=BeautifulSoup(original.read_bytes(),'html.parser')
        for tag in soup.find_all(['script','style','nav','footer','header','svg','noscript']):tag.decompose()
        out=R/'raw'/('L3-'+doc['sha256'][:12]+'.txt')
        out.write_text('\n'.join((soup.find('article') or soup).stripped_strings),encoding='utf8')
        return dict(id=id,url=doc['url'],path='../buyers/raw/'+original.name,text='raw/'+out.name,sha256=doc['sha256'],title='FAQ: Guarded rollouts',locator=detail,snapshot_utc=doc['retrieved'],last_modified=None,reused='P19; fresh URL returned HTTP 403 on 2026-11-20')
    for i in range(4):
        try:
            s=requests.Session();s.trust_env=False
            p=s.get(url,timeout=(8,24),headers={'User-Agent':'Mozilla/5.0'});p.raise_for_status()
            raw=p.content; soup=BeautifulSoup(raw,'html.parser');title=soup.title.get_text(' ',strip=True) if soup.title else ''
            assert title and len(raw)>600,(url,len(raw));break
        except Exception as e:
            if i==3:print(id,str(e),flush=True);return None
            time.sleep(1)
    h=hashlib.sha256(raw).hexdigest();file=R/'raw'/f'{id}-{h[:12]}.html'
    if not file.exists():file.write_bytes(raw)
    for tag in soup.find_all(['script','style','nav','footer','header','svg','noscript']):tag.decompose()
    core=soup.find('main') or soup.find('article') or soup
    lines=[re.sub(r'\s+',' ',line).strip() for line in core.stripped_strings if line.strip()]
    (R/'raw'/f'{id}-{h[:12]}.txt').write_text('\n'.join(lines),encoding='utf8')
    print(id,len(raw),title[:60],flush=True)
    return dict(id=id,url=p.url,path=file.relative_to(R).as_posix(),text=file.relative_to(R).with_suffix('.txt').as_posix(),sha256=h,title=title,locator=detail,snapshot_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_modified=p.headers.get('Last-Modified'))
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex: rows=[r for r in ex.map(grab,t) if r]
(R/'sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
