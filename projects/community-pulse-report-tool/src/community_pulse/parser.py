from __future__ import annotations

import csv
from pathlib import Path

from community_pulse.models import FeedbackItem

REQUIRED_COLUMNS = ("date", "source", "game_area", "sentiment", "text")
OPTIONAL_COLUMNS = ("account", "post_id", "keyword", "topic", "conversation_id")


def parse_feedback_csv(
    csv_path: str | Path,
    max_rows: int | None = None,
) -> list[FeedbackItem]:
    if max_rows is not None and max_rows < 1:
        raise ValueError("Max rows must be 1 or greater.")

    path = Path(csv_path)

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        _validate_columns(reader.fieldnames)

        feedback: list[FeedbackItem] = []
        for row_number, row in enumerate(reader, start=2):
            if max_rows is not None and len(feedback) >= max_rows:
                break
            feedback.append(_row_to_feedback_item(row, row_number))

    return feedback


def _validate_columns(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise ValueError("CSV file is empty or missing a header row.")

    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        missing_list = ", ".join(missing)
        required_list = ", ".join(REQUIRED_COLUMNS)
        raise ValueError(
            f"CSV is missing required column(s): {missing_list}. "
            f"Required columns: {required_list}."
        )


def _row_to_feedback_item(row: dict[str, str], row_number: int) -> FeedbackItem:
    cleaned = {column: (row.get(column) or "").strip() for column in REQUIRED_COLUMNS}
    optional = {column: (row.get(column) or "").strip() for column in OPTIONAL_COLUMNS}
    empty_columns = [column for column, value in cleaned.items() if not value]
    if empty_columns:
        empty_list = ", ".join(empty_columns)
        raise ValueError(f"Row {row_number} has empty required field(s): {empty_list}.")

    return FeedbackItem(
        date=cleaned["date"],
        source=cleaned["source"],
        game_area=cleaned["game_area"],
        sentiment=cleaned["sentiment"].lower(),
        text=cleaned["text"],
        account=optional["account"],
        post_id=optional["post_id"],
        keyword=optional["keyword"],
        topic=optional["topic"],
        conversation_id=optional["conversation_id"],
    )
