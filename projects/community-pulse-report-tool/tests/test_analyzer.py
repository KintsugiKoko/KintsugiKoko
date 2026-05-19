from community_pulse.analyzer import analyze_feedback
from community_pulse.models import FeedbackItem


def _items() -> list[FeedbackItem]:
    return [
        FeedbackItem("2026-05-01", "fictional-form", "Fishing", "positive", "Fun."),
        FeedbackItem("2026-05-01", "mock-note", "Fishing", "negative", "Unclear cue."),
        FeedbackItem("2026-05-02", "mock-note", "Starwell", "negative", "Needs feedback."),
        FeedbackItem("2026-05-02", "fictional-form", "Starwell", "positive", "Clear goal."),
        FeedbackItem("2026-05-03", "mock-note", "Starwell", "negative", "Still unclear."),
    ]


def test_analyze_feedback_counts_sentiment_totals() -> None:
    analysis = analyze_feedback(_items())

    assert analysis.total_items == 5
    assert analysis.sentiment_counts["negative"] == 3
    assert analysis.sentiment_counts["positive"] == 2


def test_analyze_feedback_counts_game_areas() -> None:
    analysis = analyze_feedback(_items())

    assert analysis.game_area_counts["Starwell"] == 3
    assert analysis.game_area_counts["Fishing"] == 2


def test_analyze_feedback_identifies_top_positive_and_negative_areas() -> None:
    analysis = analyze_feedback(_items())

    assert analysis.positive_areas == [("Fishing", 1), ("Starwell", 1)]
    assert analysis.negative_areas[0] == ("Starwell", 2)


def test_analyze_feedback_selects_representative_quotes() -> None:
    analysis = analyze_feedback(_items(), quote_limit=3)

    assert len(analysis.representative_quotes) == 3
    assert analysis.representative_quotes[0].sentiment == "negative"
    assert analysis.representative_quotes[1].sentiment == "positive"


def test_analyze_feedback_quotes_preserve_exact_text_and_include_mixed() -> None:
    exact_negative = "I could not tell what changed after the offering."
    exact_mixed = "The idea is cozy, but the reward cue needs work."
    analysis = analyze_feedback(
        [
            FeedbackItem(
                "2026-05-01",
                "mock-social-post",
                "Starwell",
                "positive",
                "The offering goal is clear.",
                topic="Starwell offerings",
                post_id="mock-post-001",
            ),
            FeedbackItem(
                "2026-05-02",
                "mock-comment-digest",
                "Starwell",
                "negative",
                exact_negative,
                topic="Starwell offerings",
                post_id="mock-post-002",
            ),
            FeedbackItem(
                "2026-05-03",
                "mock-comment-digest",
                "Fishing",
                "mixed",
                exact_mixed,
                topic="Fishing timing",
                post_id="mock-post-003",
            ),
        ],
        quote_limit=3,
    )

    quote_texts = [quote.text for quote in analysis.representative_quotes]

    assert exact_negative in quote_texts
    assert exact_mixed in quote_texts
    assert analysis.representative_quotes[0].text == exact_negative
    assert analysis.representative_quotes[1].text == exact_mixed


def test_analyze_feedback_counts_topic_opinion_splits() -> None:
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
            FeedbackItem(
                "2026-05-03",
                "mock-social-post",
                "Onboarding",
                "positive",
                "Clearer now.",
                topic="Onboarding clarity",
            ),
        ]
    )

    assert len(analysis.opinion_splits) == 1
    assert analysis.opinion_splits[0].label == "Onboarding clarity"
    assert analysis.opinion_splits[0].counts == {
        "negative": 1,
        "mixed": 1,
        "positive": 1,
    }
