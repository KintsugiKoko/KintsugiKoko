"""Parse rough QA notes into a structured bug report."""

from __future__ import annotations

import re
from collections import defaultdict

from bug_report_tool.models import BugReport

LABEL_MAP = {
    "actual": "actual_result",
    "actual result": "actual_result",
    "environment": "environment",
    "env": "environment",
    "expected": "expected_result",
    "expected result": "expected_result",
    "note": "notes",
    "notes": "notes",
    "priority": "priority",
    "repro rate": "repro_rate",
    "reproduction rate": "repro_rate",
    "severity": "severity",
    "steps": "steps_to_reproduce",
    "steps to reproduce": "steps_to_reproduce",
    "summary": "title",
    "title": "title",
}

LABEL_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?P<label>[A-Za-z][A-Za-z ]{1,40})\s*(?::|-)\s*(?P<value>.*)$"
)


def parse_note(raw_note: str) -> BugReport:
    """Parse a plain text QA note into a BugReport.

    The parser supports simple labels such as "Title:", "Severity:", and
    "Steps:". Lines before the first label are kept as loose notes. The first
    loose line becomes the title when no explicit title is provided.
    """

    if not raw_note or not raw_note.strip():
        raise ValueError("The QA note is empty.")

    sections: dict[str, list[str]] = defaultdict(list)
    loose_lines: list[str] = []
    current_field: str | None = None

    for original_line in raw_note.splitlines():
        line = original_line.rstrip()

        if not line.strip():
            if current_field:
                sections[current_field].append("")
            continue

        label_match = _match_label(line)
        if label_match:
            current_field, value = label_match
            if value:
                sections[current_field].append(value)
            continue

        if current_field:
            sections[current_field].append(line.strip())
        else:
            loose_lines.append(line.strip())

    title = _first_value(sections.get("title"))
    if not title and loose_lines:
        title = loose_lines[0]
        loose_lines = loose_lines[1:]

    notes = _collapse(sections.get("notes"))
    if loose_lines:
        loose_text = "\n".join(loose_lines)
        notes = f"{notes}\n{loose_text}".strip() if notes else loose_text

    return BugReport(
        title=title or "Untitled Bug Report",
        severity=_first_value(sections.get("severity")) or "Not provided",
        priority=_first_value(sections.get("priority")) or "Not provided",
        environment=_collapse(sections.get("environment")) or "Not provided",
        steps_to_reproduce=_parse_steps(sections.get("steps_to_reproduce", [])),
        expected_result=_collapse(sections.get("expected_result")) or "Not provided",
        actual_result=_collapse(sections.get("actual_result")) or "Not provided",
        repro_rate=_first_value(sections.get("repro_rate")) or "Not provided",
        notes=notes or "No additional notes.",
    )


def _match_label(line: str) -> tuple[str, str] | None:
    match = LABEL_PATTERN.match(line)
    if not match:
        return None

    normalized_label = _normalize_label(match.group("label"))
    field = LABEL_MAP.get(normalized_label)
    if not field:
        return None

    return field, match.group("value").strip()


def _normalize_label(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower().replace("_", " "))


def _first_value(lines: list[str] | None) -> str:
    if not lines:
        return ""
    for line in lines:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _collapse(lines: list[str] | None) -> str:
    if not lines:
        return ""
    return "\n".join(line.strip() for line in lines if line.strip()).strip()


def _parse_steps(lines: list[str]) -> list[str]:
    cleaned_steps = [_clean_step(line) for line in lines if line.strip()]
    cleaned_steps = [step for step in cleaned_steps if step]

    if len(cleaned_steps) == 1:
        split_steps = _split_inline_steps(cleaned_steps[0])
        if len(split_steps) > 1:
            return split_steps

    return cleaned_steps or ["Not provided."]


def _clean_step(line: str) -> str:
    stripped = line.strip()
    return re.sub(r"^(?:\d+[\).\s]+|[-*]\s+)", "", stripped).strip()


def _split_inline_steps(step_text: str) -> list[str]:
    for separator in (" -> ", " > "):
        if separator in step_text:
            return [part.strip() for part in step_text.split(separator) if part.strip()]
    return [step_text]
