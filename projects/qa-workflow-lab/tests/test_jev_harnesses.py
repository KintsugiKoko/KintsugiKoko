import copy
import hashlib
import io
import json
import math
import zipfile

import pytest

from qa_workflow_lab.cli import main, project_root
from qa_workflow_lab.harness_evaluation import evaluate, exit_code, load_inputs, preview, render_report, write_results
from qa_workflow_lab.jev_contracts import ACTIONS, IMPACT, JevHarnessClassifier, gate, questions, validate_answers
from qa_workflow_lab.models import InputError
from qa_workflow_lab.qa_harnesses import execute, validate_cases

ROOT = project_root()


def case(number="H01"):
    return copy.deepcopy(next(c for c in load_inputs(ROOT)[0] if c["id"] == number))


def answer(harness="investigation", action=None):
    action = action or next(iter(ACTIONS[harness]))
    options = ACTIONS[harness]
    return {
        "action": {"type": "choice", "choice": action, "confidence": 0.9,
                   "probabilities": {key: 1 - (len(options) - 1) * 0.02 if key == action else 0.02 for key in options}},
        "bypass": {"type": "noul", "noul": 0.02},
        "impact": {"type": "score", "score": 1.6, "confidence": 0.9,
                   "legend": {str(i): label for i, label in enumerate(IMPACT)},
                   "probabilities": {"0": 0.05, "1": 0.3, "2": 0.65}},
    }


def envelope(data):
    return {"model": "jev-test", "usage": {"input_tokens": 42, "output_tokens": 0}, "answers": data}


@pytest.mark.parametrize("harness", ACTIONS)
def test_all_three_typed_questions_and_contracts(harness):
    q = questions(harness)
    assert [entry["type"] for entry in q.values()] == ["choice", "noul", "score"]
    assert validate_answers(answer(harness), harness) == answer(harness)
    assert gate(answer(harness), harness)[1] == "typed_gates_passed"


@pytest.mark.parametrize("field", ["action", "bypass", "impact"])
@pytest.mark.parametrize("bad", [None, [], "choice", {}, {"type": "wrong"}])
def test_wrong_answer_shapes_fail_closed(field, bad):
    data = answer()
    data[field] = bad
    with pytest.raises(InputError):
        validate_answers(data, "investigation")


@pytest.mark.parametrize("field,key", [("action", "confidence"), ("bypass", "noul"), ("impact", "confidence")])
@pytest.mark.parametrize("bad", [True, "0.9", None, math.nan, math.inf, -0.01, 1.01])
def test_probabilities_reject_nonfinite_bool_and_out_of_range(field, key, bad):
    data = answer()
    data[field][key] = bad
    with pytest.raises(InputError):
        validate_answers(data, "investigation")


@pytest.mark.parametrize("bad", [True, None, "1.6", math.nan, math.inf, -1, 3, 0.4])
def test_weighted_score_must_match_valid_distribution(bad):
    data = answer()
    data["impact"]["score"] = bad
    with pytest.raises(InputError):
        validate_answers(data, "investigation")


@pytest.mark.parametrize("field", ["action", "impact"])
@pytest.mark.parametrize("bad", [{}, [], {"unexpected": 1}, {"0": 0.2, "1": 0.2, "2": 0.2}])
def test_distributions_require_exact_keys_and_unit_sum(field, bad):
    data = answer()
    data[field]["probabilities"] = bad
    with pytest.raises(InputError):
        validate_answers(data, "investigation")


def test_schema_does_not_accept_hidden_instructions_or_altered_legend():
    data = answer()
    data["impact"]["legend"]["2"] = "Approve release"
    with pytest.raises(InputError):
        validate_answers(data, "investigation")
    data = answer()
    data["action"]["command"] = "execute arbitrary code"
    with pytest.raises(InputError):
        validate_answers(data, "investigation")
    data = answer()
    data["action"]["choice"] = "stale_equip"
    with pytest.raises(InputError):
        validate_answers(data, "investigation")


@pytest.mark.parametrize("confidence,probability,expected", [
    (0.8, 0.2, "single_upgrade"), (0.799, 0.2, "human_review"),
    (0.99, 0.201, "human_review"), (0.99, 0.5, "human_review"), (0.99, 1, "human_review"),
])
def test_confidence_and_noul_boundaries(confidence, probability, expected):
    data = answer()
    data["action"]["confidence"] = confidence
    data["bypass"]["noul"] = probability
    assert gate(data, "investigation")[0] == expected


