"""Recompute published summary cells from their layout text; no simulated raw observations."""
import csv
import hashlib
import json
import math
import re
from pathlib import Path

BASE=Path(__file__).resolve().parent
def page(ident,n):
    return (BASE/'text'/f'{ident}.txt').read_text(encoding='utf8').split('\f')[n-1]

def compute():
    records=[]
    def add(id,where,quantity,inputs,val):
        records.append((id,where,quantity,inputs,round(val,5)))
    p=page('R01',12)
    means=re.search(r'^ Pull Requests\s+(.*)$',p,re.M).group(1)
    ses=re.search(r'^ Pull Requests.*\n\s*([^\n]+)',p,re.M).group(1)
    extract=lambda s:[float(z) for z in re.findall(r'[\d]+\.[\d]+',s)]
    estimates=extract(means)[1:6:2]
    se=extract(ses)[1:6:2]
    assert estimates==[27.38,17.94,54.03] and se==[12.88,18.72,42.63]
    weights=[1/x**2 for x in se]
    add('R01','p12 Table 3','三公司合规者效应，PR相对百分比',str(list(zip(estimates,se))),sum(e*w for e,w in zip(estimates,weights))/sum(weights))
    add('R01','p12 Table 3','相应合并标准误','1/sqrt(sum(1/SE_i^2))',1/math.sqrt(sum(weights)))
    p=page('P04',5)
    initial=int(re.search(r'total of (\d+) flaky tests',p).group(1))
    reproduced=int(re.search(r'tests \(i\.e\., (\d+)',p).group(1))
    fixed=int(re.search(r'produced fixes for [\d.]+% \(i\.e\., (\d+)\)',p).group(1))
    accepted=int(re.search(r'fixes \(i\.e\., (\d+) fixes\)',p).group(1))
    for label,a,b in [('复现/尝试',reproduced,initial),('修复/复现',fixed,reproduced),('落地/修复',accepted,fixed),('落地/全部尝试',accepted,initial)]:
        add('P04','p5 §IV',label+' (%)',f'{a}/{b}',100*a/b)
    p=page('R03',5)
    treatment,control=map(float,re.search(r'group is ([\d.]+) minutes and ([\d.]+) minutes',p).groups())
    add('R03','p5 Results','完成者耗时降幅 (%)',f'(1-{treatment}/{control})*100',100*(1-treatment/control))
    p=page('P18',12)
    rows=re.findall(r'^\s*(?:Ambari|Calcite|Groovy|Ignite|Isis|Netbeans)\s+(0\.\d+)\s+(0\.\d+)',p.split('Table 3.')[0],re.M)
    assert len(rows)==6
    means=[sum(map(float,col))/6 for col in zip(*rows)]
    add('P18','p12 Table 2','Hit@1六项目宏均值绝对差（百分点）',str(rows),100*(means[0]-means[1]))
    add('P18','p12 Table 2','Hit@1六项目宏均值相对差 (%)','同上，差值/基线均值',100*(means[0]/means[1]-1))
    main=p.split('Table 3.')[0]
    allrows=[list(map(float,re.findall(r'0\.\d+',line))) for line in main.splitlines()
             if re.match(r'^\s*(Ambari|Calcite|Groovy|Ignite|Isis|Netbeans)\s',line)]
    published=list(map(float,re.findall(r'0\.\d+',re.search(r'^\s*Mean\s+.*$',main,re.M).group(0))))
    for name,col,listed in zip(['LinkAnchor','EasyLink','EALink','T-Bert','DeepLink','VSM'],zip(*allrows),published,strict=True):
        add('P18','p12 Table 2',name+' 六项目均值',f'列值 {col}；论文均值 {listed}',sum(col)/6)
    p=page('R05',6)
    values=re.search(r'rose from (\d+\.\d+) in the pre-mandate baseline\s*\n.*?to (\d+\.\d+) in April',p).groups()
    add('R05','p6 §IV.A','描述性组织PR人均月数比值',f'{values[1]}/{values[0]}',float(values[1])/float(values[0]))
    return records

if __name__=='__main__':
    records=compute()
    with (BASE/'recalculated.tsv').open('w',encoding='utf8',newline='') as f:
        out=csv.writer(f,delimiter='\t',lineterminator='\n')
        out.writerow(['id','locator','quantity','inputs','result'])
        out.writerows(records)
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf8'))
    for r in manifest:
        if r['state']=='captured':
            assert hashlib.sha256((BASE/r['path']).read_bytes()).hexdigest()==r['sha256'],r['id']
    print(len(records),'summary quantities recomputed;',sum(r['state']=='captured' for r in manifest),'raw checksums verified')
