---
type: ingest-log
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.86
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-timeout-branch-review-runner]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-timeout-branch-review-runner]]"
    type: "supports"
    confidence: 0.90
    note: "Records the new focused timeout branch review runner."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# Ingest Log: M23 Belyi Timeout Branch Review Runner

## Actions

- Added `m23verify.timeout_review` for extracting unique timeout prefixes and classifying targeted reviews.
- Added `experiments/m23/scripts/review_timeout_branches.py` for rechecking quarantined Groebner timeout branches with a longer timeout.
- Added tests for timeout-prefix extraction and review classification.
- Recorded the recommended local command for the three min16 timeout branches.

## Privacy

No sensitive material was copied into the synthesized page.

## Follow-Up

Run the timeout review with `--groebner-timeout-seconds 600` and ingest the resulting report.