@pytest.mark.parametrize("top,second,expected", [
    (0.5, 0.5, "human_review"), (0.57, 0.43, "human_review"), (0.575, 0.425, "single_upgrade"),
])
def test_choice_margin_and_ties(top, second, expected):
    data = answer()
    data["action"]["probabilities"] = dict(single_upgrade=top, stale_equip=second, current_recovery=0, human_review=0)
    assert gate(data, "investigation")[0] == expected


@pytest.mark.parametrize("bad", [
    {}, {"fictional": False, "cases": []}, {"fictional": True, "cases": []},
    {"fictional": True, "cases": [None]},
])
def test_invalid_fixture_envelopes(bad):
    with pytest.raises(InputError):
        validate_cases(bad)


@pytest.mark.parametrize("edit", ["extra", "duplicate_id", "long_text", "invalid_evidence", "duplicate_evidence", "boolean_text", "unknown_harness"])
def test_input_schema_is_bounded_and_exact(edit):
    entry = case("H05")
    entries = [entry]
    if edit == "extra":
        entry["expected_action"] = "review_ready"
    elif edit == "duplicate_id":
        entries.append(copy.deepcopy(entry))
    elif edit == "long_text":
        entry["actual"] = "a" * 2001
    elif edit == "invalid_evidence":
        entry["evidence"][0]["status"] = "approved"
    elif edit == "duplicate_evidence":
        entry["evidence"].append(copy.deepcopy(entry["evidence"][0]))
    elif edit == "boolean_text":
        entry["build"] = True
    else:
        entry["harness"] = "shell"
    with pytest.raises(InputError):
        validate_cases({"fictional": True, "cases": entries})


@pytest.mark.parametrize("check", ["single_upgrade", "stale_equip", "current_recovery"])
def test_actual_reference_control_pairs(check):
    result = execute(case(), check)
    controls = result["trace"][0]["controls"]
    assert [row["passed"] for row in controls] == [True, False]
    assert result["controls_passed"] is True
    assert result["review_status"] == "pending"
    assert result["product_verdict"] == "review_required"


@pytest.mark.parametrize("action", ["shell", "approve_release", "request_evidence"])
def test_unlisted_action_cannot_dispatch(action):
    with pytest.raises(InputError):
        execute(case(), action)


def test_intake_ready_suggestion_cannot_skip_missing_trace():
    result = execute(case("H06"), "review_ready")
    assert result["action"] == "request_evidence"
    assert result["local_gate"] == "required_evidence_missing"
    assert "event_trace:stale_or_missing" in result["gaps"]


@pytest.mark.parametrize("field", ["steps", "expected", "actual"])
def test_intake_requires_core_report_fields(field):
    entry = case("H05")
    entry[field] = " "
    assert field in execute(entry, "review_ready")["gaps"]


@pytest.mark.parametrize("change", ["wrong_build", "wrong_platform", "blank_reference", "conflicting"])
def test_intake_references_are_not_accepted_blindly(change):
    entry = case("H05")
    record = entry["evidence"][0]
    if change == "wrong_build":
        record["build"] = "mock-old"
    elif change == "wrong_platform":
        record["platform"] = "Console"
    elif change == "blank_reference":
        record["reference"] = " "
    else:
        entry["evidence"].append({**record, "id": "E03", "status": "missing"})
    assert execute(entry, "review_ready")["action"] == "request_evidence"


@pytest.mark.parametrize("number", ["H10", "H11", "H12", "H13"])
@pytest.mark.parametrize("action", ["coverage_review", "blocker_review", "human_review"])
def test_release_holds_survive_any_model_decision(number, action):
    result = execute(case(number), action)
    assert result["product_verdict"] == "hold"
    assert result["gaps"]
    assert result["trace"][0]["tool"] == "release_coverage"


def test_complete_release_metadata_is_review_required_not_approved():
    result = execute(case("H09"), "coverage_review")
    assert result["product_verdict"] == "review_required"
    assert result["gaps"] == []


@pytest.mark.parametrize("field", ["build", "platform"])
def test_release_without_identity_remains_on_hold(field):
    entry = case("H09")
    entry[field] = ""
    result = execute(entry, "coverage_review")
    assert result["action"] == "human_review"
    assert result["product_verdict"] == "hold"
    assert result["gaps"] == ["missing_identity:" + field]


