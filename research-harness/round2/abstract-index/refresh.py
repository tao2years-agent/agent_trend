"""Append an optional re-observation of an existing conference entry without rewriting the frozen corpus."""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path
from bs4 import BeautifulSoup

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent / 'venue-review'))
import fetch

def digest(value):
    return hashlib.sha256(value).hexdigest()

def fields(source):
    modal = next(v['value'] for v in json.loads(source) if v['action']=='append')
    soup = BeautifulSoup(modal, 'html.parser')
    heading = soup.select_one('.event-title h4 strong') or soup.select_one('.event-title h4')
    summary = soup.select_one('.event-description')
    title = ' '.join(heading.stripped_strings)
    abstract = ' '.join(p.get_text(' ',strip=True) for p in summary.select(':scope > p') if p.get_text(strip=True))
    return {'title':title,'abstract':abstract}

def inspect_current(reference, row):
    prior = (R/reference['path']).read_bytes()
    assert digest(prior) == reference['sha256']
    with tempfile.TemporaryDirectory(prefix='program-observe-') as scratch:
        fetch.BASE = Path(scratch)
        source = fetch.capturepaper(row,{row['venue']:fetch.getform(row['venue'])})
        payload = (fetch.BASE/source['path']).read_bytes()
    before, after = fields(prior), fields(payload)
    assert before['abstract'] and after['abstract'] and source['id']==reference['id']
    key = digest(payload)
    base = R / 'history' / row['id']
    base.mkdir(parents=True,exist_ok=True)
    immutable = base / (key+'.json')
    with tempfile.NamedTemporaryFile(dir=base,delete=False) as tmp:
        tmp.write(payload)
    try:
        try:
            os.link(tmp.name,immutable)
        except FileExistsError:
            assert digest(immutable.read_bytes())==key
    finally:
        Path(tmp.name).unlink()
    now = dt.datetime.now(dt.timezone.utc)
    changes = [field for field in before if before[field]!=after[field]]
    record = {'uuid':row['id'],'venue':row['venue'],'url':source['url'],'observed_utc':now.isoformat(),
        'frozen_path':reference['path'],'frozen_sha256':digest(prior),
        'new_path':immutable.relative_to(R).as_posix(),'new_sha256':key,'changed_fields':changes,
        'action':'reopen factual review' if changes else 'retain factual review',
        'scope':'title and author abstract; byte-only page churn does not alter decisions automatically'}
    obs = base / (now.strftime('%Y%m%dT%H%M%S%fZ')+'-'+uuid.uuid4().hex[:8]+'.observation.json')
    with obs.open('x',encoding='utf8') as out:
        json.dump(record,out,ensure_ascii=False,indent=2)
    print(json.dumps(record,ensure_ascii=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('uuid',nargs='+')
    args=ap.parse_args()
    original={x['id']:x for x in map(json.loads,(R/'abstracts.jsonl').read_text('utf8').splitlines())}
    frame={x['id']:x for x in fetch.readframe()}
    for key in dict.fromkeys(args.uuid):
        inspect_current(original[key],frame[key])

