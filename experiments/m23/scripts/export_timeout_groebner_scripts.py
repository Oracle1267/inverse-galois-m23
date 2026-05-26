from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.timeout_review import (  # noqa: E402
    export_external_groebner_scripts,
    load_branch_report,
    review_timeout_prefixes_from_report,
)

from search_lambda_branches import load_seed_from_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Sage/Singular Groebner scripts for timeout branches.")
    parser.add_argument("--source-report", required=True)
    parser.add_argument("--prime", type=int, required=True)
    parser.add_argument("--levels", type=int, required=True)
    parser.add_argument("--max-numerator", type=int, required=True)
    parser.add_argument("--max-denominator", type=int, required=True)
    parser.add_argument("--consistency-min-unique", type=int, default=0)
    parser.add_argument("--groebner-timeout-seconds", type=int, default=10)
    parser.add_argument("--seed-json", required=True)
    parser.add_argument("--solution-index", type=int, default=0)
    parser.add_argument("--script-dir", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    os.environ["M23_GROEBNER_TIMEOUT_SECONDS"] = str(args.groebner_timeout_seconds)
    source_report = load_branch_report(Path(args.source_report))
    seed = load_seed_from_json(Path(args.seed_json), solution_index=args.solution_index)
    result = review_timeout_prefixes_from_report(
        source_report,
        seed=seed,
        prime=args.prime,
        levels=args.levels,
        max_numerator=args.max_numerator,
        max_denominator=args.max_denominator,
        consistency_min_unique=args.consistency_min_unique,
    )
    export_result = export_external_groebner_scripts(result, output_dir=Path(args.script_dir))
    result["source_report"] = args.source_report
    result["groebner_timeout_seconds"] = args.groebner_timeout_seconds
    result["external_exports"] = export_result

    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
