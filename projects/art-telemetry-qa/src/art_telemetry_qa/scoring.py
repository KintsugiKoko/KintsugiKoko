from __future__ import annotations

from collections import Counter, defaultdict

from art_telemetry_qa.schemas import Finding, ScanResult


SEVERITY_POINTS = {
    "Critical": 10,
    "High": 6,
    "Medium": 3,
    "Low": 1,
}

SEVERITY_ORDER = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
}


def points_for_severity(severity: str) -> int:
    try:
        return SEVERITY_POINTS[severity]
    except KeyError as error:
        raise ValueError(f"Unknown severity: {severity}") from error


def apply_risk_points(findings: list[Finding]) -> list[Finding]:
    return [
        Finding(
            asset_id=finding.asset_id,
            asset_name=finding.asset_name,
            asset_path=finding.asset_path,
            rule_id=finding.rule_id,
            title=finding.title,
            severity=finding.severity,
            likely_owner=finding.likely_owner,
            message=finding.message,
            evidence=finding.evidence,
            suggested_validation=finding.suggested_validation,
            risk_points=points_for_severity(finding.severity),
        )
        for finding in findings
    ]


def build_scan_result(total_assets: int, findings: list[Finding]) -> ScanResult:
    scored = apply_risk_points(findings)
    risk_by_asset: dict[str, int] = defaultdict(int)
    for finding in scored:
        risk_by_asset[finding.asset_name] += finding.risk_points

    return ScanResult(
        total_assets=total_assets,
        findings=sorted(scored, key=_finding_sort_key),
        risk_by_asset=dict(sorted(risk_by_asset.items(), key=lambda item: item[1], reverse=True)),
        severity_counts=dict(Counter(finding.severity for finding in scored)),
        owner_counts=dict(Counter(finding.likely_owner for finding in scored)),
    )


def _finding_sort_key(finding: Finding) -> tuple[int, int, str, str]:
    return (
        SEVERITY_ORDER.get(finding.severity, 99),
        -finding.risk_points,
        finding.asset_name.lower(),
        finding.rule_id,
    )
