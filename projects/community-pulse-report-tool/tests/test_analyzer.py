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
