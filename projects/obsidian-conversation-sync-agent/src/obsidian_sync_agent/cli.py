from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import config_from_values
from .sync import SyncResult, sync_conversations


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = config_from_values(
            source=args.source,
            vault=args.vault,
            folder=args.folder,
            tags=args.tag,
            config_path=Path(args.config).expanduser() if args.config else None,
        )
        result = sync_conversations(config, dry_run=args.dry_run, force=args.force)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    _print_result(result)
    return 1 if result.errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync exported AI conversations into Obsidian-friendly Markdown notes."
    )
    parser.add_argument("--config", help="Optional JSON config file.")
    parser.add_argument("--source", help="Conversation export file or folder.")
    parser.add_argument("--vault", help="Obsidian vault folder.")
    parser.add_argument("--folder", help="Folder inside the vault for synced notes.")
    parser.add_argument(
        "--tag",
        action="append",
        help="Tag to add to each note. Repeat this option for multiple tags.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing notes.")
    parser.add_argument("--force", action="store_true", help="Rewrite notes even when the source is unchanged.")
    return parser


def _print_result(result: SyncResult) -> None:
    for action in result.actions:
        print(f"{action.action}: {action.title} -> {action.note_path}")

    if result.errors:
        print("\nErrors:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)

    print(
        "\nSummary: "
        f"{result.created} created, "
        f"{result.updated} updated, "
        f"{result.skipped} skipped, "
        f"{result.planned} planned, "
        f"{len(result.errors)} errors"
    )
