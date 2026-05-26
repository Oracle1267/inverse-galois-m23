from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
import json
from pathlib import Path
from typing import Any

from .belyi import ElkiesIdentityFactors
from .branch_search import _evaluate_prefix


ReviewEvaluator = Callable[[list[int]], tuple[dict[str, object], dict[str, object], dict[str, object]]]


def _script_expression(raw: object) -> str:
    return str(raw).replace("**", "^")


def _script_symbol(raw: object) -> str:
    return str(raw).replace("[", "_").replace("]", "")


def timeout_prefixes_from_branch_report(report: dict[str, object]) -> list[list[int]]:
    prefixes: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for step in report.get("history", []):
        if not isinstance(step, dict):
            continue
        for candidate in step.get("timeout_candidates", []):
            if not isinstance(candidate, dict):
                continue
            raw_prefix = candidate.get("prefix")
            if not isinstance(raw_prefix, list):
                continue
            prefix = [int(digit) for digit in raw_prefix]
            key = tuple(prefix)
            if key in seen:
                continue
            seen.add(key)
            prefixes.append(prefix)
    return prefixes


def classify_timeout_review(summary: dict[str, object]) -> str:
    if int(summary.get("groebner_conflict_count") or 0) > 0:
        return "reject"
    if int(summary.get("hard_contradiction_count") or 0) > 0:
        return "reject"
    if int(summary.get("linear_system_conflict_count") or 0) > 0:
        return "reject"
    if int(summary.get("linear_conflict_count") or 0) > 0:
        return "reject"
    if int(summary.get("linear_solution_conflict_count") or 0) > 0:
        return "reject"
    if int(summary.get("groebner_timeout_count") or 0) > 0:
        return "timeout"
    return "survivor"


def review_timeout_prefixes(
    prefixes: Iterable[Iterable[int]],
    *,
    evaluator: ReviewEvaluator,
) -> dict[str, object]:
    reviews: list[dict[str, object]] = []
    counts = {"reject": 0, "timeout": 0, "survivor": 0}
    for raw_prefix in prefixes:
        prefix = [int(digit) for digit in raw_prefix]
        summary, _lift, _reconstruction = evaluator(prefix)
        classification = classify_timeout_review(summary)
        counts[classification] += 1
        reviews.append(
            {
                "classification": classification,
                "prefix": prefix,
                "final_lambda": summary.get("final_lambda"),
                "reconstruction_status": summary.get("reconstruction_status"),
                "unique_count": summary.get("unique_count"),
                "total_count": summary.get("total_count"),
                "hard_contradiction_count": summary.get("hard_contradiction_count"),
                "linear_system_conflict_count": summary.get("linear_system_conflict_count"),
                "linear_conflict_count": summary.get("linear_conflict_count"),
                "linear_solution_conflict_count": summary.get("linear_solution_conflict_count"),
                "groebner_conflict_count": summary.get("groebner_conflict_count"),
                "groebner_timeout_count": summary.get("groebner_timeout_count"),
                "symbolic_constraint_count": summary.get("symbolic_constraint_count"),
                "unknowns": (
                    _reconstruction.get("partial_consistency", {}).get("unknowns", [])
                    if isinstance(_reconstruction.get("partial_consistency"), dict)
                    else []
                ),
                "groebner_equations": (
                    _reconstruction.get("partial_consistency", {}).get("groebner_equations", [])
                    if isinstance(_reconstruction.get("partial_consistency"), dict)
                    else []
                ),
            }
        )
    return {
        "reviewed_count": len(reviews),
        "classification_counts": counts,
        "reviews": reviews,
    }


def review_timeout_prefixes_from_report(
    report: dict[str, object],
    *,
    seed: ElkiesIdentityFactors,
    prime: int,
    levels: int,
    max_numerator: int,
    max_denominator: int,
    consistency_min_unique: int,
) -> dict[str, object]:
    prefixes = timeout_prefixes_from_branch_report(report)

    def evaluator(prefix: list[int]) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        return _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=prefix,
            max_numerator=max_numerator,
            max_denominator=max_denominator,
            score_consistency=True,
            consistency_min_unique=consistency_min_unique,
        )

    result = review_timeout_prefixes(prefixes, evaluator=evaluator)
    result.update(
        {
            "source_timeout_prefix_count": len(prefixes),
            "prime": prime,
            "levels": levels,
            "max_numerator": max_numerator,
            "max_denominator": max_denominator,
            "consistency_min_unique": consistency_min_unique,
        }
    )
    return result


