"""Command-line entry point for the draft-only Second Brain Docs Agent."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.extract.summarize import build_extraction
from src.ingest.chatgpt_export import read_chatgpt_exports
from src.ingest.obsidian import read_obsidian_notes
from src.render.markdown import DRAFT_TYPES, write_draft


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local Markdown drafts from notes and chat exports.")
    parser.add_argument("--obsidian-dir", default="data/obsidian_sample", help="Local Obsidian-style notes folder.")
    parser.add_argument("--chatgpt-dir", default="data/chatgpt_sample", help="Local chat export folder.")
    parser.add_argument("--output-dir", default="docs/drafts", help="Folder for generated Markdown drafts.")
    parser.add_argument("--draft-type", default="daily_summary", choices=sorted(DRAFT_TYPES), help="Draft type to render.")
    parser.add_argument("--source", default="all", choices=("all", "obsidian", "chatgpt"), help="Which source to process.")
    args = parser.parse_args()

    generated_paths: list[Path] = []

    if args.source in {"all", "obsidian"}:
        for note in read_obsidian_notes(args.obsidian_dir):
            extraction = build_extraction(note.title, note.body, note.note_type)
            generated_paths.append(write_draft(args.output_dir, extraction, args.draft_type))

    if args.source in {"all", "chatgpt"}:
        for session in read_chatgpt_exports(args.chatgpt_dir):
            extraction = build_extraction(session.title, session.text, "chatgpt_export")
            generated_paths.append(write_draft(args.output_dir, extraction, args.draft_type))

    print(f"Generated {len(generated_paths)} draft(s):")
    for path in generated_paths:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
