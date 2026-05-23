from __future__ import annotations

import json
from pathlib import Path
from typing import Callable
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
    for key, expected_value in expected.items():
        if checkpoint.get(key) != expected_value:
            raise ValueError(
                "checkpoint is incompatible with current search: "
                + f"{key} is {checkpoint.get(key)!r}, expected {expected_value!r}"
            )


def _sort_summaries(records: list[tuple[dict[str, object], dict[str, object], dict[str, object]]]) -> None:
    records.sort(key=lambda item: tuple(item[0]["score"]), reverse=True)  # type: ignore[arg-type]


ProgressCallback = Callable[[dict[str, object]], None]


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
    prefixes: list[list[int]] = [[]]
    history: list[dict[str, object]] = []
    evaluated = 0
    start_position = 0

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
                    "digit_options": digit_options,
                },
            )
            start_position = int(checkpoint["position"]) + 1
            prefixes = [list(item["prefix"]) for item in checkpoint["kept"]]  # type: ignore[index]
            history = list(checkpoint.get("history", []))  # type: ignore[arg-type]
            evaluated = int(checkpoint.get("evaluated_branches", 0))

    best_summary: dict[str, object] | None = None
    best_lift: dict[str, object] | None = None
    best_reconstruction: dict[str, object] | None = None

    if start_position >= depth:
        best_prefix = prefixes[0] if prefixes else []
        best_summary, best_lift, best_reconstruction = _evaluate_prefix(
            seed,
            prime=prime,
            levels=levels,
            prefix=best_prefix,
            max_numerator=max_numerator,
            max_denominator=max_denominator,
        )

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
        refine_width = min(len(cheap_records), beam_width * refine_multiplier)
        refine_prefixes = [record[0]["prefix"] for record in cheap_records[:refine_width]]

        refined: list[tuple[dict[str, object], dict[str, object], dict[str, object]]] = []
        for index, prefix in enumerate(refine_prefixes, start=1):
            assert isinstance(prefix, list)
            refined.append(
                _evaluate_prefix(
                    seed,
                    prime=prime,
                    levels=levels,
                    prefix=prefix,
                    max_numerator=max_numerator,
                    max_denominator=max_denominator,
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
        prefixes = [candidate[0]["prefix"] for candidate in kept]  # type: ignore[list-item]
        if kept:
            best_summary, best_lift, best_reconstruction = kept[0]
        step = {
            "position": position,
            "expanded": expanded,
            "cheap_scored": len(cheap_records),
            "refined": len(refined),
            "kept": [candidate[0] for candidate in kept],
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
            "digit_options": digit_options,
            "evaluated_branches": evaluated,
            "history": history,
            "kept": step["kept"],
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
        "score_levels": score_levels,
        "refine_multiplier": refine_multiplier,
        "max_numerator": max_numerator,
        "max_denominator": max_denominator,
        "score_max_numerator": score_max_numerator,
        "score_max_denominator": score_max_denominator,
        "digit_options": digit_options,
        "evaluated_branches": evaluated,
        "checkpoint_dir": str(checkpoint_root) if checkpoint_root is not None else None,
        "checkpoint_prefix": checkpoint_prefix,
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
