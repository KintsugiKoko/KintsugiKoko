from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from community_pulse.models import AnalysisResult, FeedbackItem, OpinionSplit

QUOTE_SENTIMENT_ORDER = ("negative", "mixed", "positive", "neutral")


@dataclass
class _FeedbackCounts:
    sentiment: Counter[str]
    source: Counter[str]
    game_area: Counter[str]
    topic: Counter[str]
    account: Counter[str]
    post: Counter[str]
    positive_topic: Counter[str]
    mixed_topic: Counter[str]
    negative_topic: Counter[str]
    topic_sentiment: dict[str, Counter[str]]


def analyze_feedback(
    feedback_items: Iterable[FeedbackItem],
    quote_limit: int = 8,
    applied_filters: dict[str, str] | None = None,
    processing_notes: list[str] | None = None,
) -> AnalysisResult:
    items = list(feedback_items)
    counts = _aggregate_counts(items)

    return AnalysisResult(
        total_items=len(items),
        sentiment_counts=_sorted_count_dict(counts.sentiment),
        source_counts=_sorted_count_dict(counts.source),
        game_area_counts=_sorted_count_dict(counts.game_area),
        topic_counts=_sorted_count_dict(counts.topic),
        account_counts=_sorted_count_dict(counts.account),
        post_counts=_sorted_count_dict(counts.post),
        positive_areas=_top_areas_by_sentiment(counts.positive_topic),
        mixed_areas=_top_areas_by_sentiment(counts.mixed_topic),
        negative_areas=_top_areas_by_sentiment(counts.negative_topic),
        opinion_splits=_opinion_splits(counts.topic_sentiment),
        representative_quotes=_select_representative_quotes(items, quote_limit),
        applied_filters=applied_filters or {},
        processing_notes=processing_notes or [],
    )


def _aggregate_counts(items: list[FeedbackItem]) -> _FeedbackCounts:
    counts = _FeedbackCounts(
        sentiment=Counter(),
        source=Counter(),
        game_area=Counter(),
        topic=Counter(),
        account=Counter(),
        post=Counter(),
        positive_topic=Counter(),
        mixed_topic=Counter(),
        negative_topic=Counter(),
        topic_sentiment={},
    )

    for item in items:
        topic = _topic_label(item)
        counts.sentiment[item.sentiment] += 1
        counts.source[item.source] += 1
        counts.game_area[item.game_area] += 1
        counts.topic[topic] += 1
        if item.account:
            counts.account[item.account] += 1
        if item.post_id:
            counts.post[item.post_id] += 1
        if item.sentiment == "positive":
            counts.positive_topic[topic] += 1
        if item.sentiment == "mixed":
            counts.mixed_topic[topic] += 1
        if item.sentiment == "negative":
            counts.negative_topic[topic] += 1
        counts.topic_sentiment.setdefault(topic, Counter())[item.sentiment] += 1

    return counts


def _top_areas_by_sentiment(counter: Counter[str]) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))


def _opinion_splits(split_counts: dict[str, Counter[str]]) -> list[OpinionSplit]:
    varied_splits = [
        OpinionSplit(label=label, counts=_ordered_sentiment_counts(counts))
        for label, counts in split_counts.items()
        if len(counts) > 1
    ]
    return sorted(
        varied_splits,
        key=lambda split: (-sum(split.counts.values()), split.label),
    )


def _select_representative_quotes(
    items: list[FeedbackItem],
    quote_limit: int,
) -> list[FeedbackItem]:
    selected: list[FeedbackItem] = []
    selected_indexes: set[int] = set()

    for sentiment in QUOTE_SENTIMENT_ORDER:
        _select_best_quote_for_sentiment(items, sentiment, selected, selected_indexes)

    while len(selected) < quote_limit:
        best_index = _best_diverse_quote_index(items, selected, selected_indexes)
        if best_index is None:
            break
        selected.append(items[best_index])
        selected_indexes.add(best_index)

    return selected[:quote_limit]


def _select_best_quote_for_sentiment(
    items: list[FeedbackItem],
    sentiment: str,
    selected: list[FeedbackItem],
    selected_indexes: set[int],
) -> None:
    best_index = _best_diverse_quote_index(
        items,
        selected,
        selected_indexes,
        required_sentiment=sentiment,
    )
    if best_index is not None:
        selected.append(items[best_index])
        selected_indexes.add(best_index)


def _best_diverse_quote_index(
    items: list[FeedbackItem],
    selected: list[FeedbackItem],
    selected_indexes: set[int],
    required_sentiment: str | None = None,
) -> int | None:
    best_index: int | None = None
    best_score = -1

    for index, item in enumerate(items):
        if index in selected_indexes:
            continue
        if required_sentiment and item.sentiment != required_sentiment:
            continue

        score = _quote_diversity_score(item, selected)
        if score > best_score:
            best_index = index
            best_score = score

    return best_index


def _quote_diversity_score(item: FeedbackItem, selected: list[FeedbackItem]) -> int:
    if not selected:
        return 4

    selected_sentiments = {quote.sentiment for quote in selected}
    selected_topics = {_topic_label(quote) for quote in selected}
    selected_sources = {_source_or_account_label(quote) for quote in selected}
    selected_posts = {quote.post_id for quote in selected if quote.post_id}

    score = 0
    if item.sentiment not in selected_sentiments:
        score += 4
    if _topic_label(item) not in selected_topics:
        score += 3
    if _source_or_account_label(item) not in selected_sources:
        score += 2
    if item.post_id and item.post_id not in selected_posts:
        score += 1
    return score


def _sorted_count_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def _ordered_sentiment_counts(counter: Counter[str]) -> dict[str, int]:
    ordered: dict[str, int] = {}
    for sentiment in QUOTE_SENTIMENT_ORDER:
        if counter.get(sentiment):
            ordered[sentiment] = counter[sentiment]
    for sentiment, count in sorted(counter.items()):
        if sentiment not in ordered:
            ordered[sentiment] = count
    return ordered


def _topic_label(item: FeedbackItem) -> str:
    return item.topic or item.game_area


def _source_or_account_label(item: FeedbackItem) -> str:
    return item.account or item.source
