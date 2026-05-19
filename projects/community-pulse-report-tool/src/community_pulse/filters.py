from __future__ import annotations

from datetime import date
from typing import Iterable

from community_pulse.models import FeedbackFilters, FeedbackItem


def filter_feedback(
    feedback_items: Iterable[FeedbackItem],
    filters: FeedbackFilters,
) -> list[FeedbackItem]:
    return [item for item in feedback_items if _matches_filters(item, filters)]


def describe_filters(filters: FeedbackFilters) -> dict[str, str]:
    descriptions: dict[str, str] = {}
    if filters.start_date:
        descriptions["Start date"] = filters.start_date
    if filters.end_date:
        descriptions["End date"] = filters.end_date
    if filters.sources:
        descriptions["Source"] = ", ".join(filters.sources)
    if filters.accounts:
        descriptions["Account"] = ", ".join(filters.accounts)
    if filters.post_ids:
        descriptions["Post ID"] = ", ".join(filters.post_ids)
    if filters.keywords:
        descriptions["Keyword"] = ", ".join(filters.keywords)
    if filters.topics:
        descriptions["Topic"] = ", ".join(filters.topics)
    return descriptions


def validate_filter_dates(filters: FeedbackFilters) -> None:
    if filters.start_date:
        _parse_date(filters.start_date, "start date")
    if filters.end_date:
        _parse_date(filters.end_date, "end date")
    if filters.start_date and filters.end_date and filters.start_date > filters.end_date:
        raise ValueError("Start date must be before or equal to end date.")


def _matches_filters(item: FeedbackItem, filters: FeedbackFilters) -> bool:
    if filters.start_date or filters.end_date:
        item_date = _parse_date(item.date, "feedback item date")
        if filters.start_date and item_date < _parse_date(filters.start_date, "start date"):
            return False
        if filters.end_date and item_date > _parse_date(filters.end_date, "end date"):
            return False

    return (
        _matches_any(item.source, filters.sources)
        and _matches_any(item.account, filters.accounts)
        and _matches_any(item.post_id, filters.post_ids)
        and _matches_any(item.keyword, filters.keywords)
        and _matches_any(item.topic, filters.topics)
    )


def _matches_any(value: str, accepted_values: tuple[str, ...]) -> bool:
    if not accepted_values:
        return True

    normalized_value = value.casefold()
    return any(normalized_value == accepted.casefold() for accepted in accepted_values)


def _parse_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"Invalid {label}: {value}. Use YYYY-MM-DD.") from error
