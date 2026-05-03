"""Read local Obsidian-style Markdown notes.

This module intentionally uses only the Python standard library. The first MVP
supports simple frontmatter and common Markdown notes without requiring PyYAML.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ObsidianNote:
    """Normalized local Obsidian note."""

    title: str
    file_path: Path
    body: str
    tags: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    modified_date: str | None = None
    note_type: str = "note"


def read_obsidian_notes(folder: str | Path) -> list[ObsidianNote]:
    """Read Markdown files from a local Obsidian-style folder."""

    root = Path(folder)
    if not root.exists():
        raise FileNotFoundError(f"Obsidian folder does not exist: {root}")

    notes: list[ObsidianNote] = []
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        properties, body = split_frontmatter(text)
        title = extract_title(body) or path.stem
        tags = normalize_tags(properties.get("tags")) + extract_inline_tags(body)
        modified_date = datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
        notes.append(
            ObsidianNote(
                title=title,
                file_path=path,
                body=body.strip(),
                tags=sorted(set(tags)),
                properties=properties,
                modified_date=modified_date,
                note_type=classify_note(path, properties, body),
            )
        )
    return notes


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split simple YAML-like frontmatter from a Markdown body."""

    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}, text

    end_marker = normalized.find("\n---\n", 4)
    if end_marker == -1:
        return {}, text

    frontmatter_text = normalized[4:end_marker]
    body = normalized[end_marker + len("\n---\n") :]
    return parse_simple_frontmatter(frontmatter_text), body


def parse_simple_frontmatter(frontmatter_text: str) -> dict[str, Any]:
    """Parse beginner-friendly frontmatter without external dependencies."""

    properties: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if line.startswith("  - ") and current_key:
            existing = properties.setdefault(current_key, [])
            if not isinstance(existing, list):
                existing = [existing]
                properties[current_key] = existing
            existing.append(line[4:].strip().strip('"'))
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        current_key = key.strip()
        value = value.strip()
        if value == "":
            properties[current_key] = []
        elif value.startswith("[") and value.endswith("]"):
            properties[current_key] = [
                item.strip().strip('"').strip("'")
                for item in value[1:-1].split(",")
                if item.strip()
            ]
        else:
            properties[current_key] = value.strip('"').strip("'")

    return properties


def normalize_tags(value: Any) -> list[str]:
    """Normalize frontmatter tags into plain strings."""

    if value is None:
        return []
    if isinstance(value, str):
        return [tag.strip().lstrip("#") for tag in value.split(",") if tag.strip()]
    if isinstance(value, list):
        return [str(tag).strip().lstrip("#") for tag in value if str(tag).strip()]
    return [str(value).strip().lstrip("#")]


def extract_inline_tags(body: str) -> list[str]:
    """Extract simple inline hashtags from Markdown body text."""

    tags: list[str] = []
    for word in body.replace("\n", " ").split():
        if word.startswith("#") and len(word) > 1:
            cleaned = word.lstrip("#").strip(".,:;!?)]}")
            if cleaned and "/" not in cleaned:
                tags.append(cleaned)
    return tags


def extract_title(body: str) -> str | None:
    """Return the first Markdown H1 as a note title."""

    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def classify_note(path: Path, properties: dict[str, Any], body: str) -> str:
    """Classify notes into broad draft-friendly buckets."""

    explicit_type = normalize_classification_text(properties.get("type"))
    tags_text = " ".join(normalize_classification_text(tag) for tag in normalize_tags(properties.get("tags")))
    path_text = normalize_classification_text(path)
    body_start = normalize_classification_text(body[:800])
    title = normalize_classification_text(extract_title(body) or path.stem)
    project_property = normalize_classification_text(properties.get("project"))
    combined = " ".join([explicit_type, tags_text, path_text, body_start, title, project_property])

    if "weekly review" in combined or "weekly" in explicit_type:
        return "weekly_review"
    if "prompt log" in combined or "prompt" in explicit_type or "prompt" in title:
        return "prompt"
    if "journey journal" in combined or "daily note" in combined or "daily" in explicit_type:
        return "daily"
    if "project page" in combined or "project" in explicit_type or project_property:
        return "project"
    return "note"


def normalize_classification_text(value: Any) -> str:
    """Normalize text for simple note classification."""

    normalized = str(value or "").lower()
    for character in ("-", "_", "\\", "/", "."):
        normalized = normalized.replace(character, " ")
    return " ".join(normalized.split())
