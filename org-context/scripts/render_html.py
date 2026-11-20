"""Render a portable reading view with offline navigation and expandable appendices."""
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parents[1]
out=root/"outputs"
source=(out/"report.md").read_text(encoding="utf8")
soup=BeautifulSoup(markdown.markdown(source,extensions=["tables","sane_lists"]),"html.parser")
title=soup.h1.get_text()
soup.h1.extract()
parts=[]
current=None
for el in list(soup.children):
    if getattr(el,"name",None)=="h2":
        current=soup.new_tag("section")
        current["id"]="section-"+str(len(parts)+1)
        parts.append((el.get_text(),current))
    if current is not None:current.append(el)
for name,section in parts:
    for tbl in section.select("table"):
        scroller=soup.new_tag("div",attrs={"class":"scroll","tabindex":"0","aria-label":"可横向滚动的表格"})
        tbl.wrap(scroller)
    for a in section.select("a[href^='../raw/']"):
        a["title"]="随完整研究目录分发时可打开本地证据"
app_start=next(i for i,p in enumerate(parts) if p[0]=="产业机制对照表")
links="".join(f'<a href="#{s["id"]}">{name}</a>' for name,s in parts)
body=[]
for i,(name,s) in enumerate(parts):
    if i>=app_start:
        h=s.h2.extract()
        body.append(f'<details id="{s["id"]}"><summary>{h.get_text()}</summary><div class="inner">'+"".join(str(k) for k in s.contents)+"</div></details>")
    else:body.append(str(s))
template=(root/"research"/"reader.html").read_text(encoding="utf8")
(out/"report.html").write_text(template.replace("@@TITLE@@",title).replace("@@LINKS@@",links).replace("@@CONTENT@@","\n".join(body)),encoding="utf8")
