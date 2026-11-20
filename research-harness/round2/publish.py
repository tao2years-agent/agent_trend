"""Build portable Chinese decision briefs and a searchable evidence book from the Wiki."""
import base64, csv, html, json, re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
from functools import lru_cache
import markdown
from bs4 import BeautifulSoup
R = Path(__file__).resolve().parent
P = R.parent
OUT = P / 'outputs'

def read(p): return p.read_text(encoding='utf8')
def enc(s): return html.escape(str(s),quote=True)
def rows(p, sep=','):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter=sep))
def md(s): return markdown.markdown(s,extensions=['tables','fenced_code','sane_lists'])
def obj(p): return json.loads(read(p))
@lru_cache(None)
def primary_urls():
    # Keep the portable book small. Preserve a clickable official destination for captured originals.
    candidates=set()
    for pattern in ('*sources.json','manifest.json','fresh.json','git-trees.json'):
        candidates.update(R.glob('*/'+pattern))
        candidates.update(R.glob('workflows/domestic/'+pattern))
    urls={}
    for file in sorted(candidates):
        todo=[obj(file)]
        while todo:
            node=todo.pop()
            if isinstance(node,list):
                todo.extend(node);continue
            if not isinstance(node,dict):continue
            todo.extend(v for v in node.values() if isinstance(v,(dict,list)))
            name=node.get('path') or node.get('local_path') or node.get('file')
            url=node.get('url') or node.get('download')
            if not (isinstance(name,str) and isinstance(url,str) and url.startswith(('https://','http://'))):continue
            for base in (file.parent,file.parent/'raw',P,R):
                path=(base/name).resolve()
                if path.is_relative_to(P) and path.is_file():
                    urls.setdefault(path,url);break
    return urls
def tsvrows(r, cols):
    return '<div class="tablewrap"><table><thead><tr>'+''.join('<th>'+enc(label)+'</th>' for key,label in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+enc(x.get(key,''))+'</td>' for key,label in cols)+'</tr>' for x in r)+'</tbody></table></div>'

