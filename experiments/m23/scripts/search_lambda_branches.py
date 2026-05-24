from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.belyi import ElkiesIdentityFactors
from m23verify.branch_search import (
    render_branch_search_markdown,
    search_lambda_branches,
    search_lambda_branches_checkpointed,
)
from m23verify.lifting import factors_from_solution_dict


def parse_coefficients(raw: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in raw.split(",") if item.strip())


def parse_digits(raw: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in raw.split(",") if item.strip())


def load_seed_from_json(path: Path, solution_index: int) -> ElkiesIdentityFactors:
    data = json.loads(path.read_text(encoding="utf-8"))
    solutions = data.get("solutions", [])
    if not solutions:
        raise ValueError(f"seed JSON has no solutions: {path}")
    if solution_index < 0 or solution_index >= len(solutions):
        raise ValueError(f"solution index out of range: {solution_index}")
    return factors_from_solution_dict(solutions[solution_index])


def seed_from_args(args: argparse.Namespace) -> ElkiesIdentityFactors:
    if args.seed_json:
        return load_seed_from_json(Path(args.seed_json), solution_index=args.solution_index)
    required = {
        "p2": args.p2,
        "p3": args.p3,
        "p4": args.p4,
        "p7": args.p7,
        "p8": args.p8,
        "lam": args.lam,
    }
    missing = [key for key, value in required.items() if value is None]
    if missing:
        raise ValueError("provide --seed-json or all coefficient flags: " + ", ".join(missing))
    return ElkiesIdentityFactors(
        p2=args.p2,
        p3=args.p3,
        p4=args.p4,
        p7=args.p7,
        p8=args.p8,
        lam=args.lam,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Beam-search lambda correction branches for a lifted Belyi survivor.")
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--levels", type=int, required=True)
    parser.add_argument("--depth", type=int, required=True)
    parser.add_argument("--beam-width", type=int, required=True)
    parser.add_argument("--max-numerator", type=int, required=True)
    parser.add_argument("--max-denominator", type=int, required=True)
    parser.add_argument("--score-levels", type=int)
    parser.add_argument("--score-max-numerator", type=int)
    parser.add_argument("--score-max-denominator", type=int)
    parser.add_argument("--refine-multiplier", type=int, default=2)
    parser.add_argument("--refine-all", action="store_true")
    parser.add_argument("--score-consistency", action="store_true")
    parser.add_argument("--consistency-min-unique", type=int, default=0)
    parser.add_argument("--initial-prefix", action="append", type=parse_digits)
    parser.add_argument("--checkpoint-dir")
    parser.add_argument("--checkpoint-prefix", default="lambda-branch-search")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--digits", type=parse_digits)
    parser.add_argument("--seed-json")
    parser.add_argument("--solution-index", type=int, default=0)
    parser.add_argument("--p2", type=parse_coefficients)
    parser.add_argument("--p3", type=parse_coefficients)
    parser.add_argument("--p4", type=parse_coefficients)
    parser.add_argument("--p7", type=parse_coefficients)
    parser.add_argument("--p8", type=parse_coefficients)
    parser.add_argument("--lambda", dest="lam", type=int)
    parser.add_argument("--out")
    parser.add_argument("--markdown-out")
    parser.add_argument("--title", default="M23 Belyi Lambda Branch Search")
    args = parser.parse_args()

    seed = seed_from_args(args)

    def emit_progress(event: dict[str, object]) -> None:
        if args.quiet:
            return
        if event["event"] == "depth-start":
            print(
                f"depth {int(event['position']) + 1}/{event['depth']} started: "
                f"expanded={event['expanded']} beam={event['beam_width']}",
                file=sys.stderr,
                flush=True,
            )
        elif event["event"] == "cheap-progress":
            print(
                f"depth {int(event['position']) + 1}: cheap {event['done']}/{event['total']}",
                file=sys.stderr,
                flush=True,
            )
        elif event["event"] == "refine-progress":
            print(
                f"depth {int(event['position']) + 1}: refine {event['done']}/{event['total']}",
                file=sys.stderr,
                flush=True,
            )
        elif event["event"] == "depth-finished":
            best = event.get("best")
            if isinstance(best, dict):
                consistency = (
                    ""
                    if best.get("hard_contradiction_count") is None
                    else (
                        f" hard={best['hard_contradiction_count']}"
                        + f" linear_system={best.get('linear_system_conflict_count', 0)}"
                        + f" linear={best.get('linear_conflict_count', 0)}"
                        + f" linear_solution={best.get('linear_solution_conflict_count', 0)}"
                        + f" groebner={best.get('groebner_conflict_count', 0)}"
                    )
                )
                print(
                    f"depth {int(event['position']) + 1}/{event['depth']} finished: "
                    f"expanded={event['expanded']} refined={event['refined']} "
                    f"best_prefix={best['prefix']} lambda={best['final_lambda']} "
                    f"unique={best['unique_count']}/{best['total_count']} "
                    f"status={best['reconstruction_status']}"
                    + consistency,
                    file=sys.stderr,
                    flush=True,
                )

    if args.checkpoint_dir:
        score_levels = args.score_levels if args.score_levels is not None else min(args.levels, max(1, args.levels - 2))
        score_max_numerator = (
            args.score_max_numerator if args.score_max_numerator is not None else args.max_numerator
        )
        score_max_denominator = (
            args.score_max_denominator if args.score_max_denominator is not None else args.max_denominator
        )
        result = search_lambda_branches_checkpointed(
            seed,
            prime=args.prime,
            levels=args.levels,
            depth=args.depth,
            beam_width=args.beam_width,
            max_numerator=args.max_numerator,
            max_denominator=args.max_denominator,
            score_levels=score_levels,
            score_max_numerator=score_max_numerator,
            score_max_denominator=score_max_denominator,
            refine_multiplier=args.refine_multiplier,
            digits=args.digits,
            initial_prefixes=args.initial_prefix,
            refine_all=args.refine_all,
            score_consistency=args.score_consistency,
            consistency_min_unique=args.consistency_min_unique,
            checkpoint_dir=args.checkpoint_dir,
            checkpoint_prefix=args.checkpoint_prefix,
            resume=args.resume,
            progress_every=args.progress_every,
            progress_callback=emit_progress,
        )
    else:
        result = search_lambda_branches(
            seed,
            prime=args.prime,
            levels=args.levels,
            depth=args.depth,
            beam_width=args.beam_width,
            max_numerator=args.max_numerator,
            max_denominator=args.max_denominator,
            digits=args.digits,
            score_consistency=args.score_consistency,
            consistency_min_unique=args.consistency_min_unique,
        )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    if args.markdown_out:
        markdown_path = Path(args.markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_branch_search_markdown(result, title=args.title), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
