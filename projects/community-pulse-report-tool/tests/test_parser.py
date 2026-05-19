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
    assert items[0].account == ""
    assert items[0].topic == ""


def test_parse_feedback_csv_reads_optional_demo_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "\n".join(
            [
                "date,source,game_area,sentiment,text,account,post_id,keyword,topic,conversation_id",
                '2026-05-01,mock-social-post,Fishing,mixed,"Exact quote.",mock-studio-account,mock-post-001,onboarding,Onboarding clarity,mock-thread-001',
            ]
        ),
        encoding="utf-8",
    )

    items = parse_feedback_csv(csv_path)

    assert len(items) == 1
    assert items[0].account == "mock-studio-account"
    assert items[0].post_id == "mock-post-001"
    assert items[0].keyword == "onboarding"
    assert items[0].topic == "Onboarding clarity"
    assert items[0].conversation_id == "mock-thread-001"


def test_parse_feedback_csv_supports_max_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "\n".join(
            [
                "date,source,game_area,sentiment,text",
                '2026-05-01,fictional-form,Fishing,positive,"First row."',
                '2026-05-02,fictional-form,Fishing,mixed,"Second row."',
                '2026-05-03,fictional-form,Fishing,negative,"Third row."',
            ]
        ),
        encoding="utf-8",
    )

    items = parse_feedback_csv(csv_path, max_rows=2)

    assert [item.text for item in items] == ["First row.", "Second row."]


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
