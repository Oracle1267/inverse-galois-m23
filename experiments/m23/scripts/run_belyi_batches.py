from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.belyi import render_belyi_search_markdown, search_elkies_identity_mod_prime


def parse_coefficients(raw: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in raw.split(",") if item.strip())


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_batch(args: argparse.Namespace, start: int, end: int) -> dict:
    return search_elkies_identity_mod_prime(
        modulus=args.modulus,
        max_solutions=args.max_solutions,
        max_left_factor_triples=end - start,
        start_left_factor_triples=start,
        require_coprime_left=args.require_coprime_left,
        require_nonzero_lambda=args.require_nonzero_lambda,
        require_derivative=args.require_derivative,
        require_translation_normalized=args.require_translation_normalized,
        coprime_first=args.coprime_first,
        normalized_first=args.normalized_first,
        derivative_first=args.derivative_first,
        derive_lambda=args.derive_lambda,
        fixed_p2=args.fixed_p2,
        fixed_p3=args.fixed_p3,
        fixed_p4=args.fixed_p4,
    )


def batch_record(start: int, end: int, json_path: Path, markdown_path: Path, result: dict) -> dict:
    return {
        "start_left_factor_triples": start,
        "end_left_factor_triples": end,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "tested_left_factor_triples": result["tested_left_factor_triples"],
        "tested_lambda_values": result["tested_lambda_values"],
        "solutions": result["solutions"],
        "stopped_reason": result["stopped_reason"],
    }


def emit_progress(start: int, end: int, current: int, result: dict, reused: bool, quiet: bool) -> None:
    if quiet:
        return
    action = "reused" if reused else "finished"
    print(
        " ".join(
            [
                f"batch {start}-{end} {action}:",
                f"tested={result['tested_left_factor_triples']}",
                f"lambda={result['tested_lambda_values']}",
                f"solutions={len(result['solutions'])}",
                f"stop={result['stopped_reason']}",
                f"next={current}",
            ]
        ),
        file=sys.stderr,
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run resumable batches of the Elkies-style M23 Belyi search.")
    parser.add_argument("--modulus", type=int, required=True)
    parser.add_argument("--start-left-factor-triples", type=int, default=0)
    parser.add_argument("--stop-left-factor-triples", type=int, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--max-solutions", type=int, default=1)
    parser.add_argument("--require-coprime-left", action="store_true")
    parser.add_argument("--require-nonzero-lambda", action="store_true")
    parser.add_argument("--require-derivative", action="store_true")
    parser.add_argument("--require-translation-normalized", action="store_true")
    parser.add_argument("--coprime-first", action="store_true")
    parser.add_argument("--normalized-first", action="store_true")
    parser.add_argument("--derivative-first", action="store_true")
    parser.add_argument("--derive-lambda", action="store_true")
    parser.add_argument("--fixed-p2", type=parse_coefficients)
    parser.add_argument("--fixed-p3", type=parse_coefficients)
    parser.add_argument("--fixed-p4", type=parse_coefficients)
    parser.add_argument("--report-dir", default=str(ROOT / "reports"))
    parser.add_argument("--report-prefix", default=None)
    parser.add_argument("--summary-out")
    parser.add_argument("--force", action="store_true", help="Overwrite existing batch reports instead of reusing them")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-batch progress output")
    args = parser.parse_args()

    if args.start_left_factor_triples < 0:
        raise ValueError("start-left-factor-triples must be nonnegative")
    if args.stop_left_factor_triples < args.start_left_factor_triples:
        raise ValueError("stop-left-factor-triples must be greater than or equal to start-left-factor-triples")
    if args.batch_size <= 0:
        raise ValueError("batch-size must be positive")

    report_dir = Path(args.report_dir)
    prefix = args.report_prefix or f"belyi-gf{args.modulus}-batches"
    summary_path = Path(args.summary_out) if args.summary_out else report_dir / f"{prefix}-summary.json"

    batches = []
    all_solutions: list[dict] = []
    tested_total = 0
    lambda_total = 0
    current = args.start_left_factor_triples
    stopped_reason = "target_reached"

    while current < args.stop_left_factor_triples:
        batch_start = current
        end = min(batch_start + args.batch_size, args.stop_left_factor_triples)
        json_path = report_dir / f"{prefix}-{current}-{end}.json"
        markdown_path = report_dir / f"{prefix}-{current}-{end}.md"
        reused = json_path.exists() and markdown_path.exists() and not args.force

        if reused:
            result = json.loads(json_path.read_text(encoding="utf-8"))
        else:
            result = run_batch(args, start=batch_start, end=end)
            title = f"M23 Belyi GF({args.modulus}) Batch {batch_start}-{end}"
            write_json(json_path, result)
            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(render_belyi_search_markdown(result, title=title), encoding="utf-8")

        batches.append(batch_record(batch_start, end, json_path, markdown_path, result))
        all_solutions.extend(result["solutions"])
        tested_total += result["tested_left_factor_triples"]
        lambda_total += result["tested_lambda_values"]
        current += result["tested_left_factor_triples"]
        emit_progress(
            start=batch_start,
            end=end,
            current=current,
            result=result,
            reused=reused,
            quiet=args.quiet,
        )

        if result["solutions"]:
            stopped_reason = "solution_found"
            break
        if result["stopped_reason"] == "exhausted":
            stopped_reason = "exhausted"
            break
        if result["tested_left_factor_triples"] == 0:
            stopped_reason = "no_progress"
            break

    summary = {
        "modulus": args.modulus,
        "start_left_factor_triples": args.start_left_factor_triples,
        "stop_left_factor_triples": args.stop_left_factor_triples,
        "next_start_left_factor_triples": current,
        "batch_size": args.batch_size,
        "tested_left_factor_triples": tested_total,
        "tested_lambda_values": lambda_total,
        "solutions": all_solutions,
        "stopped_reason": stopped_reason,
        "report_dir": str(report_dir),
        "report_prefix": prefix,
        "batches": batches,
    }
    write_json(summary_path, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
