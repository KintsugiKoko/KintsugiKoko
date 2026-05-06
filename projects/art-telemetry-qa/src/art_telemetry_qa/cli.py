from __future__ import annotations

import argparse
import sys
from pathlib import Path

from art_telemetry_qa.jira_writer import write_jira_ready_bugs
from art_telemetry_qa.parser import load_scan_inputs
from art_telemetry_qa.report_writer import write_reports
from art_telemetry_qa.rules import evaluate_rules
from art_telemetry_qa.scoring import build_scan_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="art-telemetry-qa",
        description=(
            "Parse mock Unreal-style Art QA telemetry data and generate "
            "human-reviewed QA report drafts."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan sample telemetry and validation files.")
    scan.add_argument("--input", required=True, help="Folder containing sample input files.")
    scan.add_argument("--output", required=True, help="Folder where reports should be written.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return _scan(Path(args.input), Path(args.output))

    parser.error(f"Unsupported command: {args.command}")
    return 2


def _scan(input_dir: Path, output_dir: Path) -> int:
    try:
        scan_inputs = load_scan_inputs(input_dir)
        findings = evaluate_rules(scan_inputs)
        result = build_scan_result(len(scan_inputs.telemetry), findings)
        write_reports(result, output_dir)
        write_jira_ready_bugs(result, output_dir)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Scanned {result.total_assets} assets.")
    print(f"Generated {len(result.findings)} finding(s).")
    print(f"Wrote reports to {output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
