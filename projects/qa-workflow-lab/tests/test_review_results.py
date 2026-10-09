"""Review decisions stay tied to measured results and unresolved evidence."""

import copy

import pytest

from qa_workflow_lab.agents import run_all, run_agent, review_record
from qa_workflow_lab.fixtures import sample_bundle
from qa_workflow_lab.reports import artifact_reviews, summary_markdown, workflow_markdown
from qa_workflow_lab.review import PIPELINES, review_summary, work_product_tables


def test_candidate_shows_measured_controls_without_erasing_game_evidence_gaps():
    run = run_all(sample_bundle())
    summary = review_summary(run)
    assert summary["assessment"] == "hold"
    assert (summary["control_pairs"], summary["valid_controls_passed"], summary["injected_faults_detected"]) == (6, 6, 6)
    assert (summary["coverage_passed"], summary["coverage_total"], summary["coverage_gaps"]) == (9, 12, 3)
    assert summary["blocked_tasks"] == 2
    assert run["workflows"][7]["product_verdict"] == "hold_for_evidence"
    assert "2 candidate defect(s)" in " ".join(summary["reasons"])
    assert all(a["owner"] and a["action"] and a["verify"] for a in summary["actions"])
    ids = {r["id"] for r in run["records"]}
    assert all(set(a["evidence"]) <= ids for a in summary["actions"])


def test_corrected_case_requests_human_review_without_release_approval():
    run = run_all(sample_bundle("corrected-model"))
    summary = review_summary(run)
    assert summary["assessment"] == "review_required"
    assert summary["coverage_passed"] == 12
    assert summary["coverage_gaps"] == summary["blocked_tasks"] == 0
    assert summary["actions"] == []
    assert run["workflows"][7]["product_verdict"] == "ready_for_human_review"


def test_schema_drift_preserves_block_and_removes_rate_comparison():
    run = run_all(sample_bundle("evidence-gaps"))
    summary = review_summary(run)
    assert summary["assessment"] == "hold" and summary["blocked_workflows"] == 1
    telemetry = run["workflows"][4]
    assert not any(t["title"] == "Comparable exposure rates" for t in work_product_tables(telemetry))
    assert any(a["workflow"] == "AI5" and "corrected inputs" in a["action"] for a in summary["actions"])


@pytest.mark.parametrize("field", ["valid", "fault"])
def test_broken_control_pair_holds_even_when_fixture_coverage_passes(field):
    run = run_all(sample_bundle("corrected-model"))
    control = run["workflows"][1]["details"]["runs"][0]
    control[field]["passed"] = field == "fault"
    control["detected"] = False
    summary = review_summary(run)
    assert summary["assessment"] == "hold" and summary["control_failures"] == 1


def test_single_workflow_never_claims_a_complete_candidate_assessment():
    run = {"workflows": [run_agent(sample_bundle(), "AI2").to_dict()]}
    summary = review_summary(run)
    assert summary["assessment"] == "incomplete_scope"
    assert summary["coverage_total"] == 0


def test_exclusions_are_distinct_from_passed_tests():
    bundle = sample_bundle("corrected-model")
    bundle.get("COV-1-PC")["data"].update(result="not_applicable", exclusion_approved=True, exclusion_reason="Reviewed sample exclusion")
    summary = review_summary(run_all(bundle))
    assert summary["coverage_passed"] == 11
    assert summary["coverage_excluded"] == 1
    assert summary["coverage_gaps"] == 0


def test_tables_and_markdown_retain_actual_sql_counts_owners_and_checkpoints():
    run = run_all(sample_bundle())
    before = copy.deepcopy(run)
    tables = work_product_tables(run["workflows"][4])
    assert tables[0]["rows"] == [["METRIC-demo-101", 1, 20], ["METRIC-demo-102", 4, 20]]
    assert tables[1]["rows"][0][-1] == "+15.00"
    lead = workflow_markdown(run["workflows"][7])
    assert "QA task handoffs" in lead and "Checkpoint:" in lead
    assert "TRACE-1" in lead and "Gameplay Engineering" in lead
    summary = summary_markdown(run)
    assert "Priority Actions" in summary and "6/6 injected faults detected" in summary
    assert "9/12 passed" in summary and "Rerun this rule on the candidate build" in summary
    assert run == before


def test_acknowledged_handoff_is_information_and_includes_linked_evidence():
    lead = run_all(sample_bundle())["workflows"][7]
    finding = lead["findings"][0]
    assert finding["risk"] == "Info" and "acknowledged" in finding["title"]
    assert finding["evidence"] == ["TASK-1", "SUB-1"]
    assert "receiving" in finding["verification"].lower()


def test_every_workflow_has_a_readable_input_check_output_and_human_handoff():
    run = run_all(sample_bundle("corrected-model"))
    assert set(PIPELINES) == {r["workflow"] for r in run["workflows"]}
    for workflow in run["workflows"]:
        pipeline = PIPELINES[workflow["workflow"]]
        assert set(pipeline) == {"inputs", "checks", "output", "handoff"}
        assert all(value.strip() for value in pipeline.values())
        assert "Workflow Pipeline" in workflow_markdown(workflow)


def test_failed_executed_control_holds_the_lead_assessment_and_assigns_an_action(monkeypatch):
    from qa_workflow_lab import analysis
    original = analysis.run_check

    def broken_control(check, *, faulty=False):
        result = original(check, faulty=faulty)
        if check == "single_upgrade" and not faulty:
            result.update(actual=20, passed=False)
        return result

    monkeypatch.setattr(analysis, "run_check", broken_control)
    run = run_all(sample_bundle("corrected-model"))
    assert run["workflows"][7]["product_verdict"] == "hold_for_control_failure"
    summary = review_summary(run)
    assert summary["assessment"] == "hold"
    assert summary["control_failures"] == 1
    assert any(a["workflow"] == "AI2" and a["owner"] == "QA Engineering" for a in summary["actions"])


def test_owner_review_is_separate_from_the_run_and_expires_when_evidence_changes():
    run = run_all(sample_bundle("corrected-model"))
    original = copy.deepcopy(run)
    record = review_record(run, "AI8", "Test Reviewer", "accepted", "Reviewed artifact presentation.")
    assert artifact_reviews(run, [record])["AI8"]["decision"] == "accepted"
    assert run == original and run["workflows"][7]["review_status"] == "pending"
    run["records"][0]["data"]["owner"] = "Changed owner"
    assert artifact_reviews(run, [record]) == {}


def test_later_rejection_replaces_acceptance_without_changing_candidate_verdict():
    run = run_all(sample_bundle())
    accepted = review_record(run, "AI8", "Test Reviewer", "accepted", "Presentation accepted.")
    rejected = review_record(run, "AI8", "Test Reviewer", "rejected", "Revoked for further review.")
    assert artifact_reviews(run, [accepted, rejected])["AI8"]["decision"] == "rejected"
    assert review_summary(run)["assessment"] == "hold"
