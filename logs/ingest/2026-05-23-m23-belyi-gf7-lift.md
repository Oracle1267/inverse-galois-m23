---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.84
quality_score: 0.87
sensitivity: internal
source: "M23 GF(7) Belyi lift local run"
sources:
  - "[[wiki/m23-belyi-gf7-modular-survivor-report]]"
  - "[[experiments/m23/reports/gf7-lift/gf7-survivor-lift-mod117649]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-lift-report]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Lift Log

## Source

- Source: `experiments/m23/scripts/lift_belyi_survivor.py`
- Source kind: local lifting tool output.
- Sensitivity: internal.

## Actions

- Added a prime-power lifting helper for Elkies-style Belyi survivor data.
- Added a CLI for lifting stored modular survivors from JSON reports or explicit coefficient flags.
- Verified the trivial exact identity lifts through prime powers in automated tests.
- Lifted the `GF(7)` survivor to mod `49`, `343`, and `117649`.
- Created [[wiki/m23-belyi-gf7-lift-report]].
- Updated [[index]] and [[wiki/m23-elkies-finite-field-solver]].

## Result

- Highest completed lift: `7^6 = 117649`.
- Status: lifted.
- Correction steps: 5.
- Constraints per step: 48.
- Variables per step: 25.
- Rank per step: 24.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Try rational reconstruction or add a controlled normalization for the one free variable before attempting to derive the final degree-23 polynomial.

