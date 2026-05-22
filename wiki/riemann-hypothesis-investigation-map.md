---
type: wiki-page
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.74
quality_score: 0.86
sensitivity: internal
sources:
  - "[[Riemann Notes]]"
  - "[[llm-wiki]]"
entities:
  - "[[entities/concepts/riemann-hypothesis]]"
  - "[[entities/concepts/zero-spacing-statistics]]"
  - "[[entities/concepts/random-matrix-theory]]"
  - "[[entities/concepts/hardy-z-function]]"
  - "[[entities/concepts/hilbert-polya]]"
  - "[[entities/concepts/explicit-formula]]"
  - "[[entities/concepts/function-field-riemann-hypothesis]]"
relationships:
  - target: "[[memory/working/2026-05-20-riemann-hypothesis-exploratory-notes]]"
    type: "supports"
    confidence: 0.82
  - target: "[[entities/concepts/zero-spacing-statistics]]"
    type: "uses"
    confidence: 0.88
  - target: "[[entities/concepts/random-matrix-theory]]"
    type: "depends-on"
    confidence: 0.80
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Riemann Hypothesis Investigation Map

## Summary

There does not appear to be a single clean repository that says, for the Riemann Hypothesis, "these are all the avenues tried, these failed here, these remain open." The closest substitutes are official problem descriptions, survey papers, books of equivalent criteria, focused zero-statistics literature, and scattered bibliographies.

For the current vault hypothesis, the important finding is this: the broad path of studying gaps, gaps-between-gaps, correlations, and random-matrix shadows has already been heavily investigated. It should not be treated as untouched. The useful research path is to reproduce the known terrain, then look for residual structure only after subtracting known baselines.

## Status Legend

- **Canonical background**: foundational material needed before asking new questions.
- **Active mainstream**: serious research area with established literature.
- **Partly resolved analogue**: solved in a related mathematical world, not in classical RH.
- **Equivalent lens**: reformulation of RH, useful but not automatically easier.
- **Computationally explored**: tested at large finite ranges; not a proof.
- **Speculative or advanced**: plausible-looking but needs expert filtering.

## 1. Classical Zeta, Xi, and the Prime-Zero Link

**Status:** canonical background.

**What it is:** The classical Riemann zeta function starts as a Dirichlet series, has an Euler product over primes in its convergence region, and extends by analytic continuation. The RH asks whether all nontrivial zeros lie on the line `Re(s)=1/2`.

**What it explains:** This is the source of the prime-zero duality. The Euler product ties zeta to primes; analytic continuation and the functional equation make zeros meaningful.

**What it does not explain:** It does not by itself explain why all nontrivial zeros should lie on the critical line.

**Blocker:** Need global control of zeros in the critical strip, not only numerical evidence or local statistics.

**Relevance to this vault:** Foundation. Any alternative "real" or signal-like formulation has to preserve this structure or it stops being about the classical RH.

**Key sources:**

