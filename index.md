---
type: dashboard
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.90
quality_score: 0.90
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/projects/riemann-vault]]"
relationships:
  - target: "[[AGENTS]]"
    type: "depends-on"
    confidence: 0.95
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Riemann Vault Index

This vault is set up as a full v2 LLM wiki: raw sources, synthesized pages, typed entities, memory tiers, governance, templates, and audit logs.

## Start

- [[AGENTS]] - agent operating schema.
- [[dashboards/llm-wiki-dashboard]] - maintenance dashboard.
- [[governance/schema]] - page types, entity types, relationships, and frontmatter.
- [[governance/ingest-protocol]] - how to ingest sources.
- [[governance/query-protocol]] - how to answer and file durable knowledge.
- [[governance/lint-protocol]] - how to keep the vault healthy.

## Existing Notes

- [[llm-wiki]] - source note for this vault schema.
- [[Riemann Notes]] - exploratory notes about Riemann Hypothesis variants and related ideas.

## Synthesized Wiki Pages

- [[wiki/llm-wiki-v2]] - distilled description of the v2 wiki pattern.
- [[wiki/riemann-hypothesis-investigation-map]] - sourced map of RH research avenues and relevance to the current zero-spacing hypothesis.
- [[wiki/m23-proof-factory]] - research process for an AI-assisted M23 inverse Galois search.
- [[wiki/m23-verification-standard]] - phase-one local and external verification gates for M23 candidates.
- [[wiki/m23-known-boundary]] - seed facts and first group-boundary data for the M23 search.
- [[wiki/m23-search-loop]] - resumable candidate generation, verification, and ledger loop for M23 searches.
- [[wiki/m23-ledger-summary]] - failure-frequency summary for the M23 candidate ledger.
- [[wiki/m23-trinomial-minus20-20-report]] - durable interpretation of the completed `[-20,20]` trinomial batch.
- [[wiki/m23-literature-constraint-map]] - literature-derived constraints for the next M23 candidate generator.
- [[wiki/m23-elkies-finite-field-solver]] - bounded finite-field search scaffold for the Elkies-style M23 identity.
- [[wiki/m23-belyi-gf5-prefix-report]] - durable interpretation of the first constrained `GF(5)` Belyi prefix run.
- [[wiki/m23-belyi-gf5-normalized-500-report]] - durable interpretation of the larger normalized-first `GF(5)` Belyi run.
- [[wiki/m23-belyi-gf5-exhausted-report]] - exhaustion report for the constrained `GF(5)` Belyi search.
- [[wiki/m23-belyi-gf7-normalized-500-report]] - durable interpretation of the same normalized-first Belyi run over `GF(7)`.

## Active Project

- [[entities/projects/riemann-vault]] - this Obsidian vault as a knowledge project.
- [[entities/projects/m23-proof-factory]] - proof-factory project for the M23 inverse Galois problem.

## Bootstrapped Concepts

- [[entities/concepts/llm-wiki]]
- [[entities/concepts/knowledge-lifecycle]]
- [[entities/concepts/typed-knowledge-graph]]
- [[entities/concepts/hybrid-search]]
- [[entities/concepts/crystallization]]
- [[entities/concepts/riemann-hypothesis]]
- [[entities/concepts/zero-spacing-statistics]]
- [[entities/concepts/random-matrix-theory]]
- [[entities/concepts/hardy-z-function]]
- [[entities/concepts/hilbert-polya]]
- [[entities/concepts/explicit-formula]]
- [[entities/concepts/function-field-riemann-hypothesis]]
- [[entities/concepts/inverse-galois-problem]]
- [[entities/concepts/mathieu-group-m23]]
- [[entities/concepts/galois-candidate-search]]
- [[entities/concepts/galois-verification-pipeline]]
- [[entities/concepts/branch-cycle-class-vector]]
- [[entities/concepts/braid-orbit]]
- [[entities/concepts/belyi-map]]

## Decisions

- [[entities/decisions/full-v2-markdown-first-vault]]

## Memory

- [[memory/README]]
- [[memory/working/README]]
- [[memory/working/2026-05-20-riemann-hypothesis-exploratory-notes]]
- [[memory/episodic/README]]
- [[memory/semantic/README]]
- [[memory/procedural/README]]

## Sources

- [[sources/README]]
- Root source notes currently preserved in place:
  - [[llm-wiki]]
  - [[Riemann Notes]]

## Entities

- [[entities/README]]
- [[entities/concepts/README]]
- [[entities/projects/README]]
- [[entities/people/README]]
- [[entities/files/README]]
- [[entities/files/llm-wiki-md]]
- [[entities/files/riemann-notes-md]]
- [[entities/decisions/README]]

## Logs

- [[logs/README]]
- [[logs/ingest/README]]
- [[logs/ingest/2026-05-20-vault-bootstrap]]
- [[logs/ingest/2026-05-20-riemann-investigation-map]]
- [[logs/ingest/2026-05-22-m23-proof-factory-design]]
- [[logs/ingest/2026-05-22-m23-verification-harness-plan]]
- [[logs/ingest/2026-05-22-m23-search-loop]]
- [[logs/ingest/2026-05-22-m23-literature-constraints]]
- [[logs/ingest/2026-05-22-git-initialization]]
- [[logs/ingest/2026-05-22-m23-belyi-normalized-search]]
- [[logs/ingest/2026-05-22-m23-belyi-gf7-comparison]]
- [[logs/ingest/2026-05-22-m23-belyi-resumable-search]]
- [[logs/ingest/2026-05-22-m23-belyi-gf5-32000]]
- [[logs/ingest/2026-05-22-m23-local-batch-runner]]
- [[logs/ingest/2026-05-22-m23-belyi-gf5-exhausted]]
- [[logs/ingest/2026-05-22-m23-runner-progress]]
- [[logs/query/README]]
- [[logs/lint/README]]

## Templates

- [[templates/README]]
- [[templates/source]]
- [[templates/wiki-page]]
- [[templates/entity]]
- [[templates/decision]]
- [[templates/ingest-log]]
- [[templates/query-log]]
- [[templates/lint-log]]

## Governance

- [[governance/lifecycle-policy]]
- [[governance/privacy-and-governance]]
- [[governance/schema]]
- [[governance/ingest-protocol]]
- [[governance/query-protocol]]
- [[governance/lint-protocol]]

## Maintenance Rhythm

- On new source: run the ingest protocol.
- On substantial question: run the query protocol.
- Weekly or after several changes: run the lint protocol.
- Monthly: review pages past `review_after`.
