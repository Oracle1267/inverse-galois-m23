from __future__ import annotations

import json
from pathlib import Path
from typing import Callable
from typing import Iterable

from .belyi import ElkiesIdentityFactors
from .consistency import partial_consistency_report
from .lifting import lift_elkies_solution_mod_prime_power
from .reconstruction import reconstruct_lift_report


def _score_candidate(reconstruction: dict[str, object]) -> tuple[int, ...]:
    exact_score = 1 if (
        reconstruction.get("exact_identity") is True
        and reconstruction.get("exact_derivative") is True
        and reconstruction.get("exact_translation_normalization") is True
    ) else 0
    complete_score = 1 if reconstruction["status"] == "complete" and exact_score else 0
    inexact_penalty = -1 if (
        reconstruction.get("exact_identity") is False
        or reconstruction.get("exact_derivative") is False
        or reconstruction.get("exact_translation_normalization") is False
    ) else 0
    partial_consistency = reconstruction.get("partial_consistency")
    if isinstance(partial_consistency, dict):
        return (
            complete_score,
            exact_score,
            inexact_penalty,
            -int(partial_consistency["hard_contradiction_count"]),
            -int(partial_consistency.get("linear_system_conflict_count", 0)),
            -int(partial_consistency.get("linear_conflict_count", 0)),
            -int(partial_consistency.get("linear_solution_conflict_count", 0)),
            -int(partial_consistency.get("groebner_conflict_count", 0)),
            -int(partial_consistency.get("groebner_timeout_count", 0)),
            int(reconstruction["unique_count"]),
            -int(partial_consistency["unknown_count"]),
            -int(partial_consistency["symbolic_constraint_count"]),
            -len(reconstruction.get("unresolved", [])),  # type: ignore[arg-type]
            -len(reconstruction.get("ambiguous", [])),  # type: ignore[arg-type]
        )
    if reconstruction.get("consistency_scoring_enabled") is True:
        return (
            complete_score,
            exact_score,
            inexact_penalty,
            -1_000_000,
            -1_000_000,
            -1_000_000,
            -1_000_000,
            -1_000_000,
            -1_000_000,
            int(reconstruction["unique_count"]),
            -int(reconstruction.get("total_count", 0)),
            0,
            -len(reconstruction.get("unresolved", [])),  # type: ignore[arg-type]
            -len(reconstruction.get("ambiguous", [])),  # type: ignore[arg-type]
        )
    return (
        complete_score,
        exact_score,
        inexact_penalty,
        int(reconstruction["unique_count"]),
        -len(reconstruction.get("unresolved", [])),  # type: ignore[arg-type]
        -len(reconstruction.get("ambiguous", [])),  # type: ignore[arg-type]
    )


def _candidate_summary(
    prefix: list[int],
    lift: dict[str, object],
    reconstruction: dict[str, object],
) -> dict[str, object]:
    summary = {
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
        "hard_contradiction_count": None,
        "linear_system_conflict_count": None,
        "linear_conflict_count": None,
        "linear_solution_conflict_count": None,
        "groebner_conflict_count": None,
        "groebner_timeout_count": None,
        "symbolic_constraint_count": None,
    }
    partial_consistency = reconstruction.get("partial_consistency")
    if isinstance(partial_consistency, dict):
        summary["hard_contradiction_count"] = partial_consistency["hard_contradiction_count"]
        summary["linear_system_conflict_count"] = partial_consistency.get("linear_system_conflict_count", 0)
        summary["linear_conflict_count"] = partial_consistency.get("linear_conflict_count", 0)
        summary["linear_solution_conflict_count"] = partial_consistency.get("linear_solution_conflict_count", 0)
        summary["groebner_conflict_count"] = partial_consistency.get("groebner_conflict_count", 0)
        summary["groebner_timeout_count"] = partial_consistency.get("groebner_timeout_count", 0)
        summary["symbolic_constraint_count"] = partial_consistency["symbolic_constraint_count"]
        summary["unknown_count"] = partial_consistency["unknown_count"]
    return summary


