from pathlib import Path

import pytest

from community_pulse.parser import parse_feedback_csv


def test_parse_feedback_csv_reads_required_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "\n".join(
            [
                "date,source,game_area,sentiment,text",
                '2026-05-01,fictional-form,Fishing,Positive,"Fun loop."',
                '2026-05-02,mock-note,Starwell,negative,"Needs clearer feedback."',
            ]
        ),
        encoding="utf-8",
    )

    items = parse_feedback_csv(csv_path)

    assert len(items) == 2
    assert items[0].game_area == "Fishing"
    assert items[0].sentiment == "positive"
    assert items[1].text == "Needs clearer feedback."


def test_parse_feedback_csv_validates_required_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "date,source,game_area,text\n2026-05-01,fictional-form,Fishing,Fun loop.",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required column"):
        parse_feedback_csv(csv_path)


def test_parse_feedback_csv_rejects_empty_required_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "date,source,game_area,sentiment,text\n2026-05-01,,Fishing,positive,Fun loop.",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Row 2"):
        parse_feedback_csv(csv_path)
