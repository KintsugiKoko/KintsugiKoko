from __future__ import annotations

from art_telemetry_qa.parser import load_scan_inputs
from art_telemetry_qa.rules import evaluate_rules


def test_rules_find_required_art_qa_validation_categories() -> None:
    findings = evaluate_rules(load_scan_inputs("samples"))
    rule_ids = {finding.rule_id for finding in findings}

    assert "ART-MAT-001" in rule_ids
    assert "ART-TEX-001" in rule_ids
    assert "ART-ALPHA-001" in rule_ids
    assert "ANIM-WEIGHT-001" in rule_ids
    assert "ART-MAT-002" in rule_ids
    assert "ART-LOD-001" in rule_ids
    assert "ENG-COLL-001" in rule_ids
    assert "ART-BOUNDS-001" in rule_ids
    assert "VFX-PART-001" in rule_ids
    assert "SOAK-WARN-001" in rule_ids
    assert "QA-NAME-001" in rule_ids
    assert "PERF-LOAD-001" in rule_ids


def test_rules_route_likely_owners() -> None:
    findings = evaluate_rules(load_scan_inputs("samples"))
    owners = {finding.likely_owner for finding in findings}

    assert {"Art", "Tech Art", "VFX", "Animation", "Engineering", "Performance", "QA"}.issubset(owners)


def test_rules_keep_clean_baseline_unflagged_for_starwell() -> None:
    findings = evaluate_rules(load_scan_inputs("samples"))
    starwell_findings = [finding for finding in findings if finding.asset_id == "ART001"]

    assert starwell_findings == []
