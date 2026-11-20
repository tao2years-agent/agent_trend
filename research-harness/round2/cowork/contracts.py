"""Freeze the public per-task grading declarations; never run task code or print task content."""
from fetch import R,BASE,capture
from concurrent.futures import ThreadPoolExecutor
import json,collections
if __name__=='__main__':
    siblings=json.loads((R/'raw/release-files.json').read_bytes())['siblings']
    paths=[x['rfilename'] for x in siblings]
    inputs=[x for x in paths if x.startswith('release/tasks/') and x.endswith('/tests/config.json')]
    controls=['release/runtime/adapters/002_harbor_dynamic_colleague_adapter.py','eval-kit/scoring/campaign-20261016/coverage.py','eval-kit/scoring/campaign-20261016/collect.py','eval-kit/analysis/cowork-skill/references/definitions.md']
    with ThreadPoolExecutor(5) as ex:result=list(ex.map(capture,[(x,BASE+x) for x in inputs+controls]))
    (R/'contract-sources.json').write_text(json.dumps(result,indent=2),'utf8')
    schemas=collections.Counter()
    for i in inputs:
        d=json.loads((R/'raw'/i).read_bytes());schemas[tuple(sorted(d))]+=1
    print(len(inputs),schemas.most_common(5))

