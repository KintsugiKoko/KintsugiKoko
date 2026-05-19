from __future__ import annotations

import argparse
import sys
from pathlib import Path

from community_pulse.analyzer import analyze_feedback
from community_pulse.filters import describe_filters, filter_feedback, validate_filter_dates
from community_pulse.models import FeedbackFilters
from community_pulse.parser import parse_feedback_csv
from community_pulse.report import (
    DEFAULT_MAX_FOLLOW_UPS,
    DEFAULT_MAX_QUOTES,
    DEFAULT_MAX_THEMES,
    DEFAULT_MAX_TOPICS,
    generate_markdown_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="community-pulse",
        description=(
            "Turn fictional or manually prepared local feedback CSV data into "
            "a human-reviewed Markdown feedback report."
        ),
    )
    parser.add_argument(
        "csv_path",
        help="Path to the fictional or manually prepared local feedback CSV.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional path for the generated Markdown report.",
    )
    parser.add_argument("--start-date", help="Only include feedback on or after YYYY-MM-DD.")
    parser.add_argument("--end-date", help="Only include feedback on or before YYYY-MM-DD.")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Only include rows from this source. Can be used more than once.",
    )
    parser.add_argument(
        "--account",
        action="append",
        default=[],
        help="Only include rows from this fictional/local account. Can be used more than once.",
    )
    parser.add_argument(
        "--post-id",
        action="append",
        default=[],
        help="Only include rows tied to this fictional/local post ID. Can be used more than once.",
    )
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Only include rows with this local keyword label. Can be used more than once.",
    )
    parser.add_argument(
        "--topic",
        action="append",
        default=[],
        help="Only include rows with this local topic label. Can be used more than once.",
    )
    parser.add_argument(
        "--max-quotes",
        type=_positive_int,
        default=DEFAULT_MAX_QUOTES,
        help=f"Maximum representative quotes to include. Default: {DEFAULT_MAX_QUOTES}.",
    )
    parser.add_argument(
        "--max-topics",
        type=_positive_int,
        default=DEFAULT_MAX_TOPICS,
        help=(
            "Maximum topics, sources, accounts, posts, and opinion splits to "
            f"show. Default: {DEFAULT_MAX_TOPICS}."
        ),
    )
    parser.add_argument(
        "--max-themes",
        type=_positive_int,
        default=DEFAULT_MAX_THEMES,
        help=f"Maximum positive/mixed/negative themes to show. Default: {DEFAULT_MAX_THEMES}.",
    )
    parser.add_argument(
        "--max-follow-ups",
        type=_positive_int,
        default=DEFAULT_MAX_FOLLOW_UPS,
        help=f"Maximum suggested follow-ups to show. Default: {DEFAULT_MAX_FOLLOW_UPS}.",
    )
    parser.add_argument(
        "--max-rows",
        type=_positive_int,
        help="Optional demo/testing limit for the number of CSV rows to parse.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        feedback = parse_feedback_csv(args.csv_path, max_rows=args.max_rows)
        filters = _filters_from_args(args)
        validate_filter_dates(filters)
        filtered_feedback = filter_feedback(feedback, filters)
        analysis = analyze_feedback(
            filtered_feedback,
            quote_limit=args.max_quotes,
            applied_filters=describe_filters(filters),
            processing_notes=_processing_notes_from_args(args),
        )
        markdown = generate_markdown_report(
            analysis,
            max_quotes=args.max_quotes,
            max_topics=args.max_topics,
            max_themes=args.max_themes,
            max_follow_ups=args.max_follow_ups,
        )
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
        print(f"Wrote report to {output_path}")
    else:
        print(markdown)

    return 0


def _filters_from_args(args: argparse.Namespace) -> FeedbackFilters:
    return FeedbackFilters(
        start_date=args.start_date or "",
        end_date=args.end_date or "",
        sources=tuple(args.source),
        accounts=tuple(args.account),
        post_ids=tuple(args.post_id),
        keywords=tuple(args.keyword),
        topics=tuple(args.topic),
    )


def _processing_notes_from_args(args: argparse.Namespace) -> list[str]:
    if not args.max_rows:
        return []

    return [
        f"Input parsing limited to the first {args.max_rows} rows for demo/runtime control."
    ]


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be 1 or greater")
    return parsed
