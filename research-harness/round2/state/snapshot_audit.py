"""Re-hash local paths declared by primary-source registries. No downloads or account access."""
import hashlib,json,re,csv,sys,zipfile,tempfile
from pathlib import Path
from collections import Counter
from functools import lru_cache
R=Path(__file__).resolve().parent.parent;P=R.parent
def nested(v):
    if isinstance(v,dict):
        yield v
        for k,x in v.items():
            if isinstance(x,(list,dict)):
                yield from nested(x)
    elif isinstance(v,list):
        for x in v:yield from nested(x)
@lru_cache(None)
def hashfile(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def audit():
    names={'manifest.json','sources.json','fresh.json','bridge-sources.json','additional-sources.json','contract-sources.json','release-sources.json','git-trees.json','ablation-sources.json','rendered-sources.json','golden-source.json','tag-sources.json','diff-sources.json','supplement-sources.json','attribution-docs.json','codex-tag-sources.json','sample-manifest.json'}
    files=sorted(p for p in R.rglob('*.json') if p.name in names and not set(p.relative_to(R).parts)&{'raw','runs','results','locks','node_modules','tests'})
    out=[];bad=[]
    for file in files:
        raw=json.loads(file.read_text('utf-8-sig'))
        for item in nested(raw):
            hh=item.get('sha256');name=item.get('path') or item.get('snapshot') or item.get('local_path') or item.get('local') or item.get('file')
            if not isinstance(hh,str) or not re.fullmatch('[0-9a-fA-F]{64}',hh):continue
            anchor=str(item.get('id') or item.get('url') or str(name))[:180]
            if file.relative_to(R).as_posix()=='replication/manifest.json' and name:
                arc=Path(tempfile.gettempdir())/'esem2026-20442228-study.zip'
                if arc.is_file():
                    with zipfile.ZipFile(arc) as bundle, bundle.open(name) as member:
                        result=hashlib.file_digest(member,'sha256').hexdigest()
                    status='verified_archive_member' if result==hh else 'hash_mismatch'
                    if result!=hh:bad.append((file.relative_to(R).as_posix(),anchor,name))
                    out.append([file.relative_to(R).as_posix(),anchor,status,arc.name+'!/'+name,hh])
                    continue
            if not isinstance(name,str) or not name:
                out.append([file.relative_to(R).as_posix(),anchor,'no_declared_local_path','',hh]);continue
            target=Path(name)
            tries=[qp.resolve() for qp in [file.parent/target,file.parent/'raw'/target,P/target,R/target,P.parent/target]]
            # Local Wiki paths only; separately registered caches retain their own study-level checks.
            choices=list(dict.fromkeys(p for p in tries if p.is_relative_to(P) and p.is_file()))
            actual=next((p for p in choices if hashfile(p)==hh.lower()),None)
            status='verified' if actual else 'hash_mismatch' if choices else 'outside_or_missing'
            chosen=actual.relative_to(P).as_posix() if actual else name
            if status=='hash_mismatch':bad.append((file.relative_to(R).as_posix(),anchor,name))
            out.append([file.relative_to(R).as_posix(),anchor,status,chosen,hh])
    with (R/'state/snapshot-audit.tsv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['registry','id_or_url','result','path','declared_sha256']);w.writerows(out)
    report=dict(registries_scanned=len(files),declared_sha_rows=len(out),status=dict(Counter(x[2] for x in out)),unique_verified_paths=len({x[3] for x in out if x[2]=='verified'}),unique_verified_hashes=len({x[4] for x in out if x[2]=='verified'}),mismatches=bad)
    (R/'state/snapshot-summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),'utf8');print(str(report)[:1400]);assert not bad
if __name__=='__main__':audit()

