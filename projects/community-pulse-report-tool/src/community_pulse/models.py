from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedbackItem:
    date: str
    source: str
    game_area: str
    sentiment: str
    text: str


@dataclass(frozen=True)
class AnalysisResult:
    total_items: int
    sentiment_counts: dict[str, int]
    source_counts: dict[str, int]
    game_area_counts: dict[str, int]
    positive_areas: list[tuple[str, int]]
    negative_areas: list[tuple[str, int]]
    representative_quotes: list[FeedbackItem]
