"""Verify that publication and the evidence query survive a new directory and a disconnected reader."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[1]
project = R.parent

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(script, *args, cwd):
    result = subprocess.run([sys.executable, '-X', 'utf8', str(script), *args], cwd=cwd,
                            capture_output=True, encoding='utf8', errors='replace', timeout=300)
    if result.returncode:
        raise RuntimeError(result.stderr[-2500:] + result.stdout[-1000:])
    return result.stdout

with tempfile.TemporaryDirectory(prefix='rd-evidence-move-') as tmp:
    base = Path(tmp)
    dest = base / 'different-location' / 'research-copy'
    # Copy, never link mutable state. All source hashes and all output comparisons
    # below therefore refer to physically separate files.
    shutil.copytree(project, dest, ignore=shutil.ignore_patterns('__pycache__', '.git', '*.pyc',
        'deep-report-v2.html', 'insights-v2.html', 'insights-v2.pdf',
        'insights-decision.html', 'insights-decision.pdf', 'papers.sqlite',
        'readers.json', 'portable-rebuild.json', 'pdf-page-*.png', '*-v2-*.png'))
    moved = dest / 'round2'
    office = base / 'separate-working-directory'
    office.mkdir()
    index = json.loads(run(moved/'abstract-index/query.py','--build',cwd=office))
    lookup = run(moved/'abstract-index/query.py','handoff OR interruption','--limit','4',cwd=office)
    assert lookup.strip() and index['indexed'] == 1738
    run(moved/'publish.py',cwd=office)
    hashes = {}
    for name in ['deep-report-v2.html','insights-decision.html']:
        original = digest(project/'outputs'/name)
        new = digest(dest/'outputs'/name)
        hashes[name] = {'original':original,'relocated':new,'identical':original == new}
    run(moved/'check_reader.py',cwd=office)
    reader = json.loads((moved/'state/readers.json').read_bytes())
    assert not reader['js_errors'] and not reader['external_requests']
    assert reader['deep-report-v2-desktop']['embedded_download_verified'] and len(reader['pdf'])==4
    audit = dict(utc=datetime.now(timezone.utc).isoformat(),method='separate physical copy and cwd; regenerates HTML, PDF, SQLite, tests reader with Chromium network disabled',source_count=len(list(moved.rglob('*.py'))),
        hashes=hashes,verified_index_size=index['indexed'],query_returned_content=bool(lookup.strip()),
        reader_errors=reader['js_errors'],reader_external_requests=reader['external_requests'],
        pdf_pages=len(reader['pdf']),byte_equal_pdf_required=False,
        caveat='Same machine and installed Python and Chrome; proves path relocation and reading offline, not installation on a clean OS.')
    (R/'state/portable-rebuild.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),'utf8')
    assert all(row['identical'] for row in hashes.values()), hashes
    print(json.dumps(audit,ensure_ascii=False))

