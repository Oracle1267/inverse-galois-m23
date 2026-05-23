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
from m23verify.lifting import (
    factors_from_solution_dict,
    lift_elkies_solution_mod_prime_power,
    render_lift_report_markdown,
)


def parse_coefficients(raw: str) -> tuple[int, ...]:
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
    parser = argparse.ArgumentParser(description="Lift a modular Elkies-style M23 Belyi survivor.")
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--levels", type=int, default=2)
    parser.add_argument("--seed-json")
    parser.add_argument("--solution-index", type=int, default=0)
    parser.add_argument("--p2", type=parse_coefficients)
    parser.add_argument("--p3", type=parse_coefficients)
    parser.add_argument("--p4", type=parse_coefficients)
    parser.add_argument("--p7", type=parse_coefficients)
    parser.add_argument("--p8", type=parse_coefficients)
    parser.add_argument("--lambda", dest="lam", type=int)
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument("--markdown-out", help="Optional Markdown report output path")
    parser.add_argument("--title", default="M23 Belyi Lift Report")
    args = parser.parse_args()

    seed = seed_from_args(args)
    result = lift_elkies_solution_mod_prime_power(seed, prime=args.prime, levels=args.levels)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    if args.markdown_out:
        markdown_path = Path(args.markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_lift_report_markdown(result, title=args.title), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
