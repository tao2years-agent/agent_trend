# Repository instructions

This repository is a maintainable research knowledge base, not a collection of one-off reports. Preserve evidence, stable IDs, time boundaries, contradictions, and research state so another agent can continue without reconstructing the project from chat history.

## Start here

1. Read [`README.md`](README.md) and [`INDEX.md`](INDEX.md).
2. For the current organization-level software-engineering automation study, read [`research-harness/AGENTS.md`](research-harness/AGENTS.md), [`research-harness/round2/index.md`](research-harness/round2/index.md), and [`research-harness/round2/state/checkpoint.md`](research-harness/round2/state/checkpoint.md).
3. For the earlier organization-context study, read [`org-context/AGENTS.md`](org-context/AGENTS.md).
4. Before changing generators or validators, read [`DEVELOPMENT.md`](DEVELOPMENT.md).

## Evidence discipline

- `raw/` directories are immutable source snapshots. Add a new dated or hashed snapshot; never silently replace an older one.
- `corpus/`, ledgers, TSV/CSV/JSON fact tables, and study-specific structured files are the source of truth. Fix claims there before regenerating reports.
- `wiki/` and `outputs/` are compiled views. Do not make an output-only correction that leaves its fact source inconsistent.
- Keep source facts, research inference, planning proposals, and open questions visibly distinct.
- Documentation, fixed-revision source inspection, local reproduction, and production/runtime evidence are different evidence levels. Never report an unrun experiment as verified.
- Preserve introduced/enhanced/defaulted/fixed/documented dates separately. Current documentation does not prove historical behavior.
- Record failures, timeouts, exclusions, abandoned cases, and missing evidence. Do not report only successful cases.
- Prefer primary sources and fixed revisions. Secondary sources may provide leads but must not carry central technical claims alone.

## Updating research

- Navigate from a study index rather than rereading every raw file.
- Update an existing entity or mechanism page when new evidence changes it; avoid creating disconnected summaries.
- Give new corpus entries stable IDs and retain previous versions.
- When a correction affects one case, audit the same failure mode across all cases and aggregate conclusions.
- Persist coverage, checkpoint, and append-only operation-log updates with every material research round.
- Run the relevant study validators and the repository-level checker before committing.

## Repository hygiene

- Large binary evidence is tracked with Git LFS according to `.gitattributes`.
- Do not commit credentials, authenticated exports containing private data, or local environment files.
- Public snapshots may contain documentation examples resembling credentials. Verify that they are source examples, not live secrets, before committing.
- Preserve third-party notices and source URLs. Repository publication does not relicense captured third-party material.
- Do not upload, publish, change repository visibility, or broaden access without explicit user authorization.

