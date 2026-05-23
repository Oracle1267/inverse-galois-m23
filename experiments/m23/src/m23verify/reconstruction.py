from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable

from sympy import Poly, Rational

from .polynomial import x


FIELDS: tuple[tuple[str, int], ...] = (
    ("p2", 2),
    ("p3", 3),
    ("p4", 4),
    ("p7", 7),
    ("p8", 8),
)


def _symmetric_residue(value: int, modulus: int) -> int:
    residue = int(value) % modulus
    if residue > modulus // 2:
        residue -= modulus
    return residue


def rational_reconstruct(
    residue: int,
    modulus: int,
    max_numerator: int,
    max_denominator: int,
) -> dict[str, object]:
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    if max_numerator < 0:
        raise ValueError("max_numerator must be nonnegative")
    if max_denominator <= 0:
        raise ValueError("max_denominator must be positive")

    candidates: list[tuple[int, int]] = []
    for denominator in range(1, max_denominator + 1):
        if gcd(denominator, modulus) != 1:
            continue
        numerator = _symmetric_residue(residue * denominator, modulus)
        if abs(numerator) > max_numerator:
            continue
        common = gcd(abs(numerator), denominator)
        normalized = (numerator // common, denominator // common)
        if normalized not in candidates:
            candidates.append(normalized)

    if len(candidates) == 1:
        numerator, denominator = candidates[0]
        return {
            "status": "unique",
            "value": {"numerator": numerator, "denominator": denominator},
            "candidates": [{"numerator": numerator, "denominator": denominator}],
        }
    return {
        "status": "none" if not candidates else "ambiguous",
        "value": None,
        "candidates": [
            {"numerator": numerator, "denominator": denominator}
            for numerator, denominator in candidates[:20]
        ],
        "candidate_count": len(candidates),
    }


def _fraction_from_entry(entry: dict[str, int]) -> Fraction:
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def _sympy_rational(value: Fraction) -> Rational:
    return Rational(value.numerator, value.denominator)


def _rational_monic_polynomial(degree: int, coefficients: Iterable[Fraction]) -> Poly:
    coeffs = tuple(coefficients)
    if len(coeffs) != degree:
        raise ValueError(f"expected {degree} coefficients")
    expr = x**degree
    for offset, coefficient in enumerate(coeffs):
        exponent = degree - offset - 1
        expr += _sympy_rational(coefficient) * x**exponent
    return Poly(expr, x, domain="QQ")


def _residual_coefficients(poly: Poly, degree: int) -> tuple[Rational, ...]:
    raw = [Rational(0)] * (degree + 1)
    for (exponent,), coefficient in poly.terms():
        if exponent <= degree:
            raw[degree - exponent] = Rational(coefficient)
    return tuple(raw)


def _verify_exact(reconstructed: dict[str, object]) -> dict[str, bool] | None:
    values: dict[str, list[Fraction] | Fraction] = {}
    for field, _degree in FIELDS:
        field_values = []
        for entry in reconstructed[field]:  # type: ignore[index]
            if entry["status"] != "unique":
                return None
            field_values.append(_fraction_from_entry(entry["value"]))
        values[field] = field_values
    lam_entry = reconstructed["lam"]
    if lam_entry["status"] != "unique":  # type: ignore[index]
        return None
    values["lam"] = _fraction_from_entry(lam_entry["value"])  # type: ignore[index]

    p2 = _rational_monic_polynomial(2, values["p2"])  # type: ignore[arg-type]
    p3 = _rational_monic_polynomial(3, values["p3"])  # type: ignore[arg-type]
    p4 = _rational_monic_polynomial(4, values["p4"])  # type: ignore[arg-type]
    p7 = _rational_monic_polynomial(7, values["p7"])  # type: ignore[arg-type]
    p8 = _rational_monic_polynomial(8, values["p8"])  # type: ignore[arg-type]
    left = p2**2 * p3 * p4**4
    identity = left - p7 * p8**2 - _sympy_rational(values["lam"])  # type: ignore[arg-type]
    derivative = left.diff() - 23 * p2 * p4**3 * p8
    translation = _residual_coefficients(left, degree=23)[1]
    return {
        "exact_identity": all(coefficient == 0 for coefficient in _residual_coefficients(identity, degree=23)),
        "exact_derivative": all(coefficient == 0 for coefficient in _residual_coefficients(derivative, degree=22)),
        "exact_translation_normalization": translation == 0,
    }


def reconstruct_lift_report(
    lift_report: dict[str, object],
    max_numerator: int,
    max_denominator: int,
) -> dict[str, object]:
    modulus = int(lift_report["final_modulus"])
    lifted = lift_report["lifted"]
    if not isinstance(lifted, dict):
        raise ValueError("lift report must contain a lifted coefficient dictionary")

    reconstructed: dict[str, object] = {}
    unique_count = 0
    total_count = 0
    unresolved: list[str] = []
    ambiguous: list[str] = []
    for field, degree in FIELDS:
        coefficients = lifted[field]
        if not isinstance(coefficients, list) or len(coefficients) != degree:
            raise ValueError(f"expected {degree} coefficients for {field}")
        field_results = []
        for index, residue in enumerate(coefficients):
            result = rational_reconstruct(
                int(residue),
                modulus=modulus,
                max_numerator=max_numerator,
                max_denominator=max_denominator,
            )
            field_results.append(result)
            total_count += 1
            if result["status"] == "unique":
                unique_count += 1
            elif result["status"] == "ambiguous":
                ambiguous.append(f"{field}[{index}]")
            else:
                unresolved.append(f"{field}[{index}]")
        reconstructed[field] = field_results

    lam_result = rational_reconstruct(
        int(lifted["lam"]),
        modulus=modulus,
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    )
    reconstructed["lam"] = lam_result
    total_count += 1
    if lam_result["status"] == "unique":
        unique_count += 1
    elif lam_result["status"] == "ambiguous":
        ambiguous.append("lam")
    else:
        unresolved.append("lam")

    exact = _verify_exact(reconstructed)
    status = "complete" if unique_count == total_count else "partial"
    report: dict[str, object] = {
        "status": status,
        "modulus": modulus,
        "max_numerator": max_numerator,
        "max_denominator": max_denominator,
        "unique_count": unique_count,
        "total_count": total_count,
        "unresolved": unresolved,
        "ambiguous": ambiguous,
        "reconstructed": reconstructed,
    }
    if exact is None:
        report.update(
            {
                "exact_identity": None,
                "exact_derivative": None,
                "exact_translation_normalization": None,
            }
        )
    else:
        report.update(exact)
    return report


def render_reconstruction_markdown(result: dict[str, object], title: str = "M23 Belyi Reconstruction Report") -> str:
    lines = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Status: `{result['status']}`",
        f"- Modulus: `{result['modulus']}`",
        f"- Unique coefficients: `{result['unique_count']} / {result['total_count']}`",
        f"- Exact identity: `{result['exact_identity']}`",
        f"- Exact derivative: `{result['exact_derivative']}`",
        f"- Exact translation normalization: `{result['exact_translation_normalization']}`",
        "",
    ]
    unresolved = result.get("unresolved", [])
    ambiguous = result.get("ambiguous", [])
    if unresolved:
        lines.extend(["## Unresolved", ""])
        for item in unresolved:  # type: ignore[union-attr]
            lines.append(f"- `{item}`")
        lines.append("")
    if ambiguous:
        lines.extend(["## Ambiguous", ""])
        for item in ambiguous:  # type: ignore[union-attr]
            lines.append(f"- `{item}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
