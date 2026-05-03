"""Render extraction results into local Markdown drafts."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from src.extract.summarize import ExtractionResult


DRAFT_TYPES = {
    "daily_summary": "Daily Summary",
    "weekly_review_summary": "Weekly Review Summary",
    "project_update": "Project Update",
    "portfolio_update": "Portfolio Update",
    "codex_task_prompt": "Codex Task Prompt",
}


def render_draft(extraction: ExtractionResult, draft_type: str = "daily_summary") -> str:
    """Render one extraction result as Markdown."""

    if draft_type not in DRAFT_TYPES:
        raise ValueError(f"Unsupported draft type: {draft_type}")

    title = DRAFT_TYPES[draft_type]
    if draft_type == "codex_task_prompt":
        return render_codex_prompt(extraction)

    return "\n".join(
        [
            "---",
            f"type: {draft_type}",
            "status: draft",
            "publish: false",
            f"source: {extraction.source_title}",
            f"created: {date.today().isoformat()}",
            "---",
            "",
            f"# {title} - {extraction.source_title}",
            "",
            "> Draft-only. Human review required before publishing anywhere.",
            "",
            "## Summary",
            "",
            extraction.summary,
            "",
            "## Action Items",
            "",
            format_list(extraction.action_items),
            "",
            "## Decisions",
            "",
            format_list(extraction.decisions),
            "",
            "## Open Questions",
            "",
            format_list(extraction.open_questions),
            "",
            "## Portfolio-Worthy Proof",
            "",
            format_list(extraction.portfolio_proof),
            "",
            "## Suggested Next Codex Prompt",
            "",
            "```text",
            extraction.suggested_next_codex_prompt,
            "```",
            "",
        ]
    )


def render_codex_prompt(extraction: ExtractionResult) -> str:
    """Render a copy-ready Codex prompt draft."""

    return "\n".join(
        [
            "---",
            "type: codex_task_prompt",
            "status: draft",
            "publish: false",
            f"source: {extraction.source_title}",
            f"created: {date.today().isoformat()}",
            "---",
            "",
            f"# Codex Task Prompt - {extraction.source_title}",
            "",
            "```text",
            extraction.suggested_next_codex_prompt,
            "```",
            "",
            "## Context",
            "",
            extraction.summary,
            "",
            "## Guardrails",
            "",
            "- Keep changes local and draft-only.",
            "- Do not publish externally.",
            "- Preserve raw source notes.",
            "- Summarize verification steps.",
            "",
        ]
    )


def write_draft(
    output_dir: str | Path,
    extraction: ExtractionResult,
    draft_type: str = "daily_summary",
) -> Path:
    """Write one rendered Markdown draft to disk."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"{date.today().isoformat()}-{slugify(draft_type)}-{slugify(extraction.source_title)}.md"
    draft_path = output_path / filename
    draft_path.write_text(render_draft(extraction, draft_type), encoding="utf-8")
    return draft_path


def format_list(items: list[str]) -> str:
    """Render a list or an empty placeholder."""

    if not items:
        return "- Not found yet."
    return "\n".join(f"- {item}" for item in items)


def slugify(value: str) -> str:
    """Create a filesystem-friendly slug."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:80] or "draft"
