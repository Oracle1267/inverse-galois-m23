---
type: ingest-log
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.84
quality_score: 0.82
sensitivity: internal
source: "local timeout debugging of targeted Groebner6 min16 run"
sources:
  - "[[wiki/m23-belyi-consistency-scoring-runner]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# M23 Groebner Timeout Quarantine Ingest

## Source

- Source: interrupted local `gf7-targeted-groebner6-consistency-min16` run and traceback.
- Source kind: local debugging evidence.
- Sensitivity: internal.

## Actions

- Confirmed the repeated stall was inside SymPy's Groebner basis computation.
- Added timeout-worker handling for six-equation Groebner checks.
- Penalized Groebner timeouts in beam scoring while recording timed-out candidates for later review.
- Added per-candidate refine-start progress output so future stalls identify the exact prefix.

## Privacy Filtering

- No private or credential-like content was included. The traceback and process information were used only to identify the local mathematical bottleneck.

## Follow-Up

- Resume the min16 targeted run with `M23_GROEBNER_TIMEOUT_SECONDS` set.
