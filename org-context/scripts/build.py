"""Compile research notes, screened sources, and tables to Markdown and offline HTML."""
from pathlib import Path
import csv
import hashlib
import html
import json
import re
import markdown
from bs4 import BeautifulSoup

R=Path(__file__).resolve().parents[1]
def tsv(name):
    with (R/"corpus"/(name+".tsv")).open(encoding="utf8") as f:
        return list(csv.DictReader(f,delimiter="\t"))
def read(path): return (R/path).read_text(encoding="utf8")
def write(path, value):
    out=R/path
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(value,encoding="utf8")
def jread(path): return json.loads(read(path))
def jwrite(path,obj): write(path,json.dumps(obj,ensure_ascii=False,indent=2))
def table(header, rows):
    def fmt(row):return "| "+" | ".join(str(c).replace("|","\\|").replace("\n"," ") for c in row)+" |"
    return "\n".join([fmt(header),fmt(["---"]*len(header))]+[fmt(row) for row in rows])
def link(label,url):return "["+label+"]("+url+")"
def rawlink(path):return link("本地证据","../"+path)
papers={r["id"]:r for r in jread("corpus/papers.json")}
for r in tsv("verified"):
    paper=papers.setdefault(r["id"],{"id":r["id"],"用途与筛选理由":"推荐评审者时考虑延迟、负载及旁观者"})
    paper.update(title=r["title"],url=r["url"],first_public=r["date"],date_kind="会议/出版年份；首次公开未核",status="纳入",snapshot="raw/web/"+r["snapshot"]+".txt")
    paper.pop("error",None)
papers["A67"]["date_kind"]="arXiv v1"
included=[p for p in papers.values() if p["status"]=="纳入"]
reads={r["id"]:r for r in tsv("readings")}
src={r["id"]:r for r in jread("corpus/sources.json")}
for id,local in {"F09":"field-measure","F10":"field-measure","D01":"prod"}.items():
    if "snapshot" not in src[id]:src[id]["snapshot"]="raw/web/"+local+".txt"
base="raw/sources/2026-11-18/"
refs={}
for p in included:
    refs[p["id"]]=p["url"]
for id,r in src.items(): refs[id]=r["url"]
for p in list((R/base).glob("[CVJ]*.*.json"))+list((R/base).glob("F67.html.json")):
    id=p.name.split(".")[0]
    info=json.loads(p.read_text(encoding="utf8"))
    addr=info["url"]
    if id.startswith("C"):
        addr=addr.replace("raw.githubusercontent.com/openai/codex/","github.com/openai/codex/blob/")
    if id.startswith("J"):
        addr=addr.replace("raw.githubusercontent.com/google-gemini/gemini-cli/","github.com/google-gemini/gemini-cli/blob/")
    src[id]={"id":id,"url":addr,"name":"修订正文" if id.startswith("V") else "Codex实现/测试","snapshot":base+p.name[:-5],"status":"已抓取"}
    refs[id]=addr
names={"G01":"gemini-cli","G02":"qwen-code","G03":"aider","G04":"backstage","G05":"nx","G06":"pact_broker"}
gitrows=[]
for id,name in names.items():
    p=next((R/"raw/git"/name).rglob("manifest.json"))
    m=json.loads(p.read_text(encoding="utf8"))
    assert m["files"]
    refs[id]=m["files"][0]["url"]
    for v in m["files"]:
        local=p.parent/Path(v["file"]).name
        assert hashlib.sha256(local.read_bytes()).hexdigest()==v["sha256"]
        gitrows.append([id,m["repo"],m["date"],link(v["file"],v["url"]),rawlink(local.relative_to(R).as_posix())])
for id in ["C01","C02","C03"]:
    gitrows.append([id,"openai/codex",jread("raw/git/codex/2026-11-18/manifest.json")["date"],link(refs[id].split("/")[-1],refs[id]),rawlink(src[id]["snapshot"])])
for id in ["J01","J02","J03","J05"]:
    gitrows.append([id,"google-gemini/gemini-cli",jread("raw/git/gemini-cli/2026-11-18/manifest.json")["date"],link(refs[id].split("/")[-1],refs[id]),rawlink(src[id]["snapshot"])])
