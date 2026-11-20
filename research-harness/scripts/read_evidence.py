"""Inspect sections by page, or the primary text of a field source. No external network."""
import argparse,re
from pathlib import Path
from bs4 import BeautifulSoup
import pymupdf
R=Path(__file__).resolve().parents[1]
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("ids",nargs="+");ap.add_argument("--term",default="threat|limitation|sample|baseline|finding");ap.add_argument("--chars",type=int,default=2000)
    args=ap.parse_args()
    for key in args.ids:
        files=list((R/"raw"/"2026-11-20").glob(key+"-body.pdf")) or list((R/"raw"/"2026-11-20").glob(key+".html")) or list((R/"raw"/"2026-11-20").glob(key+".pdf"))
        if not files:continue
        p=files[0]
        if p.suffix==".pdf":
            with pymupdf.open(p) as d: paragraphs=[(n+1," ".join(pg.get_text().split())) for n,pg in enumerate(d)]
        else:
            soup=BeautifulSoup(p.read_bytes(),"lxml"); main=soup.select_one("article") or soup.select_one("main") or soup
            paragraphs=[(n," ".join(t.stripped_strings)) for n,t in enumerate(main.select("h1,h2,h3,p,li"))]
        print(key)
        count=0
        for n,body in paragraphs:
            m=re.search(args.term,body,re.I)
            if m:
                quote=body[max(0,m.start()-90):m.end()+385]
                print(n,quote);count+=len(quote)
                if count>=args.chars:break
