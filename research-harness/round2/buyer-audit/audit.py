"""Replay independently chosen locators against immutable source snapshots."""
from views import *
from collections import Counter
from functools import lru_cache
from datetime import datetime, timezone
from urllib.parse import urljoin
from hashlib import sha256
get=lru_cache(None)(get)

def tsv(filename,data):
    with (BASE/filename).open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,list(data[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(data)

def source_position(sid,loc):
    info=SRC[sid];p=ROOT/info['path']
    assert sha256(p.read_bytes()).hexdigest()==info['sha256']
    if loc.startswith(('time:','meta:')):
        doc=BeautifulSoup(p.read_bytes(),'html.parser')
        if loc.startswith('time:'): text=doc.select('time')[int(loc[5:])]['datetime']
        else:text=doc.find('meta',attrs={'property':loc[5:]})['content']
    else:
        a,b=map(int,loc.split('-')); ls=get(sid)
        assert 1<=a<=b<=len(ls),(sid,loc,len(ls))
        text='\n'.join(ls[a-1:b])
    return info,text

if __name__=='__main__':
    old={r['id']:r for r in csv.DictReader((BASE/'ledger-at-review.csv').open(encoding='utf-8-sig'))}
    new={r['id']:r for r in LEDGER}
    snapshot=[]; audit=[]; fixes=[]; seen=set()
    for row in (BASE/'notes.txt').read_text(encoding='utf8').splitlines():
        num,field,original,status,loc,reason,fix=row.split('|');bid='BUY'+num
        evidence=[]
        for part in loc.split(';'):
            sid,position=part.split('@');info,extract=source_position(sid,position)
            if part not in seen:
                seen.add(part);snapshot.append(dict(position=part,source_id=sid,url=info['url'],path=info['path'],snapshot_sha256=info['sha256'],section_sha256=sha256(extract.encode()).hexdigest()))
            evidence.append(info['url'])
            if len(sys.argv)>1 and sys.argv[1]==bid:print(part,extract)
        audit.append(dict(id=bid,product=old[bid]['product'],original_field=field,checked_claim=original,verdict_before_correction=status,actual_locator=loc,assessment=reason,revised_field=fix or '',current_field=new[bid][field],source_urls=' | '.join(dict.fromkeys(evidence))))
        if fix:
            assert fix.rstrip('。')==new[bid][field].rstrip('。'),(bid,field,new[bid][field],fix)
            fixes.append(dict(id=bid,field=field,old_value=('CircleCI Cloud + GitHub App 的适用组织；当前文档标 beta，2026-02-26 增加 inline Fix Job' if bid=='BUY35' else old[bid][field]),new_value=new[bid][field],status=status,reason=reason,locator=loc))
    assert len(audit)==70 and set(Counter(r['id'] for r in audit).values())=={2}
    tsv('claims.tsv',audit);tsv('positions.tsv',snapshot);tsv('corrections.tsv',fixes)
    # Compare both exact release files with the earlier pinned research checkout.
    tag='ccf9be8cc458bd6b8336fe84d68d8893f2691a5e'
    release=BASE/'codex-tag-0.171.0.html';raw=release.read_bytes()
    assert ('/openai/codex/commit/'+tag).encode() in raw
    tagrefs=[dict(url='https://github.com/openai/codex/releases/tag/rust-v0.171.0',sha256=sha256(raw).hexdigest(),path=release.name,locator='a[href*=commit]')]
    for k in ['E05-2','E05-3']:
        info=SRC[k];rel=info['url'].split('/blob/')[1].split('/',1)[1];p=BASE/('codex-tag-0.171.0-'+rel.split('/')[-1]);h=sha256(p.read_bytes()).hexdigest()
        assert h==info['sha256']
        tagrefs.append(dict(url=f'https://raw.githubusercontent.com/openai/codex/{tag}/{rel}',sha256=h,path=p.name,locator='raw bytes equal '+k))
    (BASE/'codex-tag-sources.json').write_text(json.dumps(tagrefs,indent=2),encoding='utf8')
    stats=Counter(r['verdict_before_correction'] for r in audit)
    rep=['# 35 个采购竞品的独立证据审稿','',f'覆盖 35/35 个 BUY 产品，每项 2 条，共 70 条主张。按修订前口径：明确 {stats["明确"]} 条，部分支持 {stats["部分支持"]} 条，未证 {stats["未证"]} 条，冲突 {stats["冲突"]} 条。所有需收窄的字段已回写采购事实源，另补证据阶段或版本区分。本次没有登录产品或重跑厂商基准。','',
         '先从 ledger 各选两条不同的具体主张，再直接读取原始 HTML、源码、Atom 或 Markdown；逐项对照对象、执行动作、验收权限或版本。HTML 的行号是 views.py 在相应快照去除导航和脚本后生成的正文行号，源码及 Markdown 使用原始行号；meta/time 定位到原始 DOM。positions.tsv 保存各片段哈希、完整快照哈希及链接。正文结果反映独立复查，不代表对其余字段全面背书。','',
         '[70 项判断与证据](claims.tsv) · [精确定位与哈希](positions.tsv) · [变更前后逐字段](corrections.tsv) · [版本源码补证](codex-tag-sources.json)','',
         '## 已写回的修订','']
    for r in fixes:rep.append(f'- **{r["id"]} · {r["field"]}**　{r["new_value"].rstrip("。")}。依据为 {r["locator"]}。')
    rep+=['','## 如何复核','', '在本目录执行 python audit.py 重新核验 70 项数量、全部片段定位和哈希、修订后的事实源及 Codex 发布标签下两份源码的一致性。执行 python audit.py BUY32 可在本地显示该产品选中的原始段落。ledger-at-review.csv 是写回前的工作副本，CircleCI 日期在接到硬冲突后已先由主研究人员更正，因此其更早的原字段另记入 corrections.tsv。', '',
          '核查边界最清楚的反例包括 Rootly 原生调查工具与连接器写权限不同、Cline 恢复文件与会话的约束不同、PR-Agent 发行说明与另一个源码提交中的条件分支不同，以及 PR 创建与业务部署的责任不同。没有把缺少文档说明的具体管理员角色推成已证实的购买条件。']
    (BASE/'result.md').write_text('\n'.join(rep)+'\n',encoding='utf8')
    print(len(audit),'claims,',len(fixes),'fields,',stats)
