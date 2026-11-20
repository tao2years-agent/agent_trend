import concurrent.futures as cf,csv,datetime,hashlib,json,subprocess
from pathlib import Path
import pymupdf
R=Path(__file__).resolve().parent
def run(row):
    p=R/(row["id"]+".pdf")
    if not p.exists():
        res=subprocess.run(["curl.exe","--noproxy","*","-fsSL","--retry","2","--connect-timeout","8","--max-time","75",row["url"]],capture_output=True)
        if res.returncode or not res.stdout.startswith(b"%PDF"):return dict(row,failed=True)
        p.write_bytes(res.stdout)
    with pymupdf.open(p) as d:
        text=[a.get_text() for a in d];pages=len(d)
    f=R/(row["id"]+"-text.json");f.write_text(json.dumps(text,ensure_ascii=False),encoding="utf8")
    decision = "排除：原文为天文学论文，发现条目和 arXiv ID 错配" if row["id"] == "H07" else "纳入：正文方法及结果复核"
    return dict(row,decision=decision,path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=pages,header=" ".join(text[0].split())[:240])
with cf.ThreadPoolExecutor(max_workers=7) as pool:rows=list(pool.map(run,list(csv.DictReader((R/"seeds.tsv").read_text("utf8").splitlines(),delimiter="\t"))))
(R/"sources.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf8");print([(x["id"],x.get("pages")) for x in rows])
