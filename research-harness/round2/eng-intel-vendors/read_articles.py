from pathlib import Path
import sys
from bs4 import BeautifulSoup as B
r=Path(__file__).resolve().parent/'raw'
for key in sys.argv[1:]:
 p=next(r.glob(key+'-*'),None)
 if not p:continue
 s=B(p.read_bytes(),'html.parser')
 h=s.find('h1');print('\n==',key,h.get_text(' ',strip=True)[:75] if h else '',[(t.get('property'),t.get('content')) for t in s.select('meta[property*=published_time]')][:1])
 if h:
  for bad in s.select('nav,footer,script,style,aside'):bad.decompose()
  st=0
  for n in s.find_all(['h1','h2','h3','h4','p','li','time','tr']):
   if n==h:st=1
   if st and not n.find(['h1','h2','h3','h4','p','li','tr']):print(n.get_text(' ',strip=True))
