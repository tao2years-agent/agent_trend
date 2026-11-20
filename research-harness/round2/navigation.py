"""Keep the original edition queryable and put the current report at each previous entry point."""
from pathlib import Path
R=Path(__file__).resolve().parent
P=R.parent
def note(path, line):
    txt=path.read_text('utf8')
    mark='<!-- second-edition -->'
    if mark in txt:
        start=txt.index(mark);end=txt.index('<!-- /second-edition -->',start)+len('<!-- /second-edition -->')
        txt=txt[:start]+mark+'\n'+line+'\n<!-- /second-edition -->'+txt[end:]
    else:
        h,rest=txt.split('\n',1)
        txt=h+'\n\n'+mark+'\n'+line+'\n<!-- /second-edition -->\n'+rest
    path.write_text(txt,'utf8')
for path,pref in [(P.parent/'README.md','research-harness/'),(P.parent/'wiki/index.md','../research-harness/'),(P/'README.md',''),(P/'wiki/index.md','../'),(P/'state/checkpoint.md','../')]:
    note(path,'**2026-11-20 决策版**　[深度分析]('+pref+'outputs/deep-report-v2.html) · [四页决策稿]('+pref+'outputs/insights-decision.html) · [分享 PDF]('+pref+'outputs/insights-decision.pdf) · [复核 Wiki]('+pref+'round2/index.md)。下方早期交付与当时覆盖数保留供追溯。')
for basename,other in [('insights','insights-v2'),('deep-report','deep-report-v2')]:
    path=P/'outputs'/(basename+'.html')
    txt=path.read_text('utf8')
    insert='<p data-edition="first" style="padding:10px 14px;border:1px solid #a5b8ad">这是第一轮研究地图。<a href="'+other+'.html">阅读第二版的复核结果与修订判断 →</a></p>'
    if 'data-edition="first"' not in txt:path.write_text(txt.replace('<article>','<article>'+insert,1),'utf8')
note(P/'outputs/deep-report.md','这是第一轮研究地图。当前结论见[第二版深度分析](deep-report-v2.html)与[复核证据索引](../round2/index.md)。')
