from __future__ import annotations

from collections.abc import Iterable

import sympy as sp

from .polynomial import x
from .reconstruction import FIELDS, _fraction_from_entry


def _sympy_value(entry: dict[str, object], label: str, unknowns: list[str]) -> sp.Expr:
    if entry["status"] == "unique":
        fraction = _fraction_from_entry(entry["value"])  # type: ignore[arg-type]
        return sp.Rational(fraction.numerator, fraction.denominator)
    unknowns.append(label)
    return sp.Symbol(label.replace("[", "_").replace("]", ""))


def _monic_expr(degree: int, coefficients: Iterable[sp.Expr]) -> sp.Expr:
    expr: sp.Expr = x**degree
    for offset, coefficient in enumerate(coefficients):
        exponent = degree - offset - 1
        expr += coefficient * x**exponent
    return sp.expand(expr)


def _residual_coefficients(expr: sp.Expr, degree: int) -> list[sp.Expr]:
    expanded = sp.expand(expr)
    return [sp.expand(expanded.coeff(x, exponent)) for exponent in range(degree, -1, -1)]


def _linear_implication_from_expression(
    expr: sp.Expr,
    *,
    source: str,
    index: int,
) -> dict[str, object] | None:
    symbols = sorted(expr.free_symbols, key=lambda symbol: symbol.name)
    if len(symbols) != 1:
        return None
    symbol = symbols[0]
    polynomial = sp.Poly(expr, symbol)
    if polynomial.degree() != 1:
        return None
    coefficient = polynomial.coeff_monomial(symbol)
    constant = polynomial.coeff_monomial(1)
    value = sp.factor(sp.cancel(-constant / coefficient))
    return {
        "symbol": str(symbol),
        "value": str(value),
        "source": source,
        "index": index,
        "expression": str(expr),
    }


def _linear_conflicts(implications: list[dict[str, object]]) -> list[dict[str, object]]:
    by_symbol: dict[str, list[dict[str, object]]] = {}
    for implication in implications:
        by_symbol.setdefault(str(implication["symbol"]), []).append(implication)

    conflicts: list[dict[str, object]] = []
    for symbol, items in by_symbol.items():
        values = sorted({str(item["value"]) for item in items})
        if len(values) <= 1:
            continue
        conflicts.append(
            {
                "symbol": symbol,
                "values": values[:20],
                "constraints": [
                    {
                        "source": item["source"],
                        "index": item["index"],
                        "value": item["value"],
                    }
                    for item in items[:20]
                ],
            }
        )
    return conflicts


def _linear_system_report(records: list[tuple[str, int, sp.Expr]]) -> dict[str, object]:
    symbols = sorted(
        set().union(*(expr.free_symbols for _source, _index, expr in records)) if records else set(),
        key=lambda symbol: symbol.name,
    )
    linear_records: list[tuple[str, int, sp.Expr]] = []
    for source, index, expr in records:
        try:
            polynomial = sp.Poly(expr, *symbols)
        except (sp.PolynomialError, TypeError):
            continue
        if polynomial.total_degree() <= 1:
            linear_records.append((source, index, expr))

    if not linear_records or not symbols:
        return {
            "linear_system_equation_count": len(linear_records),
            "linear_system_rank": 0,
            "linear_system_augmented_rank": 0,
            "linear_system_consistent": True,
            "linear_system_conflict_count": 0,
            "linear_system_equations": [],
        }

    equations = [expr for _source, _index, expr in linear_records]
    coefficient_matrix, rhs_matrix = sp.linear_eq_to_matrix(equations, symbols)
    rank = coefficient_matrix.rank()
    augmented_rank = coefficient_matrix.row_join(rhs_matrix).rank()
    consistent = rank == augmented_rank
    return {
        "linear_system_equation_count": len(linear_records),
        "linear_system_rank": rank,
        "linear_system_augmented_rank": augmented_rank,
        "linear_system_consistent": consistent,
        "linear_system_conflict_count": 0 if consistent else 1,
        "linear_system_equations": [
            {
                "source": source,
                "index": index,
                "expression": str(expr),
            }
            for source, index, expr in linear_records[:20]
        ],
    }


