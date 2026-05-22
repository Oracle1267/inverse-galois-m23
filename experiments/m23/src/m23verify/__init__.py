"""Verification harness for M23 inverse Galois candidate polynomials."""

from .polynomial import (
    CoefficientBoundResult,
    ModularFactorization,
    PolynomialSummary,
    coefficient_digit_count,
    factor_degrees_mod_prime,
    parse_polynomial,
    summarize_polynomial,
)
from .belyi import (
    ElkiesIdentityFactors,
    derive_right_factorizations,
    elkies_derivative_residual,
    elkies_identity_residual,
    elkies_translation_normalization_residual,
    is_elkies_derivative_solution,
    is_elkies_identity_solution,
    is_elkies_translation_normalized,
    monic_polynomial,
    render_belyi_search_markdown,
    search_elkies_identity_mod_prime,
)
from .group_data import M23CycleData, load_m23_cycle_data
from .report import build_report
from .families import count_trinomial_candidates, generate_trinomial_candidates, parse_int_range
from .ledger import append_ledger_entry, entry_from_report, read_ledger, resolved_candidates, seen_candidates
from .search import run_search_batch
from .summary import render_markdown_report, summarize_ledger

__all__ = [
    "CoefficientBoundResult",
    "ElkiesIdentityFactors",
    "M23CycleData",
    "ModularFactorization",
    "PolynomialSummary",
    "build_report",
    "coefficient_digit_count",
    "count_trinomial_candidates",
    "append_ledger_entry",
    "entry_from_report",
    "derive_right_factorizations",
    "elkies_derivative_residual",
    "elkies_identity_residual",
    "elkies_translation_normalization_residual",
    "factor_degrees_mod_prime",
    "generate_trinomial_candidates",
    "is_elkies_identity_solution",
    "is_elkies_derivative_solution",
    "is_elkies_translation_normalized",
    "load_m23_cycle_data",
    "monic_polynomial",
    "parse_polynomial",
    "parse_int_range",
    "read_ledger",
    "resolved_candidates",
    "render_markdown_report",
    "render_belyi_search_markdown",
    "run_search_batch",
    "seen_candidates",
    "search_elkies_identity_mod_prime",
    "summarize_ledger",
    "summarize_polynomial",
]
