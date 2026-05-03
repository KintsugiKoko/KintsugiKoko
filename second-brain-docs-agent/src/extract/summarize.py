"""Deterministic summary extraction for local draft generation."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.extract.decisions import extract_decisions, extract_open_questions
from src.extract.tasks import extract_action_items


PROOF_KEYWORDS = (
    "built",
    "created",
    "implemented",
    "tested",
    "passed",
    "verified",
    "documented",
    "generated",
    "fixed",
)


@dataclass(frozen=True)
class ExtractionResult:
    """Draft-ready extracted signals from one source."""

    source_title: str
    source_kind: str
    summary: str
    action_items: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    portfolio_proof: list[str] = field(default_factory=list)
    suggested_next_codex_prompt: str = ""


def build_extraction(source_title: str, text: str, source_kind: str = "note") -> ExtractionResult:
    """Build a deterministic extraction result for one note or chat session.

    TODO: Future LLM summarization can plug in here after local draft review,
    privacy rules, and API configuration are intentionally designed.
    """

    summary = summarize_text(text)
    action_items = extract_action_items(text)
    decisions = extract_decisions(text)
    open_questions = extract_open_questions(text)
    portfolio_proof = extract_portfolio_proof(text)
    suggested_prompt = suggest_next_codex_prompt(source_title, source_kind, action_items, open_questions)
    return ExtractionResult(
        source_title=source_title,
        source_kind=source_kind,
        summary=summary,
        action_items=action_items,
        decisions=decisions,
        open_questions=open_questions,
        portfolio_proof=portfolio_proof,
        suggested_next_codex_prompt=suggested_prompt,
    )


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Create a small deterministic summary from the first useful sentences."""

    sentences: list[str] = []
    for line in text.replace("\r\n", "\n").splitlines():
        cleaned = line.strip().strip("- ").strip()
        if should_skip_summary_line(cleaned):
            continue
        sentence = cleaned.rstrip(".")
        if len(sentence) >= 25:
            sentences.append(sentence)
        if len(sentences) >= max_sentences:
            return ". ".join(sentences) + "."
    return "No clear summary could be extracted yet."


def extract_portfolio_proof(text: str, limit: int = 8) -> list[str]:
    """Extract lines that look like concrete evidence."""

    proof: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip(" -\t")
        if not cleaned:
            continue
        if cleaned.endswith(":"):
            continue
        lower = cleaned.lower()
        if any(keyword in lower for keyword in PROOF_KEYWORDS):
            proof.append(cleaned)
        if len(proof) >= limit:
            break
    return proof


def suggest_next_codex_prompt(
    source_title: str,
    source_kind: str,
    action_items: list[str],
    open_questions: list[str],
) -> str:
    """Suggest one local Codex task prompt based on extracted signals."""

    if action_items:
        return (
            f"Review `{source_title}` and turn this action item into a small draft-only docs task: "
            f"{action_items[0]}"
        )
    if open_questions:
        return (
            f"Review `{source_title}` and create a short local research note answering this open question: "
            f"{open_questions[0]}"
        )
    return (
        f"Review `{source_title}` as a {source_kind} source and suggest one small local documentation draft. "
        "Do not publish externally."
    )


def should_skip_summary_line(line: str) -> bool:
    """Return whether a line is likely structure instead of summary content."""

    if not line:
        return True
    if line.startswith("---") or line.startswith("#"):
        return True
    if line.endswith(":"):
        return True
    if line.startswith("[[") and line.endswith("]]"):
        return True
    return False
