"""Compile the reviewed product, paper, and field records into the Wiki and the two reports."""
import csv, hashlib, html, json, re
from pathlib import Path
import markdown
R=Path(__file__).resolve().parents[1]
def rd(p):return (R/p).read_text(encoding="utf-8-sig")
def put(p,s):p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding="utf8")
def js(p):return json.loads(rd(p))
def dump(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def tsv(p):return list(csv.DictReader(rd(p).splitlines(),delimiter="\t"))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def md(s):return markdown.markdown(s,extensions=["tables","sane_lists"])
def esc(s):return html.escape(str(s),quote=True)
def weburl(path):
    return re.search(r"\((https?://[^\n]+?)\)\s*$",rd(path).splitlines()[0]).group(1)
lanes={"execution":"执行框架","delivery":"工程交付","organization":"组织平台","frontier":"自动化前沿","managed":"商业工作流","market":"效能度量"}
cases=[]
for lane,label in lanes.items():
    for c in js("lanes/"+lane+"/cases.json"):
        c.update(lane=label,source_review=c["id"][0] in "EDO" or c["id"] in ("F01","F02","F05"))
        cases.append(c)
reads={x["id"]:x for x in js("corpus/reading-capture.json")}
fields={x["id"]:x for x in js("corpus/field-capture.json")}
sources=[]
def attach(k,url,path,detail,date="",expected=""):
    digest=sha(path)
    if expected:assert digest==expected,(k,path)
    assert url.startswith("https://") or url.startswith("http://"),url
    item=dict(entity=k,url=url,path=path,detail=detail,date=date,sha256=digest)
    sources.append(item);return item
for c in cases:
    c["sources"]=[attach(c["id"],x["url"],x["path"],x["detail"],x.get("date",""),x.get("sha256","")) for x in c["sources"]]
papers=[]
for note in tsv("corpus/paper-notes.tsv"):
    k=note["id"];c=reads[k];src=[]
    if c.get("record"):
        p=c["record"];m=js(p+".meta.json");src.append(attach(k,m["url"],p,"书目或作者摘要；按完整题名匹配",c.get("date",""),m["sha256"]))
    if c.get("pdf"):
        p=c["pdf"];src.append(attach(k,c["pdf_url"],p,note["locator"],c.get("date",""),js(p+".meta.json")["sha256"]))
    p="raw/web/"+k+"-view.txt"
    if (R/p).exists():src.append(attach(k,weburl(p),p,"会议或出版页的浏览器文本摘录"))
    assert src
    authors=c.get("authors") or (["Ningzhi Tang","Chaoran Chen","Zihan Fang","Gelei Xu","Maria Dhakal","Yiyu Shi","Collin McMillan","Yu Huang","Toby Jia-Jun Li"] if k=="P09" else ["John Yang","Carlos E. Jimenez","Alexander Wettig","Kilian Lieret","Shunyu Yao","Karthik Narasimhan","Ofir Press"])
    papers.append(dict(**note,name=c.get("title") or c["key"],venue=c["kind"],authors=authors,url=c.get("doi") or src[-1]["url"],level="正文定点复核" if c.get("pdf") else "摘要及书目",sources=src))
field=[]
for n in tsv("corpus/field-notes.tsv"):
    k=n["id"];p=fields.get(k,{}).get("artifact");date=""
    if p:
        m=js(p+".meta.json");u=m["url"];expected=m["sha256"]
    else:
        p="raw/web/"+("discovery-human.txt" if k=="I22" else k+"-view.txt")
        u=weburl(p);expected=""
    src=attach(k,u,p,n["location"],date,expected);field.append(dict(**n,sources=[src]))
allrows=cases+papers+field
byid={x["id"]:x for x in allrows}
assert len(byid)==len(allrows)
dump("corpus/products.json",cases);dump("corpus/papers.json",papers);dump("corpus/field.json",field);dump("corpus/sources.json",sources)
cov={"products":len(cases),"fixed_revision_implementation":sum(c["source_review"] for c in cases),"local_mechanisms":["D07","D09","E10","F05","O10"],"papers":len(papers),"research_track_CCF_A":sum(bool(re.match("ICSE|FSE|ASE|ISSTA",p["venue"])) and "SEIP" not in p["venue"] for p in papers),"full_text_section_review":sum(p["level"]=="正文定点复核" for p in papers),"field_sources":len(field),"evidence_pointers":len(sources),"cited_snapshot_paths":len(set(s["path"] for s in sources)),"source_urls":len(set(s["url"] for s in sources)),"product_breakdown":{v:sum(c["lane"]==v for c in cases) for v in lanes.values()}}
dump("state/coverage.json",cov)
def cite(s,target="md"):
    def sub(m):
        k=m.group(1);assert k in byid,k
        return "["+k+"]("+(("#"+k) if target=="web" else "../wiki/"+k+".md")+")"
    return re.sub(r"\[([A-Z]\d\d)\](?!\()",sub,s)
def details(x,local=False):
    k=x["id"]
    if "mechanism" in x:
        rows=[("适用场景",x["scenario"]),("实现机制",x["mechanism"]),("人工决策",x["human"]),("组织影响",x["org"]),("版本与演进",x["change"]),("适用边界",x["limits"]),("研究推断",x["insight"]),("复核实验设计",x["experiment"])]
        if x.get("platform"):rows.insert(0,("平台",x["platform"]))
    elif "finding" in x:
        rows=[("论文与轨道",x["venue"]+" · "+x["level"]),("作者","、".join(x["authors"])),("作者结果",x["finding"]),("对研发平台的启示",x["implication"]),("适用边界",x["limit"]),("复核位置",x["locator"]+" · [论文入口]("+x["url"]+")")]
    else:rows=[("复核位置",x["location"]),("一手材料",x["fact"]),("证据边界",x["boundary"])]
    s="\n\n".join("**"+a+"**　"+b for a,b in rows)+"\n\n"
    for i,t in enumerate(x["sources"],1):
        label=t["detail"].replace("[","（").replace("]","）")
        s+=f"- {label}"+(f" · {t['date']}" if t['date'] else "")+f" · [原始来源 {i}]({t['url']})"+(f" · [本地快照](../{t['path']})" if local else "")+"\n"
    return s
def title(x):return x.get("name") or x["title"]
for x in allrows:
    put("wiki/"+x["id"]+".md","# "+x["id"]+" · "+title(x)+"\n\n"+details(x,True)+"\n[返回索引](index.md)\n")
idx="# 组织级研发自动化研究 Wiki\n\n[深度报告](../outputs/deep-report.md) · [离线洞察报告](../outputs/insights.html) · [研究协议](../research/protocol.md) · [检查点](../state/checkpoint.md)\n"
for name,group in [(lane,[x for x in cases if x["lane"]==lane]) for lane in lanes.values()]+[("学术阅读",papers),("产业现场与补充证据",field)]:
    idx+="\n## "+name+"\n\n"+"\n".join("- ["+x["id"]+" "+title(x)+"]("+x["id"]+".md)" for x in group)+"\n"
put("wiki/index.md",idx)
with (R/"outputs/product-matrix.csv").open("w",encoding="utf-8-sig",newline="") as f:
    keys=["id","lane","name","category","scenario","mechanism","human","org","change","limits","insight","experiment","source_review"]
    w=csv.writer(f);w.writerow(["编号","研究层","名称","类型","场景","机制","人的介入","组织影响","演进","限制","判断","验证设计","固定修订实现复核","来源","Wiki"])
    for c in cases:w.writerow([c[k] for k in keys]+["\n".join(x["url"] for x in c["sources"]),"../wiki/"+c["id"]+".md"])
analysis=rd("research/analysis.md")
analysis=analysis.replace("## 从市场能力到产品设计",rd("research/marketfront.md")+"\n\n## 从市场能力到产品设计")
analysis=analysis.replace("## 试哪里，怎么知道该停",rd("research/measurement.md")+"\n\n"+rd("research/frontiers.md")+"\n\n"+rd("research/labs.md")+"\n\n## 试哪里，怎么知道该停")
analysis+="\n\n"+rd("research/method-notes.md")
summary=f"截至 2026-11-20，研究覆盖 {len(cases)} 个产品、项目及组件，{cov['fixed_revision_implementation']} 项有固定修订实现证据，5 项完成局部实验；20 项学术工作中 8 项复核了正文具体章节。"
analysis=analysis.replace("## 组织到底购买什么",summary+"\n\n## 组织到底购买什么")
annex="\n\n## 逐项证据与复核边界\n"
for name,group in [("产品与项目",cases),("论文",papers),("工程现场与对照",field)]:
    annex+="\n## "+name+"\n"
    for x in group:annex+="\n### "+x["id"]+" "+title(x)+"\n\n"+details(x,True)+"\n"
put("outputs/deep-report.md",cite(analysis)+annex)
brief=rd("research/share.md")
def cards():
    out=[]
    for x in allrows:
        k=x["id"];sub=x.get("lane") or ("学术研究" if "finding" in x else "工程现场")
        out.append(f'<details class="record" data-section="{esc(sub)}" id="{k}"><summary><small>{k} · {esc(sub)}</small><strong>{esc(title(x))}</strong></summary><div>{md(details(x))}</div></details>')
    return "\n".join(out)
def render(body,deep):
    h=md(cite(body,"web"))
    if deep:h=re.sub(r"<h1>.*?</h1>","",h,count=1)
    nav=[]
    def heading(m):
        anchor="s"+str(len(nav)+1);nav.append((anchor,m[1]));return f'<h2 id="{anchor}">{m[1]}</h2>'
    h=re.sub(r"<h2>(.*?)</h2>",heading,h)
    h=h.replace("<table>",'<div class="tablewrap"><table>').replace("</table>","</table></div>")
    data={"NCASES":str(len(cases)),"NPAPERS":str(len(papers)),"TITLE":"研发自动化的组织边界" if not deep else "从 Code Agent 到组织级研发自动化","KIND":"决策洞察" if not deep else "深度分析","INTRO":"当机器可以持续接单，团队最需要解决的是验证、接管，以及何时停止。" if not deep else "产业实现、软件工程研究与可复验的试点方案。","NAV":"".join(f'<a href="#{a}">{b}</a>' for a,b in nav)+ '<a href="#evidence">证据索引</a>',"BODY":h,"RECORDS":cards(),"FILTERS":"".join(f'<option>{t}</option>' for t in [*lanes.values(),"学术研究","工程现场"])}
    tpl=rd("research/reader.html")
    for k,v in data.items():tpl=tpl.replace("{{"+k+"}}",v)
    return tpl
put("outputs/insights.html",render(brief,False));put("outputs/deep-report.html",render(analysis,True))
print(cov)
if (R/"round2/navigation.py").exists() and (R/"outputs/deep-report-v2.html").exists():
    import runpy
    runpy.run_path(str(R/"round2/navigation.py"))
