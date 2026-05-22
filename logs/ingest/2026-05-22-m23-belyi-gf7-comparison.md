---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.82
quality_score: 0.84
sensitivity: internal
source: "M23 GF(7) normalized-first Belyi comparison"
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-normalized-500-report]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(7) Comparison Log

## Actions

- Ran a 50-triple normalized-first prefix search over `GF(7)`.
- Generated `experiments/m23/reports/2026-05-22-belyi-gf7-normalized-prefix.json`.
- Generated [[experiments/m23/reports/2026-05-22-belyi-gf7-normalized-prefix]].
- Ran a 500-triple normalized-first search over `GF(7)`.
- Generated `experiments/m23/reports/2026-05-22-belyi-gf7-normalized-500.json`.
- Generated [[experiments/m23/reports/2026-05-22-belyi-gf7-normalized-500]].
- Created [[wiki/m23-belyi-gf7-normalized-500-report]].
- Updated [[wiki/m23-elkies-finite-field-solver]], [[experiments/m23/README]], [[wiki/m23-belyi-gf5-normalized-500-report]], and [[index]].

## Result

- The 50-triple `GF(7)` probe generated 110 normalized triples, tested 50 coprime triples, scanned 300 lambda values, and found no solutions.
- The 500-triple `GF(7)` run generated 827 normalized triples, tested 500 coprime triples, scanned 3,000 lambda values, and found no solutions.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Run a smaller cross-prime grid to compare early rejection profiles.
- Add mathematical filters before square-divisor factorization if longer runs become too slow.