def _evaluate_prefix(
    seed: ElkiesIdentityFactors,
    *,
    prime: int,
    levels: int,
    prefix: list[int],
    max_numerator: int,
    max_denominator: int,
    score_consistency: bool = False,
    consistency_min_unique: int = 0,
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
    if score_consistency:
        reconstruction["consistency_scoring_enabled"] = True
        if int(reconstruction["unique_count"]) >= consistency_min_unique:
            reconstruction["partial_consistency"] = partial_consistency_report(reconstruction)
        else:
            reconstruction["partial_consistency_skipped"] = "unique_count_below_threshold"
    return _candidate_summary(prefix, lift, reconstruction), lift, reconstruction


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checkpoint_path(checkpoint_dir: Path, checkpoint_prefix: str, position: int) -> Path:
    return checkpoint_dir / f"{checkpoint_prefix}-depth-{position}.json"


def _checkpoint_position(path: Path, checkpoint_prefix: str) -> int:
    stem_prefix = f"{checkpoint_prefix}-depth-"
    if not path.stem.startswith(stem_prefix):
        raise ValueError(f"unexpected checkpoint name: {path.name}")
    return int(path.stem[len(stem_prefix) :])


def _latest_checkpoint(checkpoint_dir: Path, checkpoint_prefix: str) -> dict[str, object] | None:
    if not checkpoint_dir.exists():
        return None
    checkpoints = sorted(
        checkpoint_dir.glob(f"{checkpoint_prefix}-depth-*.json"),
        key=lambda path: _checkpoint_position(path, checkpoint_prefix),
    )
    if not checkpoints:
        return None
    return json.loads(checkpoints[-1].read_text(encoding="utf-8"))


def _validate_checkpoint_compatibility(checkpoint: dict[str, object], expected: dict[str, object]) -> None:
    defaults: dict[str, object] = {
        "initial_prefixes": [[]],
        "refine_all": False,
        "score_consistency": False,
        "consistency_min_unique": 0,
    }
    for key, expected_value in expected.items():
        actual_value = checkpoint[key] if key in checkpoint else defaults.get(key)
        if actual_value != expected_value:
            raise ValueError(
                "checkpoint is incompatible with current search: "
                + f"{key} is {actual_value!r}, expected {expected_value!r}"
            )


def _sort_summaries(records: list[tuple[dict[str, object], dict[str, object], dict[str, object]]]) -> None:
    records.sort(key=lambda item: _summary_sort_key(item[0]), reverse=True)


ProgressCallback = Callable[[dict[str, object]], None]
BranchRecord = tuple[dict[str, object], dict[str, object], dict[str, object]]


def _summary_sort_key(summary: dict[str, object]) -> tuple[tuple[object, ...], int]:
    return (tuple(summary["score"]), len(summary["prefix"]))  # type: ignore[arg-type]


def _is_better_summary(candidate: dict[str, object], current: dict[str, object] | None) -> bool:
    return current is None or _summary_sort_key(candidate) > _summary_sort_key(current)


def _is_better_record(candidate: BranchRecord, current: BranchRecord | None) -> bool:
    return current is None or _is_better_summary(candidate[0], current[0])


def _is_exact_complete_summary(summary: dict[str, object]) -> bool:
    return (
        summary["reconstruction_status"] == "complete"
        and summary.get("exact_identity") is True
        and summary.get("exact_derivative") is True
        and summary.get("exact_translation_normalization") is True
    )


def _best_summary_from_history(history: list[dict[str, object]]) -> dict[str, object] | None:
    best: dict[str, object] | None = None
    for step in history:
        for candidate in step.get("kept", []):  # type: ignore[union-attr]
            if isinstance(candidate, dict) and _is_better_summary(candidate, best):
                best = candidate
    return best


def _normalize_initial_prefixes(
    initial_prefixes: Iterable[Iterable[int]] | None,
    *,
    prime: int,
    depth: int,
) -> tuple[list[list[int]], int]:
    if initial_prefixes is None:
        return [[]], 0
    prefixes = [[int(digit) for digit in prefix] for prefix in initial_prefixes]
    if not prefixes:
        raise ValueError("initial_prefixes cannot be empty")
    prefix_length = len(prefixes[0])
    if prefix_length > depth:
        raise ValueError("initial prefix length cannot exceed depth")
    for prefix in prefixes:
        if len(prefix) != prefix_length:
            raise ValueError("initial prefixes must have the same length")
        for digit in prefix:
            if not 0 <= digit < prime:
                raise ValueError("initial prefix digits must be in range 0..prime-1")
    return prefixes, prefix_length


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
    score_consistency: bool = False,
    consistency_min_unique: int = 0,
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
    best_record: BranchRecord | None = None
    final_record: BranchRecord | None = None

    if depth == 0:
        best_record = _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=[],
            max_numerator=max_numerator,
            max_denominator=max_denominator,
            score_consistency=score_consistency,
            consistency_min_unique=consistency_min_unique,
        )
        final_record = best_record
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
                        score_consistency=score_consistency,
                        consistency_min_unique=consistency_min_unique,
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
            final_record = kept[0]
            if _is_better_record(final_record, best_record):
                best_record = final_record
        if best_record and _is_exact_complete_summary(best_record[0]):
            break

    assert best_record is not None
    assert final_record is not None
    best_summary, best_lift, best_reconstruction = best_record
    return {
        "status": best_summary["reconstruction_status"],
        "prime": prime,
        "levels": levels,
        "depth": depth,
        "beam_width": beam_width,
        "max_numerator": max_numerator,
        "max_denominator": max_denominator,
        "score_consistency": score_consistency,
        "consistency_min_unique": consistency_min_unique,
        "digit_options": digit_options,
        "evaluated_branches": evaluated,
        "best": best_summary,
        "final_best": final_record[0],
        "best_lift": best_lift,
        "best_reconstruction": best_reconstruction,
        "history": history,
    }


