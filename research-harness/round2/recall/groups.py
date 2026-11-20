from select_fetch import *
from bs4 import BeautifulSoup
GROUPS=[
('工业值班与跨组分派',['Chaoyun Zhang','Qingwei Lin','Saravan Rajmohan'],['H059','H078'],'StepFly 先整顿手册再离线编译；Triangle 允许多个团队角色协商分诊。可沿两条工作分别追踪诊断执行与责任归属。'),
('可复现的 flaky 测试',['August Shi','Wing Lam'],['H009','H107','H118'],'从按顺序依赖排列测试，到复现计时相关失败，再到多类基准。可复现实验先说明是哪一类 flaky。'),
('软件工程 Agent 的程序分析与验证',['Abhik Roychoudhury'],['H048','H120'],'一项把形式验证器反馈接回生成流程，一项把符号解释变成可执行的补丁判据。两篇共同作者确认研究连续性。'),
('交付基础设施与构建成本',['Shane McIntosh'],['H074','H077','H121'],'研究对象从 OpenStack 的重查请求扩展到构建系统迁移、构建依赖优化；分开计算等待、内存和构建活动。'),
('基于风险的审查者推荐',['Peter Rigby'],['H037','H055'],'前者瞄准人员离开导致的知识集中，后者按缺陷风险派专家。二者有相似模拟框架，但目标代理不同。'),
('从语言模型生成到文档测试预言',['Soneya Binta Hossain','Matthew B Dwyer'],['H010','H045'],'先考查正确且强的断言，再把 Javadoc 与被测方法作对照输入，检验有效证据来自哪里。'),
('预言生成与评估偏差',['Davide Molinelli','Alberto Martin-Lopez','Michael D. Ernst'],['H067','H115'],'Tratto 从代码与文档生成可执行预言；另一工作重新控制预言评测数据的偏差，检验模型是否真的有用。'),
('跨库变化的可验证影响',['Xing Hu','Xin Xia','Yi Gao'],['H021','H054'],'DepRadar 追踪依赖更新怎样影响下游；IntentTester 追踪测试意图怎样跨库迁移。两者可共同校准依赖升级验收。'),
('评审器数据与实际反馈',['Yanjie Jiang','Hui Liu'],['H033','H069','H126'],'安全评语数据构造、带上下文检索的评语生成及低成本专门审查器连接训练材料、输出效用和推理成本。'),
('按变更范围分配回归测试',['Michael Pradel'],['H019','H134'],'ChaCo 在未测试的 PR 差异上添加测试，NameRTS 从既有用例中选出应重跑者；一个补欠缺、一个省冗余。')]

if __name__=='__main__':
    rbase=BASE.parent/'venue-review';rs={r['id']:r for r in load(rbase/'review.tsv')}
    text=['# 可持续追踪的十条研究线','', '按至少两项实际论文中的重复作者归并。下列名称描述研究问题；作者并非其所在机构的全部研究团队。每篇的署名和页面明示单位均由官方会议详情卡复查。同一学校或看起来相似的作者姓名，均不足以单独归组。某页缺少单位时保留缺失，不把雇主名称扩写成实验室名。', ''];links=[]
    for topic,people,ids,why in GROUPS:
        text.extend([f'## {topic}','','共同署名者为 '+ '、'.join(people)+'。'+why,''])
        for i in ids:
            r=rs[i];el=BeautifulSoup(json.loads((rbase/r['path']).read_bytes())[0]['value'],'html.parser')
            names={}
            for a in el.select('.event-description .row a[href*="/profile/"]'):
                headings=a.select('.media-heading'); name=headings[0].get_text(' ',strip=True)
                names[name]=(a['href'],headings[1].get_text(' ',strip=True) if len(headings)>1 else '')
            assert set(people).issubset(names),(topic,i,people,names)
            affiliations='、'.join(filter(None,dict.fromkeys(names[n][1] for n in people))) or '该条目未标明单位'
            text.append(f'- {r["venue"].upper()} · {r["title"]}。该页署名单位：{affiliations}。[{i} 官方作者页]({r["url"]})')
            for n in people:links.append(dict(topic=topic,name=n,paper=i,author_profile=names[n][0],stated_affiliation=names[n][1],url=r['url'],snapshot='../venue-review/'+r['path']))
        text.append('')
    (BASE/'groups.md').write_text('\n'.join(text)+'\n',encoding='utf8')
    tsv(BASE/'group-evidence.tsv',links)
