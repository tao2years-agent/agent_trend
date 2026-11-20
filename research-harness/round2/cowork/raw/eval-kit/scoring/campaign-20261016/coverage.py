#!/usr/bin/env python3
"""Colleague fact coverage for Claude Code CoWork runs.

Reuses the shared scorer (eval-kit common/fact_coverage.py, also used by the Codex harness);
only the "messages returned to the solver" extraction is adapted from Codex
app-server frames to Claude stream-json (assistant tool_use -> user tool_result).
Inputs per run: jobs/NNN-cowork/{STATUS.json, sidecar-events/, attempts/*/trajectory.jsonl}
inside a result tarball, plus the knowledge packs extracted from the workplace image.
Writes coverage.json (per run) and prints per-model aggregates for merged.json 'ok' runs.
"""
import json, os, sys, tarfile, io
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

# Shared eval-kit scorer (common/fact_coverage.py, also used by the Codex harness).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common'))
from fact_coverage import score_task_coverage, _parse_time  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PACKS = f'{HERE}/packs'
B = '/leixinping/cowork_runs/20261016-model-eval/backup'
P = '/leixinping/cowork_runs/20261016-model-eval/p1/results'
SRCDIR = {'p1': None, 'final-1900': None}
MESSAGE_TOOLS = {'chat_send', 'chat_fetch', 'chat_search', 'chat_check_updates'}


def message_objects(value):
    if isinstance(value, dict):
        if value.get('id') and isinstance(value.get('text'), str) and value.get('author_id'):
            yield value
        for child in value.values():
            yield from message_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from message_objects(child)


def exposure(lines):
    """Successful chat-tool results -> message ids returned to the solver."""
    names, out, seen = {}, [], set()
    for raw in lines:
        try:
            rec = json.loads(raw)
        except ValueError:
            continue
        msg = rec.get('message') if isinstance(rec, dict) else None
        if not isinstance(msg, dict):
            continue
        for block in msg.get('content') or []:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use':
                names[block.get('id')] = block.get('name', '')
            elif block.get('type') == 'tool_result' and not block.get('is_error'):
                tool = names.get(block.get('tool_use_id'), '')
                if tool.rsplit('__', 1)[-1] not in MESSAGE_TOOLS:
                    continue
                content = block.get('content')
                texts = [content] if isinstance(content, str) else [c.get('text') for c in content or [] if isinstance(c, dict)]
                for t in texts:
                    try:
                        val = json.loads(t)
                    except (TypeError, ValueError):
                        continue
                    if isinstance(val, dict) and val.get('isError'):
                        continue
                    for m in message_objects(val):
                        mid = str(m['id']).strip()
                        if mid and mid not in seen:
                            seen.add(mid); out.append({'message_id': mid, 'tool': tool, 'at': rec.get('timestamp')})
    return out


def run_one(args):
    key, tgz, slug, row = args
    pre = f'{slug}/jobs/{row:03d}-cowork/'
    events, lines, status, index = [], [], {}, None
    with tarfile.open(tgz) as t:
        for m in t:
            if not m.name.startswith(pre) or not m.isfile():
                continue
            rel = m.name[len(pre):]
            if rel == 'STATUS.json':
                status = json.load(t.extractfile(m))
            elif rel == 'sidecar-events/INDEX.json':
                index = json.load(t.extractfile(m))
            elif rel.startswith('sidecar-events/') and rel.endswith('-colleague-model-events.jsonl'):
                for l in t.extractfile(m).read().decode('utf-8', 'replace').splitlines():
                    try:
                        events.append(json.loads(l))
                    except ValueError:
                        pass
            elif rel.startswith('attempts/') and rel.endswith('/trajectory.jsonl'):
                lines += t.extractfile(m).read().decode('utf-8', 'replace').splitlines()
    started = status.get('agent_started_at') or status.get('started_at')
    finished = status.get('agent_finished_at') or status.get('finished_at') or status.get('updated_at')
    # The Claude harness runs one `find /run /tmp /workspace ...`; it exits 1 when one of those roots is
    # absent even though the colleague ledger was found and copied with `docker cp`. Treat the ledger as
    # complete when the colleague events file is listed in INDEX and present in the job directory.
    sidecar_complete = bool(index) and any(p.endswith('colleague-model-events.jsonl') for p in index.get('event_files', [])) and bool(events)
    res = score_task_coverage(f'{PACKS}/{row:03d}', events if events else None, exposure(lines) if lines else None,
                              started_at=started, finished_at=finished, sidecar_complete=sidecar_complete,
                              sidecar_scope_known=_parse_time(started) is not None and _parse_time(finished) is not None,
                              exposure_complete=bool(lines))
    keep = ('status', 'reason', 'colleague_fact_total', 'colleague_fact_disclosed', 'colleague_fact_retrieved',
            'colleague_fact_disclosure_coverage', 'colleague_fact_retrieval_coverage')
    return key, {k: res.get(k) for k in keep}


def source_tgz(slug, row, src):
    if src == 'p1':
        return f'{P}/{slug}/{row:03d}/r.tgz'
    import glob
    hits = sorted(glob.glob(f'{B}/*/{src}/r.tgz'))
    return hits[-1] if hits else None


def main():
    merged = json.load(open(f'{HERE}/merged.json'))
    jobs = []
    for key, x in merged.items():
        if x['v'] != 'ok':
            continue
        slug, row = key.split(':'); row = int(row)
        tgz = source_tgz(slug, row, x['src'])
        if tgz:
            jobs.append((key, tgz, slug, row))
    out = {}
    with ProcessPoolExecutor(12) as ex:
        for key, res in ex.map(run_one, jobs, chunksize=2):
            out[key] = res
    json.dump(out, open(f'{HERE}/coverage.json', 'w'), indent=0)
    agg = defaultdict(lambda: {'n': 0, 'obs': 0, 'disc': [], 'retr': [], 'tot': 0, 'got': 0})
    for key, r in out.items():
        a = agg[key.split(':')[0]]; a['n'] += 1
        if r['status'] == 'observable':
            a['obs'] += 1
            a['retr'].append(r['colleague_fact_retrieval_coverage'] or 0)
            a['disc'].append(r['colleague_fact_disclosure_coverage'] or 0)
            a['tot'] += r['colleague_fact_total'] or 0; a['got'] += r['colleague_fact_retrieved'] or 0
    reasons = defaultdict(lambda: defaultdict(int))
    for key, r in out.items():
        if r['status'] != 'observable':
            reasons[key.split(':')[0]][r.get('reason')] += 1
    for s, a in sorted(agg.items(), key=lambda kv: -sum(kv[1]['retr']) / max(1, len(kv[1]['retr']))):
        print(f"{s:22s} runs={a['n']:3d} observed={a['obs']:3d} retrieval_avg={sum(a['retr'])/max(1,len(a['retr'])):6.1%} "
              f"retrieval_pooled={a['got']/max(1,a['tot']):6.1%} disclosure_avg={sum(a['disc'])/max(1,len(a['disc'])):6.1%}  "
              f"unobserved={dict(reasons[s])}")


if __name__ == '__main__':
    main()
