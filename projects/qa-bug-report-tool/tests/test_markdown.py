from bug_report_tool.markdown import format_markdown
from bug_report_tool.models import BugReport


def test_format_markdown_contains_required_sections():
    report = BugReport(
        title="Save button stays disabled",
        severity="Medium",
        priority="High",
        environment="Windows 11, Firefox",
        steps_to_reproduce=["Open Settings.", "Move the volume slider."],
        expected_result="Save button becomes enabled.",
        actual_result="Save button stays disabled.",
        repro_rate="2/2",
        notes="Blocks a basic settings flow.",
    )

    markdown = format_markdown(report)

    assert markdown.startswith("# Save button stays disabled")
    assert "| Severity | Medium |" in markdown
    assert "| Priority | High |" in markdown
    assert "## Steps to Reproduce" in markdown
    assert "1. Open Settings." in markdown
    assert "2. Move the volume slider." in markdown
    assert "## Expected Result" in markdown
    assert "## Actual Result" in markdown
    assert "## Notes" in markdown


def test_format_markdown_escapes_table_pipes():
    report = BugReport(
        title="Pipe example",
        environment="Chrome | Windows",
        steps_to_reproduce=["Open page."],
    )

    markdown = format_markdown(report)

    assert "| Environment | Chrome \\| Windows |" in markdown


def test_format_markdown_includes_evidence_when_present():
    report = BugReport(
        title="Evidence example",
        steps_to_reproduce=["Open page."],
        evidence=["screenshots/example.png", "logs/client-output.txt"],
    )

    markdown = format_markdown(report)

    assert "## Evidence / Attachments" in markdown
    assert "- screenshots/example.png" in markdown
    assert "- logs/client-output.txt" in markdown
