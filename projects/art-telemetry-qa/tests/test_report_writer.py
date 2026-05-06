from __future__ import annotations

from pathlib import Path

from art_telemetry_qa.cli import main
from art_telemetry_qa.jira_writer import generate_jira_ready_markdown
from art_telemetry_qa.parser import load_scan_inputs
from art_telemetry_qa.report_writer import generate_summary_markdown, write_reports
from art_telemetry_qa.rules import evaluate_rules
from art_telemetry_qa.scoring import build_scan_result


def _sample_result():
    inputs = load_scan_inputs("samples")
    return build_scan_result(len(inputs.telemetry), evaluate_rules(inputs))


def test_generate_summary_markdown_includes_boundaries() -> None:
    markdown = generate_summary_markdown(_sample_result())

    assert "# Art QA Telemetry Summary" in markdown
    assert "Risk By Asset" in markdown
    assert "Likely Owner Routing" in markdown
    assert "mock Unreal-style data only" in markdown
    assert "Human review is required" in markdown


def test_write_reports_creates_summary_and_failures_csv(tmp_path: Path) -> None:
    write_reports(_sample_result(), tmp_path)

    assert (tmp_path / "art_qa_summary.md").exists()
    failures = (tmp_path / "art_qa_failures.csv").read_text(encoding="utf-8")
    assert "asset_id,asset_name,severity" in failures
    assert "SM_Merchant_Caravan_Wagon" in failures


def test_generate_jira_ready_markdown_is_human_reviewed() -> None:
    markdown = generate_jira_ready_markdown(_sample_result().findings)

    assert "# Jira-Ready Art QA Bug Drafts" in markdown
    assert "human QA reviewer should verify" in markdown
    assert "Observed Result" in markdown
    assert "Suggested Validation" in markdown


def test_cli_scan_generates_expected_reports(tmp_path: Path) -> None:
    exit_code = main(["scan", "--input", "samples", "--output", str(tmp_path)])

    assert exit_code == 0
    assert (tmp_path / "art_qa_summary.md").exists()
    assert (tmp_path / "art_qa_failures.csv").exists()
    assert (tmp_path / "jira_ready_bugs.md").exists()
