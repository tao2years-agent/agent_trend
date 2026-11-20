# Main research track instructions

This subtree contains the current organization-level software-engineering automation study. The canonical reader entry is `round2/index.md`; the canonical continuation state is `round2/state/checkpoint.md`.

## Routing

- Products and buyer claims: `round2/buyers/`, `buyer-audit/`, `product-code/`, `product-history/`.
- Auto Harness and self-improvement: `round2/optimizers/`, `optimizersrc/`, `pairing/`, `promotion-replay/`.
- Human supervision: `round2/supervision/`, `attention/`, `message-quality/`, `ownership/`.
- Gateway, tests, and evidence: `round2/gates/`, `oracles/`, `oracle-releases/`, `interoperability/`, `ci*/`.
- Organization metrics and sampling: `round2/devlake/`, `empirical/`, `cohorts/`, `selection-effect/`, `throughput/`.
- Academic coverage: `round2/venue-frame/`, `venue-review/`, `recall/`, `abstract-index/`, `papers/`, `labs/`.

Each study directory normally contains its protocol/method, structured data, immutable `raw/` evidence, a result page, and validation artifacts. Read those local files before changing a conclusion.

## Update rules

- The second-edition outputs are generated from fixed chapters plus structured evidence. Correct the chapter/fact source, then run `round2/publish.py` and `round2/verify.py`.
- Keep the first-edition material for historical traceability. Do not rewrite old evidence to make it agree with later conclusions.
- A benchmark improvement is not a production outcome. Record model, harness, budget, split, oracle, exclusions, and whether the result is reproduced locally.
- For product direction, explicitly separate existing product behavior, research inference, proposed product architecture, and untested hypothesis.
- For organization-level claims, retain all eligible tasks in the denominator, including failure, timeout, abandonment, and human takeover.
- For human supervision and gateway work, record the exact action, scope, approval binding, side effect, evidence, and resume/rollback behavior.

## Validation

From this directory, use the build commands in `README.md`. From `round2/`, run `python -X utf8 verify.py`. Do not update recorded audit output by hand.

