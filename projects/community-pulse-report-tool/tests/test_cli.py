from pathlib import Path
from tempfile import TemporaryDirectory

from community_pulse.cli import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_generates_report_from_high_engagement_sample(tmp_path: Path) -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"
    output_path = tmp_path / "report.md"

    result = main(
        [
            str(sample_path),
            "--keyword",
            "onboarding",
            "--output",
            str(output_path),
        ]
    )

    report = output_path.read_text(encoding="utf-8")

    assert result == 0
    assert "# Weekly Community Feedback Review Report" in report
    assert "- **Keyword**: onboarding" in report
    assert "## Topic Opinion Splits" in report
    assert "Onboarding clarity" in report


def test_cli_applies_output_limits_and_max_rows(tmp_path: Path) -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"
    output_path = tmp_path / "report.md"

    result = main(
        [
            str(sample_path),
            "--max-rows",
            "3",
            "--max-quotes",
            "2",
            "--max-topics",
            "1",
            "--max-themes",
            "1",
            "--max-follow-ups",
            "2",
            "--output",
            str(output_path),
        ]
    )

    report = output_path.read_text(encoding="utf-8")

    assert result == 0
    assert "Input parsing limited to the first 3 rows" in report
    assert "_Representative quotes limited to 2 for readability._" in report
    assert "_Suggested follow-ups limited to 2 for readability._" in report


def test_cli_report_respects_max_quotes(tmp_path: Path) -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"
    output_path = tmp_path / "report.md"

    result = main(
        [
            str(sample_path),
            "--max-quotes",
            "3",
            "--output",
            str(output_path),
        ]
    )

    report = output_path.read_text(encoding="utf-8")
    quote_section = _section(report, "## Representative Quotes", "## Suggested Follow-ups")

    assert result == 0
    assert quote_section.count('\n- "') == 3
    assert "_Representative quotes limited to 3 for readability._" in quote_section


def test_cli_report_respects_max_topics() -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"

    report = _run_report([str(sample_path), "--max-topics", "2"])
    topic_section = _section(
        report,
        "## Top Mentioned Topics / Game Areas",
        "## Topic Opinion Splits",
    )
    split_section = _section(report, "## Topic Opinion Splits", "## Positive Themes")

    assert "| Fishing timing | 6 |" in topic_section
    assert "| Onboarding clarity | 6 |" in topic_section
    assert "| Starwell offerings | 4 |" not in topic_section
    assert "_Showing top 2 topics by mention count._" in topic_section
    assert split_section.count("\n- **") == 2
    assert "_Showing top 2 topic opinion splits by mention count._" in split_section


def test_cli_report_respects_max_followups() -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"

    report = _run_report([str(sample_path), "--max-follow-ups", "2"])
    followup_section = _section(report, "## Suggested Follow-ups", "## Method / Limitations")

    assert followup_section.count("\n- ") == 2
    assert "_Suggested follow-ups limited to 2 for readability._" in followup_section


def test_cli_filtering_happens_before_aggregation_and_quote_selection(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "feedback.csv"
    csv_path.write_text(
        "\n".join(
            [
                "date,source,game_area,sentiment,text,account,post_id,keyword,topic,conversation_id",
                '2026-05-01,mock-social-post,Fishing,negative,"Do not include this other account quote.",other-account,mock-post-001,fishing,Fishing timing,thread-001',
                '2026-05-01,mock-social-post,Fishing,positive,"Target account liked the timing.",target-account,mock-post-002,fishing,Fishing timing,thread-002',
                '2026-05-02,mock-social-post,Onboarding,mixed,"Target account needed one clearer prompt.",target-account,mock-post-003,onboarding,Onboarding clarity,thread-003',
            ]
        ),
        encoding="utf-8",
    )

    report = _run_report([str(csv_path), "--account", "target-account"])

    assert "- Total local feedback records reviewed: **2**" in report
    assert "| positive | 1 |" in report
    assert "| mixed | 1 |" in report
    assert "| negative |" not in _section(report, "## Sentiment Snapshot", "## Local Feedback Inputs")
    assert "Target account liked the timing." in report
    assert "Target account needed one clearer prompt." in report
    assert "Do not include this other account quote." not in report


def test_cli_large_fictional_csv_preserves_report_correctness(tmp_path: Path) -> None:
    csv_path = tmp_path / "large-feedback.csv"
    output_path = tmp_path / "large-report.md"
    rows = ["date,source,game_area,sentiment,text,account,post_id,keyword,topic,conversation_id"]
    for index in range(120):
        topic_index = index % 3
        sentiment = ("positive", "mixed", "negative")[topic_index]
        rows.append(
            (
                f"2026-05-{(index % 28) + 1:02d},mock-source-{topic_index},"
                f"Area {topic_index},{sentiment},"
                f"\"Fictional feedback row {index}.\",mock-account-{topic_index},"
                f"mock-post-{topic_index},keyword-{topic_index},Topic {topic_index},"
                f"thread-{topic_index}"
            )
        )
    csv_path.write_text("\n".join(rows), encoding="utf-8")

    result = main(
        [
            str(csv_path),
            "--max-quotes",
            "4",
            "--max-topics",
            "2",
            "--output",
            str(output_path),
        ]
    )

    report = output_path.read_text(encoding="utf-8")
    topic_section = _section(
        report,
        "## Top Mentioned Topics / Game Areas",
        "## Topic Opinion Splits",
    )

    assert result == 0
    assert "- Total local feedback records reviewed: **120**" in report
    assert "| positive | 40 |" in report
    assert "| mixed | 40 |" in report
    assert "| negative | 40 |" in report
    assert "| Topic 0 | 40 |" in topic_section
    assert "| Topic 1 | 40 |" in topic_section
    assert "| Topic 2 | 40 |" not in topic_section
    assert "_Showing top 2 topics by mention count._" in topic_section
    assert "_Representative quotes limited to 4 for readability._" in report


def test_cli_quote_selection_is_deterministic_when_limits_are_applied(
    tmp_path: Path,
) -> None:
    sample_path = PROJECT_ROOT / "sample-data" / "high-engagement-feedback-sample.csv"
    first_output = tmp_path / "first.md"
    second_output = tmp_path / "second.md"
    args = [
        str(sample_path),
        "--max-quotes",
        "4",
        "--max-topics",
        "3",
        "--output",
    ]

    first_result = main([*args, str(first_output)])
    second_result = main([*args, str(second_output)])

    first_report = first_output.read_text(encoding="utf-8")
    second_report = second_output.read_text(encoding="utf-8")

    assert first_result == 0
    assert second_result == 0
    assert _section(
        first_report,
        "## Representative Quotes",
        "## Suggested Follow-ups",
    ) == _section(
        second_report,
        "## Representative Quotes",
        "## Suggested Follow-ups",
    )


def _run_report(args: list[str]) -> str:
    with TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "report.md"
        result = main([*args, "--output", str(output_path)])
        assert result == 0
        return output_path.read_text(encoding="utf-8")


def _section(report: str, start: str, end: str) -> str:
    start_index = report.index(start)
    end_index = report.index(end, start_index)
    return report[start_index:end_index]
