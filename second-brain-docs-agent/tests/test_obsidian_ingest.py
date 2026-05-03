from pathlib import Path

from src.ingest.obsidian import classify_note, read_obsidian_notes, split_frontmatter


def test_reads_obsidian_markdown_sample():
    notes = read_obsidian_notes(Path("data/obsidian_sample"))

    titles = {note.title for note in notes}
    assert "Journey Journal - 2026-05-03" in titles
    assert "Weekly Review - 2026-W18" in titles
    assert "Nyx Project Page" in titles

    journal = next(note for note in notes if note.title == "Journey Journal - 2026-05-03")
    assert journal.note_type == "daily"
    assert "qa" in journal.tags
    assert journal.properties["project"] == "Nyx"
    assert "Nyx merchant placeholder interaction" in journal.body
    assert journal.modified_date is not None


def test_classifies_sample_note_types():
    notes = read_obsidian_notes(Path("data/obsidian_sample"))
    note_types = {note.title: note.note_type for note in notes}

    assert note_types["Journey Journal - 2026-05-03"] == "daily"
    assert note_types["Weekly Review - 2026-W18"] == "weekly_review"
    assert note_types["Nyx Project Page"] == "project"
    assert note_types["Prompt Log - Nyx Merchant"] == "prompt"


def test_classifies_notes_from_title_tags_and_properties():
    assert classify_note(Path("notes/2026-05-03.md"), {"tags": ["journey-journal"]}, "# Untitled\nBody") == "daily"
    assert classify_note(Path("reviews/week.md"), {}, "# Weekly Review\nBody") == "weekly_review"
    assert classify_note(Path("notes/idea.md"), {"project": "Nyx"}, "# Nyx\nBody") == "project"
    assert classify_note(Path("notes/log.md"), {}, "# Prompt Log - Nyx\nBody") == "prompt"


def test_extracts_simple_frontmatter():
    properties, body = split_frontmatter("---\ntags:\n  - qa\nproject: Nyx\n---\n# Title\nBody")

    assert properties["tags"] == ["qa"]
    assert properties["project"] == "Nyx"
    assert body.startswith("# Title")
