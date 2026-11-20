"""Lay out the brief from its reviewed Markdown and source registry; embed CJK fonts."""
from pathlib import Path
import json,re,html
import markdown
from bs4 import BeautifulSoup
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1]
data=[x for n in ("products","papers","field") for x in json.loads((R/f"corpus/{n}.json").read_text("utf8"))]
reg={x["id"]:x for x in data}
for fam,file in [("Deng","Deng.ttf"),("DengB","Dengb.ttf")]:pdfmetrics.registerFont(TTFont(fam,"C:/Windows/Fonts/"+file))
pdfmetrics.registerFontFamily("Deng",normal="Deng",bold="DengB")
W,H=180*mm,245*mm
c=Canvas(str(R/"outputs/insights.pdf"),pagesize=(W,H));c.setTitle("从 Code Agent 到组织级研发自动化 · 决策洞察");c.setAuthor("研发自动化专题研究")
ink="#163739";accent="#156C61";muted="#46615D";line="#B8C9C1"
def style(size,lead,bold=False,color=ink):
    return ParagraphStyle("body",fontName="DengB" if bold else "Deng",fontSize=size,leading=lead,textColor=HexColor(color),wordWrap="CJK",spaceAfter=0,splitLongWords=True)
soup=BeautifulSoup(markdown.markdown((R/"research/share.md").read_text("utf8"),extensions=["tables"]),"html.parser")
sections=[]
for child in soup.find_all(recursive=False):
    if child.name=="h2":sections.append([])
    sections[-1].append(child)
def rich(t):
    st=t.decode_contents().replace("<strong>","<b>").replace("</strong>","</b>")
    def link(m):
        row=reg[m[1]];url=row.get("url") or row["sources"][0]["url"]
        return '<a color="'+accent+'" href="'+html.escape(url,quote=True)+'"><font size="8">['+m[1]+']</font></a>'
    return re.sub(r"\[([A-Z]\d\d)\]",link,st)
def para(s,sty,x,width,y,after=9):
    ob=Paragraph(s,sty);_,h=ob.wrap(width,1000);ob.drawOn(c,x,y-h);return y-h-after
left=32;aw=W-2*left
groups=[[0,1],[2,3],[4,5],[6]]
for n,grp in enumerate(groups,1):
    c.setFillColor(HexColor("#F8F8F2"));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HexColor(ink));c.rect(0,H-71,W,71,fill=1,stroke=0)
    c.setFillColor(HexColor("#BAE5A2"));c.setFont("DengB",9);c.drawString(left,H-22,"研发效能研究   /   决策洞察                                 2026.11.20")
    c.setFillColor(HexColor("#FFFFFF"));c.setFont("DengB",19);c.drawString(left,H-52,"从 Code Agent 到组织级研发自动化")
    y=H-88
    for i in grp:
        for e in sections[i]:
            if e.name=="h2":y=para(e.get_text(),style(16.5,24,True),left,aw,y,7)
            elif e.name=="p":y=para(rich(e),style(12.0,19),left,aw,y,9)
            elif e.name=="ul":
                for li in e.select("li"):y=para("•　"+rich(li),style(12.0,19),left+3,aw-3,y,6)
            elif e.name=="table":
                rows=[]
                for row in e.select("tr"):
                    rows.append([Paragraph(rich(cell),style(10.5,16.5,cell.name=="th")) for cell in row.select("td,th")])
                widths=([.21,.37,.42] if len(rows[0])==3 else [.45,.55])
                tab=Table(rows,colWidths=[aw*v for v in widths],hAlign="LEFT")
                tab.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,0),HexColor("#DEE9DF")),("LINEBELOW",(0,0),(-1,-1),.35,HexColor(line)),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
                _,h=tab.wrap(aw,1000);y-=h;tab.drawOn(c,left,y);y-=14
    if n==4:
        y=para("研究范围与证据",style(16.5,24,True),left,aw,y-7)
        y=para("50 个产品、开源项目及组件，36 项核对固定修订的实现源码，5 项有本地局部运行。20 项学术工作覆盖 ICSE、FSE、ASE、ISSTA 等，8 项复核 PDF 正文的具体章节。工程访谈、供应商报告与论文结论各按其适用范围解释。本研究未在企业租户或生产环境验证组织收益。",style(12.0,19),left,aw,y)
        y=para("正文中的编号链接到原始来源。完整竞品、学术与工程现场的 92 条解读见同名离线网页的证据索引。",style(10.5,16.5,color=muted),left,aw,y)
    assert y>34,(n,y)
    c.setStrokeColor(HexColor(line));c.line(left,32,W-left,32);c.setFont("Deng",8.5);c.setFillColor(HexColor(muted));c.drawString(left,18,"上海   /   2026 年 11 月   ·   研究与决策建议");c.drawRightString(W-left,18,f"{n} / 4");c.showPage()
c.save()
