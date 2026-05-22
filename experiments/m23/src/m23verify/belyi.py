from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator
import warnings

from sympy import Poly, factor_list, gcd
from sympy.utilities.exceptions import SymPyDeprecationWarning

from .polynomial import x


@dataclass(frozen=True)
class ElkiesIdentityFactors:
    p2: tuple[int, ...]
    p3: tuple[int, ...]
    p4: tuple[int, ...]
    p7: tuple[int, ...]
    p8: tuple[int, ...]
    lam: int


def monic_polynomial(degree: int, coefficients: Iterable[int], modulus: int) -> Poly:
    coeffs = tuple(int(coefficient) for coefficient in coefficients)
    if len(coeffs) != degree:
        raise ValueError(f"expected {degree} coefficients for a monic degree-{degree} polynomial")
    expr = x**degree
    for offset, coefficient in enumerate(coeffs):
        exponent = degree - offset - 1
        expr += coefficient * x**exponent
    return Poly(expr, x, modulus=modulus)


def _residual_coefficients(poly: Poly, modulus: int, degree: int = 23) -> tuple[int, ...]:
    raw = [0] * (degree + 1)
    for (exponent,), coefficient in poly.terms():
        if exponent <= degree:
            raw[degree - exponent] = int(coefficient) % modulus
    return tuple(raw)


def _nonleading_coefficients(poly: Poly, degree: int, modulus: int) -> tuple[int, ...]:
    coeffs = [int(coefficient) % modulus for coefficient in poly.all_coeffs()]
    coeffs = ([0] * (degree + 1 - len(coeffs))) + coeffs
    return tuple(coeffs[1:])


def _is_prime_candidate(value: int) -> bool:
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _coefficient_options(degree: int, modulus: int, fixed: Iterable[int] | None) -> list[tuple[int, ...]]:
    if fixed is not None:
        coeffs = tuple(int(item) % modulus for item in fixed)
        if len(coeffs) != degree:
            raise ValueError(f"expected {degree} fixed coefficients")
        return [coeffs]
    return [tuple(items) for items in product(range(modulus), repeat=degree)]


def _monic_divisors_from_factorization(factors: list[tuple[object, int]], modulus: int) -> Iterator[Poly]:
    divisors = [Poly(1, x, modulus=modulus)]
    for factor_expr, multiplicity in factors:
        factor = Poly(factor_expr, x, modulus=modulus)
        powers = [Poly(1, x, modulus=modulus)]
        for _ in range(int(multiplicity)):
            powers.append(powers[-1] * factor)
        divisors = [divisor * power for divisor in divisors for power in powers]
    yield from divisors


def _left_factors_are_coprime(p2: Poly, p3: Poly, p4: Poly) -> bool:
    factors = [p2, p3, p4]
    for left_index, left in enumerate(factors):
        for right in factors[left_index + 1 :]:
            if gcd(left, right).degree() > 0:
                return False
    return True


def _markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(row) + " |" for row in rows),
    ]


def elkies_identity_residual(factors: ElkiesIdentityFactors, modulus: int) -> tuple[int, ...]:
    p2 = monic_polynomial(2, factors.p2, modulus)
    p3 = monic_polynomial(3, factors.p3, modulus)
    p4 = monic_polynomial(4, factors.p4, modulus)
    p7 = monic_polynomial(7, factors.p7, modulus)
    p8 = monic_polynomial(8, factors.p8, modulus)

    left = p2**2 * p3 * p4**4
    right = p7 * p8**2 + factors.lam
    residual = Poly(left.as_expr() - right.as_expr(), x, modulus=modulus)
    return _residual_coefficients(residual, modulus=modulus, degree=23)


def is_elkies_identity_solution(factors: ElkiesIdentityFactors, modulus: int) -> bool:
    return all(coefficient == 0 for coefficient in elkies_identity_residual(factors, modulus=modulus))


def elkies_derivative_residual(factors: ElkiesIdentityFactors, modulus: int) -> tuple[int, ...]:
    if modulus == 23:
        raise ValueError("derivative normalization is singular in characteristic 23")
    p2 = monic_polynomial(2, factors.p2, modulus)
    p3 = monic_polynomial(3, factors.p3, modulus)
    p4 = monic_polynomial(4, factors.p4, modulus)
    p8 = monic_polynomial(8, factors.p8, modulus)

    left = p2**2 * p3 * p4**4
    derivative_target = (23 % modulus) * p2 * p4**3 * p8
    residual = Poly(left.diff().as_expr() - derivative_target.as_expr(), x, modulus=modulus)
    return _residual_coefficients(residual, modulus=modulus, degree=22)


