---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.82
quality_score: 0.84
sensitivity: internal
source: "M23 normalized-first Belyi search"
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf5-normalized-500-report]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi Normalized Search Log

## Actions

- Added `normalized_first` support to the finite-field Belyi search API.
- Added the `--normalized-first` CLI flag.
- Added tests for the Python API and CLI behavior.
- Generated `experiments/m23/reports/2026-05-22-belyi-gf5-normalized-prefix.json`.
- Generated [[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-prefix]].
- Generated `experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.json`.
- Generated [[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500]].
- Created [[wiki/m23-belyi-gf5-normalized-500-report]].
- Updated [[wiki/m23-elkies-finite-field-solver]], [[experiments/m23/README]], and [[index]].

## Result

- The 50-triple normalized-first comparison generated 88 normalized triples, tested 50 coprime triples, scanned 200 lambda values, and found no solutions.
- The 500-triple normalized-first run generated 948 normalized triples, tested 500 coprime triples, scanned 2,000 lambda values, and found no solutions.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Test another small finite field with the same constraints.
- Encode additional branch-cycle restrictions before scaling to much larger runs.
