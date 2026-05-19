from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedbackItem:
    date: str
    source: str
    game_area: str
    sentiment: str
    text: str
    account: str = ""
    post_id: str = ""
    keyword: str = ""
    topic: str = ""
    conversation_id: str = ""


@dataclass(frozen=True)
class FeedbackFilters:
    start_date: str = ""
    end_date: str = ""
    sources: tuple[str, ...] = ()
    accounts: tuple[str, ...] = ()
    post_ids: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    topics: tuple[str, ...] = ()


@dataclass(frozen=True)
class OpinionSplit:
    label: str
    counts: dict[str, int]


@dataclass(frozen=True)
class AnalysisResult:
    total_items: int
    sentiment_counts: dict[str, int]
    source_counts: dict[str, int]
    game_area_counts: dict[str, int]
    topic_counts: dict[str, int]
    account_counts: dict[str, int]
    post_counts: dict[str, int]
    positive_areas: list[tuple[str, int]]
    mixed_areas: list[tuple[str, int]]
    negative_areas: list[tuple[str, int]]
    opinion_splits: list[OpinionSplit]
    representative_quotes: list[FeedbackItem]
    applied_filters: dict[str, str]
    processing_notes: list[str]