def cite(id):
    return link(id,refs[id])
def resolve(s):return re.sub(r"\{\{([A-Z]\d\d)\}\}",lambda m:cite(m[1]),s)
def multi(ids):return " ".join(cite(i) for i in ids.split())
def bodyref(p):
    n=p["id"]
    if n not in reads:return ""
    f="F"+("16" if n=="A61" else n[1:])
    return link("正文",src[f]["url"])+" "+rawlink(src[f]["snapshot"])
docs={}
for key in ("decision","mechanisms","evidence","pilots","method"):
    docs[key]=resolve(read("research/"+key+".md"))
    write("wiki/"+key+".md",docs[key])
def pubdate(r):
    if r.get("date_kind")=="arXiv v1":return r["first_public"]+" · arXiv v1"
    return r.get("first_public","未核")+" · 出版，首公开未核"
for r in included:
    r["depth"]="正文复核" if r["id"] in reads else "书目/摘要索引"
for p in papers.values():
    if p["status"]!="纳入":p["depth"]="待核，未计覆盖"
jwrite("corpus/screened-papers.json",list(papers.values()))

reading="## 学术证据详表\n\n"+table(["论文与正文定位","方法、样本与基线","作者结果","局限与迁移边界"],[[cite(i)+" "+included_title+" · "+r["正文定位"]+" "+bodyref(papers[i]),r["方法、样本与比较"],r["作者结果"],r["局限与可迁移判断"]] for i,r in reads.items() for included_title in [papers[i]["title"]]])
reading+="\n\n**版本复核。** 上表 A01、A03、A04、A07、A08、A61 的定量引文取所链接的正文版本。A01 v3 使用 CTXbench 名称，A04 v3 扩大实验，详见主体。补查了 A07 v2、A08 v2、A61 v2 的主要结论。A03 较新版正文未取得，保留 v1 数字。"+multi("V01 V04 V07 V08 V61")
prodrows=tsv("products")
products="## 产业机制对照表\n\n"+table(["产品 / 项目","使用现场和行为","选择与边界","对内部产品的判断、来源"],[[r["产品或项目"],r["现场与公开行为"],r["选择、权限与边界"],r["可迁移之处与替代"]+" "+multi(r["证据"])] for r in prodrows])
opps=tsv("opportunities")
oppsections=["## 产品机会清单","以下为设计建议；举例均为拟议交互。每项的证据等级针对其问题或机制，并非对产品收益的评级。"]
for r in opps:
    evidence=r["证据强度与来源"]
    evidence=re.sub(r"\b[ADG]\d\d\b",lambda m:cite(m[0]),evidence)
    pairs=[["触发者与时机",r["用户、触发"]],["现状与缺口",r["当前做法与缺口"]],["交互与机制",r["机制与交互例子（均为设计示例）"]],["复用资产／关键依赖",r["可复用资产"]+" ／ "+r["最难依赖"]],["失败代价",r["失败代价"]],["最低成本验证",r["最便宜的验证"]],["证据强度",evidence]]
    oppsections+=["### "+r["id"]+"　"+r["可感知的行为"],table(["维度","判断"],pairs)]
opportunities="\n\n".join(oppsections)
paper_index="## 论文索引与筛查决策\n\n"+table(["ID、论文及一手入口","时间口径","深度与研究用途","证据快照"],[[cite(p["id"])+" "+p["title"],pubdate(p),p["depth"]+"。"+p["用途与筛选理由"],rawlink(p["snapshot"])] for p in included])
paper_index+="\n\n**未纳入计数。** "+"；".join(p["id"]+" "+p["key"]+"（书目未可靠核对）" for p in papers.values() if p["status"]!="纳入")+"。"
date_map={"D03":"2026-06-23 beta","D04":"2026-10-28 GA/预览","D13":"2026-11-03 版本2.39","D15":"2018-11-21 部署文章","D16":"2026-08-13 增强","D17":"2026-01-15 公开预览","D18":"2026-05-26 控制增强","D20":"2025-12-19 早期开放"}
sledger=[]
date_map.update(D21="2026-04-02 工作项入口",D22="2026-06-22 3.9增强")
for id,r in sorted(src.items()):
    if not id.startswith("D"):continue
    updated="未核"
    p=R/r["snapshot"]
    if p.suffix==".html":
        s=BeautifulSoup(p.read_bytes(),"html.parser")
        for attr in ["article:modified_time","og:updated_time"]:
            tag=s.find("meta",property=attr)
            if tag and tag.get("content"): updated=tag["content"][:10];break
    sledger.append([cite(id)+" "+r["name"],date_map.get(id,"仅当前文档，首发未核"),updated,rawlink(r["snapshot"])])