def is_elkies_derivative_solution(factors: ElkiesIdentityFactors, modulus: int) -> bool:
    return all(coefficient == 0 for coefficient in elkies_derivative_residual(factors, modulus=modulus))


def elkies_translation_normalization_residual(factors: ElkiesIdentityFactors, modulus: int) -> int:
    if modulus == 23:
        raise ValueError("translation normalization is singular in characteristic 23")
    p2 = monic_polynomial(2, factors.p2, modulus)
    p3 = monic_polynomial(3, factors.p3, modulus)
    p4 = monic_polynomial(4, factors.p4, modulus)
    left = p2**2 * p3 * p4**4
    coefficients = _residual_coefficients(left, modulus=modulus, degree=23)
    return coefficients[1]


def is_elkies_translation_normalized(factors: ElkiesIdentityFactors, modulus: int) -> bool:
    return elkies_translation_normalization_residual(factors, modulus=modulus) == 0


def derive_right_factorizations(left_minus_lambda: Poly, modulus: int) -> Iterator[dict[str, tuple[int, ...]]]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SymPyDeprecationWarning)
        _, factors = factor_list(left_minus_lambda.as_expr(), x, modulus=modulus)
    for p8 in _monic_divisors_from_factorization(factors, modulus=modulus):
        if p8.degree() != 8:
            continue
        p7, remainder = divmod(left_minus_lambda, p8 * p8)
        if remainder.is_zero and p7.degree() == 7 and int(p7.LC()) % modulus == 1:
            yield {
                "p7": _nonleading_coefficients(p7, degree=7, modulus=modulus),
                "p8": _nonleading_coefficients(p8, degree=8, modulus=modulus),
            }


