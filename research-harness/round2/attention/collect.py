"""Freeze author/institution copies, immutable by content hash. Never execute author code."""
from pathlib import Path
import hashlib,json,requests,subprocess,concurrent.futures,datetime
import pymupdf
B=Path(__file__).resolve().parent
TARGETS={
'A01':('Reducing Interruptions at Work: A Large-Scale Field Study of FlowLight','CHI 2017',['https://christop.club/publications/pdfs/Zuger-etal_2017.pdf','https://boyangcs.github.io/CHI17FlowLight.pdf']),
'A02':('Evaluating Cues for Resuming Interrupted Programming Tasks','CHI 2010',['https://chrisparnin.me/pdf/cues-chi09.pdf']),
'A03':('Information Needs in Collocated Software Development Teams','ICSE 2007',['https://www.microsoft.com/en-us/research/wp-content/uploads/2007/05/icse07_ko.pdf','https://www.cs.cmu.edu/~marmalade/papers/Ko2007InformationNeeds.pdf']),
'A04':('When to Show a Suggestion? Integrating Human Feedback in AI-Assisted Programming','AAAI 2024',['https://ojs.aaai.org/index.php/AAAI/article/download/28878/29669','https://arxiv.org/pdf/2306.04930']),
'A05':('Assistance or Disruption? Exploring and Evaluating the Design and Trade-offs of Proactive AI Programming Support','CHI 2025',['https://kevinpjk.github.io/assets/pdf/codellaborator_chi_2025.pdf','https://arxiv.org/pdf/2502.18658']),
'A06':('Developer Interaction Patterns with Proactive AI: A Five-Day Field Study','IUI 2026',['https://arxiv.org/pdf/2601.10253']),
'A07':('How AI Impacts Skill Formation','arXiv 2026 (R04 overlap)',['https://arxiv.org/pdf/2601.20245'])}
TARGETS['A08']=('Expectations, Outcomes, and Challenges of Modern Code Review','ICSE 2013',['https://www.cabird.com/pubs/bacchelli2013eoc.pdf','https://sback.it/publications/icse2013.pdf'])
TARGETS['A04f']=(TARGETS['A04'][0],'AAAI 2024 author conference copy',['https://erichorvitz.com/copilot_display_AAAI.pdf'])
def grab(k):
    title,venue,urls=TARGETS[k]
    for url in urls:
        try:
            r=requests.get(url,timeout=(10,40));r.raise_for_status();b=r.content
            assert b[:4]==b'%PDF';sha=hashlib.sha256(b).hexdigest();path=B/'raw'/f'{k}-{sha[:12]}.pdf'
            if not path.exists():path.write_bytes(b)
            with pymupdf.open(path) as d:
                txt='\n'.join('=== PDF PAGE %d ===\n%s'%(n+1,p.get_text(sort=True)) for n,p in enumerate(d));npages=len(d)
            (B/'text'/f'{k}.txt').write_text(txt,encoding='utf8')
            return dict(id=k,title=title,venue=venue,url=url,local=path.relative_to(B).as_posix(),sha256=sha,pages=npages,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        except Exception as e:print(k,type(e).__name__,str(e)[:150],flush=True)
    raise RuntimeError(k)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(6) as pool:manifest=list(pool.map(grab,TARGETS))
    (B/'sources.json').write_text(json.dumps(manifest,indent=2),'utf8')
    print([(m['id'],m['pages']) for m in manifest])
