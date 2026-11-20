"""Enumerate fixed revisions and ingest only selected raw files into the immutable ledger."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import sys
import tarfile
import tempfile
import time

import requests


BASE = pathlib.Path(__file__).resolve().parent
REFS = json.loads((BASE / 'refs.json').read_text(encoding='utf-8'))
CACHE = pathlib.Path(tempfile.gettempdir()) / 'harness-org-20261120'
CACHE.mkdir(exist_ok=True)


def archive(ref):
    dest = CACHE / (ref['sha'] + '.tgz')
    if not dest.exists():
        session = requests.Session()
        session.trust_env = False
        url = f"https://codeload.github.com/{ref['repo']}/tar.gz/{ref['sha']}"
        for attempt in range(6):
            try:
                with session.get(url, stream=True, timeout=(15, 50)) as response:
                    response.raise_for_status()
                    tmp = dest.with_suffix('.partial')
                    with tmp.open('wb') as out:
                        for data in response.iter_content(256 * 1024):
                            out.write(data)
                    tmp.replace(dest)
                break
            except requests.RequestException:
                if attempt == 5:
                    raise
                time.sleep(1)
    return dest


def process(ref):
    out = []
    with tarfile.open(archive(ref), 'r:gz') as handle:
        files = {member.name.split('/', 1)[1]: member for member in handle if member.isfile() and '/' in member.name}
        (CACHE / (ref['id'] + '.paths')).write_text('\n'.join(files), encoding='utf-8')
        if '--ingest' in sys.argv:
            selection = json.loads((BASE / 'selection.json').read_text(encoding='utf-8'))[ref['id']]
            for path in selection:
                raw = handle.extractfile(files[path]).read()
                digest = hashlib.sha256(raw).hexdigest()
                local = BASE / 'raw' / ref['id'] / ref['sha'] / path
                local.parent.mkdir(parents=True, exist_ok=True)
                if local.exists():
                    assert hashlib.sha256(local.read_bytes()).hexdigest() == digest
                else:
                    local.write_bytes(raw)
                out.append(dict(id=ref['id'], path=local.relative_to(BASE.parent.parent).as_posix(),
                                source_path=path, url=f"https://github.com/{ref['repo']}/blob/{ref['sha']}/{path}",
                                sha256=digest, commit=ref['sha'], size=len(raw)))
    print(ref['id'], len(files), len(out), flush=True)
    return out


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = [x for block in pool.map(process, REFS) for x in block]
    if records:
        manifest = BASE / 'raw' / 'manifest.json'
        if not manifest.exists():
            manifest.write_text(json.dumps(dict(retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                                files=records), indent=2), encoding='utf-8')
