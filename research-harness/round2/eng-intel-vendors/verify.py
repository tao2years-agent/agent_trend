from pathlib import Path
from bs4 import BeautifulSoup as B
import json,re,hashlib,subprocess,sys
R=Path(__file__).resolve().parent;ROOT=R.parent.parent
def hashit(b):return hashlib.sha256(b).hexdigest()
def get(p):return json.loads(p.read_text('utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),'utf8')
def main():
    old=get(ROOT/'corpus/products.json');reused={}
    for product in old:
        if product['id'] not in ['B01','B02']:continue
        for n,s in enumerate(product['sources'],1):
            if (product['id'],n) not in [('B01',3),('B02',1),('B02',2)]:continue
            k={('B01',3):'dx-q3',('B02',1):'lb-thresholds',('B02',2):'lb-cycle-old'}[product['id'],n]
            assert hashit((ROOT/s['path']).read_bytes())==s['sha256']
            reused[k]={**s,'path_relative_to':'research-harness'}
    write(R/'reused.json',reused)
    src={k:ROOT/v['path'] for k,v in reused.items()}
    for e in get(R/'sources.json'):
        if 'path' not in e:continue
        p=R/e['path'];assert hashit(p.read_bytes())==e['sha256'];src[e['key']]=p
    checks={
    'dx-owner':['definitive agreement to acquire DX'],'dx-10k':['On November 10, 2025, the Company acquired 100%'],'dx-deploy':['Multi-tenant SaaS','DX Dedicated','DX Managed'],'dx-managed':['GCP (coming soon)'],'dx-throughput':['bot-authored','0.5 developers'],'dx-snapshot':['recurring surveys'],'dx-scores':['total_respondents','total_cohort','minimum response threshold'],'dx-privacy':['non-anonymous comments'],'dx-initiative':['Generate tasks for entities with failing checks','Due Date'],'dx-q3':['500+ companies','Weighted PRs/week/dev'],
    'jf-trends':['committing user is an agent','human-opened PRs merged','merged code additions'],'jf-impact':['Nov 18, 2025','Autonomous Agent Insights'],'jf-june':['over 2 million PRs'],'jf-own':['from 26 to 58','two weeks','answers are anonymous'],
    'lb-thresholds':['day (UTC)','default is 25%','1 out of 10 commits = 10%'],'lb-cycle-old':['Draft PRs are counted as coding time','first non-author comment'],'lb-working':['WorkerB','Slack or MS Teams'],'lb-survey-change':['October 21, 2026','personal link','Slack connected'],'lb-release-blog':['September 8, 2025','DevEx surveys']}
    def clean(t):return ''.join(t.lower().split()).replace('’',"'")
    for k,items in checks.items():
        p=src[k]
        txt=subprocess.check_output(['pdftotext','-layout',str(p),'-'],stderr=subprocess.DEVNULL).decode('utf8') if p.suffix=='.pdf' else B(p.read_bytes(),'html.parser').get_text(' ',strip=True)
        for value in items:assert clean(value) in clean(txt),(k,value)
    write(R/'claim-checks.json',[dict(id=k,sha256=hashit(src[k].read_bytes()),locators=terms) for k,terms in checks.items()])
    subprocess.run([sys.executable,str(R/'fixture.py')],check=True)
    for link in re.findall(r'\]\(([^)]+)\)',(R/'result.md').read_text('utf-8-sig')):
        if not link.startswith('https:'):assert (R/link).exists(),link
    print(f'{len(src)} available unique source IDs; {len(checks)} publication/document anchors; {sum(map(len,checks.values()))} string locators verified.')
if __name__=='__main__':main()