- [Clay Mathematics Institute: Riemann Hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/)
- [DLMF 25.2: Riemann zeta definition, analytic continuation, Euler product](https://dlmf.nist.gov/25.2)
- [Bombieri, official Clay problem description](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf)

## 2. Real-Valued Critical-Line Observables

**Status:** canonical background and computational tool.

**What it is:** Hardy's or Riemann-Siegel's `Z(t)` is a real-valued function for real `t`. Its zeros correspond to zeta zeros on the critical line.

**What it explains:** This directly supports the user's instinct that a real signal can be studied. The complex formulation remains useful, but the critical-line computation can be made real-valued.

**What it does not explain:** Zeros of `Z(t)` only certify zeros on the line. To prove RH, one must also know that no zeros exist off the line, usually by comparing sign changes against a zero-counting formula.

**Blocker:** Real-valued critical-line analysis is not enough by itself; it must be paired with global zero counting.

**Relevance to this vault:** High. This is the natural home for the "real signal" version of the investigation.

**Key sources:**

- [DLMF 25.10: zeros and real-valued `Z(t)`](https://dlmf.nist.gov/25.10)
- [LMFDB knowledge note on the Z-function](https://www.lmfdb.org/knowledge/show/lfunction.zfunction)

## 3. Zero Spacing, Pair Correlation, and GUE

**Status:** active mainstream.

**What it is:** Study the normalized spacings between adjacent zeros and correlations between pairs of zeros. Montgomery's pair-correlation conjecture and Odlyzko's computations connect zeta zeros to the Gaussian Unitary Ensemble from random matrix theory.

**What it explains:** It explains why zeta zeros look like eigenvalues of large random Hermitian matrices. It also explains why simple visual pattern hunting is dangerous: a lot of structure is already predicted by random matrix baselines.

**What it does not explain:** These statistics do not prove RH. Much of the strongest theory is asymptotic, conditional, or restricted by test-function support.

**Blocker:** Translating statistical agreement into a proof about every zero is a major unresolved gap.

**Relevance to this vault:** Highest. This is the direct ancestor of "gaps between zeros" and "hidden periodicity."

**Key sources:**

- [Montgomery, pair correlation of zeros](https://www-personal.umich.edu/~hlm/paircor1.pdf)
- [Odlyzko, distribution of spacings between zeros](https://www-users.cse.umn.edu/~odlyzko/doc/arch/zeta.zero.spacing.pdf)
- [Rudnick and Sarnak, zeros of principal L-functions and random matrix theory](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)

## 4. Gaps Between Gaps, Gap Ratios, and Higher-Order Correlations

**Status:** active mainstream, with recent work very close to the user's proposed direction.

**What it is:** Instead of only measuring adjacent gaps `g_n = gamma_{n+1}-gamma_n`, study consecutive gap pairs, gap ratios, triple correlations, and general `n`-level correlations.

**What it explains:** This is the rigorous version of "first, second, third derivative-like structure" in zero positions. It asks whether the sequence of gaps has secondary structure beyond ordinary spacing distributions.

**What is already tried:** Triple correlation, n-level correlation, joint distributions of consecutive spacings, gap-ratio distributions, finite-size corrections, and comparisons to CUE/GUE/sine-kernel predictions.

**Blocker:** Known random-matrix and sine-kernel corrections already explain a lot. Any candidate pattern must survive unfolding, baseline comparison, and finite-size correction.

**Relevance to this vault:** Very high. The next productive step is not to ask whether this path exists; it does. The next step is to reproduce known gap-ratio and consecutive-spacing results, then look for residuals.

**Key sources:**

- [Rudnick and Sarnak, n-level correlations in principal L-functions](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)
- [Distributions of consecutive level spacings and their ratio; finite-size corrections and Riemann zeta zeros](https://academic.oup.com/ptep/article/doi/10.1093/ptep/ptag006/8488783)

## 5. Random Matrix Theory and Quantum Chaos

**Status:** active mainstream.

**What it is:** Model zeta zero statistics using eigenvalues of random matrices, especially GUE/CUE. This overlaps with physics because spectra of quantum chaotic systems show similar statistics.

**What it explains:** It gives a baseline for pair correlations, level repulsion, spacing distributions, and spectral rigidity.

**What it does not explain:** Random matrix agreement is a statistical model, not an operator proof of RH.

**Blocker:** The missing bridge is an accepted self-adjoint operator or structural mechanism whose spectrum is exactly the zeta zeros.

**Relevance to this vault:** High. Any pattern-finding project must compare against random matrix predictions first.

**Key sources:**

- [Odlyzko spacing computations](https://www-users.cse.umn.edu/~odlyzko/doc/arch/zeta.zero.spacing.pdf)
- [Rudnick and Sarnak](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)
- [Katz and Sarnak, Random Matrices, Frobenius Eigenvalues, and Monodromy](https://www.ams.org/books/coll/045/)

## 6. Hilbert-Polya and Spectral Approaches

**Status:** active but unresolved.

**What it is:** Search for a self-adjoint operator whose eigenvalues correspond to the imaginary parts of nontrivial zeros. If such an operator is found with the right properties, RH would follow naturally.

**What it explains:** This fits the user's physics intuition: zeros as a spectrum rather than arbitrary complex roots.

**What it does not explain:** No accepted operator has been found that proves RH.

**Blocker:** Need a precise operator, a proof of self-adjointness, and an exact spectral correspondence.

**Relevance to this vault:** High conceptually, lower for immediate computation.

**Key sources:**

- [Lagarias survey: arithmetic, geometry, and spectral analogies](https://websites.umich.edu/~lagarias/doc/mt-holyoke-rev.pdf)
- [Connes, trace formula in noncommutative geometry and zeta zeros](https://arxiv.org/abs/math/9811068)

## 7. Function-Field and Finite-Field Analogues

**Status:** partly resolved analogue.

**What it is:** RH-like statements over finite fields are known in major cases. Weil proved the curve case; Deligne proved the Weil conjectures in broad generality.

**What it explains:** This is some of the strongest evidence that the "critical line" phenomenon reflects deep geometry, cohomology, and symmetry.

**What it does not explain:** The proof does not transfer directly to the classical number-field case.

**Blocker:** The classical integers do not currently have a directly analogous geometric/cohomological proof framework that completes RH.

**Relevance to this vault:** Medium-high. Useful for conceptual grounding and avoiding overly narrow complex-plane thinking.

**Key sources:**

- [Deligne, La conjecture de Weil I](https://publications.ias.edu/node/368)
- [Milne, The Riemann Hypothesis over Finite Fields](https://arxiv.org/abs/1509.00797)
- [Bombieri official Clay description, finite-field evidence section](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf)

## 8. L-Functions, Automorphic Forms, and Generalized RH

**Status:** active mainstream.

**What it is:** Riemann zeta is one member of a larger family of L-functions. Researchers study generalized RH, families of zeros, symmetry types, and automorphic L-functions.

**What it explains:** It reframes zeta as a special case. Some patterns are universal across primitive L-functions; other behaviors change when L-functions factor or belong to different families.

**What it does not explain:** Making the universe larger can clarify structure, but it does not make the classical proof simpler by default.

**Blocker:** Generalized RH is harder, not easier, unless a unifying mechanism appears.

**Relevance to this vault:** Medium. Helpful for checking whether a suspected pattern is zeta-specific or family-wide.

**Key sources:**

- [Rudnick and Sarnak](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)
- [Katz and Sarnak, AMS book page](https://www.ams.org/books/coll/045/)

## 9. Explicit Formula and Prime-Zero Duality

**Status:** canonical background and active tool.

**What it is:** Explicit formulas relate sums over zeros to sums over primes and prime powers. They are the mathematical bridge between zero statistics and prime distribution.

**What it explains:** Odlyzko explicitly notes that long-range correlations between zero spacings can be explained through primes using explicit formulas.

**What it does not explain:** The formula is a bridge, not a proof that all zeros are on the critical line.

**Blocker:** Need estimates strong enough to rule out every off-line zero.

**Relevance to this vault:** Very high. If a residual pattern appears in zero gaps, the first serious question is whether the explicit formula already predicts it from primes.

**Key sources:**

- [Odlyzko spacing paper](https://www-users.cse.umn.edu/~odlyzko/doc/arch/zeta.zero.spacing.pdf)
- [Rudnick and Sarnak explicit formula setup](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)

## 10. Equivalent Criteria

**Status:** equivalent lens.

**What it is:** RH has many equivalent formulations: Robin's inequality, Lagarias' elementary inequality, Li's criterion, Nyman-Beurling, Riesz-type criteria, prime-counting error bounds, and many more.

**What it explains:** These criteria show RH is not just a statement about complex zeros. It has arithmetic, analytic, functional-analytic, and computational faces.

**What it does not explain:** Equivalence does not mean easier. Many criteria translate the difficulty rather than remove it.

**Blocker:** Proving the equivalent statement usually requires strength comparable to proving RH itself.

**Relevance to this vault:** Medium. Useful for building the "avenues tried" map and for finding accessible computational side projects.

**Key sources:**

- [Lagarias, elementary problem equivalent to RH](https://arxiv.org/abs/math/0008177)
- [Robin's criterion overview in Ramanujan Journal article](https://link.springer.com/article/10.1007/s11139-022-00683-0)
- [MAA review of Broughan's two-volume Equivalents of RH](https://old.maa.org/press/maa-reviews/equivalents-of-the-riemann-hypothesis-volume-one-arithmetic-equivalents)

## 11. Computational Verification

**Status:** computationally explored.

**What it is:** Rigorous computation has checked very large finite regions for zeros and has provided high-precision datasets for statistical work.

**What it explains:** It gives strong evidence and data for pattern-finding, but not a proof for all heights.

**What it does not explain:** A finite height verification cannot rule out a counterexample above that height.

**Blocker:** Infinite problem; finite computation must be paired with proof techniques.

**Relevance to this vault:** High as a data source. Good for computational notebooks and sanity checks.

**Key sources:**

- [Platt and Trudgian, RH true up to height 3 x 10^12](https://arxiv.org/abs/2004.09765)
- [DLMF 25.10 zero computation notes](https://dlmf.nist.gov/25.10)
- [Odlyzko zero-spacing datasets and computations](https://www-users.cse.umn.edu/~odlyzko/doc/arch/zeta.zero.spacing.pdf)

## 12. de Bruijn-Newman Constant and Heat-Flow Deformation

**Status:** active mainstream; equivalent/near-equivalent lens.

**What it is:** Deform a function related to xi by a heat-flow parameter. RH is equivalent to one inequality for the de Bruijn-Newman constant. Rodgers and Tao proved the complementary lower bound, supporting Newman's idea that RH, if true, is "barely" true.

**What it explains:** This is a mathematically serious version of "stability under deformation." It may be closer to the user's original physical intuition than raw zero plotting.

**What it does not explain:** It still does not prove RH unless the remaining bound is shown.

**Blocker:** Need to close the exact value of the constant.

**Relevance to this vault:** Medium-high. Strong candidate for a later conceptual note.

**Key sources:**

- [Rodgers and Tao, de Bruijn-Newman constant is non-negative](https://arxiv.org/abs/1801.05914)

## 13. Noncommutative, Adelic, and p-adic Directions

**Status:** speculative or advanced.

**What it is:** These approaches change the mathematical setting: adeles, noncommutative geometry, p-adic zeta/L-functions, arithmetic schemes, and trace formulas.

**What it explains:** They answer the user's "other planes" question: yes, there are other mathematical worlds in which zeta-like objects are studied.

**What it does not explain:** They are not quick alternative coordinate systems for the same computational experiment. They require specialized background.

**Blocker:** High abstraction and no broadly accepted classical RH proof.

**Relevance to this vault:** Low for immediate computation, medium for conceptual map.

**Key sources:**

- [Connes, noncommutative geometry and zeta zeros](https://arxiv.org/abs/math/9811068)
- [Lagarias survey](https://websites.umich.edu/~lagarias/doc/mt-holyoke-rev.pdf)

## 14. Proposed Proofs and Failed Attempts

**Status:** scattered and noisy.

**What it is:** RH has many proposed proofs, most incorrect or unverified. There are lists, references, reviews, and folklore, but no definitive maintained public repository of every avenue tried and why it failed.

**What it explains:** The user's doubt is justified. The literature is not organized like an engineering postmortem database.

**Blocker:** Requires expert triage. Many papers use standard words such as "spectral," "operator," "quantum," or "prime transfer" without meeting the standards needed for RH.

**Relevance to this vault:** High as a governance rule: never treat an RH proof-like path as credible until it is reconciled with the known map.

**Key source:**

- [Conrey and Li on difficulty in a de Branges-style positivity approach](https://arxiv.org/abs/math/9812166)

## Direct Answer to the Current Hypothesis

The specific path "study gaps, gaps-between-gaps, correlations two or three levels deep, and hidden periodicity" has already been investigated in serious forms:

- Adjacent gaps and spacing distributions: yes.
- Pair correlation: yes.
- Triple and n-level correlations: yes.
- Consecutive gap pairs and gap ratios: yes, including recent finite-size correction studies.
- Residual deviations from random-matrix/sine-kernel baselines: yes, and still a reasonable computational learning target.

The productive version is:

> Reproduce known spacing and gap-ratio results, then inspect residuals after unfolding, random-matrix baseline subtraction, and finite-size correction.

## Research Path for This Vault

### Phase 1: Terrain Reproduction

- Build a small notebook around known zero data.
- Compute normalized gaps.
- Compute gap ratios and consecutive gap-pair histograms.
- Reproduce simple versions of known spacing plots.
- Compare against random or random-matrix baselines.

### Phase 2: Residual Search

- Subtract the expected sine-kernel or CUE/GUE baseline.
- Look at residuals across multiple heights.
- Use autocorrelation and FFT only after unfolding and detrending.
- Treat any periodic-looking feature as suspect until it survives baselines.

### Phase 3: Prime Link Check

- Ask whether any residual structure is already predicted by the explicit formula.
- Compare long-range spacing behavior against prime-related explanations in Odlyzko.
- File durable findings into wiki pages with confidence scores.

### Phase 4: Conceptual Branches

- Study de Bruijn-Newman as a stability/deformation lens.
- Study function-field analogues as the cleanest proved geometric model.
- Study Hilbert-Polya only after the zero-statistics baseline is understood.

## Avoid for Now

- Literal moving critical line for the classical zeta function.
- Raw Fourier transforms of unnormalized zero heights.
- Visual pattern claims without null models.
- Proof attempts that do not address functional equation, Euler product, explicit formula, and known zero statistics.

## Confidence Notes

This map is a first-pass research map, not an exhaustive bibliography. Confidence is moderate-high for the broad categories and low for claims about completeness. The map should evolve as the vault ingests more focused sources.