def load_branch_report(path: Path) -> dict[str, object]:
    data: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected branch report object: {path}")
    return data


def render_timeout_review_markdown(result: dict[str, object], *, title: str) -> str:
    lines = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Reviewed timeout prefixes: `{result['reviewed_count']}`",
        f"- Rejects: `{result['classification_counts']['reject']}`",  # type: ignore[index]
        f"- Survivors: `{result['classification_counts']['survivor']}`",  # type: ignore[index]
        f"- Still timed out: `{result['classification_counts']['timeout']}`",  # type: ignore[index]
        "",
        "## Reviews",
        "",
    ]
    for review in result.get("reviews", []):
        if not isinstance(review, dict):
            continue
        lines.append(
            "- "
            + f"`{review['classification']}` "
            + f"prefix `{review['prefix']}` "
            + f"lambda `{review.get('final_lambda')}` "
            + f"unique `{review.get('unique_count')} / {review.get('total_count')}` "
            + f"hard `{review.get('hard_contradiction_count')}` "
            + f"linear-system `{review.get('linear_system_conflict_count')}` "
            + f"linear `{review.get('linear_conflict_count')}` "
            + f"linear-solution `{review.get('linear_solution_conflict_count')}` "
            + f"groebner `{review.get('groebner_conflict_count')}` "
            + f"groebner-timeout `{review.get('groebner_timeout_count')}`"
        )
    lines.append("")
    return "\n".join(lines)


def render_sage_groebner_script(equations: list[dict[str, object]], *, symbols: list[str]) -> str:
    symbol_list = ",".join(_script_symbol(symbol) for symbol in symbols)
    equation_list = ", ".join(_script_expression(equation["expression"]) for equation in equations)
    return "\n".join(
        [
            "# Auto-generated by review_timeout_branches.py",
            f"R.<{symbol_list}> = PolynomialRing(QQ, order='lex')",
            f"I = ideal([{equation_list}])",
            "G = I.groebner_basis()",
            "print('basis_length', len(G))",
            "print('contains_one', any(g == 1 for g in G))",
            "for g in G:",
            "    print(g)",
            "",
        ]
    )


def render_singular_groebner_script(equations: list[dict[str, object]], *, symbols: list[str]) -> str:
    symbol_list = ",".join(_script_symbol(symbol) for symbol in symbols)
    equation_list = ", ".join(_script_expression(equation["expression"]) for equation in equations)
    return "\n".join(
        [
            "// Auto-generated by review_timeout_branches.py",
            f"ring r = 0,({symbol_list}),lp;",
            f"ideal I = {equation_list};",
            "ideal G = groebner(I);",
            "G;",
            'print("contains_one");',
            "reduce(1,G);",
            "",
        ]
    )


def export_external_groebner_scripts(
    result: dict[str, object],
    *,
    output_dir: Path,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    exports: list[dict[str, object]] = []
    for index, review in enumerate(result.get("reviews", []), start=1):
        if not isinstance(review, dict):
            continue
        equations = review.get("groebner_equations")
        symbols = review.get("unknowns")
        if not isinstance(equations, list) or not isinstance(symbols, list) or not equations or not symbols:
            continue
        stem = f"timeout-branch-{index:02d}"
        sage_path = output_dir / f"{stem}.sage"
        singular_path = output_dir / f"{stem}.singular"
        sage_path.write_text(
            render_sage_groebner_script(equations, symbols=[str(symbol) for symbol in symbols]),
            encoding="utf-8",
        )
        singular_path.write_text(
            render_singular_groebner_script(equations, symbols=[str(symbol) for symbol in symbols]),
            encoding="utf-8",
        )
        exports.append(
            {
                "prefix": review.get("prefix"),
                "equation_count": len(equations),
                "symbol_count": len(symbols),
                "sage_path": str(sage_path),
                "singular_path": str(singular_path),
            }
        )
    return {"export_count": len(exports), "exports": exports}