queries=[]
for p in sorted((R/"raw/web").glob("*.txt")):
    args=json.loads(p.read_text(encoding="utf8").splitlines()[0].split(" ",1)[1])
    if "search_query" in args:
        queries.append([p.stem," / ".join(q["q"] for q in args["search_query"]),rawlink(p.relative_to(R).as_posix())])
ledger="## 来源、固定提交与检索明细\n\n### 开源实现与测试定位\n\n"+table(["证据","仓库","提交时间（UTC）","固定提交文件","本地"],gitrows)+"\n\n### 产品来源的时间口径\n\n"+table(["官方来源","发布/增强日期","页面更新元数据","快照"],sledger)+"\n\n### 检索式与未筛选返回\n\n下列均在2026-11-18执行。多库检索通过网页索引、出版方及作者站点完成；网站返回的相对时间不作为发布日期。书目逐题检索另见 papers.tsv 和 Crossref 原始响应。\n\n"+table(["批次","关键词与时间限制","检索摘录"],queries)
for key,s in [("papers",reading+"\n\n"+paper_index),("products",products),("opportunities",opportunities),("ledger",ledger)]:write("wiki/"+key+".md",s)
checkpoint=f"论文候选 {len(papers)}，核准 {len(included)}，其中正文复核 {len(reads)}，其余索引 {len(included)-len(reads)}。产业表 {len(prodrows)} 行，GitHub CODEOWNERS 与 Copilot 合并按同一平台计为 {len(prodrows)-1} 个产品或项目。固定提交源码复核 {len(names)+1} 个项目。机会 {len(opps)} 个，实验 4 个。Gemini CLI 的 JIT 适配函数已在受控条件下执行；竞品端到端运行 0，内部用户实验 0。"
report="\n\n".join([docs["decision"],docs["mechanisms"],docs["evidence"],docs["pilots"],docs["method"],"**本轮覆盖。** "+checkpoint,products,reading,opportunities,paper_index,ledger])
write("outputs/report.md",report)
write("wiki/index.md","# 组织级上下文与团队记忆\n\n"+checkpoint+"\n\n"+"\n".join("- "+link(label,n+".md") for n,label in [("decision","决策摘要与工作现场"),("mechanisms","机制与真实增量"),("evidence","学术判断"),("pilots","优先级与实验"),("method","方法与未决问题"),("products","产业对照"),("papers","学术详表"),("opportunities","机会清单"),("ledger","检索台账")]))
write("state/checkpoint.md","# 2026-11-18 研究覆盖\n\n"+checkpoint+"\n\n"+link("报告","../outputs/report.md")+" · "+link("后续问题","../wiki/method.md")+" · "+link("检索台账","../wiki/ledger.md")+"\n\n网页摘录有别于原页字节；F09/F10 与 D01 通过网页摘录补证。修订版本有单独来源，产品效果未复现。")
jwrite("state/coverage.json",dict(candidates=len(papers),papers=len(included),fulltext_review=len(reads),recent_three_years=sum(str(p["first_public"])>="2023-11-18" for p in included),industry_rows=len(prodrows),products=len(prodrows)-1,source_review=7,opportunities=len(opps),experiments=4,web_queries=len(queries)))
for p in included:assert (R/p["snapshot"]).is_file(),p
for r in src.values():
    if "snapshot" in r:assert (R/r["snapshot"]).is_file(),r
assert len(included)>=50 and len(reads)>=12 and len(opps)>=12 and "{{" not in report
print(checkpoint)
