from __future__ import annotations

import pytest

from art_telemetry_qa.parser import load_scan_inputs
from art_telemetry_qa.rules import evaluate_rules
from art_telemetry_qa.scoring import build_scan_result, points_for_severity


def test_points_for_severity() -> None:
    assert points_for_severity("Critical") == 10
    assert points_for_severity("High") == 6
    assert points_for_severity("Medium") == 3
    assert points_for_severity("Low") == 1


def test_unknown_severity_raises() -> None:
    with pytest.raises(ValueError, match="Unknown severity"):
        points_for_severity("Urgent")


def test_build_scan_result_adds_risk_points_and_counts() -> None:
    inputs = load_scan_inputs("samples")
    result = build_scan_result(len(inputs.telemetry), evaluate_rules(inputs))

    assert result.total_assets == 6
    assert result.findings[0].risk_points in {10, 6}
    assert result.severity_counts["Critical"] >= 1
    assert result.owner_counts["Performance"] >= 1
    assert result.risk_by_asset["SM_Merchant_Caravan_Wagon"] > 0
