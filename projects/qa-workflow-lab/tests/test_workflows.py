import copy
import pytest
from qa_workflow_lab.agents import run_all, run_agent
from qa_workflow_lab.analysis import ANALYZERS
from qa_workflow_lab.fixtures import sample_bundle, sample_data
from qa_workflow_lab.models import Bundle, InputError
from qa_workflow_lab.queries import query_exposure


def test_all_eight_artifacts_are_pending_review_and_traceable():
    run = run_all(sample_bundle())
    assert len(run["workflows"]) == 8
    ids = {r["id"] for r in run["records"]}
    for result in run["workflows"]:
        assert result["status"] == "review_required"
        assert result["review_status"] == "pending"
        assert result["trace"][-1]["tool"] == "finish"
        assert all(set(f["evidence"]) <= ids for f in result["findings"])
    assert run["workflows"][6]["product_verdict"] == "hold_for_evidence"


def test_corrected_fixture_retains_human_release_decision():
    result = ANALYZERS["AI7"](sample_bundle("corrected-model"))
    assert result.product_verdict == "ready_for_human_review"
    assert result.review_status == "pending"


def test_remote_missing_evidence_does_not_become_pass():
    result = ANALYZERS["AI6"](sample_bundle())
    first, second = result.details["submissions"]
    assert first["disposition"] == "actionable"
    assert first["reported_result"] == "failed"
    assert second["disposition"] == "incomplete"
    assert "trace evidence" in second["gaps"]
    assert "reported pass contradicts supplied assertion values" in second["gaps"]


@pytest.mark.parametrize("mutation,gap", [
    ("wrong_build", "matching assigned build"), ("wrong_rule", "current rule version"),
    ("unreadable", "readable artifact SUBART-1-state"), ("wrong_run", "matching artifact identity SUBART-1-state"),
])
def test_remote_held_out_identity_cases(mutation, gap):
    bundle = sample_bundle("corrected-model")
    if mutation == "wrong_build":
        bundle.get("SUB-1")["build"] = "stale-build"
    elif mutation == "wrong_rule":
        bundle.get("SUB-1")["data"]["rule_version"] = "rules-0"
    else:
        artifact = bundle.get("SUBART-1-state")["data"]
        artifact["readable" if mutation == "unreadable" else "run"] = False if mutation == "unreadable" else "different-run"
    result = ANALYZERS["AI6"](bundle)
    assert gap in result.details["submissions"][0]["gaps"]
    assert result.details["submissions"][0]["disposition"] == "incomplete"


def test_false_followups_absent_for_complete_fixture():
    result = ANALYZERS["AI6"](sample_bundle("corrected-model"))
    assert all(s["gaps"] == [] and s["disposition"] == "actionable" for s in result.details["submissions"])


def test_telemetry_reproduces_rates_with_sql():
    result = ANALYZERS["AI5"](sample_bundle())
    assert result.details["comparisons"][0]["delta_percentage_points"] == 15
    assert [(q["numerator"], q["denominator"]) for q in result.details["queries"]] == [(1, 20), (4, 20)]
    assert all("WHERE build = ?" in q["sql"] for q in result.details["queries"])


def test_incomparable_schema_blocks_trend():
    result = ANALYZERS["AI5"](sample_bundle("evidence-gaps"))
    assert result.status == "blocked"
    assert result.details["comparisons"] == []


def test_duplicate_event_deduplication_and_conflict():
    bundle = sample_bundle()
    duplicate = copy.deepcopy(bundle.get("EV-demo-102-0"))
    duplicate["id"] = "EV-retry"
    bundle.records.append(duplicate)
    result = query_exposure(bundle, bundle.get("METRIC-demo-102"))
    assert (result["numerator"], result["denominator"]) == (4, 20)
    duplicate["data"]["violation"] = False
    with pytest.raises(InputError, match="conflicting"):
        query_exposure(bundle, bundle.get("METRIC-demo-102"))


def test_metric_aggregate_cannot_invent_exposure():
    bundle = sample_bundle()
    bundle.get("METRIC-demo-102")["data"]["denominator"] = 1000
    result = run_agent(bundle, "AI5")
    assert result.status == "blocked"
    assert "disagrees" in result.trace[-1]["output"]["error"]


@pytest.mark.parametrize("field,value", [("window_seconds", 0), ("sample_rate", 0), ("sample_rate", 2)])
def test_invalid_measurement_contract_blocks(field, value):
    bundle = sample_bundle()
    bundle.get("METRIC-demo-102")["data"][field] = value
    assert run_agent(bundle, "AI5").status == "blocked"


