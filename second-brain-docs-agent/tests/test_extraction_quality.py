from src.extract.summarize import build_extraction
from src.extract.decisions import extract_open_questions
from src.extract.summarize import extract_portfolio_proof, summarize_text
from src.extract.tasks import extract_action_items


def test_action_extraction_avoids_reflection_and_questions():
    text = """
# Journey Journal

I keep getting confused about tidy notes. I need to keep raw journaling untouched so I can measure improvement.

Questions I still have:

- How should I tag notes that could become portfolio updates?

Decision: the docs agent should generate draft suggestions only.

Next: create a draft-only agent that can turn notes into Markdown summaries.
"""

    assert extract_action_items(text) == [
        "Next: create a draft-only agent that can turn notes into Markdown summaries."
    ]


def test_action_extraction_handles_explicit_task_sections():
    text = """
## Action Items

- Review the latest Journey Journal entry.
- Add tests for classification.
- What should I do with private notes?
"""

    assert extract_action_items(text) == [
        "Review the latest Journey Journal entry.",
        "Add tests for classification.",
    ]


def test_suggested_prompt_uses_clear_next_step_not_confusion_line():
    extraction = build_extraction(
        "Journal",
        "I need to keep my raw note intact.\n\nNext: draft a portfolio update from the reviewed note.",
        "daily",
    )

    assert "Next: draft a portfolio update" in extraction.suggested_next_codex_prompt
    assert "raw note intact" not in extraction.suggested_next_codex_prompt


def test_question_and_proof_extraction_skip_section_labels():
    text = """
Questions I still have:
- What should I test next?

Current implemented proof:
- Built a local draft generator.
"""

    assert extract_open_questions(text) == ["What should I test next?"]
    assert extract_portfolio_proof(text) == ["Built a local draft generator."]


def test_summary_skips_section_labels():
    text = """
# Project Page

Current implemented proof:
- Built a source-level fishing loop foundation.
- Created a Starwell offering path.
"""

    assert summarize_text(text, max_sentences=2) == (
        "Built a source-level fishing loop foundation. Created a Starwell offering path."
    )