def _default_groebner_report() -> dict[str, object]:
    return {
        "groebner_equation_count": 0,
        "groebner_symbol_count": 0,
        "groebner_contains_one": False,
        "groebner_conflict_count": 0,
        "groebner_basis_preview": [],
        "groebner_equations": [],
    }


def _record_degree(expr: sp.Expr, symbols: list[sp.Symbol]) -> int:
    if not symbols:
        return 0
    try:
        return int(sp.Poly(expr, *symbols).total_degree())
    except (sp.PolynomialError, TypeError):
        return 1_000_000


def _groebner_subset_report(records: list[tuple[str, int, sp.Expr]], max_equations: int) -> dict[str, object]:
    symbols = sorted(
        set().union(*(expr.free_symbols for _source, _index, expr in records)) if records else set(),
        key=lambda symbol: symbol.name,
    )
    if not records or not symbols:
        return _default_groebner_report()

    sorted_records = sorted(
        records,
        key=lambda record: (_record_degree(record[2], symbols), str(record[2])),
    )
    chosen = sorted_records[:max_equations]
    expressions = [sp.expand(expr) for _source, _index, expr in chosen]
    basis = sp.groebner(expressions, *symbols, order="lex")
    contains_one = any(sp.expand(poly.as_expr()) == 1 for poly in basis.polys)
    return {
        "groebner_equation_count": len(chosen),
        "groebner_symbol_count": len(symbols),
        "groebner_contains_one": contains_one,
        "groebner_conflict_count": 1 if contains_one else 0,
        "groebner_basis_preview": [str(poly.as_expr()) for poly in basis.polys[:8]],
        "groebner_equations": [
            {
                "source": source,
                "index": index,
                "degree": _record_degree(expr, symbols),
                "expression": str(expr),
            }
            for source, index, expr in chosen
        ],
    }


def _linearly_reduced_records(records: list[tuple[str, int, sp.Expr]]) -> list[tuple[str, int, sp.Expr]]:
    symbols = sorted(
        set().union(*(expr.free_symbols for _source, _index, expr in records)) if records else set(),
        key=lambda symbol: symbol.name,
    )
    if not records or not symbols:
        return records

    linear_equations: list[sp.Expr] = []
    for _source, _index, expr in records:
        try:
            polynomial = sp.Poly(expr, *symbols)
        except (sp.PolynomialError, TypeError):
            continue
        if polynomial.total_degree() <= 1:
            linear_equations.append(expr)
    if not linear_equations:
        return records

    solutions = sp.solve(linear_equations, symbols, dict=True)
    if not solutions:
        return records

    substitution = solutions[0]
    reduced: list[tuple[str, int, sp.Expr]] = []
    for source, index, expr in records:
        reduced_expr = sp.factor(sp.cancel(expr.subs(substitution)))
        if reduced_expr != 0:
            reduced.append((source, index, reduced_expr))
    return reduced


def _low_degree_groebner_report(
    records: list[tuple[str, int, sp.Expr]],
    max_equations: int = 4,
) -> dict[str, object]:
    if max_equations <= 0:
        return _default_groebner_report()
    try:
        direct = _groebner_subset_report(records, max_equations=max_equations)
        if direct["groebner_contains_one"]:
            return direct

        reduced_records = _linearly_reduced_records(records)
        if reduced_records == records:
            return direct
        reduced = _groebner_subset_report(reduced_records, max_equations=max_equations)
        if reduced["groebner_equation_count"] == 0:
            return direct
        reduced["groebner_linear_reduced"] = True
        return reduced
    except Exception as exc:  # pragma: no cover - defensive guard for long searches
        report = _default_groebner_report()
        report["groebner_error"] = str(exc)
        return report