def search_lambda_branches_checkpointed(
    seed: ElkiesIdentityFactors,
    *,
    prime: int,
    levels: int,
    depth: int,
    beam_width: int,
    max_numerator: int,
    max_denominator: int,
    score_levels: int,
    score_max_numerator: int,
    score_max_denominator: int,
    refine_multiplier: int = 2,
    digits: Iterable[int] | None = None,
    initial_prefixes: Iterable[Iterable[int]] | None = None,
    refine_all: bool = False,
    score_consistency: bool = False,
    consistency_min_unique: int = 0,
    checkpoint_dir: Path | str | None = None,
    checkpoint_prefix: str = "lambda-branch-search",
    resume: bool = False,
    progress_every: int = 0,
    progress_callback: ProgressCallback | None = None,
) -> dict[str, object]:
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if depth > max(0, levels - 1):
        raise ValueError("depth cannot exceed levels - 1")
    if beam_width <= 0:
        raise ValueError("beam_width must be positive")
    if refine_multiplier <= 0:
        raise ValueError("refine_multiplier must be positive")
    if not 1 <= score_levels <= levels:
        raise ValueError("score_levels must be between 1 and levels")

    digit_options = list(range(prime)) if digits is None else [int(digit) for digit in digits]
    if not digit_options:
        raise ValueError("digits cannot be empty")
    for digit in digit_options:
        if not 0 <= digit < prime:
            raise ValueError("digits must be in range 0..prime-1")

    checkpoint_root = Path(checkpoint_dir) if checkpoint_dir is not None else None
    prefixes, initial_depth = _normalize_initial_prefixes(initial_prefixes, prime=prime, depth=depth)
    initial_roots = [list(prefix) for prefix in prefixes]
    history: list[dict[str, object]] = []
    evaluated = 0
    start_position = initial_depth
    checkpoint_best_summary: dict[str, object] | None = None

    if resume and checkpoint_root is not None:
        checkpoint = _latest_checkpoint(checkpoint_root, checkpoint_prefix)
        if checkpoint is not None:
            _validate_checkpoint_compatibility(
                checkpoint,
                {
                    "prime": prime,
                    "levels": levels,
                    "beam_width": beam_width,
                    "score_levels": score_levels,
                    "max_numerator": max_numerator,
                    "max_denominator": max_denominator,
                    "score_max_numerator": score_max_numerator,
                    "score_max_denominator": score_max_denominator,
                    "refine_multiplier": refine_multiplier,
                    "refine_all": refine_all,
                    "score_consistency": score_consistency,
                    "consistency_min_unique": consistency_min_unique,
                    "initial_prefixes": initial_roots,
                    "digit_options": digit_options,
                },
            )
            start_position = int(checkpoint["position"]) + 1
            prefixes = [list(item["prefix"]) for item in checkpoint["kept"]]  # type: ignore[index]
            history = list(checkpoint.get("history", []))  # type: ignore[arg-type]
            evaluated = int(checkpoint.get("evaluated_branches", 0))
            stored_best = checkpoint.get("best")
            checkpoint_best_summary = stored_best if isinstance(stored_best, dict) else _best_summary_from_history(history)

    best_record: BranchRecord | None = None
    final_record: BranchRecord | None = None

    if start_position > 0:
        initial_records = [
            _evaluate_prefix(
                seed,
                prime=prime,
                levels=levels,
                prefix=prefix,
                max_numerator=max_numerator,
                max_denominator=max_denominator,
                score_consistency=score_consistency,
                consistency_min_unique=consistency_min_unique,
            )
            for prefix in prefixes
        ]
        _sort_summaries(initial_records)
        best_record = initial_records[0]
        final_record = initial_records[0]

    if checkpoint_best_summary is not None:
        best_record = _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=list(checkpoint_best_summary["prefix"]),  # type: ignore[arg-type]
            max_numerator=max_numerator,
            max_denominator=max_denominator,
            score_consistency=score_consistency,
            consistency_min_unique=consistency_min_unique,
        )
        final_record = best_record

    if start_position >= depth:
        best_prefix = prefixes[0] if prefixes else []
        final_record = _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=best_prefix,
            max_numerator=max_numerator,
            max_denominator=max_denominator,
            score_consistency=score_consistency,
            consistency_min_unique=consistency_min_unique,
        )
        if _is_better_record(final_record, best_record):
            best_record = final_record

    for position in range(start_position, depth):
        cheap_records: list[tuple[dict[str, object], dict[str, object], dict[str, object]]] = []
        expanded = len(prefixes) * len(digit_options)
        processed = 0
        if progress_callback:
            progress_callback(
                {
                    "event": "depth-start",
                    "position": position,
                    "depth": depth,
                    "expanded": expanded,
                    "beam_width": beam_width,
                }
            )
        for prefix in prefixes:
            for digit in digit_options:
                processed += 1
                trial_prefix = [*prefix, digit]
                cheap_records.append(
                    _evaluate_prefix(
                        seed,
                        prime=prime,
                        levels=max(score_levels, len(trial_prefix) + 1),
                        prefix=trial_prefix,
                        max_numerator=score_max_numerator,
                        max_denominator=score_max_denominator,
                    )
                )
                if progress_callback and progress_every > 0 and processed % progress_every == 0:
                    progress_callback(
                        {
                            "event": "cheap-progress",
                            "position": position,
                            "done": processed,
                            "total": expanded,
                        }
                    )
        evaluated += expanded
        _sort_summaries(cheap_records)
        refine_width = len(cheap_records) if refine_all else min(len(cheap_records), beam_width * refine_multiplier)
        refine_prefixes = [record[0]["prefix"] for record in cheap_records[:refine_width]]

        refined: list[tuple[dict[str, object], dict[str, object], dict[str, object]]] = []
        for index, prefix in enumerate(refine_prefixes, start=1):
            assert isinstance(prefix, list)
            if progress_callback:
                progress_callback(
                    {
                        "event": "refine-start",
                        "position": position,
                        "done": index,
                        "total": refine_width,
                        "prefix": prefix,
                    }
                )
            refined.append(
                _evaluate_prefix(
                    seed,
                    prime=prime,
                    levels=levels,
                    prefix=prefix,
                    max_numerator=max_numerator,
                    max_denominator=max_denominator,
                    score_consistency=score_consistency,
                    consistency_min_unique=consistency_min_unique,
                )
            )
            if progress_callback and progress_every > 0 and index % progress_every == 0:
                progress_callback(
                    {
                        "event": "refine-progress",
                        "position": position,
                        "done": index,
                        "total": refine_width,
                    }
                )
        _sort_summaries(refined)
        kept = refined[:beam_width]
        timeout_candidates = [
            candidate[0]
            for candidate in refined
            if int(candidate[0].get("groebner_timeout_count") or 0) > 0
        ]
        prefixes = [candidate[0]["prefix"] for candidate in kept]  # type: ignore[list-item]
        if kept:
            final_record = kept[0]
            if _is_better_record(final_record, best_record):
                best_record = final_record
        step = {
            "position": position,
            "expanded": expanded,
            "cheap_scored": len(cheap_records),
            "refined": len(refined),
            "kept": [candidate[0] for candidate in kept],
            "timeout_candidates": timeout_candidates,
        }
        history.append(step)
        checkpoint_data = {
            "position": position,
            "prime": prime,
            "levels": levels,
            "depth": depth,
            "beam_width": beam_width,
            "score_levels": score_levels,
            "max_numerator": max_numerator,
            "max_denominator": max_denominator,
            "score_max_numerator": score_max_numerator,
            "score_max_denominator": score_max_denominator,
            "refine_multiplier": refine_multiplier,
            "refine_all": refine_all,
            "score_consistency": score_consistency,
            "consistency_min_unique": consistency_min_unique,
            "initial_prefixes": initial_roots,
            "digit_options": digit_options,
            "evaluated_branches": evaluated,
            "history": history,
            "kept": step["kept"],
            "best": best_record[0] if best_record is not None else None,
        }
        if checkpoint_root is not None:
            _write_json(_checkpoint_path(checkpoint_root, checkpoint_prefix, position), checkpoint_data)
        if progress_callback:
            best = kept[0][0] if kept else None
            progress_callback(
                {
                    "event": "depth-finished",
                    "position": position,
                    "depth": depth,
                    "expanded": expanded,
                    "refined": len(refined),
                    "best": best,
                }
            )
        if best_record and _is_exact_complete_summary(best_record[0]):
            break

    assert best_record is not None
    assert final_record is not None
    best_summary, best_lift, best_reconstruction = best_record
    return {
        "status": best_summary["reconstruction_status"],
        "prime": prime,
        "levels": levels,
        "depth": depth,
        "beam_width": beam_width,
        "score_levels": score_levels,
        "refine_multiplier": refine_multiplier,
        "max_numerator": max_numerator,
        "max_denominator": max_denominator,
        "score_max_numerator": score_max_numerator,
        "score_max_denominator": score_max_denominator,
        "initial_prefixes": initial_roots,
        "refine_all": refine_all,
        "score_consistency": score_consistency,
        "consistency_min_unique": consistency_min_unique,
        "digit_options": digit_options,
        "evaluated_branches": evaluated,
        "checkpoint_dir": str(checkpoint_root) if checkpoint_root is not None else None,
        "checkpoint_prefix": checkpoint_prefix,
        "best": best_summary,
        "final_best": final_record[0],
        "best_lift": best_lift,
        "best_reconstruction": best_reconstruction,
        "history": history,
    }


