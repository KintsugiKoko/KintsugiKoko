from pathlib import Path

from src.extract.summarize import build_extraction
from src.render.markdown import render_draft, write_draft


def test_renders_markdown_draft():
    extraction = build_extraction(
        "Nyx Test Note",
        "I built a Nyx service menu. Decision: keep it draft-only. What should I test next? Next: run tests.",
        "project",
    )

    markdown = render_draft(extraction, "project_update")

    assert "# Project Update - Nyx Test Note" in markdown
    assert "Draft-only" in markdown
    assert "Decision: keep it draft-only" in markdown
    assert "Suggested Next Codex Prompt" in markdown


def test_writes_markdown_draft(tmp_path: Path):
    extraction = build_extraction("Daily Note", "Created a QA checklist. Next: review it.", "daily")

    draft_path = write_draft(tmp_path, extraction, "daily_summary")

    assert draft_path.exists()
    assert draft_path.suffix == ".md"
    assert "Daily Summary" in draft_path.read_text(encoding="utf-8")
