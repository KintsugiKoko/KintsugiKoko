from __future__ import annotations

import csv
from pathlib import Path

from art_telemetry_qa.schemas import Finding, ScanResult


def write_reports(result: ScanResult, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    write_summary_markdown(result, output / "art_qa_summary.md")
    write_failures_csv(result.findings, output / "art_qa_failures.csv")


def write_summary_markdown(result: ScanResult, path: str | Path) -> None:
    Path(path).write_text(generate_summary_markdown(result), encoding="utf-8")


def generate_summary_markdown(result: ScanResult) -> str:
    lines = [
        "# Art QA Telemetry Summary",
        "",
        "> Portfolio-safe report generated from mock Unreal-style telemetry and validation data.",
        "",
        "## Executive Summary",
        "",
        f"- Assets scanned: **{result.total_assets}**",
        f"- Findings generated: **{len(result.findings)}**",
        f"- Total risk points: **{sum(result.risk_by_asset.values())}**",
        "- This report supports human Art QA / Technical QA review; it is not final Tech Art, Performance, or Engineering sign-off.",
        "",
        "## Risk By Asset",
        "",
        _count_table("Asset", "Risk Points", result.risk_by_asset),
        "",
        "## Severity Counts",
        "",
        _count_table("Severity", "Count", result.severity_counts),
        "",
        "## Likely Owner Routing",
        "",
        _count_table("Owner", "Count", result.owner_counts),
        "",
        "## Findings",
        "",
        *_finding_lines(result.findings),
        "",
        "## Method / Limitations",
        "",
        "- Uses mock Unreal-style data only.",
        "- Does not use private studio data, proprietary schemas, internal telemetry, Jira, or Unreal project files.",
        "- Thresholds are simple review triggers, not universal asset budgets.",
        "- Findings are meant to support capture, parse, isolate, report, and validate-fix workflows.",
        "- Human review is required before filing bugs or requesting cross-discipline follow-up.",
        "",
    ]
    return "\n".join(lines)


def write_failures_csv(findings: list[Finding], path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "asset_id",
                "asset_name",
                "severity",
                "risk_points",
                "likely_owner",
                "rule_id",
                "title",
                "message",
                "suggested_validation",
            ],
        )
        writer.writeheader()
        for finding in findings:
            writer.writerow(
                {
                    "asset_id": finding.asset_id,
                    "asset_name": finding.asset_name,
                    "severity": finding.severity,
                    "risk_points": finding.risk_points,
                    "likely_owner": finding.likely_owner,
                    "rule_id": finding.rule_id,
                    "title": finding.title,
                    "message": finding.message,
                    "suggested_validation": finding.suggested_validation,
                }
            )


def _count_table(label: str, value_label: str, counts: dict[str, int]) -> str:
    if not counts:
        return "_No items found._"
    rows = [f"| {label} | {value_label} |", "| --- | ---: |"]
    rows.extend(f"| {name} | {count} |" for name, count in counts.items())
    return "\n".join(rows)


def _finding_lines(findings: list[Finding]) -> list[str]:
    if not findings:
        return ["- No findings generated."]

    lines: list[str] = []
    for finding in findings:
        lines.extend(
            [
                f"### {finding.severity}: {finding.asset_name} - {finding.title}",
                "",
                f"- Rule: `{finding.rule_id}`",
                f"- Likely owner: {finding.likely_owner}",
                f"- Risk points: {finding.risk_points}",
                f"- Asset path: `{finding.asset_path}`",
                f"- Finding: {finding.message}",
                f"- Evidence: {finding.evidence}",
                f"- Suggested validation: {finding.suggested_validation}",
                "",
            ]
        )
    return lines
