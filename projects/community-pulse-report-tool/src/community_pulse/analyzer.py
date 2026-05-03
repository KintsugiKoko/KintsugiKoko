from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from community_pulse.models import AnalysisResult, FeedbackItem

QUOTE_SENTIMENT_ORDER = ("negative", "positive", "mixed", "neutral")


def analyze_feedback(
    feedback_items: Iterable[FeedbackItem],
    quote_limit: int = 6,
) -> AnalysisResult:
    items = list(feedback_items)

    sentiment_counts = Counter(item.sentiment for item in items)
    source_counts = Counter(item.source for item in items)
    game_area_counts = Counter(item.game_area for item in items)

    return AnalysisResult(
        total_items=len(items),
        sentiment_counts=_sorted_count_dict(sentiment_counts),
        source_counts=_sorted_count_dict(source_counts),
        game_area_counts=_sorted_count_dict(game_area_counts),
        positive_areas=_top_areas_by_sentiment(items, "positive"),
        negative_areas=_top_areas_by_sentiment(items, "negative"),
        representative_quotes=_select_representative_quotes(items, quote_limit),
    )


def _top_areas_by_sentiment(
    items: list[FeedbackItem],
    sentiment: str,
) -> list[tuple[str, int]]:
    counter = Counter(item.game_area for item in items if item.sentiment == sentiment)
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))


def _select_representative_quotes(
    items: list[FeedbackItem],
    quote_limit: int,
) -> list[FeedbackItem]:
    selected: list[FeedbackItem] = []
    selected_indexes: set[int] = set()

    for sentiment in QUOTE_SENTIMENT_ORDER:
        for index, item in enumerate(items):
            if index not in selected_indexes and item.sentiment == sentiment:
                selected.append(item)
                selected_indexes.add(index)
                break

    for index, item in enumerate(items):
        if len(selected) >= quote_limit:
            break
        if index not in selected_indexes:
            selected.append(item)
            selected_indexes.add(index)

    return selected[:quote_limit]


def _sorted_count_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))
