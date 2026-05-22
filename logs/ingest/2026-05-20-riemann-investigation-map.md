---
type: ingest-log
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.76
quality_score: 0.84
sensitivity: internal
source: "web research and [[Riemann Notes]]"
sources:
  - "[[Riemann Notes]]"
  - "[[wiki/riemann-hypothesis-investigation-map]]"
entities:
  - "[[entities/concepts/riemann-hypothesis]]"
  - "[[entities/concepts/zero-spacing-statistics]]"
  - "[[entities/concepts/random-matrix-theory]]"
  - "[[entities/concepts/hardy-z-function]]"
  - "[[entities/concepts/hilbert-polya]]"
  - "[[entities/concepts/explicit-formula]]"
  - "[[entities/concepts/function-field-riemann-hypothesis]]"
relationships:
  - target: "[[wiki/riemann-hypothesis-investigation-map]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Riemann Investigation Map Ingest

## Source

- Local source: [[Riemann Notes]]
- Web sources: Clay, DLMF, Lagarias, Odlyzko, Rudnick-Sarnak, Deligne, Milne, Connes, Rodgers-Tao, Broughan/MAA, Platt-Trudgian, and a recent consecutive-gap-ratio paper.
- Sensitivity: internal

## Actions

- Created [[wiki/riemann-hypothesis-investigation-map]].
- Added concept entities for zero-spacing statistics, random matrix theory, Hardy Z, Hilbert-Polya, explicit formula, and function-field RH.
- Classified the user's zero-spacing hypothesis as already heavily investigated but still useful as a reproducible computational notebook path.

## Entities Created or Updated

- [[entities/concepts/zero-spacing-statistics]]
- [[entities/concepts/random-matrix-theory]]
- [[entities/concepts/hardy-z-function]]
- [[entities/concepts/hilbert-polya]]
- [[entities/concepts/explicit-formula]]
- [[entities/concepts/function-field-riemann-hypothesis]]

## Wiki Pages Created or Updated

- [[wiki/riemann-hypothesis-investigation-map]]
- [[index]]

## Privacy Filtering

No sensitive material was involved.

## Confidence and Quality Notes

The categories are reliable at a broad level, but this is not an exhaustive bibliography. The map should be revised as more focused sources are ingested.

## Follow-Up

- Build a computational notebook plan for normalized gaps, gap ratios, and residual analysis.
- Add dedicated notes for Montgomery pair correlation, Odlyzko computations, and the consecutive gap-ratio literature.
