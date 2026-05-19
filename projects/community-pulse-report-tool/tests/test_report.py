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

    assert "# Weekly Community Feedback Review Report" in report
    assert "## Executive Summary" in report
    assert "## Sentiment Snapshot" in report
    assert "## Local Feedback Inputs" in report
    assert "## Top Mentioned Topics / Game Areas" in report
    assert "## Topic Opinion Splits" in report
    assert "## Positive Themes" in report
    assert "## Mixed Themes" in report
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
    assert "Generated from local CSV data only" in report
    assert "Built-in sample data is fictional" in report
    assert "The tool does not scrape, monitor, fetch, discover, or ingest live community conversations." in report
    assert "The tool does not perform automated moderation, automated player decisions, or product direction decisions." in report


def test_generate_markdown_report_includes_applied_filters() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "mock-social-post",
                "Onboarding",
                "negative",
                "I needed a clearer first step.",
                account="mock-studio-account",
                post_id="mock-post-001",
                keyword="onboarding",
                topic="Onboarding clarity",
            ),
        ],
        applied_filters={
            "Account": "mock-studio-account",
            "Keyword": "onboarding",
        },
    )

    report = generate_markdown_report(analysis)

    assert "## Filters Applied" in report
    assert "- **Account**: mock-studio-account" in report
    assert "- **Keyword**: onboarding" in report


def test_generated_report_uses_local_feedback_inputs_language() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "fictional-form",
                "Fishing",
                "positive",
                "Fishing felt calm.",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "## Local Feedback Inputs" in report
    assert "## Feedback Sources" not in report


def test_generate_markdown_report_adds_account_and_post_sections_when_present() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "mock-social-post",
                "Onboarding",
                "negative",
                "I needed a clearer first step.",
                account="mock-studio-account",
                post_id="mock-post-001",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "## Accounts Represented" in report
    assert "| mock-studio-account | 1 |" in report
    assert "## Posts Represented" in report
    assert "| mock-post-001 | 1 |" in report


def test_generate_markdown_report_skips_account_and_post_sections_when_missing() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "fictional-form",
                "Fishing",
                "positive",
                "Fishing felt calm.",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "## Accounts Represented" not in report
    assert "## Posts Represented" not in report


def test_generate_markdown_report_includes_topic_opinion_splits() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "mock-social-post",
                "Onboarding",
                "negative",
                "Needs clarity.",
                topic="Onboarding clarity",
            ),
            FeedbackItem(
                "2026-05-02",
                "mock-social-post",
                "Onboarding",
                "mixed",
                "Cute but unclear.",
                topic="Onboarding clarity",
            ),
        ]
    )

    report = generate_markdown_report(analysis)

    assert "- **Onboarding clarity**: 1 negative, 1 mixed" in report
    assert "copied exactly from the CSV `text` field" in report


def test_generate_markdown_report_caps_topics_themes_and_followups() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem("2026-05-01", "source-a", "Area A", "negative", "A."),
            FeedbackItem("2026-05-02", "source-b", "Area B", "negative", "B."),
            FeedbackItem("2026-05-03", "source-c", "Area C", "mixed", "C."),
            FeedbackItem("2026-05-04", "source-d", "Area D", "positive", "D."),
        ],
        quote_limit=2,
    )

    report = generate_markdown_report(
        analysis,
        max_quotes=2,
        max_topics=2,
        max_themes=1,
        max_follow_ups=2,
    )

    assert "_Showing top 2 topics by mention count._" in report
    assert "_Showing top 1 negative themes by mention count._" in report
    assert "_Representative quotes limited to 2 for readability._" in report
    assert "_Suggested follow-ups limited to 2 for readability._" in report


def test_generate_markdown_report_includes_processing_notes() -> None:
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "fictional-form",
                "Fishing",
                "positive",
                "Fishing felt calm.",
            ),
        ],
        processing_notes=["Input parsing limited to the first 1 rows for demo/runtime control."],
    )

    report = generate_markdown_report(analysis)

    assert "## Report Scope Notes" in report
    assert "Input parsing limited to the first 1 rows" in report
