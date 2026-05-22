# M23 Trinomial [-20,20] Ledger Report

## Outcome

- Ledger: `C:\Projects\Riemann\experiments\m23\reports\candidate_ledger.jsonl`
- Entries: 1601
- Unique polynomials: 1600
- Superseded entries: 1
- Active survivors: 0

| latest classification | count |
| --- | --- |
| reject | 1600 |

## Generators

| generator | entries |
| --- | --- |
| escalation | 1 |
| trinomial | 1600 |

## Rejection Reasons

| reason | count |
| --- | --- |
| 3 good primes have cycle types not present in M23 | 692 |
| 4 good primes have cycle types not present in M23 | 436 |
| 2 good primes have cycle types not present in M23 | 331 |
| polynomial is reducible over Q | 78 |
| 5 good primes have cycle types not present in M23 | 74 |
| 1 good primes have cycle types not present in M23 | 60 |
| 7 good primes have cycle types not present in M23 | 1 |

## First Rejecting Good Primes

| prime | count |
| --- | --- |
| 5 | 554 |
| 3 | 420 |
| 2 | 400 |
| 7 | 190 |
| 11 | 30 |

## Incompatible Cycle Types

| prime | cycle type | count |
| --- | --- | --- |
| 2 | `[13, 8, 2]` | 400 |
| 3 | `[9, 7, 5, 2]` | 392 |
| 11 | `[22, 1]` | 360 |
| 11 | `[21, 2]` | 278 |
| 5 | `[15, 6, 2]` | 256 |
| 5 | `[22, 1]` | 256 |
| 5 | `[12, 6, 4, 1]` | 254 |
| 5 | `[16, 5, 2]` | 254 |
| 7 | `[10, 6, 6, 1]` | 210 |
| 7 | `[11, 8, 4]` | 210 |
| 7 | `[12, 7, 2, 1, 1]` | 210 |
| 7 | `[19, 2, 2]` | 206 |
| 7 | `[20, 3]` | 206 |
| 3 | `[10, 10, 2, 1]` | 168 |
| 7 | `[22, 1]` | 144 |
| 11 | `[15, 5, 2, 1]` | 144 |
| 11 | `[17, 3, 2, 1]` | 140 |
| 11 | `[20, 1, 1, 1]` | 140 |
| 11 | `[7, 7, 6, 3]` | 138 |
| 11 | `[19, 2, 1, 1]` | 138 |

## Active Survivors

- None.

## Interpretation

This report is a local-filter diagnosis. A rejection records an incompatibility observed by the current harness; a survivor would still require external Magma/GAP verification and a written subgroup-exclusion proof.
