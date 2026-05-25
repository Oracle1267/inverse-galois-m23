---
type: wiki-page
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.86
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
  - "[[wiki/m23-belyi-gf7-clean-continuation-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
    type: "depends-on"
    confidence: 0.88
    note: "The runner rechecks Groebner timeout candidates recorded by the min16 rescore."
  - target: "[[wiki/m23-belyi-gf7-clean-continuation-result]]"
    type: "supports"
    confidence: 0.82
    note: "After the clean continuation weakened, timeout review became the narrower next branch."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# M23 Belyi Timeout Branch Review Runner

## Summary

`experiments/m23/scripts/review_timeout_branches.py` rechecks only the Groebner timeout branches recorded in a branch-search report. It extracts unique `timeout_candidates`, reruns their partial consistency check with a longer `M23_GROEBNER_TIMEOUT_SECONDS` value, and classifies each branch as:

- `reject`: a hard, linear, linear-system, linear-solution, or Groebner contradiction is found.
- `timeout`: the longer Groebner check still times out.
- `survivor`: no contradiction is found and the longer Groebner check completes.

## Recommended Run

```powershell
.\.venv\Scripts\python experiments/m23/scripts/review_timeout_branches.py --source-report experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.json --prime 7 --levels 13 --max-numerator 250000 --max-denominator 250000 --consistency-min-unique 16 --groebner-timeout-seconds 600 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-groebner-timeout-review-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-groebner-timeout-review-summary.md --title "M23 Belyi GF(7) Groebner Timeout Branch Review"
```

## Interpretation

This is a bounded uncertainty-clearing step, not a broad search. It answers whether the three quarantined branches are actual algebraic contradictions, still computationally hard, or clean survivors under a longer timeout.
