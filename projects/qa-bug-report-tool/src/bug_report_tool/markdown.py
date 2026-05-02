"""Format bug reports as Markdown."""

from bug_report_tool.models import BugReport


def format_markdown(report: BugReport) -> str:
    """Return a Markdown bug report."""

    steps = "\n".join(
        f"{number}. {step}" for number, step in enumerate(report.steps_to_reproduce, start=1)
    )

    return "\n".join(
        [
            f"# {report.title}",
            "",
            "| Field | Details |",
            "| --- | --- |",
            f"| Severity | {_table_cell(report.severity)} |",
            f"| Priority | {_table_cell(report.priority)} |",
            f"| Environment | {_table_cell(report.environment)} |",
            f"| Repro Rate | {_table_cell(report.repro_rate)} |",
            "",
            "## Steps to Reproduce",
            "",
            steps,
            "",
            "## Expected Result",
            "",
            report.expected_result,
            "",
            "## Actual Result",
            "",
            report.actual_result,
            "",
            "## Notes",
            "",
            report.notes,
        ]
    ).strip()


def _table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")
