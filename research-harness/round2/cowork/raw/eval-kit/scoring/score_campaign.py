#!/usr/bin/env python3
"""Score one or more Claude-harness campaign roots.

usage: score_campaign.py ROOT [ROOT ...] [--exclude-rows 72,85] [--json out.json]

Each ROOT is a campaign directory created by `harness.py prepare` (it contains jobs/NNN-cowork/STATUS.json).
When several roots hold the same row (reruns, migrated hosts), a valid result wins over an invalid one and a later
root wins over an earlier one.

Validity rules (the ones used for the 2026-10-16 six-model campaign):
  ok            phase=finished and agent_end_reason in {completed, time_budget}
  ok            phase=finished, reason=cancelled and agent ran > 7 h (the 8 h budget expired during shutdown)
  ok            phase=finished, reason=agent_error caused by the model itself (registry_error / invalid protocol)
  agent_error   any other agent_error (provider/transport failure; rerun the row)
  <phase>       grading_error, environment_error, recovery_error, ... (infrastructure; rerun the row)
Placeholder jobs written by one-row sandboxes (assigned_elsewhere / migrated_inflight) are ignored.
"""
import argparse
import collections
import glob
import json
import os


def validity(status):
    phase, reason = status.get('phase'), status.get('agent_end_reason')
    elapsed = status.get('agent_elapsed_seconds') or 0
    if reason in ('assigned_elsewhere', 'migrated_inflight'):
        return None
    if phase == 'finished' and reason in ('completed', 'time_budget'):
        return 'ok'
    if phase == 'finished' and reason == 'cancelled' and elapsed > 7 * 3600:
        return 'ok'
    if phase == 'finished' and reason == 'agent_error':
        error = str(status.get('agent_error', ''))
        if 'registry_error' in error or 'Invalid Claude protocol' in error:
            return 'ok'
        return 'agent_error'
    return phase


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('roots', nargs='+')
    ap.add_argument('--exclude-rows', default='', help='rows to drop, e.g. runs whose colleague API was down')
    ap.add_argument('--json')
    args = ap.parse_args()
    excluded = {int(x) for x in args.exclude_rows.split(',') if x.strip()}
    best = {}
    for root in args.roots:
        for path in sorted(glob.glob(os.path.join(root, 'jobs', '*-cowork', 'STATUS.json'))):
            status = json.load(open(path))
            row = int(status['row'])
            v = validity(status)
            if v is None or row in excluded:
                continue
            model = status.get('model', '?')
            current = best.get((model, row))
            if current is None or current['valid'] != 'ok' or v == 'ok':
                best[(model, row)] = dict(valid=v, reward=status.get('reward'), root=root,
                                          reason=status.get('agent_end_reason'),
                                          elapsed=status.get('agent_elapsed_seconds'))
    print(f"{'model':24s} {'valid':>5s} {'pass':>4s} {'pass/valid':>10s} {'f2p':>6s} {'p2p':>6s}  issues")
    for model in sorted({m for m, _ in best}):
        rows = {r: x for (m, r), x in best.items() if m == model}
        ok = [x for x in rows.values() if x['valid'] == 'ok' and isinstance(x['reward'], dict)]
        passes = sum(1 for x in ok if float(x['reward'].get('reward') or 0) >= 1)
        f2p = [x['reward']['f2p_passed'] / x['reward']['f2p_total'] for x in ok if x['reward'].get('f2p_total')]
        p2p = [x['reward']['p2p_passed'] / x['reward']['p2p_total'] for x in ok if x['reward'].get('p2p_total')]
        issues = collections.Counter(x['valid'] for x in rows.values() if x['valid'] != 'ok')
        mean = lambda xs: sum(xs) / len(xs) if xs else 0
        print(f"{model:24s} {len(ok):5d} {passes:4d} {passes / max(1, len(ok)):10.1%} {mean(f2p):6.1%} {mean(p2p):6.1%}  {dict(issues)}")
    if args.json:
        json.dump({f'{m}:{r}': x for (m, r), x in best.items()}, open(args.json, 'w'), indent=1)


if __name__ == '__main__':
    main()
