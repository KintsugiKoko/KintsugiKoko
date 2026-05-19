import pytest

from community_pulse.filters import filter_feedback, validate_filter_dates
from community_pulse.models import FeedbackFilters, FeedbackItem


def _items() -> list[FeedbackItem]:
    return [
        FeedbackItem(
            "2026-05-01",
            "mock-social-post",
            "Fishing",
            "positive",
            "Fishing felt calm.",
            account="mock-studio-account",
            post_id="mock-post-001",
            keyword="fishing",
            topic="Fishing timing",
        ),
        FeedbackItem(
            "2026-05-03",
            "mock-comment-digest",
            "Onboarding",
            "negative",
            "I needed a clearer first step.",
            account="mock-community-team",
            post_id="mock-post-002",
            keyword="onboarding",
            topic="Onboarding clarity",
        ),
        FeedbackItem(
            "2026-05-07",
            "mock-playtest-summary",
            "Starwell",
            "mixed",
            "The reward was interesting but unclear.",
            account="mock-playtest-lab",
            post_id="mock-post-003",
            keyword="starwell",
            topic="Starwell offerings",
        ),
    ]


def test_filter_feedback_by_date_range() -> None:
    filters = FeedbackFilters(start_date="2026-05-02", end_date="2026-05-04")

    filtered = filter_feedback(_items(), filters)

    assert [item.text for item in filtered] == ["I needed a clearer first step."]


def test_filter_feedback_by_account() -> None:
    filters = FeedbackFilters(accounts=("mock-studio-account",))

    filtered = filter_feedback(_items(), filters)

    assert len(filtered) == 1
    assert filtered[0].account == "mock-studio-account"


def test_filter_feedback_by_post_id() -> None:
    filters = FeedbackFilters(post_ids=("mock-post-002",))

    filtered = filter_feedback(_items(), filters)

    assert len(filtered) == 1
    assert filtered[0].post_id == "mock-post-002"


def test_filter_feedback_by_keyword() -> None:
    filters = FeedbackFilters(keywords=("onboarding",))

    filtered = filter_feedback(_items(), filters)

    assert len(filtered) == 1
    assert filtered[0].keyword == "onboarding"


def test_filter_feedback_by_topic() -> None:
    filters = FeedbackFilters(topics=("Starwell offerings",))

    filtered = filter_feedback(_items(), filters)

    assert len(filtered) == 1
    assert filtered[0].topic == "Starwell offerings"


def test_validate_filter_dates_rejects_backwards_range() -> None:
    filters = FeedbackFilters(start_date="2026-05-07", end_date="2026-05-01")

    with pytest.raises(ValueError, match="Start date"):
        validate_filter_dates(filters)
