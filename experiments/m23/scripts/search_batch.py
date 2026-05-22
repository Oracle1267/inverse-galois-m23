from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.families import parse_int_range
from m23verify.search import run_search_batch


def normalize_range_args(argv: list[str]) -> list[str]:
    normalized: list[str] = []
    index = 0
    while index < len(argv):
        item = argv[index]
        if item in {"--a-range", "--b-range"} and index + 1 < len(argv):
            normalized.append(f"{item}={argv[index + 1]}")
            index += 2
            continue
        normalized.append(item)
        index += 1
    return normalized


def parse_primes(raw: str) -> list[int]:
    primes = [int(item.strip()) for item in raw.split(",") if item.strip()]
    if not primes:
        raise argparse.ArgumentTypeError("at least one prime is required")
    return primes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a resumable batch search for M23 candidate polynomials.")
    parser.add_argument("--family", default="trinomial", choices=["trinomial"])
    parser.add_argument("--a-range", type=parse_int_range, default=parse_int_range("-20:20"))
    parser.add_argument("--b-range", type=parse_int_range, default=parse_int_range("-20:20"))
    parser.add_argument("--primes", type=parse_primes, default=parse_primes("2,3,5,7,11,13,17,19,23,29,31"))
    parser.add_argument("--max-candidates", type=int, default=100)
    parser.add_argument("--ledger", default=str(ROOT / "reports" / "candidate_ledger.jsonl"))
    parser.add_argument("--data", default=str(ROOT / "data" / "m23_23t5_cycle_types.json"))
    parser.add_argument("--run-id", help="Optional stable label for this batch run")
    parser.add_argument(
        "--continue-on-survivor",
        action="store_true",
        help="Keep testing after a candidate survives the local filters.",
    )
    args = parser.parse_args(normalize_range_args(argv or sys.argv[1:]))

    result = run_search_batch(
        family=args.family,
        a_range=args.a_range,
        b_range=args.b_range,
        primes=args.primes,
        max_candidates=args.max_candidates,
        ledger_path=args.ledger,
        data_path=args.data,
        stop_on_survivor=not args.continue_on_survivor,
        run_id=args.run_id,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
