import json
import math

import pytest

from qa_workflow_lab.cli import main, project_root
from qa_workflow_lab.models import InputError
from qa_workflow_lab.routing import REVIEW, ROUTES, baseline, gate_answer, request_payload, validate_reports
from qa_workflow_lab.routing_evaluation import dry_run, evaluate_routing, load_cases, load_labels, metrics, render_report


def answer(choice="AI3", confidence=0.9):
    return {"type": "choice", "choice": choice, "confidence": confidence,
            "probabilities": {key: 0.92 if key == choice else 0.02 for key in ROUTES}}


@pytest.mark.parametrize("case,expected", [
    ("R01", "AI3"), ("R02", "AI5"), ("R03", "AI4"), ("R04", "AI6"),
    ("R05", REVIEW), ("R06", REVIEW), ("R07", REVIEW), ("R08", REVIEW),
    ("R09", "AI3"), ("R10", REVIEW),
])
def test_baseline_strengths_and_documented_semantic_limits(case, expected):
    report = next(r for r in load_cases(project_root()) if r["id"] == case)
    assert baseline(report).route == expected
    assert baseline(report).confidence is None


@pytest.mark.parametrize("confidence,expected", [(0.799, REVIEW), (0.8, "AI3"), (1, "AI3")])
def test_confidence_boundary(confidence, expected):
    result = gate_answer(answer(confidence=confidence))
    assert result.route == expected
    assert result.review_status == "pending"


def test_ties_and_explicit_human_option_are_not_specialist_suggestions():
    tied = answer(confidence=1)
    tied["probabilities"] = {"AI3": 0.46, "AI4": 0.46, "AI5": 0.02, "AI6": 0.03, REVIEW: 0.03}
    assert gate_answer(tied).route == REVIEW
    assert gate_answer(answer(REVIEW)).reason == "model_requested_review"


@pytest.mark.parametrize("value", [True, None, "0.9", -0.1, 1.1, math.nan, math.inf])
def test_invalid_confidence_and_threshold_fail_closed(value):
    with pytest.raises(InputError):
        gate_answer(answer(confidence=value))
    with pytest.raises(InputError):
        gate_answer(answer(), value)


@pytest.mark.parametrize("change", [
    {"type": "score"}, {"choice": "AI7"}, {"choice": []}, {"choice": None},
    {"probabilities": {}}, {"probabilities": None},
    {"probabilities": {key: 0.8 for key in ROUTES}},
    {"probabilities": {key: True for key in ROUTES}},
    {"probabilities": {key: math.nan for key in ROUTES}},
    {"choice": "AI4"},
])
def test_bad_answers_are_rejected(change):
    data = answer()
    data.update(change)
    with pytest.raises(InputError):
        gate_answer(data)


@pytest.mark.parametrize("mutation", ["not-fictional", "unknown-field", "duplicate", "oversize", "invalid-id", "nontext", "empty"])
def test_fixture_contract(mutation):
    data = {"fictional": True, "reports": load_cases(project_root())}
    if mutation == "not-fictional": data["fictional"] = "true"
    if mutation == "unknown-field": data["reports"][0]["expected_route"] = "AI3"
    if mutation == "duplicate": data["reports"][1]["id"] = "R01"
    if mutation == "oversize": data["reports"][0]["title"] = "x" * 2001
    if mutation == "invalid-id": data["reports"][0]["id"] = "../private"
    if mutation == "nontext": data["reports"][0]["steps"] = None
    if mutation == "empty": data["reports"] = []
    with pytest.raises(InputError):
        validate_reports(data)


def test_labels_and_rationales_are_never_in_request_state():
    root = project_root()
    for report in load_cases(root):
        request = request_payload({**report, "expected_route": "SECRET_LABEL", "rationale": "SECRET_REASON"}, "jev-latest")
        assert request["state"] == {"report": report}
        assert "SECRET_" not in json.dumps(request)
    assert load_labels(root, load_cases(root))["status"] == "authored_expectations_pending_owner_review"


