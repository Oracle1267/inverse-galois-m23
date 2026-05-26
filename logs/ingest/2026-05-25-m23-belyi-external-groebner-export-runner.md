---
type: ingest-log
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.84
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-external-groebner-export-runner]]"
  - "[[wiki/m23-belyi-gf7-timeout-review-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-external-groebner-export-runner]]"
    type: "supports"
    confidence: 0.90
    note: "Records the runner that exports timeout-branch equations for Sage/Singular."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# Ingest Log: M23 Belyi External Groebner Export Runner

## Actions

- Added a script to export timeout-branch Groebner equations to Sage and Singular.
- Added tests for external script rendering and symbol-name normalization.
- Recorded the recommended export command and external execution commands.

## Privacy

No sensitive material was copied into the synthesized page.

## Follow-Up

Run the export command, then run the generated scripts in Sage or Singular if available.
