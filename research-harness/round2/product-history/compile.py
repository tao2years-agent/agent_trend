"""Recompile the exact historical ledger; release-note dates and verified source scope are explicit."""
from pathlib import Path
import collections,csv,hashlib,html,json,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parent
root=R.parent.parent
def read(p):return json.loads(p.read_text('utf8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf8')
def digest(b):return hashlib.sha256(b).hexdigest()
def rows(p,delim=','):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delim))
def main():
    prior=rows(R.parent/'buyers/ledger.csv')
    ref={x['id']:x for x in read(R.parent/'buyers/sources.json')}
    for x in read(R.parent/'version-anchors/sources.json'):
        if x.get('path'): ref['A'+x['id'][3:]]={**x,'path':'round2/version-anchors/'+x['path']}
    for x in read(R.parent/'evolution/sources.json'):ref[x['id']]=x
    for x in read(R/'fresh.json'):
        if x.get('path'):ref[x['key']]=x
    for i,(key,date) in enumerate([('graphite23','2023-05-30'),('graphite24','2024-04-09')],1):
        p=R/'raw'/f'graphite-{i}-index-response.txt'
        ref[f'graphite-index{i}']=dict(url=next(x['url'] for x in read(R/'fresh.json') if x['key']==key),path=p.relative_to(root).as_posix(),sha256=digest(p.read_bytes()),via='检索索引内厂商原文，2026-11-20 直接 GET 返回 404')
    out=[]; used={}
    def canonical(ids):
        for s in ids:
            x=ref[s];bytes_=(root/x['path']).read_bytes();assert digest(bytes_)==x['sha256'],s
            used[s]={k:x[k] for k in ('url','path','sha256','via','fetched_utc','retrieved','date') if k in x}
    def normalized(i):
        p=root/ref[i]['path'];data=p.read_text('utf8',errors='replace')
        if p.suffix=='.atom':
            import xml.etree.ElementTree as ET
            data=' '.join((BeautifulSoup(v,'html.parser').get_text(' ',strip=True) if '<' in v else v) for v in ET.fromstring(data).itertext())
        elif p.suffix=='.html':data=BeautifulSoup(html.unescape(data),'html.parser').get_text(' ',strip=True)
        return re.sub(r'\s+','',html.unescape(data)).lower()
    cache={}
    for x in rows(R/'claims.psv','|'):
        ids=x['source'].split();canonical(ids)
        for i in ids:
            if i not in cache:cache[i]=normalized(i)
        loc=re.sub(r'\s+','',x['locator']).lower()
        assert any(loc in cache[i] for i in ids),(x['id'],x['locator'])
        prec='日' if len(x['date'])==10 else '月' if len(x['date'])==7 else '版本'
        level='index-only' if x['id']=='23' else 'context' if x['kind'] in ['month','version-context','policy','campaign-context','community-context'] else 'direct'
        out.append(dict(id='BUY'+x['id'],date=x['date'],version=x['version'],precision=prec,kind=x['kind'],scope=x['subject'],evidence=level,refs=ids,locator=x['locator']))
    mapping={'Devin':'BUY11','Sourcegraph src-cli':'BUY16','PR-Agent':'BUY20','Argo Rollouts':'BUY25','Atlantis':'BUY27'}
    for x in rows(R.parent/'evolution/timeline.csv'):
        if x['product'] not in mapping:continue
        ids=x['evidence_ids'].split();canonical(ids)
        context='配置·不可归入' in x['change_type'];kind=x['change_type']
        out.append(dict(id=mapping[x['product']],date=x['date'],version=x['entry'],precision='日',kind=kind,scope=x['fact'],evidence='context' if context else 'direct',refs=ids,locator=x['entry'],upstream_entry_url=x['url']))
    ledger=[]
    for p in prior:
        group=[x for x in out if x['id']==p['id']]
        assert group,p['id']
        group.sort(key=lambda x:(x['date'],int(re.search(r'\d+\.([0-9]+)',x['version'])[1]) if re.search(r'\d+\.([0-9]+)',x['version']) else 0))
        direct=[x for x in group if x['evidence']=='direct'];indexed=[x for x in group if x['evidence']=='index-only']
        if len(direct)>1:status='直接原件可作先后对照'
        elif indexed and len(indexed)>1:status='仅索引原文可作先后对照'
        elif direct:status='严格口径单点'
        else:status='具体日或正式版的功能变化仍未定位'
        ledger.append(dict(id=p['id'],product=p['product'],status=status,direct=len(direct),index_only=len(indexed),context=len(group)-len(direct)-len(indexed),events=group))
    assert len(ledger)==35 and len({p['id'] for p in ledger})==35
    counts=dict(collections.Counter(x['status'] for x in ledger))
    write(R/'ledger.json',ledger);write(R/'sources.json',used);write(R/'coverage.json',dict(products=35,status=counts,observations=len(out),direct=sum(x['direct'] for x in ledger),index_only=sum(x['index_only'] for x in ledger),context=sum(x['context'] for x in ledger),sources=len(used),prior_window_units=113,prior_six_lines_in_procurement=5))
    with (R/'timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['产品ID','产品','证据口径','日期','版本','日期精度','事件分类','具体变化','定位','来源及原文'])
        for p in ledger:
            for e in p['events']:
                w.writerow([p['id'],p['product'],e['evidence'],e['date'],e['version'],e['precision'],e['kind'],e['scope'],e['locator'],' '.join(e['refs'])])
    report=['# 35 个产品的发布史覆盖台账','',f"截至 2026-11-20，35 个采购对象中，{counts.get('直接原件可作先后对照',0)} 个有至少两个可直接复核的日期或正式版本，1 个的功能演进目前只能精确到月（另有政策生效日及体验招募日期），1 个只能从检索索引中的厂商原文重建两个时点。{sum(x['direct'] for x in ledger)} 条直接证据记录的是版本行为和发布范围，不等于同样多的独立新功能。",'','**对产品决策影响最大的三个变化**','','- CircleCI Chunk 的特定 ad-hoc 任务在 2025 年 11 月就可以推入变更并触发客户 CI。2026 年 2 月的更新是失败作业入口与上下文传递。Renovate 本地 lookup 的试验边界不能移用到 Chunk。[CircleCI 记录](https://circleci.com/changelog/chunk-now-validates-changes-by-running-your-ci-pipeline/)','- 华为码道 2026 年 2 月公测，4 月的公测检查点支持回退；11 月更新的 Review 与 Fix Agent 明列商用。TRAE 和 Qoder 也有带日期的形态迁移。采购记录要带产品端、版本和灰度状态。[华为云版本表](https://support.huaweicloud.com/wtsnew-codeartsagent/index.html)','- Datadog 的 Bits AI SRE 有同一功能从有限开放到 GA 的链；Sentry 原有 Seer Debugger GA 之后，新交互形态 Seer Agent 仍是 beta。两个厂商相似的营销词不能处理成同一成熟度。[Datadog 公告](https://www.datadoghq.com/about/latest-news/press-releases/datadog-unveils-latest-ai-agents-to-rapidly-resolve-application-issues/) · [Sentry 公告](https://blog.sentry.io/introducing-seer-agent/)','','## 产品与证据','','每行展示首、末两个可用锚点；云效单列月度精度。事件明细、支线、发布命名和来源快照见[逐事件 CSV](timeline.csv)、[结构化台账](ledger.json)与[来源索引](sources.json)。点击每项的前后证据可跳到对应官方发布材料。','','|产品|严格覆盖|较早锚点|较晚锚点|','|---|---|---|---|']
    for p in ledger:
        active=[e for e in p['events'] if e['evidence']!='context']
        if not active:
            active=[e for e in p['events'] if e['kind']=='month']
        def md(e):
            a=used[e['refs'][0]];return (e['date'] or e['version'])+' '+e['scope']+' [原文]('+e.get('upstream_entry_url',a['url'])+')'
        report.append('|'+p['id']+' '+p['product']+'|'+p['status']+'|'+md(active[0])+'|'+(md(active[-1]) if len(active)>1 else '2025-10、2026-03、2026-09 三条官方月报另列；首个具体上线日未知。 [月报](https://help.aliyun.com/zh/yunxiao/product-overview/monthly-product-update-overview)')+'|')
    report+=['','## 时间窗口与复算','','35 的分母完全继承采购台账；6 条原先按 2026-05-01 至 11-20 逐版复盘的产品线有 5 条在这 35 项中。Jules 已退场，被记录在原专项，不加入采购分母。原有 113 个发布单元及 28 条精选观察仅对应那 6 条产品线；此次对其余产品采用定向核查，不计算发版速度，也不声称穷尽历年日志。除上述窗口外，其余历史锚点不设统一下界，上界均为 2026-11-20。[严格采购分母](../buyers/ledger.csv) · [六线原始筛选](../evolution/result.md) · [原十项锚点](../version-anchors/result.md)','','同一产品可含多项功能或多个客户端，逐事件保留适用面。事件种类含引入、增强、默认改变、修复、预览、GA、弃用、退场及计费/入口政策；修复不等于功能首次上线。GitHub Releases Atom 的日期取条目 updated，若无独立发布日则以正式 tag 表述版本。CodeBuddy 与 SonarQube 依据正式版本的先后排序；不补造日历日期。索引转录、只有月份的云效功能记录、云效政策生效日与体验招募期均未混入严格两点数。阿里云云原生社区账号发布过有具体日的单提交评审介绍，原页标为社区供稿，留作辅助披露。Argo 的 backport 计为不同 tag 记录，但同一调整不能反复计算成多个新机制。Spacelift v5.1.1 仅是版本化迁移说明，PR-Agent 仓库自身的托管配置也只列作背景。','','从本目录执行 `python compile.py` 可在离线环境核对每份原件哈希、手工锚点的定位词、采购分母、索引证据分类，重新生成上述表和本页。`python fetch.py` 负责补抓清单并保留失败；能恢复的旧官方原页与关闭的 Graphite 链接分别入账。研究没有测量安装率、真实采用时间、组织成本或功能效果。[补抓原始结果](fresh.json) · [覆盖计数](coverage.json)']
    (R/'result.md').write_text('\n'.join(report)+'\n','utf8')
    print((R/'coverage.json').read_text('utf8'))
if __name__=='__main__':main()