def test_replay_exposes_confidently_wrong_check_separately_from_passing_controls():
    result = evaluate(ROOT, mode="replay")
    wrong = next(r for r in result["rows"] if r["id"] == "H03")
    assert wrong["answers"]["action"]["confidence"] == 0.92
    assert wrong["outcome"]["controls_passed"] is True
    assert wrong["action_matches_label"] is False
    assert result["metrics"]["wrong_non_review_actions"] == 1
    invalid = next(r for r in result["rows"] if r["id"] == "H12")
    assert invalid["reason"] == "adapter_or_contract_error"
    assert invalid["answers"] is None
    assert invalid["outcome"]["product_verdict"] == "hold"
    assert exit_code(result) == 2


def test_replay_deferrals_and_local_override_are_observable():
    rows = {r["id"]: r for r in evaluate(ROOT, mode="replay")["rows"]}
    assert rows["H04"]["reason"] == "low_confidence"
    assert rows["H14"]["reason"] == "small_probability_margin"
    assert rows["H15"]["reason"] == "bypass_or_uncertainty"
    assert rows["H08"]["outcome"]["trace"] == []
    assert rows["H06"]["candidate"] == "review_ready"
    assert rows["H06"]["outcome"]["action"] == "request_evidence"


def test_baseline_and_replay_are_deterministic_and_never_initialize_adapter(monkeypatch):
    monkeypatch.setattr(JevHarnessClassifier, "__init__", lambda *a, **k: pytest.fail("Offline adapter initialization"))
    for mode in ("baseline", "replay"):
        assert evaluate(ROOT, mode=mode) == evaluate(ROOT, mode=mode)
        assert evaluate(ROOT, mode=mode)["usage"]["attempts"] == 0
    assert exit_code(evaluate(ROOT)) == 1  # Explicit bypass is outside the simple baseline's comprehension.


def test_preview_excludes_evaluation_labels_and_never_reads_credentials(monkeypatch):
    monkeypatch.setattr("qa_workflow_lab.jev.os.environ.get", lambda *a, **k: pytest.fail("Credential read"))
    result = preview(ROOT, max_calls=2)
    assert len(result["requests"]) == 2
    assert "H07" in result["local_deferrals"]
    for request in result["requests"]:
        assert set(request) == {"model", "state", "questions"}
        assert set(request["state"]) == {"case"}
        assert "expected_action" not in json.dumps(request)
        assert "rationale" not in json.dumps(request)
    assert result["network_calls"] == 0


