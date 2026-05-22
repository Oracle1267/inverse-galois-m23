from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.group_data import load_m23_cycle_data
from m23verify.ledger import append_ledger_entry, entry_from_report
from m23verify.report import build_report


def parse_primes(raw: str) -> list[int]:
    primes = [int(item.strip()) for item in raw.split(",") if item.strip()]
    if not primes:
        raise argparse.ArgumentTypeError("at least one prime is required")
    return primes


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify local fingerprints for an M23 candidate polynomial.")
    parser.add_argument("polynomial", help="Polynomial in Magma-like syntax, for example x^23 - x - 1")
    parser.add_argument("--primes", type=parse_primes, default=parse_primes("2,3,5,7,11,13,17,19,23,29,31"))
    parser.add_argument("--data", default=str(ROOT / "data" / "m23_23t5_cycle_types.json"))
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument("--ledger", help="Optional JSONL ledger path to append this verification result")
    parser.add_argument("--generator", default="manual-verify", help="Ledger generator label")
    parser.add_argument("--run-id", help="Optional stable run id for ledger entries")
    args = parser.parse_args()

    cycle_data = load_m23_cycle_data(args.data)
    report = build_report(args.polynomial, primes=args.primes, cycle_data=cycle_data)
    if args.ledger:
        append_ledger_entry(
            args.ledger,
            entry_from_report(report, generator=args.generator, run_id=args.run_id or str(uuid4())),
        )
    output = json.dumps(report, indent=2, sort_keys=True)

    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
