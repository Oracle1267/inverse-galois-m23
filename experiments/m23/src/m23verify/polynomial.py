from __future__ import annotations

from dataclasses import dataclass
import warnings

from sympy import Poly, ZZ, discriminant, factor_list, symbols
from sympy.polys.polyerrors import CoercionFailed
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)
from sympy.utilities.exceptions import SymPyDeprecationWarning


x = symbols("x")
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


@dataclass(frozen=True)
class CoefficientBoundResult:
    ok: bool
    max_digits: int
    bound_digits: int


@dataclass(frozen=True)
class ModularFactorization:
    prime: int
    cycle_type: tuple[int, ...]
    is_good_prime: bool
    reason: str


@dataclass(frozen=True)
class PolynomialSummary:
    input: str
    degree: int
    coefficients: tuple[int, ...]
    coefficient_bound: CoefficientBoundResult
    is_irreducible: bool
    discriminant: int


def parse_polynomial(poly_text: str) -> Poly:
    try:
        expr = parse_expr(
            poly_text,
            local_dict={"x": x},
            transformations=TRANSFORMATIONS,
            evaluate=True,
        )
        return Poly(expr, x, domain=ZZ)
    except (CoercionFailed, TypeError, ValueError) as exc:
        raise ValueError(f"polynomial must have integer coefficients in x: {poly_text}") from exc


def coefficient_digit_count(value: int) -> int:
    return len(str(abs(int(value))))


def coefficient_bound(poly: Poly, bound_digits: int = 99) -> CoefficientBoundResult:
    max_digits = max(coefficient_digit_count(int(coeff)) for coeff in poly.all_coeffs())
    return CoefficientBoundResult(
        ok=max_digits <= bound_digits,
        max_digits=max_digits,
        bound_digits=bound_digits,
    )


def _is_prime_candidate(prime: int) -> bool:
    if prime < 2:
        return False
    if prime == 2:
        return True
    if prime % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= prime:
        if prime % divisor == 0:
            return False
        divisor += 2
    return True


def factor_degrees_mod_prime(poly: Poly, prime: int) -> ModularFactorization:
    if not _is_prime_candidate(prime):
        raise ValueError(f"not a prime: {prime}")

    leading = int(poly.LC())
    disc = int(discriminant(poly.as_expr(), x))
    is_good = leading % prime != 0 and disc % prime != 0
    reason = "good prime" if is_good else "bad prime: leading coefficient or discriminant vanishes mod p"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SymPyDeprecationWarning)
        _, factors = factor_list(poly.as_expr(), x, modulus=prime)
    degrees: list[int] = []
    for factor_expr, multiplicity in factors:
        factor_poly = Poly(factor_expr, x, modulus=prime)
        degrees.extend([factor_poly.degree()] * int(multiplicity))

    return ModularFactorization(
        prime=prime,
        cycle_type=tuple(sorted(degrees, reverse=True)),
        is_good_prime=is_good,
        reason=reason,
    )


def summarize_polynomial(poly_text: str, bound_digits: int = 99) -> PolynomialSummary:
    poly = parse_polynomial(poly_text)
    return PolynomialSummary(
        input=poly_text,
        degree=poly.degree(),
        coefficients=tuple(int(coeff) for coeff in poly.all_coeffs()),
        coefficient_bound=coefficient_bound(poly, bound_digits=bound_digits),
        is_irreducible=bool(poly.is_irreducible),
        discriminant=int(discriminant(poly.as_expr(), x)),
    )
