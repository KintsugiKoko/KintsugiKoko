"""Deterministic action item extraction."""

from __future__ import annotations


ACTION_HEADINGS = ("action", "todo", "to do", "next", "follow up")
DIRECTIVE_PREFIXES = (
    "next:",
    "next week",
    "todo:",
    "to do:",
    "action:",
    "task:",
    "follow-up:",
    "follow up:",
)
IMPERATIVE_VERBS = (
    "add",
    "ask",
    "build",
    "create",
    "document",
    "draft",
    "fix",
    "prepare",
    "review",
    "run",
    "test",
    "turn",
    "update",
    "write",
)
NON_ACTION_PREFIXES = (
    "decision:",
    "question:",
    "questions i still have:",
    "open questions:",
    "what confused me:",
    "what worked:",
    "what i practiced:",
    "portfolio proof:",
)


def extract_action_items(text: str, limit: int = 8) -> list[str]:
    """Extract simple action items from note text.

    This intentionally favors explicit task language over broad keywords like
    "should" or "need to" so reflective journal lines do not become tasks.
    """

    items: list[str] = []
    current_heading = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            current_heading = stripped.lstrip("#").strip().lower()
            continue

        cleaned = stripped.strip(" -\t")
        if not cleaned:
            continue

        if is_action_item(cleaned, current_heading):
            items.append(cleaned)
        if len(items) >= limit:
            break
    return items


def is_action_item(line: str, current_heading: str = "") -> bool:
    """Return whether one cleaned line is likely an action item."""

    lower = line.lower()
    if any(lower.startswith(prefix) for prefix in NON_ACTION_PREFIXES):
        return False
    if lower.endswith("?"):
        return False
    if lower.startswith("[ ]"):
        return True
    if any(lower.startswith(prefix) for prefix in DIRECTIVE_PREFIXES):
        return True
    if any(keyword in current_heading for keyword in ACTION_HEADINGS):
        return starts_with_imperative(line)
    return starts_with_imperative(line) and not lower.startswith("created ")


def starts_with_imperative(line: str) -> bool:
    """Detect beginner-readable imperative task bullets."""

    first_word = line.split(maxsplit=1)[0].strip(":").lower()
    return first_word in IMPERATIVE_VERBS
