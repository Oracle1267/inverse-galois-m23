from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from sympy import Poly

from .belyi import ElkiesIdentityFactors
from .polynomial import x


VARIABLES: tuple[tuple[str, int | None], ...] = (
    *(("p2", index) for index in range(2)),
    *(("p3", index) for index in range(3)),
    *(("p4", index) for index in range(4)),
    *(("p7", index) for index in range(7)),
    *(("p8", index) for index in range(8)),
    ("lam", None),
)


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


def _integer_monic_polynomial(degree: int, coefficients: Iterable[int]) -> Poly:
    coeffs = tuple(int(coefficient) for coefficient in coefficients)
    if len(coeffs) != degree:
        raise ValueError(f"expected {degree} coefficients for a monic degree-{degree} polynomial")
    expr = x**degree
    for offset, coefficient in enumerate(coeffs):
        exponent = degree - offset - 1
        expr += coefficient * x**exponent
    return Poly(expr, x, domain="ZZ")


def _residual_coefficients(poly: Poly, degree: int) -> tuple[int, ...]:
    raw = [0] * (degree + 1)
    for (exponent,), coefficient in poly.terms():
        if exponent <= degree:
            raw[degree - exponent] = int(coefficient)
    return tuple(raw)


def _constraint_residuals(factors: ElkiesIdentityFactors) -> tuple[int, ...]:
    p2 = _integer_monic_polynomial(2, factors.p2)
    p3 = _integer_monic_polynomial(3, factors.p3)
    p4 = _integer_monic_polynomial(4, factors.p4)
    p7 = _integer_monic_polynomial(7, factors.p7)
    p8 = _integer_monic_polynomial(8, factors.p8)

    left = p2**2 * p3 * p4**4
    identity = left - p7 * p8**2 - int(factors.lam)
    derivative = left.diff() - 23 * p2 * p4**3 * p8
    translation = _residual_coefficients(left, degree=23)[1]
    return (
        *_residual_coefficients(identity, degree=23),
        *_residual_coefficients(derivative, degree=22),
        translation,
    )


def _constraint_names() -> list[str]:
    names = [f"identity_x^{degree}" for degree in range(23, -1, -1)]
    names.extend(f"derivative_x^{degree}" for degree in range(22, -1, -1))
    names.append("translation_x^22")
    return names


def _factors_to_dict(factors: ElkiesIdentityFactors) -> dict[str, object]:
    return {
        "p2": list(factors.p2),
        "p3": list(factors.p3),
        "p4": list(factors.p4),
        "p7": list(factors.p7),
        "p8": list(factors.p8),
        "lam": int(factors.lam),
    }


def factors_from_solution_dict(solution: dict[str, object]) -> ElkiesIdentityFactors:
    return ElkiesIdentityFactors(
        p2=tuple(int(item) for item in solution["p2"]),  # type: ignore[index]
        p3=tuple(int(item) for item in solution["p3"]),  # type: ignore[index]
        p4=tuple(int(item) for item in solution["p4"]),  # type: ignore[index]
        p7=tuple(int(item) for item in solution["p7"]),  # type: ignore[index]
        p8=tuple(int(item) for item in solution["p8"]),  # type: ignore[index]
        lam=int(solution["lam"]),
    )


def _bump_variable(factors: ElkiesIdentityFactors, variable_index: int, amount: int) -> ElkiesIdentityFactors:
    field, coefficient_index = VARIABLES[variable_index]
    if field == "lam":
        return replace(factors, lam=int(factors.lam) + amount)
    values = list(getattr(factors, field))
    assert coefficient_index is not None
    values[coefficient_index] += amount
    return replace(factors, **{field: tuple(values)})


def _apply_correction(
    factors: ElkiesIdentityFactors,
    correction: list[int],
    current_modulus: int,
    target_modulus: int,
) -> ElkiesIdentityFactors:
    lifted = factors
    for index, digit in enumerate(correction):
        if digit:
            lifted = _bump_variable(lifted, index, current_modulus * digit)
    return ElkiesIdentityFactors(
        p2=tuple(value % target_modulus for value in lifted.p2),
        p3=tuple(value % target_modulus for value in lifted.p3),
        p4=tuple(value % target_modulus for value in lifted.p4),
        p7=tuple(value % target_modulus for value in lifted.p7),
        p8=tuple(value % target_modulus for value in lifted.p8),
        lam=lifted.lam % target_modulus,
    )


