"""Command-line interface for the QA bug report tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bug_report_tool.markdown import format_markdown
from bug_report_tool.parser import parse_note


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""

    cli_parser = build_parser()
    args = cli_parser.parse_args(argv)

    try:
        if args.batch:
            converted_count = _convert_batch(args.input_dir, args.output_dir)
            print(f"Converted {converted_count} note(s) to {args.output_dir}.")
            return 0

        raw_note = _read_note(args)
        markdown = format_markdown(parse_note(raw_note))
        _write_report(markdown, args.output)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Turn rough QA notes into structured Markdown bug reports. "
            "Use it for one note at a time, or batch-convert a folder of .txt notes."
        ),
        epilog="""Examples:
  Convert one sample note and print the Markdown:
    python -m bug_report_tool sample-data/001-inventory-count-note.txt

  Convert one note and save the report:
    python -m bug_report_tool sample-data/001-inventory-count-note.txt --output reports/001-inventory-count.md

  Convert every .txt note in sample-data/ to reports/:
    python -m bug_report_tool --batch

  Convert a custom notes folder:
    python -m bug_report_tool --batch --input-dir my-notes --output-dir my-reports

  Pass a short note directly:
    python -m bug_report_tool --text "Title: Button does not respond"

  Read a note from stdin:
    Get-Content sample-data/001-inventory-count-note.txt | python -m bug_report_tool
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help=(
            "Path to one plain text QA note. Use '-' or omit this argument to read "
            "from stdin."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Save one generated Markdown report to this path instead of printing it.",
    )
    parser.add_argument(
        "--text",
        help="QA note text passed directly on the command line. Overrides the input path.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Convert every .txt note in --input-dir to Markdown reports in --output-dir.",
    )
    parser.add_argument(
        "--input-dir",
        default="sample-data",
        help="Folder of .txt notes for batch mode. Default: sample-data.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Folder for generated Markdown reports in batch mode. Default: reports.",
    )
    return parser


def _read_note(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text

    if args.input == "-":
        return sys.stdin.read()

    return Path(args.input).read_text(encoding="utf-8")


def _write_report(markdown: str, output: str | None) -> None:
    if not output:
        print(markdown)
        return

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{markdown}\n", encoding="utf-8")


def _convert_batch(input_dir: str, output_dir: str) -> int:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.is_dir():
        raise ValueError(f"Input folder does not exist: {input_path}")

    note_paths = sorted(input_path.glob("*.txt"))
    if not note_paths:
        raise ValueError(f"No .txt notes found in: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    for note_path in note_paths:
        markdown = format_markdown(parse_note(note_path.read_text(encoding="utf-8")))
        report_path = output_path / _report_filename(note_path)
        report_path.write_text(f"{markdown}\n", encoding="utf-8")

    return len(note_paths)


def _report_filename(note_path: Path) -> str:
    stem = note_path.stem
    if stem.endswith("-note"):
        stem = stem[: -len("-note")]
    return f"{stem}.md"
