"""Create QA triage summaries from generated bug reports."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from bug_report_tool.models import BugReport

LEVEL_ORDER = ("Critical", "High", "Medium", "Low", "Not provided")
CHECK_FIELDS = (
    ("Environment", lambda report: report.environment),
    ("Steps", lambda report: report.steps_to_reproduce),
    ("Expected Result", lambda report: report.expected_result),
    ("Actual Result", lambda report: report.actual_result),
    ("Repro Rate", lambda report: report.repro_rate),
    ("Evidence", lambda report: report.evidence),
)


def summarize_reports(reports_dir: str | Path) -> str:
    """Return a Markdown triage summary for generated Markdown reports."""

    source_dir = Path(reports_dir)
    if not source_dir.is_dir():
        raise ValueError(f"Reports folder does not exist: {source_dir}")

    reports = _read_reports(source_dir)
    if not reports:
        raise ValueError(f"No generated Markdown bug reports found in: {source_dir}")

    severity_counts = Counter(report.severity for report in reports)
    priority_counts = Counter(report.priority for report in reports)
    missing_rows = _missing_field_rows(reports)
    warning_titles = [report.title for report in reports if "Warning:" in report.notes]

    sections = [
        "# QA Triage Summary",
        "",
        f"Source folder: `{source_dir}`",
        f"Reports reviewed: {len(reports)}",
        "",
        "## Severity Counts",
        "",
        _count_table("Severity", severity_counts),
        "",
        "## Priority Counts",
        "",
        _count_table("Priority", priority_counts),
        "",
        "## Missing-Field Checks",
        "",
        _missing_table(missing_rows),
        "",
        "## Validation Warnings",
        "",
        _warning_list(warning_titles),
        "",
        "## Reviewer Notes",
        "",
        _reviewer_notes(reports, missing_rows, warning_titles),
    ]
    return "\n".join(sections).strip()


def _read_reports(source_dir: Path) -> list[BugReport]:
    reports = []
    for report_path in sorted(source_dir.glob("*.md")):
        if report_path.name.lower().startswith("triage-summary"):
            continue
        report = _parse_markdown_report(report_path)
        if report:
            reports.append(report)
    return reports


def _parse_markdown_report(report_path: Path) -> BugReport | None:
    text = report_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = _first_heading(lines)
    fields = _table_fields(lines)
    if not title or "Severity" not in fields or "Priority" not in fields:
        return None

    sections = _sections(lines)
    return BugReport(
        title=title,
        severity=fields.get("Severity", "Not provided"),
        priority=fields.get("Priority", "Not provided"),
        environment=fields.get("Environment", "Not provided"),
        steps_to_reproduce=_numbered_items(sections.get("Steps to Reproduce", [])),
        expected_result=_section_text(sections.get("Expected Result", [])),
        actual_result=_section_text(sections.get("Actual Result", [])),
        repro_rate=fields.get("Repro Rate", "Not provided"),
        evidence=_bullet_items(sections.get("Evidence / Attachments", [])),
        notes=_section_text(sections.get("Notes", [])),
    )


def _first_heading(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return ""


def _table_fields(lines: list[str]) -> dict[str, str]:
    fields = {}
    for line in lines:
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] == "Field":
            continue
        fields[cells[0]] = cells[1].replace("<br>", "\n").replace("\\|", "|")
    return fields


def _sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading = ""
    for line in lines:
        if line.startswith("## "):
            current_heading = line.removeprefix("## ").strip()
            sections[current_heading] = []
            continue
        if current_heading:
            sections[current_heading].append(line)
    return sections


def _numbered_items(lines: list[str]) -> list[str]:
    items = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if ". " in stripped:
            stripped = stripped.split(". ", 1)[1]
        items.append(stripped)
    return items or ["Not provided."]


def _bullet_items(lines: list[str]) -> list[str]:
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped.removeprefix("- ").strip())
    return items


def _section_text(lines: list[str] | None) -> str:
    if not lines:
        return "Not provided"
    text = "\n".join(line.strip() for line in lines if line.strip()).strip()
    return text or "Not provided"


def _count_table(label: str, counts: Counter[str]) -> str:
    rows = [f"| {label} | Count |", "| --- | --- |"]
    seen = set()
    for level in LEVEL_ORDER:
        rows.append(f"| {level} | {counts.get(level, 0)} |")
        seen.add(level)
    for level, count in sorted(counts.items()):
        if level not in seen:
            rows.append(f"| {level} | {count} |")
    return "\n".join(rows)


def _missing_field_rows(reports: list[BugReport]) -> list[tuple[str, list[str]]]:
    rows = []
    for report in reports:
        missing = [
            field_name
            for field_name, getter in CHECK_FIELDS
            if _is_missing(getter(report))
        ]
        if missing:
            rows.append((report.title, missing))
    return rows


def _is_missing(value: str | list[str]) -> bool:
    if isinstance(value, list):
        return not value or value == ["Not provided."]
    return not value or value == "Not provided"


def _missing_table(rows: list[tuple[str, list[str]]]) -> str:
    table = ["| Report | Missing fields |", "| --- | --- |"]
    if not rows:
        table.append("| None | No missing fields found |")
        return "\n".join(table)

    for title, missing in rows:
        table.append(f"| {_table_cell(title)} | {', '.join(missing)} |")
    return "\n".join(table)


def _warning_list(titles: list[str]) -> str:
    if not titles:
        return "- No validation warnings found."
    return "\n".join(f"- Review validation warnings in `{title}`." for title in titles)


def _reviewer_notes(
    reports: list[BugReport],
    missing_rows: list[tuple[str, list[str]]],
    warning_titles: list[str],
) -> str:
    notes = []
    urgent_reports = [
        report.title
        for report in reports
        if report.severity in {"Critical", "High"}
        or report.priority in {"Critical", "High"}
    ]

    if urgent_reports:
        notes.append(
            "- Review high-impact reports first: "
            + ", ".join(f"`{title}`" for title in urgent_reports)
            + "."
        )
    else:
        notes.append("- No Critical or High severity/priority reports found.")

    if missing_rows:
        notes.append("- Fill missing fields before sharing reports for final review.")
    else:
        notes.append("- Reports include the tracked fields used by this summary.")

    if warning_titles:
        notes.append("- Resolve unknown severity or priority labels before final triage.")
    else:
        notes.append("- Severity and priority values are normalized or recognized.")

    return "\n".join(notes)


def _table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")