def test_replay_exposes_confident_error_deferrals_and_bad_contract():
    result = evaluate_routing(project_root(), mode="replay")
    rows = {row["id"]: row for row in result["rows"]}
    assert rows["R12"]["selected"]["route"] == "AI4"
    assert rows["R12"]["expected"] == "AI6"
    assert rows["R13"]["selected"]["route"] == REVIEW
    assert rows["R14"]["selected"]["reason"] == "adapter_or_contract_error"
    assert rows["R15"]["selected"]["route"] == REVIEW
    assert result["selected_metrics"]["wrong_specialist"] == 1
    assert result["selected_metrics"]["unnecessary_deferrals"] == 3
    assert result["model_evidence"] == "not_measured"
    assert evaluate_routing(project_root(), mode="replay") == result
    report = render_report(result)
    assert "not measured Jev predictions" in report
    assert "Wrong suggestions" in report
    assert chr(0x2014) not in report


def test_metrics_do_not_reward_deferring_every_case():
    rows = [{"expected": "AI3", "selected": {"route": REVIEW}}, {"expected": REVIEW, "selected": {"route": REVIEW}}]
    result = metrics(rows, "selected")
    assert result["decision_matches"] == 1
    assert result["suggestion_coverage"] == 0
    assert result["specialist_precision"] is None
    assert result["unnecessary_deferrals"] == 1


def test_missing_fields_cannot_reach_adapter_or_dispatch_agents(monkeypatch):
    from qa_workflow_lab import agents
    monkeypatch.setattr(agents, "run_agent", lambda *args: pytest.fail("Routing must not dispatch agents"))

    class FakeRouter:
        usage = {"attempts": 0}
        trace = []

        def choose(self, report):
            assert report["id"] not in ("R05", "R06")
            self.usage["attempts"] += 1
            return answer(REVIEW)

    result = evaluate_routing(project_root(), mode="jev", router=FakeRouter())
    assert result["usage"]["attempts"] == 13
    assert all(row["selected"]["review_status"] == "pending" for row in result["rows"])


def test_cli_offline_replay_and_dry_run(tmp_path, monkeypatch):
    from qa_workflow_lab import jev
    monkeypatch.setattr(jev, "JevRouter", lambda *args, **kwargs: pytest.fail("Offline mode cannot initialize a credentialed adapter"))
    assert main(["route-evaluate", "--output", str(tmp_path / "baseline")]) == 0
    # The malformed synthetic response intentionally preserves a nonzero run.
    assert main(["route-evaluate", "--mode", "replay", "--output", str(tmp_path / "replay")]) == 2
    assert main(["route-evaluate", "--mode", "jev", "--dry-run", "--max-calls", "2", "--output", str(tmp_path / "preview")]) == 0
    preview = json.loads((tmp_path / "preview/routing.json").read_text())
    assert len(preview["requests"]) == 2
    assert preview["network_calls"] == 0
    assert preview["deferred_missing_fields"] == ["R05", "R06"]
    assert len(preview["budget_deferred"]) == 11
    assert "Authorization" not in json.dumps(preview)
    assert (tmp_path / "baseline/routing.md").is_file()
    with pytest.raises(SystemExit) as exc:
        main(["route-evaluate", "--mode", "jev", "--allow-network", "--output", str(tmp_path / "baseline")])
    assert exc.value.code == 2


@pytest.mark.parametrize("flags", [
    ["--mode", "jev"], ["--allow-network"], ["--dry-run"], ["--threshold", "nan"],
    ["--mode", "jev", "--dry-run", "--max-calls", "0"],
    ["--mode", "jev", "--dry-run", "--model", "https://example.invalid"],
])
def test_cli_safety_preconditions(tmp_path, flags):
    with pytest.raises(SystemExit) as exc:
        main(["route-evaluate", "--output", str(tmp_path / "run"), *flags])
    assert exc.value.code == 2
    assert not (tmp_path / "run").exists()
