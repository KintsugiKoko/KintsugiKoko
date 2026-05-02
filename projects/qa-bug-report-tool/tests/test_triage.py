import pytest

from bug_report_tool.triage import summarize_reports


def test_summarize_reports_counts_fields_and_reviewer_notes(tmp_path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    (reports_dir / "001-critical.md").write_text(
        """# Login blocker

| Field | Details |
| --- | --- |
| Severity | Critical |
| Priority | High |
| Environment | Windows 11 |
| Repro Rate | 3/3 |

## Steps to Reproduce

1. Open login.

## Expected Result

Player reaches account page.

## Actual Result

Login hangs.

## Evidence / Attachments

- videos/login-hang.mp4

## Notes

Blocks sign-in.""",
        encoding="utf-8",
    )
    (reports_dir / "002-missing.md").write_text(
        """# Missing context report

| Field | Details |
| --- | --- |
| Severity | Medium |
| Priority | Not provided |
| Environment | Not provided |
| Repro Rate | Not provided |

## Steps to Reproduce

1. Not provided.

## Expected Result

Not provided

## Actual Result

Button does not respond.

## Notes

Warning: Priority value 'Whenever' was not recognized.""",
        encoding="utf-8",
    )

    summary = summarize_reports(reports_dir)

    assert "# QA Triage Summary" in summary
    assert "Reports reviewed: 2" in summary
    assert "| Critical | 1 |" in summary
    assert "| Medium | 1 |" in summary
    assert "| High | 1 |" in summary
    assert "| Missing context report | Environment, Steps, Expected Result, Repro Rate, Evidence |" in summary
    assert "Review validation warnings in `Missing context report`." in summary
    assert "Review high-impact reports first: `Login blocker`." in summary


def test_summarize_reports_requires_generated_reports(tmp_path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    (reports_dir / "README.md").write_text("# Notes", encoding="utf-8")

    with pytest.raises(ValueError, match="No generated Markdown bug reports"):
        summarize_reports(reports_dir)
