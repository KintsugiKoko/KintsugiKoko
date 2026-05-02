from pathlib import Path
import json
import sys
from io import StringIO

import pytest

from bug_report_tool.cli import _report_filename, main


def test_cli_writes_markdown_report(tmp_path):
    input_path = tmp_path / "note.txt"
    output_path = tmp_path / "report.md"
    input_path.write_text(
        """Title: Project card opens wrong page
Severity: Low
Priority: Medium
Steps:
1. Open homepage.
2. Click project card.
Expected: Correct page opens.
Actual: Wrong page opens.
Repro Rate: 1/1""",
        encoding="utf-8",
    )

    result = main([str(input_path), "--output", str(output_path)])

    assert result == 0
    markdown = output_path.read_text(encoding="utf-8")
    assert "# Project card opens wrong page" in markdown
    assert "1. Open homepage." in markdown
    assert "Wrong page opens." in markdown


def test_cli_accepts_direct_text(capsys):
    result = main(
        [
            "--text",
            "Title: Direct note\nSeverity: Low\nActual: Button did not respond.",
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert "# Direct note" in captured.out
    assert "| Severity | Low |" in captured.out


def test_cli_outputs_json_for_direct_text(capsys):
    result = main(
        [
            "--text",
            "Title: JSON note\nSeverity: med\nPriority: P1\nActual: JSON worked.",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert result == 0
    assert report == {
        "title": "JSON note",
        "severity": "Medium",
        "priority": "High",
        "environment": "Not provided",
        "steps_to_reproduce": ["Not provided."],
        "expected_result": "Not provided",
        "actual_result": "JSON worked.",
        "repro_rate": "Not provided",
        "evidence": [],
        "notes": "No additional notes.",
    }


def test_cli_json_output_includes_evidence(capsys):
    result = main(
        [
            "--text",
            (
                "Title: Evidence JSON note\n"
                "Evidence:\n"
                "- screenshots/example.png\n"
                "- logs/client-output.txt\n"
                "Actual: Evidence exported."
            ),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert result == 0
    assert report["evidence"] == [
        "screenshots/example.png",
        "logs/client-output.txt",
    ]


def test_cli_reads_note_from_stdin(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO("Title: Stdin note\nSeverity: Low\nActual: Read from stdin."),
    )

    result = main(["-"])

    captured = capsys.readouterr()

    assert result == 0
    assert "# Stdin note" in captured.out
    assert "| Severity | Low |" in captured.out
    assert "Read from stdin." in captured.out


def test_sample_data_has_five_notes():
    project_root = Path(__file__).resolve().parents[1]

    samples = sorted((project_root / "sample-data").glob("*.txt"))

    assert len(samples) == 5


def test_batch_mode_converts_txt_notes(tmp_path, capsys):
    input_dir = tmp_path / "sample-data"
    output_dir = tmp_path / "reports"
    input_dir.mkdir()
    (input_dir / "001-menu-note.txt").write_text(
        """Title: Menu overlaps title
Severity: Low
Steps:
1. Open the homepage.
Expected: Menu opens below the header.
Actual: Menu covers the title.""",
        encoding="utf-8",
    )
    (input_dir / "002-save-button.txt").write_text(
        """Title: Save button stays disabled
Priority: High
Actual: Save button does not respond.""",
        encoding="utf-8",
    )
    (input_dir / "ignored.md").write_text("Not a note.", encoding="utf-8")

    result = main(
        [
            "--batch",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert "Converted 2 note(s)" in captured.out
    assert (output_dir / "001-menu.md").exists()
    assert (output_dir / "002-save-button.md").exists()
    assert not (output_dir / "ignored.md").exists()
    assert "# Menu overlaps title" in (output_dir / "001-menu.md").read_text(
        encoding="utf-8"
    )


def test_batch_mode_can_write_json_reports(tmp_path):
    input_dir = tmp_path / "sample-data"
    output_dir = tmp_path / "reports"
    input_dir.mkdir()
    (input_dir / "001-menu-note.txt").write_text(
        """Title: Menu overlaps title
Severity: Low
Priority: P2
Actual: Menu covers the title.""",
        encoding="utf-8",
    )

    result = main(
        [
            "--batch",
            "--format",
            "json",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ]
    )

    report_path = output_dir / "001-menu.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result == 0
    assert report_path.exists()
    assert report["title"] == "Menu overlaps title"
    assert report["priority"] == "Medium"


def test_report_filename_removes_note_suffix():
    assert (
        _report_filename(Path("001-inventory-count-note.txt"))
        == "001-inventory-count.md"
    )
    assert _report_filename(Path("002-settings-save.txt")) == "002-settings-save.md"
    assert (
        _report_filename(Path("003-profile-link-note.txt"), "json")
        == "003-profile-link.json"
    )


def test_help_documents_beginner_friendly_examples(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--help"])

    captured = capsys.readouterr()

    assert error.value.code == 0
    assert "Examples:" in captured.out
    assert "Convert one sample note and print the Markdown:" in captured.out
    assert "Convert one note and save the report:" in captured.out
    assert "Convert one note to JSON:" in captured.out
    assert "Convert every .txt note in sample-data/ to reports/:" in captured.out
    assert "Pass a short note directly:" in captured.out
    assert "Read a note from stdin:" in captured.out


def test_help_documents_main_commands(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])

    captured = capsys.readouterr()

    assert "python -m bug_report_tool sample-data/001-inventory-count-note.txt" in captured.out
    assert "--output reports/001-inventory-count.md" in captured.out
    assert "python -m bug_report_tool --batch" in captured.out
    assert "--format json" in captured.out
    assert "--input-dir my-notes --output-dir my-reports" in captured.out
    assert '--text "Title: Button does not respond"' in captured.out