def _classify_expression(
    expr: sp.Expr,
    *,
    source: str,
    index: int,
    hard_contradictions: list[dict[str, object]],
    symbolic_constraints: list[dict[str, object]],
    symbolic_expressions: list[tuple[str, int, sp.Expr]],
    linear_implications: list[dict[str, object]],
) -> str:
    numerator = sp.factor(sp.together(expr).as_numer_denom()[0])
    if numerator == 0:
        return "zero"
    entry = {
        "source": source,
        "index": index,
        "expression": str(numerator),
    }
    if numerator.free_symbols:
        symbolic_constraints.append(entry)
        symbolic_expressions.append((source, index, numerator))
        implication = _linear_implication_from_expression(numerator, source=source, index=index)
        if implication is not None:
            linear_implications.append(implication)
        return "symbolic"
    hard_contradictions.append(entry)
    return "hard"


def partial_consistency_report(reconstruction_report: dict[str, object]) -> dict[str, object]:
    reconstructed = reconstruction_report["reconstructed"]
    if not isinstance(reconstructed, dict):
        raise ValueError("reconstruction report must contain reconstructed values")

    unknowns: list[str] = []
    values: dict[str, list[sp.Expr] | sp.Expr] = {}
    for field, degree in FIELDS:
        entries = reconstructed[field]
        if not isinstance(entries, list) or len(entries) != degree:
            raise ValueError(f"expected {degree} reconstructed entries for {field}")
        values[field] = [
            _sympy_value(entry, f"{field}[{index}]", unknowns)  # type: ignore[arg-type]
            for index, entry in enumerate(entries)
        ]
    lam_entry = reconstructed["lam"]
    if not isinstance(lam_entry, dict):
        raise ValueError("expected reconstructed lambda entry")
    values["lam"] = _sympy_value(lam_entry, "lam", unknowns)

    p2 = _monic_expr(2, values["p2"])  # type: ignore[arg-type]
    p3 = _monic_expr(3, values["p3"])  # type: ignore[arg-type]
    p4 = _monic_expr(4, values["p4"])  # type: ignore[arg-type]
    p7 = _monic_expr(7, values["p7"])  # type: ignore[arg-type]
    p8 = _monic_expr(8, values["p8"])  # type: ignore[arg-type]
    lam = values["lam"]
    assert isinstance(lam, sp.Expr)

    identity = p2**2 * p3 * p4**4 - p7 * p8**2 - lam
    derivative = sp.diff(p2**2 * p3 * p4**4, x) - 23 * p2 * p4**3 * p8
    translation = _residual_coefficients(p2**2 * p3 * p4**4, degree=23)[1]

    hard_contradictions: list[dict[str, object]] = []
    symbolic_constraints: list[dict[str, object]] = []
    symbolic_expressions: list[tuple[str, int, sp.Expr]] = []
    linear_implications: list[dict[str, object]] = []
    zero_count = 0
    for source, expr, degree in (
        ("identity", identity, 23),
        ("derivative", derivative, 22),
    ):
        for index, coefficient in enumerate(_residual_coefficients(expr, degree=degree)):
            classification = _classify_expression(
                coefficient,
                source=source,
                index=index,
                hard_contradictions=hard_contradictions,
                symbolic_constraints=symbolic_constraints,
                symbolic_expressions=symbolic_expressions,
                linear_implications=linear_implications,
            )
            if classification == "zero":
                zero_count += 1
    classification = _classify_expression(
        translation,
        source="translation",
        index=1,
        hard_contradictions=hard_contradictions,
        symbolic_constraints=symbolic_constraints,
        symbolic_expressions=symbolic_expressions,
        linear_implications=linear_implications,
    )
    if classification == "zero":
        zero_count += 1

    linear_conflicts = _linear_conflicts(linear_implications)
    linear_system = _linear_system_report(symbolic_expressions)
    groebner = _low_degree_groebner_report(symbolic_expressions)
    return {
        "unknowns": unknowns,
        "unknown_count": len(unknowns),
        "hard_contradiction_count": len(hard_contradictions),
        "linear_implication_count": len(linear_implications),
        "linear_conflict_count": len(linear_conflicts),
        **linear_system,
        **groebner,
        "symbolic_constraint_count": len(symbolic_constraints),
        "zero_coefficient_count": zero_count,
        "hard_contradictions": hard_contradictions[:20],
        "linear_implications": linear_implications[:20],
        "linear_conflicts": linear_conflicts[:20],
        "symbolic_constraints": symbolic_constraints[:20],
    }
