"""Recompute procurement case studies using the source-pinned USD tariffs in assumptions.json."""
from pathlib import Path
from math import ceil
import json,csv,hashlib
R=Path(__file__).resolve().parent
p=json.loads((R/'assumptions.json').read_text(encoding='utf-8-sig'))
def rows_file(name, rows):
    with (R/name).open('w',newline='',encoding='utf-8-sig') as f:
        out=csv.DictWriter(f,fieldnames=list(rows[0]));out.writeheader();out.writerows(rows)
def make_line(id,what,qty,unit,rate,class_,source):
    return dict(id=id,item=what,quantity=qty,unit=unit,rate_usd=rate,amount_usd=round(qty*rate,6) if rate is not None else '',classification=class_,tariff=source)
seats=p['github_new_seats']
lines=[
 make_line('P1','Copilot Business 新开席位',seats,'seat-month',p['github_business_seat_usd'],'新增现金','G1/G4'),
 make_line('P2','组织共享池用完后的 AI credits',max(0,p['github_total_ai_credits']-seats*p['github_included_credits_per_seat']),'GitHub AI credit',p['github_credit_usd'],'新增现金','G4'),
 make_line('P3','假设仓主 Linux x64 2-core 已扣尽可用额度后的计费分钟',p['github_billable_standard_linux_minutes_after_allowance'],'已按作业取整的分钟',p['github_linux_minute_usd'],'新增现金','G2/G3'),
 make_line('P4','Mergify Max，整月活跃且计费的自然人',p['mergify_active_full_period_humans'],'contributor-month',p['mergify_max_monthly_per_human_usd'],'新增现金','M1/M2'),
 make_line('P5','试点新增人工复核',p['incremental_active_review_minutes']/60,'人时',p['reviewer_loaded_usd_hour'],'内部机会成本','假设'),
 make_line('P6','排队经过的时间，未占用人员',p['elapsed_queue_minutes'],'历时分钟',None,'仅服务水平指标','假设'),
 make_line('P7','现有共享平台分摊',1,'月',p['existing_shared_platform_monthly_allocation_usd'],'既有成本，排除增量总计','假设')]
rows_file('pilot-ledger.csv',lines)
cash=sum(x['amount_usd'] for x in lines if x['classification']=='新增现金')
human=lines[4]['amount_usd'];n=p['accepted_distinct_end_to_end_changes']
counts={a:{'cash_per_accepted_usd':round(cash/a,4),'economic_per_accepted_usd':round((cash+human)/a,4)} for a in [48,n,96]}
q={}
for name,v in p['qoder_distribution'].items():
    assert len(v)==p['qoder_international_seats']
    st=sum(max(0,n-p['qoder_teams_allowance']) for n in v)
    et=sum(v)
    packs=lambda credits:ceil(credits/p['qoder_pack_credits'])
    q[name]=dict(total=sum(v),teams_packs=packs(st),teams_usd=len(v)*p['qoder_teams_seat']+packs(st)*p['qoder_pack_usd'],enterprise_packs=packs(et),enterprise_usd=len(v)*p['qoder_enterprise_seat']+packs(et)*p['qoder_pack_usd'])
dd={}
for avg in p['datadog_average_credits_scenarios']:
    c=avg*p['datadog_investigations_per_month']
    usd=p['datadog_on_demand_usd_credit']
    dd[avg]=dict(monthly_credits=c,on_demand_usd=round(c*usd,2),annual_commitment_monthly_equivalent_usd=round(p['datadog_annual_bundle_monthly_usd']+max(0,c-p['datadog_annual_bundle_credits'])*usd,2))
loc=p['sonar_project_branches_loc']
result={'cash_increment_usd':round(cash,2),'active_review_shadow_usd':human,'economic_increment_usd':round(cash+human,2),'accepted_sensitivity':counts,'gross_hours_saved_break_even':round((cash+human)/p['reviewer_loaded_usd_hour'],4),'qoder':q,'datadog':dd,'datadog_break_even_credits_per_month_if_use_repeats_for_12_months':round(p['datadog_annual_bundle_monthly_usd']/p['datadog_on_demand_usd_credit'],3),'sonar':{'billed_loc':sum(map(max,loc)),'mistaken_summed_branches':sum(map(sum,loc)),'hypothetical_cap':p['sonar_license_cap']}}
assert result['cash_increment_usd']==315.60 and q['balanced']['teams_usd']==240 and q['concentrated']['teams_usd']==360 and dd[3]['on_demand_usd']==390 and dd[5]['on_demand_usd']==650 and result['sonar']['billed_loc']==135000
(R/'sensitivity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
d=json.loads((R/'sources.json').read_text(encoding='utf8'))
assert len(d)==27 and len(set(i['id'] for i in d))==len(d)
for s in d:
    assert (R/s['text']).is_file() and hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
registry={s['id']:s for s in d}
with (R/'tariffs.psv').open(encoding='utf-8-sig') as f:
    tariff_rows=list(csv.DictReader(f,delimiter='|'))
assert len(tariff_rows)==8 and len(set(x['buyer'] for x in tariff_rows))==8
for row in tariff_rows:
    row['verified_as_of']='2026-11-20'
    assert all(s in registry for s in row['evidence'].split())
rows_file('tariffs.csv',tariff_rows)
import re
for link in re.findall(r'\]\(([^ )]+)\)',(R/'result.md').read_text(encoding='utf-8-sig')):
    assert link.startswith('https://') or (R/link).exists(),link
print(result)