def _solve_linear_system_mod_prime(
    matrix: list[list[int]],
    rhs: list[int],
    prime: int,
) -> dict[str, object]:
    if not matrix:
        return {"status": "solved", "solution": [], "rank": 0, "pivot_columns": []}
    row_count = len(matrix)
    column_count = len(matrix[0])
    rows = [
        [*(entry % prime for entry in matrix[row_index]), rhs[row_index] % prime]
        for row_index in range(row_count)
    ]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(column_count):
        pivot = None
        for candidate in range(pivot_row, row_count):
            if rows[candidate][column] % prime:
                pivot = candidate
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % prime, -1, prime)
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
        for row_index in range(row_count):
            if row_index == pivot_row:
                continue
            factor = rows[row_index][column] % prime
            if factor:
                rows[row_index] = [
                    (rows[row_index][item] - factor * rows[pivot_row][item]) % prime
                    for item in range(column_count + 1)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    inconsistent_rows = [
        row_index
        for row_index, row in enumerate(rows)
        if all(entry % prime == 0 for entry in row[:column_count]) and row[-1] % prime != 0
    ]
    if inconsistent_rows:
        return {
            "status": "inconsistent",
            "solution": None,
            "rank": len(pivot_columns),
            "pivot_columns": pivot_columns,
            "inconsistent_rows": inconsistent_rows,
        }

    solution = [0] * column_count
    for row_index, column in enumerate(pivot_columns):
        solution[column] = rows[row_index][-1] % prime
    return {
        "status": "solved",
        "solution": solution,
        "rank": len(pivot_columns),
        "pivot_columns": pivot_columns,
        "inconsistent_rows": [],
    }


def _lift_one_level(
    factors: ElkiesIdentityFactors,
    prime: int,
    current_modulus: int,
) -> tuple[ElkiesIdentityFactors | None, dict[str, object]]:
    target_modulus = current_modulus * prime
    base_residuals = _constraint_residuals(factors)
    names = _constraint_names()

    invalid_rows = [
        {"index": index, "constraint": names[index], "residual": residual}
        for index, residual in enumerate(base_residuals)
        if residual % current_modulus != 0
    ]
    if invalid_rows:
        return None, {
            "from_modulus": current_modulus,
            "to_modulus": target_modulus,
            "status": "invalid_seed",
            "invalid_rows": invalid_rows,
        }

    rhs = [(-residual // current_modulus) % prime for residual in base_residuals]
    columns: list[list[int]] = []
    for variable_index in range(len(VARIABLES)):
        bumped = _bump_variable(factors, variable_index, current_modulus)
        bumped_residuals = _constraint_residuals(bumped)
        columns.append(
            [
                ((bumped_residual - base_residual) // current_modulus) % prime
                for bumped_residual, base_residual in zip(bumped_residuals, base_residuals)
            ]
        )
    matrix = [
        [columns[column_index][row_index] for column_index in range(len(VARIABLES))]
        for row_index in range(len(base_residuals))
    ]
    solved = _solve_linear_system_mod_prime(matrix, rhs, prime)
    step: dict[str, object] = {
        "from_modulus": current_modulus,
        "to_modulus": target_modulus,
        "variables": len(VARIABLES),
        "constraints": len(base_residuals),
        "rank": solved["rank"],
        "pivot_columns": solved["pivot_columns"],
    }
    if solved["status"] != "solved":
        inconsistent_rows = [
            {
                "index": row_index,
                "constraint": names[row_index],
                "rhs": rhs[row_index],
            }
            for row_index in solved["inconsistent_rows"]  # type: ignore[index]
        ]
        step.update(
            {
                "status": "blocked",
                "inconsistent_rows": inconsistent_rows,
            }
        )
        return None, step

    correction = solved["solution"]
    assert isinstance(correction, list)
    lifted = _apply_correction(
        factors,
        correction=correction,
        current_modulus=current_modulus,
        target_modulus=target_modulus,
    )
    lifted_residuals = _constraint_residuals(lifted)
    verified = all(residual % target_modulus == 0 for residual in lifted_residuals)
    step.update(
        {
            "status": "lifted" if verified else "verification_failed",
            "correction": _factors_to_dict(
                ElkiesIdentityFactors(
                    p2=tuple(correction[0:2]),
                    p3=tuple(correction[2:5]),
                    p4=tuple(correction[5:9]),
                    p7=tuple(correction[9:16]),
                    p8=tuple(correction[16:24]),
                    lam=correction[24],
                )
            ),
            "residual_mod_target_all_zero": verified,
        }
    )
    return (lifted if verified else None), step


def lift_elkies_solution_mod_prime_power(
    seed: ElkiesIdentityFactors,
    prime: int,
    levels: int = 2,
) -> dict[str, object]:
    if not _is_prime_candidate(prime):
        raise ValueError(f"prime must be prime: {prime}")
    if levels < 1:
        raise ValueError("levels must be at least 1")

    current_modulus = prime
    current = ElkiesIdentityFactors(
        p2=tuple(value % prime for value in seed.p2),
        p3=tuple(value % prime for value in seed.p3),
        p4=tuple(value % prime for value in seed.p4),
        p7=tuple(value % prime for value in seed.p7),
        p8=tuple(value % prime for value in seed.p8),
        lam=seed.lam % prime,
    )
    steps: list[dict[str, object]] = []

    if any(residual % current_modulus != 0 for residual in _constraint_residuals(current)):
        return {
            "prime": prime,
            "requested_levels": levels,
            "status": "invalid_seed",
            "initial_modulus": prime,
            "final_modulus": current_modulus,
            "seed": _factors_to_dict(current),
            "lifted": None,
            "steps": steps,
        }

    for _ in range(1, levels):
        lifted, step = _lift_one_level(current, prime=prime, current_modulus=current_modulus)
        steps.append(step)
        if lifted is None:
            return {
                "prime": prime,
                "requested_levels": levels,
                "status": step["status"],
                "initial_modulus": prime,
                "final_modulus": current_modulus,
                "seed": _factors_to_dict(seed),
                "lifted": _factors_to_dict(current),
                "steps": steps,
            }
        current = lifted
        current_modulus *= prime

    return {
        "prime": prime,
        "requested_levels": levels,
        "status": "lifted",
        "initial_modulus": prime,
        "final_modulus": current_modulus,
        "seed": _factors_to_dict(seed),
        "lifted": _factors_to_dict(current),
        "steps": steps,
    }


def render_lift_report_markdown(result: dict[str, object], title: str = "M23 Belyi Lift Report") -> str:
    lines = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Prime: `{result['prime']}`",
        f"- Status: `{result['status']}`",
        f"- Final modulus: `{result['final_modulus']}`",
        "",
        "## Lifted Coefficients",
        "",
    ]
    lifted = result.get("lifted")
    if lifted:
        assert isinstance(lifted, dict)
        for key in ("p2", "p3", "p4", "p7", "p8", "lam"):
            lines.append(f"- `{key}`: `{lifted[key]}`")
    else:
        lines.append("- No lifted coefficients.")
    lines.extend(["", "## Steps", ""])
    for step in result["steps"]:  # type: ignore[index]
        assert isinstance(step, dict)
        lines.extend(
            [
                f"### {step['from_modulus']} to {step['to_modulus']}",
                "",
                f"- Status: `{step['status']}`",
                f"- Rank: `{step.get('rank', 'n/a')}`",
                f"- Constraints: `{step.get('constraints', 'n/a')}`",
                f"- Variables: `{step.get('variables', 'n/a')}`",
                "",
            ]
        )
        if step.get("inconsistent_rows"):
            lines.append("Blocked rows:")
            lines.append("")
            for row in step["inconsistent_rows"]:  # type: ignore[index]
                lines.append(f"- `{row}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