def render_branch_search_markdown(result: dict[str, object], title: str = "M23 Belyi Lambda Branch Search") -> str:
    best = result["best"]
    assert isinstance(best, dict)
    final_best = result.get("final_best")
    assert final_best is None or isinstance(final_best, dict)
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
        f"- Score consistency: `{result.get('score_consistency', False)}`",
        f"- Consistency min unique: `{result.get('consistency_min_unique', 0)}`",
        f"- Evaluated branches: `{result['evaluated_branches']}`",
        f"- Best prefix: `{best['prefix']}`",
        f"- Best lambda: `{best['final_lambda']}`",
        f"- Unique coefficients: `{best['unique_count']} / {best['total_count']}`",
    ]
    if best.get("hard_contradiction_count") is not None:
        lines.extend(
            [
                f"- Hard consistency contradictions: `{best['hard_contradiction_count']}`",
                f"- Linear system conflicts: `{best.get('linear_system_conflict_count', 0)}`",
                f"- Linear symbolic conflicts: `{best.get('linear_conflict_count', 0)}`",
                f"- Linear-solution residual conflicts: `{best.get('linear_solution_conflict_count', 0)}`",
                f"- Groebner low-degree conflicts: `{best.get('groebner_conflict_count', 0)}`",
                f"- Groebner timeouts: `{best.get('groebner_timeout_count', 0)}`",
                f"- Symbolic consistency constraints: `{best['symbolic_constraint_count']}`",
            ]
        )
    if isinstance(final_best, dict) and final_best["prefix"] != best["prefix"]:
        lines.extend(
            [
                f"- Final frontier prefix: `{final_best['prefix']}`",
                f"- Final frontier lambda: `{final_best['final_lambda']}`",
                f"- Final frontier unique coefficients: `{final_best['unique_count']} / {final_best['total_count']}`",
            ]
        )
    lines.extend(["", "## Beam History", ""])
    for step in result["history"]:  # type: ignore[index]
        assert isinstance(step, dict)
        lines.extend([f"### Position {step['position']}", ""])
        for candidate in step["kept"]:  # type: ignore[index]
            consistency = (
                ""
                if candidate.get("hard_contradiction_count") is None
                else (
                    f" hard `{candidate['hard_contradiction_count']}`"
                    + f" linear-system `{candidate.get('linear_system_conflict_count', 0)}`"
                    + f" linear `{candidate.get('linear_conflict_count', 0)}`"
                    + f" linear-solution `{candidate.get('linear_solution_conflict_count', 0)}`"
                    + f" groebner `{candidate.get('groebner_conflict_count', 0)}`"
                    + f" groebner-timeout `{candidate.get('groebner_timeout_count', 0)}`"
                )
            )
            lines.append(
                "- "
                + f"`{candidate['prefix']}` "
                + f"lambda `{candidate['final_lambda']}` "
                + f"unique `{candidate['unique_count']} / {candidate['total_count']}` "
                + f"status `{candidate['reconstruction_status']}`"
                + consistency
            )
        lines.append("")
        timeout_candidates = step.get("timeout_candidates", [])
        if timeout_candidates:
            lines.extend(["Timed-out Groebner candidates:", ""])
            for candidate in timeout_candidates:  # type: ignore[assignment]
                lines.append(
                    "- "
                    + f"`{candidate['prefix']}` "
                    + f"lambda `{candidate['final_lambda']}` "
                    + f"unique `{candidate['unique_count']} / {candidate['total_count']}` "
                    + f"status `{candidate['reconstruction_status']}`"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