chapters=[
('executive.md','执行摘要','从 code agent 团队的角度，下一步投什么'),
('decision.md','选题和试点','本团队先投入哪里'),
('pilot/protocol.md','选题和试点','怎样用一次内部试点决定是否扩面'),
('buyers/result.md','采购','35 个有可验收产物的选择'),
('buyer-audit/result.md','采购','70 个产品主张的独立核对'),
('product-code/result.md','采购','35 项产品中能直接查到哪些实现'),
('evolution/result.md','演进','固定窗口内的发布与变更'),
('product-history/result.md','演进','每项采购候选有哪些带日期的变化'),
('version-anchors/result.md','演进','十项选型判断的版本与日期'),
('evalops/result.md','采购','反馈、评估与发布判定的产品'),
('economics/result.md','采购','同一次试点分别在哪些地方计费'),
('eng-intel-vendors/result.md','采购','组织效能平台如何界定开发者、AI 使用和交付'),
('devlake/result.md','组织效能','同一个变更失败率，换数据库还会得出同一个答案吗'),
('workflows/result.md','采购','全球产品的三组同题对照'),
('workflows/domestic/result.md','采购','国内产品的授权与接管'),
('field/result.md','工程现场','迁移、质量与事故恢复'),
('factories/result.md','工程现场','Stripe、Ramp、OpenAI 和 StrongDM 的取舍'),
('migration/result.md','本地实验','12 个发布版本的规则迁移'),
('compat/result.md','本地实验','真实依赖升级要按什么顺序'),
('dependency-bot/result.md','本地实验','依赖更新机器人会验收到哪一步'),
('ci/result.md','组织效能','CI 重跑的历史留出与成本'),
('ci-availability/result.md','组织效能','做重跑决定时已经知道哪些信息'),
('ci-cross/result.md','组织效能','换到 GitHub Actions 后，重跑数据能说明什么'),
('oracles/result.md','本地实验','公开修复与独立验收'),
('gates/result.md','本地实验','整个测试子包也漏过的错误'),
('oracle-releases/result.md','本地实验','把历史验收反例追到十个正式发行版'),
('js-compat/result.md','本地实验','换到 JavaScript 后，安装约束能挡住哪些错配'),
('evolving-tests/result.md','论文','从三篇顶会工作看跨版本验收'),
('handoff/result.md','本地实验','跨进程接管与丢失回执'),
('interoperability/result.md','本地实验','五组现有规范怎样记录批准、运行与回执'),
('optimizers/result.md','自动优化','六种外层优化方法'),
('optimizersrc/result.md','自动优化','两个固定提交的选择逻辑'),
('pairing/result.md','自动优化','同一模型的五次提交与任务分派'),
('empirical/result.md','组织效能','公开 PR 的分层抽样'),
('cohorts/result.md','组织效能','共同仓库和月份的敏感性'),
('ownership/result.md','组织效能','历史能否找对接班人'),
('supervision/result.md','组织效能','排队一天的 PR 是否值得提醒维护人'),
('attention/result.md','组织效能','从真人研究判断什么时候该打断工程师'),
('message-quality/result.md','组织效能','怎样验收真正帮助接班人的一条消息'),
('papers/result.md','组织效能','论文正文与统计量复算'),
('throughput/result.md','组织效能','从提交到交付的独立口径'),
('replication/result.md','组织效能','复算公开开发者研究'),
('selection-effect/result.md','组织效能','谁愿意进入开发者提效试验，谁会退出'),
('promotion-replay/result.md','自动优化','提示版本真的能按获批对象发布和回滚吗'),
('venue-frame/result.md','论文','八届顶会的检索边界'),
('venue-review/result.md','论文','候选复核与研究组'),
('recall/result.md','论文','改写检索词后还能找到什么'),
('recall/groups.md','论文','研究团队与持续跟踪问题'),
('labs/result.md','论文','六条能提供可复用实验工件的研究线'),
('cowork/result.md','本地复算','模拟同事补全需求后，能否整件交付'),
('abstract-index/result.md','论文','用摘要作第二道筛查能找回哪些问题'),
('protocol.md','复核','复算、反例与覆盖边界'),
('conclusion.md','研究建议','给下一次研发平台评审的决定')]
def book(deep):
    sections=[]; attachments={}; attached_paths={}; nav=[]; buyerrows=rows(R/'buyers/ledger.csv')
    bp={x['id']:x for x in obj(R/'buyers/sources.json')}
    chapids={ (R/rel).resolve():'ch'+str(i+1) for i,(rel,_,_) in enumerate(chapters) if (R/rel).exists()}
    pdfmap=primary_urls().copy()
    for directory in ['papers','throughput']:
        for x in obj(R/directory/'manifest.json'):
            if x.get('path'):pdfmap[(R/directory/x['path']).resolve()]=x['url']
    for x in obj(R/'optimizers/sources.json'):
        if x.get('path'):pdfmap[(R/'optimizers'/x['path']).resolve()]=x['url']
    for x in bp.values():pdfmap[(P/x['path']).resolve()]=x['url']
    def rich(source):
        soup=BeautifulSoup(md(read(source)),'html.parser')
        for h in soup.find_all('h1'):h.decompose()
        for tab in soup.find_all('table'):tab.wrap(soup.new_tag('div',attrs={'class':'tablewrap'}))
        for a in soup.find_all('a',href=True):
            href=a['href']
            if href.startswith(('http://','https://','#','mailto:')): continue
            path=(source.parent/unquote(urlsplit(href).path)).resolve()
            if path in chapids:a['href']='#'+chapids[path];continue
            if path in pdfmap:a['href']=pdfmap[path];continue
            if not path.is_relative_to(P) or not path.is_file():
                a.replace_with(a.get_text()+'（见专题 Wiki）');continue
            if path.stat().st_size>1750000 or path.suffix.lower() in ('.pdf','.zip','.png','.html'):
                a.replace_with(a.get_text()+'（专题 Wiki 原件）');continue
            if path not in attached_paths:
                aid='f'+str(len(attachments)+1)
                payload=path.read_bytes()
                if path.suffix.lower() in ('.txt','.json','.log','.csv','.tsv'):
                    exported=re.sub(rb'(?i)([a-z]:[\\/]+users[\\/]+)[^\\/\s"\']+',rb'\1[local-user]',payload)
                else:
                    exported=payload
                attachments[aid]=dict(n=path.name,b=base64.b64encode(exported).decode('ascii'),redacted=exported!=payload)
                attached_paths[path]=aid
            aid=attached_paths[path]
            a['href']='#download';a['data-attachment']=aid;a['title']='下载报告内附的证据文件'
            if attachments[aid]['redacted']:
                a['title']='下载已隐去本机用户目录的副本；完整哈希对应 Wiki 原件'
        return str(soup)
    def section(id,title,content,category=''):
        page = '' if deep else ' data-page="'+str(len(sections)+1)+' / 4"'
        sections.append('<section class="chapter" id="'+id+'"'+page+'><span class="kicker">'+enc(category)+'</span><h2>'+enc(title)+'</h2>'+content+'</section>')
        nav.append((id,title,category))
    if deep:
        src_counts=obj(R/'product-code/coverage.json')
        cohort=obj(R/'cohorts/audit.json')
        gh=obj(R/'ci-cross/holdout.json')['registered']
        gh_rule=next(x for x in gh['policies'] if x['target']==.95)
        js=obj(R/'js-compat/validation.json')
        crosschecks=[
          ('产品源码',f"{src_counts['buyers']} 个采购对象，{src_counts['layers']['核心模块']} 项读到直接核心模块。",'product-code/result.md'),
          ('能否直接跳过 CI',f"GitHub {gh['test']:,} 个留出 run 中少派 {gh_rule['saved_retries']} 次，错过 {gh_rule['missed_green']} 次本可转绿。",'ci-cross/result.md'),
          ('依赖工具的强基线',f"React 共 {js['matrix_strict']} 种预选组合，严格安装拒绝 {js['strict_rejected']} 种，允许的 {js['strict_passed_probe']} 种全通过所测交互。",'js-compat/result.md'),
          ('人的可见决定',f"{cohort['total']:,} 个真实公开 PR，能观察到正式个人评审决定的有 {cohort['formal_observed']:,} 个。",'cohorts/result.md'),
        ]
        for rel,cat,title in chapters:
            path=R/rel
            if path.exists():
                content=rich(path)
                if rel=='executive.md':
                    block='<h3>直接查看复算证据</h3><div class="tablewrap"><table><thead><tr><th>问题</th><th>固定样本结果</th></tr></thead><tbody>'
                    for label,fact,dest in crosschecks:
                        block+='<tr><td><a href="#'+chapids[(R/dest).resolve()]+'">'+enc(label)+'</a></td><td>'+enc(fact)+'</td></tr>'
                    content+=block+'</tbody></table></div>'
                section(chapids[path.resolve()],title,content,cat)
        paperrows=rows(R/'papers/results.tsv','\t')
        section('paperlist','16 篇正文逐项复核',tsvrows(paperrows,[('title','论文'),('locator','原文位置'),('sample','样本'),('comparison','对照'),('finding','结果'),('validity','局限'),('test','验证办法')]),'证据明细')
        records=[]
        code={r['id']:r for r in rows(R/'product-code/ledger.csv')}
        anchors=rows(R/'product-code/mechanisms.csv')
        code_src={r['id']:r['url'] for r in obj(R/'product-code/sources.json')}
        history={r['id']:r for r in obj(R/'product-history/ledger.json')}
        historical_sources=obj(R/'product-history/sources.json')
        pricing={r['buyer']:r for r in rows(R/'economics/tariffs.csv')}
        price_sources={r['id']:r['url'] for r in obj(R/'economics/sources.json')}
        for x in buyerrows:
            ids=x['evidence_ids'].split()
            sources=' · '.join('<a href="'+enc(bp[k]['url'])+'">'+enc(k)+'</a>' for k in ids)
            fields=[('采购工作',x['task']),('触发',x['trigger']),('验收产物',x['accepted_artifact']),('人工接管',x['human_takeover']),('适用版本与形态',x['availability_version']),('证据边界',x['unknown_or_boundary'])]
            cr=code[x['id']]
            fields += [('公开实现所处层级',cr['layer']),('代码能查到什么',cr['observed']),('仍需演示',cr['unverified_and_test'])]
            lines=[a for a in anchors if a['buyer']==x['id']]
            files=[(i,code_src[i]) for i in cr['new_evidence_ids'].split(' | ') if i in code_src]
            links=[(a['locator'],a['url']) for a in lines] if lines else files[:2]
            if links:
                sources+=' · '+' · '.join('<a href="'+enc(url)+'">'+enc(label)+'</a>' for label,url in links)
            hist=history[x['id']]
            events=[]
            for e in hist['events']:
                cited=' · '.join('<a href="'+enc(historical_sources[k]['url'])+'">'+enc(k)+'</a>' for k in e['refs'] if k in historical_sources)
                events.append('<li>'+enc(' '.join(v for v in [e['date'],e['version'],e['scope']] if v))+' '+cited+'</li>')
            timeline='<h4>版本演进 · '+enc(hist['status'])+'</h4><ul>'+''.join(events)+'</ul>'
            if x['id'] in pricing:
                f=pricing[x['id']]
                fields.extend([('计费单位',f['billable_unit']),('公开套餐与日期',f['verified_as_of']+' '+f['public_rate']),('需确认',f['request_quote_or_invoice'])])
                sources+=' · '+' · '.join('<a href="'+enc(price_sources[k])+'">'+enc(k)+'</a>' for k in f['evidence'].split() if k in price_sources)
            records.append('<details class="record"><summary>'+enc(x['id']+'　'+x['product'])+'</summary><dl>'+''.join('<dt>'+enc(label)+'</dt><dd>'+enc(val)+'</dd>' for label,val in fields)+'</dl><p>'+sources+'</p>'+timeline+'</details>')
        section('catalog','逐产品查证','<label for="search">筛选产品、工作或限制</label><input id="search" type="search" placeholder="例如　合并队列"><output aria-live="polite" id="matches"></output>'+''.join(records),'35 项产品台账')
    else:
        brief=BeautifulSoup(md(read(R/'share.md')),'html.parser')
        for tab in brief.find_all('table'):
            tab.wrap(brief.new_tag('div',attrs={'class':'tablewrap'}))
        for i,heading in enumerate(brief.find_all('h2')):
            body=[]
            for node in heading.next_siblings:
                if getattr(node,'name',None)=='h2':break
                body.append(str(node))
            section('s'+str(i+1),heading.get_text(),''.join(body),'')
    title='从 Code Agent 到组织级研发自动化' if deep else '从 Code Agent 到组织级工作控制面'
    lead='比较产品如何接单、接管与验收，并用源码、公开数据和本地故障实验检验这些能力。' if deep else '一项主攻、三项停手，以及 90 天内可以被证伪的产品计划'
    base=read(R/'reader-v2.html')
    def link(n):
        return '<a href="#'+n[0]+'">'+enc(n[1])+'</a>'
    if deep:
        buckets={}
        for n in nav:buckets.setdefault(n[2],[]).append(n)
        contents=''.join('<details class="navgroup"'+(' open' if key in ['执行摘要','选题和试点'] else '')+'><summary>'+enc(key)+'</summary>'+''.join(map(link,items))+'</details>' for key,items in buckets.items())
        contents='<a class="cataloglink" href="#catalog">查询 35 项产品 ↓</a>'+contents
    else:
        contents=''.join(map(link,nav))
    replacements={'TITLE':title,'KIND':'深度分析 · 第二版' if deep else '产品决策稿 · 重制版',
      'LEAD':lead,'NAV':contents,
      'SECTIONS':''.join(sections),'ATTACHMENTS':json.dumps(attachments,separators=(',',':')),
      'MODE':'deep' if deep else 'brief'}
    for key,val in replacements.items():base=base.replace('{{'+key+'}}',val)
    target=OUT/('deep-report-v2.html' if deep else 'insights-decision.html')
    target.write_text(base,'utf8')
    if not deep:
        # Keep the established link current while preserving a distinct handoff name
        # for the decision-oriented revision.
        (OUT/'insights-v2.html').write_text(base,'utf8')

if __name__=='__main__':
    import sys
    missing=[rel for rel,_,_ in chapters if not (R/rel).is_file()]
    if missing and '--draft' not in sys.argv:
        raise SystemExit('Missing sections: '+', '.join(missing))
    book(True)
    book(False)
