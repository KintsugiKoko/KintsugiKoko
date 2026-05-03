from community_pulse.analyzer import analyze_feedback
from community_pulse.models import FeedbackItem
from community_pulse.report import generate_markdown_report


def test_generate_markdown_report_includes_required_sections() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "fictional-form",
                "Fishing",
                "positive",
                "Fishing felt calm.",
            ),
            FeedbackItem(
                "2026-05-02",
                "mock-note",
                "Onboarding",
                "negative",
                "I needed a clearer first step.",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "# Weekly Community Sentiment Report" in report
    assert "## Executive Summary" in report
    assert "## Sentiment Snapshot" in report
    assert "## Feedback Sources" in report
    assert "## Top Mentioned Game Areas" in report
    assert "## Positive Themes" in report
    assert "## Negative Themes" in report
    assert "## Representative Quotes" in report
    assert "## Suggested Follow-ups" in report
    assert "## Method / Limitations" in report


def test_generate_markdown_report_includes_counts_and_quotes() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "fictional-form",
                "Fishing",
                "positive",
                "Fishing felt calm.",
            ),
            FeedbackItem(
                "2026-05-02",
                "mock-note",
                "Onboarding",
                "negative",
                "I needed a clearer first step.",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "| positive | 1 |" in report
    assert "| negative | 1 |" in report
    assert "| Fishing | 1 |" in report
    assert "| fictional-form | 1 |" in report
    assert '"I needed a clearer first step."' in report
    assert "fictional sample data only" in report
