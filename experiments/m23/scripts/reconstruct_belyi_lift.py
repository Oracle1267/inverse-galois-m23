from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.reconstruction import reconstruct_lift_report, render_reconstruction_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Attempt rational reconstruction of a lifted M23 Belyi survivor.")
    parser.add_argument("--lift-json", required=True)
    parser.add_argument("--max-numerator", type=int, required=True)
    parser.add_argument("--max-denominator", type=int, required=True)
    parser.add_argument("--out")
    parser.add_argument("--markdown-out")
    parser.add_argument("--title", default="M23 Belyi Reconstruction Report")
    args = parser.parse_args()

    lift_report = json.loads(Path(args.lift_json).read_text(encoding="utf-8"))
    result = reconstruct_lift_report(
        lift_report,
        max_numerator=args.max_numerator,
        max_denominator=args.max_denominator,
    )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    if args.markdown_out:
        markdown_path = Path(args.markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_reconstruction_markdown(result, title=args.title), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
