---
type: wiki-page
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.84
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-timeout-review-result]]"
  - "[[wiki/m23-belyi-timeout-branch-review-runner]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-timeout-review-result]]"
    type: "depends-on"
    confidence: 0.90
    note: "The export runner is the escalation step after all timeout branches remained undecided under Sympy."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# M23 Belyi External Groebner Export Runner

## Summary

`experiments/m23/scripts/export_timeout_groebner_scripts.py` exports the six selected low-degree Groebner equations for each quarantined timeout branch. It writes Sage and Singular scripts so the same algebra can be checked by stronger Groebner engines outside Sympy.

The runner produces:

- A JSON export summary.
- One `.sage` script per timeout branch.
- One `.singular` script per timeout branch.

## Recommended Export

```powershell
.\.venv\Scripts\python experiments/m23/scripts/export_timeout_groebner_scripts.py --source-report experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.json --prime 7 --levels 13 --max-numerator 250000 --max-denominator 250000 --consistency-min-unique 16 --groebner-timeout-seconds 1 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --script-dir experiments/m23/reports/gf7-branch-search/external-groebner-timeouts --out experiments/m23/reports/gf7-branch-search/gf7-timeout-external-export-summary.json
```

The `--groebner-timeout-seconds 1` setting is intentional. The goal is to collect the equations selected for the Groebner check, not to solve them again in Sympy.

## Running The Exported Scripts

If Sage is installed:

```powershell
sage experiments/m23/reports/gf7-branch-search/external-groebner-timeouts/timeout-branch-01.sage
```

If Singular is installed:

```powershell
Singular experiments/m23/reports/gf7-branch-search/external-groebner-timeouts/timeout-branch-01.singular
```

Repeat for `timeout-branch-02` and `timeout-branch-03`.

## Interpretation

If an external Groebner basis contains `1`, that timeout branch is rejected. If an external system completes without `1`, the branch becomes a stronger survivor candidate for the next lift/search stage.