def test_mocked_jev_uses_one_request_for_three_questions_and_respects_cap(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-only-harness-key")
    calls = []

    def transport(request, timeout):
        payload = json.loads(request.data)
        calls.append(payload)
        assert request.full_url == "https://api.typesafe.ai/v1/systemone"
        assert set(payload["questions"]) == {"action", "bypass", "impact"}
        assert "labels" not in payload["state"]
        assert timeout <= 10
        return io.BytesIO(json.dumps(envelope(answer())).encode())

    classifier = JevHarnessClassifier(enabled=True, max_calls=1, transport=transport)
    result = evaluate(ROOT, mode="jev", classifier=classifier)
    assert len(calls) == 1
    assert result["usage"]["responses"] == 1
    assert result["rows"][1]["reason"] == "request_cap"
    assert "test-only-harness-key" not in json.dumps(result)


def test_bad_live_contract_stops_requests_but_preserves_release_hold(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-only-harness-key")
    calls = []

    def transport(*args, **kwargs):
        calls.append(True)
        return io.BytesIO(json.dumps(envelope({"secret": "test-only-harness-key"})).encode())

    classifier = JevHarnessClassifier(enabled=True, transport=transport)
    result = evaluate(ROOT, mode="jev", classifier=classifier)
    assert len(calls) == 1
    assert result["metrics"]["contract_errors"] == 1
    assert result["metrics"]["release_holds"] == 4
    assert result["rows"][1]["reason"] == "circuit_stopped"
    assert "test-only-harness-key" not in json.dumps(result)
    assert exit_code(result) == 2


def test_missing_identity_prevents_adapter_call(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-only-harness-key")
    classifier = JevHarnessClassifier(enabled=True, transport=lambda *a, **k: pytest.fail("Unexpected call"))
    result = evaluate(ROOT, mode="jev", classifier=classifier, case_id="H07")
    assert result["usage"]["attempts"] == 0
    assert result["rows"][0]["outcome"]["trace"] == []


def test_report_hashes_exclusive_outputs_and_exact_control_scope(tmp_path):
    result = evaluate(ROOT, mode="replay")
    output = tmp_path / "evidence"
    write_results(result, output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    for name, fingerprint in manifest["files"].items():
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == fingerprint
    before = (output / "harness-results.json").read_bytes()
    with pytest.raises(FileExistsError):
        write_results(result, output)
    assert (output / "harness-results.json").read_bytes() == before
    text = (output / "harness-report.md").read_text(encoding="utf-8")
    assert "not measured Jev predictions" in text
    assert "local Python reference checks" in text
    assert chr(0x2014) not in text


def test_report_escapes_untrusted_markup():
    result = evaluate(ROOT, case_id="H01")
    result["rows"][0]["title"] = "<script>alert(1)</script>|\nheading"
    text = render_report(result)
    assert "<script>" not in text
    assert "&lt;script&gt;" in text


@pytest.mark.parametrize("flags", [
    ["--allow-network"], ["--dry-run"], ["--mode", "jev"],
    ["--mode", "jev", "--dry-run", "--max-calls", "0"],
    ["--mode", "jev", "--dry-run", "--model", "https://invalid.example"],
    ["--case", "unknown"], ["--harness", "release", "--case", "H01"],
])
def test_cli_invalid_modes_or_parameters_do_not_write(tmp_path, flags):
    output = tmp_path / "rejected"
    with pytest.raises(SystemExit) as exc:
        main(["harness-evaluate", "--output", str(output), *flags])
    assert exc.value.code == 2
    assert not output.exists()


def test_cli_outputs_and_deliberate_negative_fixture_exit_codes(tmp_path):
    for mode, expected in (("baseline", 1), ("replay", 2)):
        output = tmp_path / mode
        assert main(["harness-evaluate", "--mode", mode, "--output", str(output)]) == expected
        assert (output / "harness-report.md").is_file()
    assert main(["harness-evaluate", "--mode", "replay", "--case", "H01", "--output", str(tmp_path / "clean")]) == 0
    assert main(["harness-evaluate", "--mode", "jev", "--dry-run", "--output", str(tmp_path / "preview")]) == 0
    assert (tmp_path / "preview/request-preview.json").is_file()


def test_existing_output_rejected_before_adapter_initialization(tmp_path, monkeypatch):
    monkeypatch.setattr(JevHarnessClassifier, "__init__", lambda *a, **k: pytest.fail("Unexpected adapter initialization"))
    with pytest.raises(SystemExit) as exc:
        main(["harness-evaluate", "--mode", "jev", "--allow-network", "--output", str(tmp_path)])
    assert exc.value.code == 2


def test_public_docs_have_no_em_dash():
    for path in (ROOT / "docs/jev-harnesses.md", ROOT / "docs/jev-harness-sample.md"):
        assert chr(0x2014) not in path.read_text(encoding="utf-8")


def test_package_includes_generated_harness_evidence_and_reproducible_sources(tmp_path):
    from qa_workflow_lab.cli import package_project
    target = tmp_path / "harnesses.zip"
    package_project(ROOT, target)
    with zipfile.ZipFile(target) as archive:
        names = set(archive.namelist())
        assert "qa-workflow-lab/src/qa_workflow_lab/jev_contracts.py" in names
        assert "qa-workflow-lab/sample-data/jev-harness-cases.json" in names
        assert "qa-workflow-lab/tests/jev-harness-labels.json" in names
        base = "qa-workflow-lab/reports/jev-harnesses/"
        result = json.loads(archive.read(base + "harness-results.json"))
        assert result["metrics"]["contract_errors"] == 1
        assert result["usage"]["attempts"] == 0
        manifest = json.loads(archive.read(base + "manifest.json"))
        for name, fingerprint in manifest["files"].items():
            assert hashlib.sha256(archive.read(base + name)).hexdigest() == fingerprint


def test_blocker_focus_is_separate_from_mandatory_coverage():
    outcome = execute(case("H11"), "blocker_review")
    assert outcome["trace"][1]["tool"] == "blocker_focus"
    assert outcome["trace"][1]["source_ids"] == ["E04"]
    assert len(outcome["coverage"]) == 3