def search_elkies_identity_mod_prime(
    modulus: int,
    max_solutions: int = 10,
    max_left_factor_triples: int | None = None,
    require_coprime_left: bool = False,
    require_nonzero_lambda: bool = False,
    require_derivative: bool = False,
    require_translation_normalized: bool = False,
    coprime_first: bool = False,
    fixed_p2: Iterable[int] | None = None,
    fixed_p3: Iterable[int] | None = None,
    fixed_p4: Iterable[int] | None = None,
) -> dict:
    if not _is_prime_candidate(modulus):
        raise ValueError(f"modulus must be prime: {modulus}")
    if max_solutions < 0:
        raise ValueError("max_solutions must be nonnegative")
    if require_derivative and modulus == 23:
        raise ValueError("derivative constraint is singular in characteristic 23")
    if require_translation_normalized and modulus == 23:
        raise ValueError("translation normalization is singular in characteristic 23")

    p2_options = _coefficient_options(2, modulus, fixed_p2)
    p3_options = _coefficient_options(3, modulus, fixed_p3)
    p4_options = _coefficient_options(4, modulus, fixed_p4)
    lambda_values = range(1, modulus) if require_nonzero_lambda else range(modulus)
    search_options = {
        "max_solutions": max_solutions,
        "max_left_factor_triples": max_left_factor_triples,
        "require_coprime_left": require_coprime_left,
        "require_nonzero_lambda": require_nonzero_lambda,
        "require_derivative": require_derivative,
        "require_translation_normalized": require_translation_normalized,
        "coprime_first": coprime_first,
        "fixed_p2": list(fixed_p2) if fixed_p2 is not None else None,
        "fixed_p3": list(fixed_p3) if fixed_p3 is not None else None,
        "fixed_p4": list(fixed_p4) if fixed_p4 is not None else None,
    }

    def build_result(stopped_reason: str) -> dict:
        return {
            "modulus": modulus,
            "search_options": search_options,
            "enumerated_left_factor_triples": enumerated_left,
            "tested_left_factor_triples": tested_left,
            "skipped_left_factor_triples": skipped_left,
            "tested_lambda_values": tested_lambdas,
            "normalization_rejections": normalization_rejections,
            "derivative_rejections": derivative_rejections,
            "solutions": solutions,
            "stopped_reason": stopped_reason,
        }

    tested_left = 0
    enumerated_left = 0
    skipped_left = 0
    tested_lambdas = 0
    normalization_rejections = 0
    derivative_rejections = 0
    solutions: list[dict] = []

    for p2_coeffs in p2_options:
        p2 = monic_polynomial(2, p2_coeffs, modulus)
        for p3_coeffs in p3_options:
            p3 = monic_polynomial(3, p3_coeffs, modulus)
            for p4_coeffs in p4_options:
                enumerated_left += 1
                p4 = monic_polynomial(4, p4_coeffs, modulus)
                left_is_coprime = _left_factors_are_coprime(p2, p3, p4)
                if coprime_first and require_coprime_left and not left_is_coprime:
                    continue
                if max_left_factor_triples is not None and tested_left >= max_left_factor_triples:
                    enumerated_left -= 1
                    return build_result("max_left_factor_triples")
                tested_left += 1
                placeholder = ElkiesIdentityFactors(
                    p2=p2_coeffs,
                    p3=p3_coeffs,
                    p4=p4_coeffs,
                    p7=(0,) * 7,
                    p8=(0,) * 8,
                    lam=0,
                )
                if require_translation_normalized and not is_elkies_translation_normalized(
                    placeholder, modulus=modulus
                ):
                    normalization_rejections += 1
                    continue
                if require_coprime_left and not left_is_coprime:
                    skipped_left += 1
                    continue
                left = p2**2 * p3 * p4**4
                for lam in lambda_values:
                    tested_lambdas += 1
                    if max_solutions == 0:
                        continue
                    left_minus_lambda = Poly(left.as_expr() - lam, x, modulus=modulus)
                    for right in derive_right_factorizations(left_minus_lambda, modulus=modulus):
                        factors = ElkiesIdentityFactors(
                            p2=p2_coeffs,
                            p3=p3_coeffs,
                            p4=p4_coeffs,
                            p7=right["p7"],
                            p8=right["p8"],
                            lam=lam,
                        )
                        if not is_elkies_identity_solution(factors, modulus=modulus):
                            continue
                        if require_derivative and not is_elkies_derivative_solution(factors, modulus=modulus):
                            derivative_rejections += 1
                            continue
                        solutions.append(
                            {
                                "p2": list(p2_coeffs),
                                "p3": list(p3_coeffs),
                                "p4": list(p4_coeffs),
                                "p7": list(right["p7"]),
                                "p8": list(right["p8"]),
                                "lam": lam,
                            }
                        )
                        if len(solutions) >= max_solutions:
                            return build_result("max_solutions")

    return build_result("exhausted")


def render_belyi_search_markdown(result: dict, title: str = "M23 Belyi Finite-Field Search Report") -> str:
    lines: list[str] = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Modulus: `{result['modulus']}`",
        f"- Stopped reason: `{result['stopped_reason']}`",
        f"- Solutions: {len(result['solutions'])}",
        "",
    ]
    lines.extend(
        _markdown_table(
            ["statistic", "value"],
            [
                ["enumerated_left_factor_triples", str(result.get("enumerated_left_factor_triples", 0))],
                ["tested_left_factor_triples", str(result["tested_left_factor_triples"])],
                ["skipped_left_factor_triples", str(result["skipped_left_factor_triples"])],
                ["tested_lambda_values", str(result["tested_lambda_values"])],
                ["normalization_rejections", str(result["normalization_rejections"])],
                ["derivative_rejections", str(result["derivative_rejections"])],
            ],
        )
    )

    lines.extend(["", "## Search Options", ""])
    options = result.get("search_options", {})
    lines.extend(
        _markdown_table(
            ["option", "value"],
            [[str(key), str(value)] for key, value in sorted(options.items())],
        )
    )

    lines.extend(["", "## Solutions", ""])
    if result["solutions"]:
        lines.extend(
            _markdown_table(
                ["lambda", "P2", "P3", "P4", "P7", "P8"],
                [
                    [
                        str(solution["lam"]),
                        f"`{solution['p2']}`",
                        f"`{solution['p3']}`",
                        f"`{solution['p4']}`",
                        f"`{solution['p7']}`",
                        f"`{solution['p8']}`",
                    ]
                    for solution in result["solutions"][:20]
                ],
            )
        )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is a finite-field search report for the Elkies-style M23 identity. A solution here is only a modular equation-system survivor; it is not a rational M23 polynomial.",
            "",
        ]
    )
    return "\n".join(lines)
