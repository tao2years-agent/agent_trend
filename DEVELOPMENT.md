# Development and maintenance index

## Layout

| Path | Role | Edit policy |
|---|---|---|
| `raw/`, `*/raw/` | Immutable captured evidence | Add snapshots; do not overwrite history |
| `corpus/`, ledgers, structured study files | Stable IDs, screening decisions, fact data | Primary edit surface |
| `wiki/`, `*/wiki/` | Navigable knowledge pages | Update with source facts and cross-links |
| `outputs/`, `*/outputs/` | Generated/shareable reports | Regenerate from the same fact sources |
| `state/`, `*/state/` | Checkpoints, coverage, audits, logs | Update every material round |
| `research/`, `*/research/` | Protocols and synthesis | Separate inference from source fact |
| `scripts/`, `*/scripts/` | Ingest, build, and verification | Keep deterministic and offline where possible |

## Environment

- Python 3.11+ is recommended.
- Use UTF-8 mode on Windows: `python -X utf8 ...`.
- Clone binary evidence with Git LFS: `git lfs install` and `git lfs pull`.
- Some report/render validators require BeautifulSoup, Markdown, ReportLab, Chromium/Chrome, and Poppler. Study READMEs document their exact scope.

## Fast validation

From the repository root:

```powershell
python -X utf8 scripts/check_repository.py
python -X utf8 scripts/lint_research.py
```

The repository checker validates stable entry points and their local navigation. The legacy research lint validates first-party research pages but intentionally skips immutable, partial third-party snapshots under `raw/`; upstream-relative links in those captures are evidence, not repository navigation.

For the current main study:

```powershell
Set-Location research-harness/round2
python -X utf8 verify.py
```

`verify.py` checks fixed denominators, structured evidence, hashes, study-specific experiments, generated readers, and local links. It writes the current strict audit to `research-harness/round2/state/final-audit.json`.

## Rebuilding the current main report

Read [`research-harness/README.md`](research-harness/README.md) and [`research-harness/round2/protocol.md`](research-harness/round2/protocol.md) before rebuilding. The relevant entry points are:

```powershell
Set-Location research-harness
python -X utf8 scripts/build.py
python -X utf8 scripts/share_pdf.py
python -X utf8 scripts/check_reader.py
python -X utf8 scripts/audit.py

Set-Location round2
python -X utf8 publish.py
python -X utf8 check_reader.py
python -X utf8 verify.py
```

Do not treat successful generation as visual verification. Keep the existing desktop/mobile/offline render checks when changing shareable HTML or PDF.

## Adding a research increment

1. Read the applicable `AGENTS.md`, index, protocol, checkpoint, and coverage file.
2. Create new immutable source snapshots with acquisition time, source URL, version/revision, and hash.
3. Update the structured ledger or fact source using stable IDs.
4. Update entity/topic pages and cross-links; record contradictions and superseded claims.
5. Regenerate reports from the shared fact source.
6. Run study validators and `scripts/check_repository.py`.
7. Update checkpoint, coverage, and operation log in the same commit.

## Commit conventions

- `research(scope): ...` for evidence and synthesis changes.
- `data(scope): ...` for ledgers or snapshots.
- `docs(scope): ...` for navigation and method documentation.
- `build(scope): ...` for generators and validation tooling.

Keep a research round internally consistent: fact source, Wiki, output, checkpoint, and audit should not describe different states.

