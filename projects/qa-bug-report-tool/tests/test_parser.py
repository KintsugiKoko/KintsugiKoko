import pytest

from bug_report_tool.parser import parse_note


def test_parse_labeled_note():
    note = """Title: Inventory count does not update
Severity: Medium
Priority: High
Environment: Windows 11, Chrome
Steps:
1. Open inventory.
2. Use potion.
Expected: Count decreases.
Actual: Count stays the same.
Repro Rate: 3/3
Notes: Rough note from a practice test."""

    report = parse_note(note)

    assert report.title == "Inventory count does not update"
    assert report.severity == "Medium"
    assert report.priority == "High"
    assert report.environment == "Windows 11, Chrome"
    assert report.steps_to_reproduce == ["Open inventory.", "Use potion."]
    assert report.expected_result == "Count decreases."
    assert report.actual_result == "Count stays the same."
    assert report.repro_rate == "3/3"
    assert report.notes == "Rough note from a practice test."


def test_parse_rough_note_uses_first_line_as_title():
    note = """Menu overlaps title on mobile
Saw this at 390px width while checking the homepage.
Actual: Menu covers part of the title."""

    report = parse_note(note)

    assert report.title == "Menu overlaps title on mobile"
    assert report.actual_result == "Menu covers part of the title."
    assert report.expected_result == "Not provided"
    assert report.notes == "Saw this at 390px width while checking the homepage."


def test_parse_inline_steps():
    note = """Title: Inline steps are split
Steps: Open page -> Click settings -> Change volume
Expected: Save button appears."""

    report = parse_note(note)

    assert report.steps_to_reproduce == [
        "Open page",
        "Click settings",
        "Change volume",
    ]


def test_parse_empty_note_raises_error():
    with pytest.raises(ValueError):
        parse_note("   ")


def test_parse_normalizes_common_severity_and_priority_values():
    note = """Title: Values need cleanup
Severity: med
Priority: P1
Actual: The rough note used shorthand."""

    report = parse_note(note)

    assert report.severity == "Medium"
    assert report.priority == "High"
    assert "Warning:" not in report.notes


def test_parse_preserves_unknown_values_with_warning_notes():
    note = """Title: Unknown values stay visible
Severity: Spicy
Priority: Whenever
Notes: Tester used custom labels."""

    report = parse_note(note)

    assert report.severity == "Spicy"
    assert report.priority == "Whenever"
    assert "Tester used custom labels." in report.notes
    assert "Warning: Severity value 'Spicy' was not recognized." in report.notes
    assert "Warning: Priority value 'Whenever' was not recognized." in report.notes
    assert "Preserved the original value." in report.notes


def test_parse_collects_evidence_and_attachment_fields():
    note = """Title: Evidence links are included
Severity: High
Evidence:
- screenshots/inventory-count.png
- videos/repro-clip.mp4
Logs: logs/client-output.txt
Actual: Evidence should stay attached to the report."""

    report = parse_note(note)

    assert report.evidence == [
        "screenshots/inventory-count.png",
        "videos/repro-clip.mp4",
        "logs/client-output.txt",
    ]