def test_old_pass_and_original_failure_remain_visible():
    result = ANALYZERS["AI7"](sample_bundle())
    matrix = result.details["coverage_matrix"]
    assert any(r["requirement"] == "RULE-05" and r["state"] == "stale" for r in matrix)
    assert any(r["state"] == "unresolved_original_failure" for r in matrix)
    assert result.product_verdict == "hold_for_evidence"


def test_passing_retry_does_not_erase_conflicting_failure():
    bundle = sample_bundle("corrected-model")
    failed = copy.deepcopy(bundle.get("COV-1-PC"))
    failed["id"] = "COV-failed-earlier"
    failed["data"]["result"] = "failed"
    bundle.records.append(failed)
    result = ANALYZERS["AI7"](bundle)
    assert result.details["coverage_matrix"][0]["state"] == "conflicting"
    assert result.product_verdict == "hold_for_evidence"


def test_missing_critical_platform_and_unreadable_evidence_hold_candidate():
    bundle = sample_bundle("corrected-model")
    bundle.records = [r for r in bundle.records if r["id"] != "COV-1-Console"]
    bundle.get("ART-3-PC")["data"]["readable"] = False
    result = ANALYZERS["AI7"](bundle)
    assert {"not_run", "unreadable_evidence"} <= {r["state"] for r in result.details["coverage_matrix"]}


def test_duplicate_candidates_keep_separate_reports():
    result = ANALYZERS["AI4"](sample_bundle())
    drafts = result.details["draft_defects"]
    assert len(drafts) == 2
    assert drafts[0]["duplicate_candidates"] == ["BUG-2"]
    assert drafts[0]["actual"] != drafts[1]["actual"]
    assert all(d["disposition"] == "draft_ready" for d in drafts)


def test_investigation_separates_hypothesis_and_executed_model_result():
    result = ANALYZERS["AI3"](sample_bundle())
    assert {f.kind for f in result.findings} == {"observation", "hypothesis"}
    assert result.details["experiment"]["control"]["passed"]
    assert not result.details["experiment"]["fault"]["passed"]


def test_dependency_cycle_blocks_coordination():
    bundle = sample_bundle()
    bundle.get("TASK-1")["data"]["dependencies"] = ["TASK-4"]
    result = run_agent(bundle, "AI8")
    assert result.status == "blocked"
    assert "cycle" in result.trace[-1]["output"]["error"]


def test_completed_task_requires_receiving_acknowledgement():
    bundle = sample_bundle("corrected-model")
    bundle.get("TASK-2")["data"]["receiving_acknowledgement"] = False
    result = ANALYZERS["AI8"](bundle)
    assert "receiving acknowledgement and evidence" in result.details["task_register"][1]["blockers"]


def test_unapproved_exclusion_cannot_hide_required_coverage():
    bundle = sample_bundle("corrected-model")
    bundle.get("COV-1-PC")["data"]["result"] = "not_applicable"
    result = ANALYZERS["AI7"](bundle)
    assert result.details["coverage_matrix"][0]["state"] == "unapproved_exclusion"
    assert result.product_verdict == "hold_for_evidence"


def test_empty_evidence_reference_blocks_release_even_with_pass_label():
    bundle = sample_bundle("corrected-model")
    bundle.get("COV-1-PC")["data"]["evidence"] = []
    result = ANALYZERS["AI7"](bundle)
    assert result.details["coverage_matrix"][0]["state"] == "missing_evidence"


def test_event_outside_window_is_excluded_from_exposure():
    bundle = sample_bundle()
    extra = copy.deepcopy(bundle.get("EV-demo-102-0"))
    extra["id"] = "event-late"
    extra["data"].update(event_id="late", second=60)
    bundle.records.append(extra)
    result = query_exposure(bundle, bundle.get("METRIC-demo-102"))
    assert (result["numerator"], result["denominator"]) == (4, 20)


@pytest.mark.parametrize("change", ["duplicate", "private", "path", "missing_meta"])
def test_input_rejects_invalid_identity(change):
    data = sample_data()
    if change == "duplicate":
        data["records"].append(copy.deepcopy(data["records"][0]))
    elif change == "private":
        data["metadata"]["fictional"] = False
    elif change == "path":
        data["records"][0]["id"] = "../outside"
    else:
        del data["metadata"]["build"]
    with pytest.raises(InputError):
        Bundle.from_dict(data)
