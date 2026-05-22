from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.summary import render_markdown_report, summarize_ledger


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize the M23 candidate ledger.")
    parser.add_argument("--ledger", default=str(ROOT / "reports" / "candidate_ledger.jsonl"))
    parser.add_argument("--markdown-out", help="Optional Markdown report output path")
    parser.add_argument("--title", default="M23 Ledger Summary")
    args = parser.parse_args()

    summary = summarize_ledger(args.ledger)
    if args.markdown_out:
        markdown_path = Path(args.markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown_report(summary, title=args.title), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
