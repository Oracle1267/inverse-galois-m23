from __future__ import annotations

from typing import Iterable

from .belyi import ElkiesIdentityFactors
from .lifting import lift_elkies_solution_mod_prime_power
from .reconstruction import reconstruct_lift_report


def _score_candidate(reconstruction: dict[str, object]) -> tuple[int, int, int, int, int]:
    complete_score = 1 if reconstruction["status"] == "complete" else 0
    exact_score = 1 if (
        reconstruction.get("exact_identity") is True
        and reconstruction.get("exact_derivative") is True
        and reconstruction.get("exact_translation_normalization") is True
    ) else 0
    return (
        complete_score,
        exact_score,
        int(reconstruction["unique_count"]),
        -len(reconstruction.get("unresolved", [])),  # type: ignore[arg-type]
        -len(reconstruction.get("ambiguous", [])),  # type: ignore[arg-type]
    )


def _candidate_summary(
    prefix: list[int],
    lift: dict[str, object],
    reconstruction: dict[str, object],
) -> dict[str, object]:
    return {
        "prefix": prefix,
        "score": list(_score_candidate(reconstruction)),
        "lift_status": lift["status"],
        "final_modulus": lift["final_modulus"],
        "final_lambda": lift["lifted"]["lam"],  # type: ignore[index]
        "reconstruction_status": reconstruction["status"],
        "unique_count": reconstruction["unique_count"],
        "total_count": reconstruction["total_count"],
        "unresolved_count": len(reconstruction.get("unresolved", [])),  # type: ignore[arg-type]
        "ambiguous_count": len(reconstruction.get("ambiguous", [])),  # type: ignore[arg-type]
        "exact_identity": reconstruction.get("exact_identity"),
        "exact_derivative": reconstruction.get("exact_derivative"),
        "exact_translation_normalization": reconstruction.get("exact_translation_normalization"),
    }


def _evaluate_prefix(
    seed: ElkiesIdentityFactors,
    *,
    prime: int,
    levels: int,
    prefix: list[int],
    max_numerator: int,
    max_denominator: int,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    lift = lift_elkies_solution_mod_prime_power(
        seed,
        prime=prime,
        levels=levels,
        lambda_corrections=prefix,
    )
    reconstruction = reconstruct_lift_report(
        lift,
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    )
    return _candidate_summary(prefix, lift, reconstruction), lift, reconstruction


def search_lambda_branches(
    seed: ElkiesIdentityFactors,
    *,
    prime: int,
    levels: int,
    depth: int,
    beam_width: int,
    max_numerator: int,
    max_denominator: int,
    digits: Iterable[int] | None = None,
) -> dict[str, object]:
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if depth > max(0, levels - 1):
        raise ValueError("depth cannot exceed levels - 1")
    if beam_width <= 0:
        raise ValueError("beam_width must be positive")

    digit_options = list(range(prime)) if digits is None else [int(digit) for digit in digits]
    if not digit_options:
        raise ValueError("digits cannot be empty")
    for digit in digit_options:
        if not 0 <= digit < prime:
            raise ValueError("digits must be in range 0..prime-1")

    prefixes: list[list[int]] = [[]]
    history: list[dict[str, object]] = []
    evaluated = 0
    best_summary: dict[str, object] | None = None
    best_lift: dict[str, object] | None = None
    best_reconstruction: dict[str, object] | None = None

    if depth == 0:
        best_summary, best_lift, best_reconstruction = _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=[],
            max_numerator=max_numerator,
            max_denominator=max_denominator,
        )
        evaluated = 1

    for position in range(depth):
        candidates: list[tuple[dict[str, object], dict[str, object], dict[str, object]]] = []
        for prefix in prefixes:
            for digit in digit_options:
                evaluated += 1
                candidates.append(
                    _evaluate_prefix(
                        seed,
                        prime=prime,
                        levels=levels,
                        prefix=[*prefix, digit],
                        max_numerator=max_numerator,
                        max_denominator=max_denominator,
                    )
                )
        candidates.sort(key=lambda item: tuple(item[0]["score"]), reverse=True)  # type: ignore[arg-type]
        kept = candidates[:beam_width]
        prefixes = [candidate[0]["prefix"] for candidate in kept]  # type: ignore[list-item]
        history.append(
            {
                "position": position,
                "evaluated": len(candidates),
                "kept": [candidate[0] for candidate in kept],
            }
        )
        if kept:
            best_summary, best_lift, best_reconstruction = kept[0]
        if best_summary and best_summary["reconstruction_status"] == "complete":
            break

    assert best_summary is not None
    assert best_lift is not None
    assert best_reconstruction is not None
    return {
        "status": best_summary["reconstruction_status"],
        "prime": prime,
        "levels": levels,
        "depth": depth,
        "beam_width": beam_width,
        "max_numerator": max_numerator,
        "max_denominator": max_denominator,
        "digit_options": digit_options,
        "evaluated_branches": evaluated,
        "best": best_summary,
        "best_lift": best_lift,
        "best_reconstruction": best_reconstruction,
        "history": history,
    }


def render_branch_search_markdown(result: dict[str, object], title: str = "M23 Belyi Lambda Branch Search") -> str:
    best = result["best"]
    assert isinstance(best, dict)
    lines = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Status: `{result['status']}`",
        f"- Prime: `{result['prime']}`",
        f"- Levels: `{result['levels']}`",
        f"- Depth: `{result['depth']}`",
        f"- Beam width: `{result['beam_width']}`",
        f"- Evaluated branches: `{result['evaluated_branches']}`",
        f"- Best prefix: `{best['prefix']}`",
        f"- Best lambda: `{best['final_lambda']}`",
        f"- Unique coefficients: `{best['unique_count']} / {best['total_count']}`",
        "",
        "## Beam History",
        "",
    ]
    for step in result["history"]:  # type: ignore[index]
        assert isinstance(step, dict)
        lines.extend([f"### Position {step['position']}", ""])
        for candidate in step["kept"]:  # type: ignore[index]
            lines.append(
                "- "
                + f"`{candidate['prefix']}` "
                + f"lambda `{candidate['final_lambda']}` "
                + f"unique `{candidate['unique_count']} / {candidate['total_count']}` "
                + f"status `{candidate['reconstruction_status']}`"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
