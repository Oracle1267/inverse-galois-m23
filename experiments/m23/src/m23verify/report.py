from __future__ import annotations

from typing import Iterable

from .group_data import M23CycleData
from .polynomial import factor_degrees_mod_prime, parse_polynomial, summarize_polynomial


def _classification(reasons: list[str], incompatible_good_primes: int) -> str:
    if reasons:
        return "reject"
    if incompatible_good_primes:
        return "reject"
    return "needs_external_group_verification"


def build_report(
    poly_text: str,
    primes: Iterable[int],
    cycle_data: M23CycleData,
    coefficient_bound_digits: int = 99,
) -> dict:
    poly = parse_polynomial(poly_text)
    summary = summarize_polynomial(poly_text, bound_digits=coefficient_bound_digits)

    reasons: list[str] = []
    if summary.degree != cycle_data.degree:
        reasons.append(f"degree is {summary.degree}, expected {cycle_data.degree}")
    if not summary.coefficient_bound.ok:
        reasons.append(
            f"maximum coefficient has {summary.coefficient_bound.max_digits} digits, "
            f"expected at most {summary.coefficient_bound.bound_digits}"
        )
    if not summary.is_irreducible:
        reasons.append("polynomial is reducible over Q")
    if summary.discriminant == 0:
        reasons.append("polynomial has zero discriminant")

    modular_factorizations = []
    incompatible_good_primes = 0
    for prime in primes:
        factorization = factor_degrees_mod_prime(poly, int(prime))
        compatible = cycle_data.is_allowed(factorization.cycle_type)
        if factorization.is_good_prime and not compatible:
            incompatible_good_primes += 1
        modular_factorizations.append(
            {
                "prime": factorization.prime,
                "cycle_type": list(factorization.cycle_type),
                "is_good_prime": factorization.is_good_prime,
                "reason": factorization.reason,
                "m23_compatible": compatible,
            }
        )

    if incompatible_good_primes:
        reasons.append(f"{incompatible_good_primes} good primes have cycle types not present in M23")

    return {
        "candidate": poly_text,
        "target": {
            "group_label": cycle_data.group_label,
            "group_name": cycle_data.group_name,
            "degree": cycle_data.degree,
            "order": cycle_data.order,
        },
        "summary": {
            "degree": summary.degree,
            "coefficients": list(summary.coefficients),
            "max_coefficient_digits": summary.coefficient_bound.max_digits,
            "coefficient_digit_bound": summary.coefficient_bound.bound_digits,
            "is_irreducible": summary.is_irreducible,
            "discriminant": summary.discriminant,
        },
        "modular_factorizations": modular_factorizations,
        "classification": _classification(reasons, incompatible_good_primes),
        "reasons": reasons,
        "warning": (
            "This local report is a filter, not a proof. "
            "A surviving candidate still needs Magma/GAP group verification and a written subgroup-exclusion proof."
        ),
    }
