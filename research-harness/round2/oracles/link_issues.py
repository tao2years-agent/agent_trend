from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib,json,re
from bs4 import BeautifulSoup
from ingest import P,get
def one(m):
    u=m["pull_request_url"]
    b=get(u)
    soup=BeautifulSoup(b,"html.parser");a=soup.select_one(".comment-body")
    text=a.get_text("\n",strip=True) if a else ""
    if not text:return u,"NO_BODY",None
    lines=text.splitlines(); refs=[]
    for i,s in enumerate(lines):
        if re.search(r"\b(close[ds]?|fix(?:es|ed)?|resolve[ds]?)\b",s,re.I):
            clip=" ".join(lines[i:i+2])
            mm=re.search(r"(?:#|/issues/)(\d+)",clip)
            if mm:refs.append(int(mm[1]))
    out={"pr_url":u,"source_page_sha256":hashlib.sha256(b).hexdigest(),"pr_body_text":text,"issue_references_in_closing_phrases":list(dict.fromkeys(refs))}
    d=P/"raw"/m["instance_id"]
    (d/"pr-body.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
    return m["instance_id"],refs,text[:150]
if __name__=="__main__":
    with ThreadPoolExecutor(4) as e:
        for item in e.map(one,json.loads((P/"cohort.json").read_bytes())["selected"]):print(item)
