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


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the Elkies-style M23 Belyi identity over GF(p).")
    parser.add_argument("--modulus", type=int, required=True)
    parser.add_argument("--max-solutions", type=int, default=10)
    parser.add_argument("--max-left-factor-triples", type=int)
    parser.add_argument("--require-coprime-left", action="store_true")
    parser.add_argument("--require-nonzero-lambda", action="store_true")
    parser.add_argument("--require-derivative", action="store_true")
    parser.add_argument("--require-translation-normalized", action="store_true")
    parser.add_argument("--coprime-first", action="store_true")
    parser.add_argument("--fixed-p2", type=parse_coefficients)
    parser.add_argument("--fixed-p3", type=parse_coefficients)
    parser.add_argument("--fixed-p4", type=parse_coefficients)
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument("--markdown-out", help="Optional Markdown report output path")
    parser.add_argument("--title", default="M23 Belyi Finite-Field Search Report")
    args = parser.parse_args()

    result = search_elkies_identity_mod_prime(
        modulus=args.modulus,
        max_solutions=args.max_solutions,
        max_left_factor_triples=args.max_left_factor_triples,
        require_coprime_left=args.require_coprime_left,
        require_nonzero_lambda=args.require_nonzero_lambda,
        require_derivative=args.require_derivative,
        require_translation_normalized=args.require_translation_normalized,
        coprime_first=args.coprime_first,
        fixed_p2=args.fixed_p2,
        fixed_p3=args.fixed_p3,
        fixed_p4=args.fixed_p4,
    )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    if args.markdown_out:
        markdown_path = Path(args.markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_belyi_search_markdown(result, title=args.title), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
