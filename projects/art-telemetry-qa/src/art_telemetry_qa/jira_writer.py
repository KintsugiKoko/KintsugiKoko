from __future__ import annotations

from pathlib import Path

from art_telemetry_qa.schemas import Finding, ScanResult


def write_jira_ready_bugs(result: ScanResult, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "jira_ready_bugs.md").write_text(
        generate_jira_ready_markdown(result.findings),
        encoding="utf-8",
    )


def generate_jira_ready_markdown(findings: list[Finding]) -> str:
    lines = [
        "# Jira-Ready Art QA Bug Drafts",
        "",
        "> Draft bug language from mock telemetry. A human QA reviewer should verify repro, impact, and owner before filing.",
        "",
    ]

    if not findings:
        lines.extend(["_No bug drafts generated._", ""])
        return "\n".join(lines)

    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"## {index}. [{finding.severity}] {finding.asset_name} - {finding.title}",
                "",
                f"**Likely owner:** {finding.likely_owner}",
                "",
                f"**Asset path:** `{finding.asset_path}`",
                "",
                "**Summary**",
                "",
                f"{finding.asset_name} triggered `{finding.rule_id}` during mock Art QA telemetry validation.",
                "",
                "**Observed Result**",
                "",
                finding.message,
                "",
                "**Expected Result**",
                "",
                "Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.",
                "",
                "**Evidence To Attach / Verify**",
                "",
                f"- {finding.evidence}",
                "- Screenshot or capture from the reviewed map, if available.",
                "- Repeat capture after the suspected fix, if this becomes a filed issue.",
                "",
                "**Suggested Validation**",
                "",
                finding.suggested_validation,
                "",
            ]
        )

    return "\n".join(lines)
