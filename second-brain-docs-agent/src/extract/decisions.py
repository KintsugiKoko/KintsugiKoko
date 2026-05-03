"""Deterministic decision and question extraction."""

from __future__ import annotations


DECISION_KEYWORDS = ("decided", "decision", "chose", "now i think", "settled on", "will use")


def extract_decisions(text: str, limit: int = 8) -> list[str]:
    """Extract simple decision lines from note text."""

    decisions: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip(" -\t")
        if not cleaned:
            continue
        lower = cleaned.lower()
        if any(keyword in lower for keyword in DECISION_KEYWORDS):
            decisions.append(cleaned)
        if len(decisions) >= limit:
            break
    return decisions


def extract_open_questions(text: str, limit: int = 8) -> list[str]:
    """Extract open questions from note text."""

    questions: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip(" -\t")
        if not cleaned:
            continue
        lower = cleaned.lower()
        if lower.endswith(":") and not cleaned.endswith("?"):
            continue
        if cleaned.endswith("?") or "still unclear" in lower:
            questions.append(cleaned)
        if len(questions) >= limit:
            break
    return questions
