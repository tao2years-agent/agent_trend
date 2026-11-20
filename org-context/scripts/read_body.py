"""Read sections from locally captured full text. Usage: read_body.py F01 ..."""
from pathlib import Path
import re,sys
from bs4 import BeautifulSoup
import fitz
ROOT=Path(__file__).resolve().parents[1]/"raw"/"sources"/"2026-11-18"
for arg in sys.argv[1:]:
    bits=arg.split(":")
    paths=[p for p in ROOT.glob(bits[0]+".*") if p.suffix in [".html",".pdf"]]
    if not paths:continue
    p=paths[0]
    if p.suffix==".pdf":
        doc=fitz.open(p)
        for pg in ([int(b) for b in bits[1:]] or [0,len(doc)-2]):
            print(p.stem,pg+1," ".join(doc[pg].get_text().split())[:4200])
    else:
        soup=BeautifulSoup(p.read_bytes(),"html.parser")
        for sel in ["nav","footer","script","style","header",".ltx_bibliography"]:
            for el in soup.select(sel): el.decompose()
        base=soup.select_one("article") or soup.select_one("main") or soup
        parts=base.select("p.ltx_p, .ltx_abstract p, figcaption") or base.select("p,li")
        txt=[" ".join(el.stripped_strings) for el in parts]
        if len(bits)>1: ix=[i for i,s in enumerate(txt) if re.search(bits[1],s,re.I)][:9]
        else: ix=[0,1,len(txt)//2,len(txt)-3,len(txt)-2]
        print(p.stem,"paragraphs",len(txt))
        for i in ix:
            if 0<=i<len(txt):print(i,txt[i][:1200])
