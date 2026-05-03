from __future__ import annotations

import argparse
import sys
from pathlib import Path

from community_pulse.analyzer import analyze_feedback
from community_pulse.parser import parse_feedback_csv
from community_pulse.report import generate_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="community-pulse",
        description=(
            "Turn fictional community feedback CSV data into a weekly Markdown "
            "sentiment report."
        ),
    )
    parser.add_argument("csv_path", help="Path to the fictional weekly feedback CSV.")
    parser.add_argument(
        "--output",
        "-o",
        help="Optional path for the generated Markdown report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        feedback = parse_feedback_csv(args.csv_path)
        analysis = analyze_feedback(feedback)
        markdown = generate_markdown_report(analysis)
    except OSError as error:
        print(f"Error reading input: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote weekly report to {output_path}")
    else:
        print(markdown)

    return 0
