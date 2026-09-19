"""Negative contracts: incomplete evidence must never earn a stronger verdict."""

import copy
import io
import json
import urllib.error
import urllib.request

import pytest

from qa_workflow_lab.agents import run_agent, run_all
from qa_workflow_lab.analysis import ANALYZERS
from qa_workflow_lab.cli import main, package_project, project_root
from qa_workflow_lab.fixtures import CASES, sample_bundle
from qa_workflow_lab.models import Bundle, InputError, digest
from qa_workflow_lab.provider import NoRedirect, OpenAIPolicy
from qa_workflow_lab.queries import query_exposure


@pytest.fixture
def model_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-secret")
    monkeypatch.setenv("OPENAI_MODEL", "mock-model")


def choose_response(raw):
    policy = OpenAIPolicy(enabled=True, transport=lambda *args, **kwargs: io.BytesIO(raw))
    return policy.choose({"instructions": "Test", "allowed_tools": ["catalog"], "remaining_seconds": 10})


@pytest.mark.parametrize("body", [
    None, [], "invalid", 123,
    {"status": "completed", "usage": []},
    {"status": "completed", "usage": {"input_tokens": -1}},
    {"status": "completed", "usage": {"output_tokens": "secret"}},
    {"status": "completed", "output": None},
    {"status": "completed", "output": [None]},
    {"status": "completed", "output": [{"type": "message", "content": None}]},
    {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text"}]}]},
    {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": 4}]}]},
], ids=["null", "list", "text", "number", "invalid-usage", "negative-tokens", "invalid-tokens",
        "null-output", "null-item", "null-content", "missing-text", "numeric-text"])
def test_malformed_provider_envelope_has_safe_contract_error(model_environment, body):
    with pytest.raises(InputError) as error:
        choose_response(json.dumps(body).encode())
    assert "secret" not in str(error.value)


@pytest.mark.parametrize("raw", [b"not json", b"\xff", b"x" * 1_000_001,
    b'{"status":"incomplete"}', b'{"status":"completed","output":[]}',
    b'{"status":"completed","output":[{"type":"message","content":[{"type":"refusal"}]}]}',
    b'{"status":"completed","output":[{"type":"message","content":[{"type":"output_text","text":"bad json"}]}]}',
], ids=["invalid-json", "invalid-encoding", "oversize", "incomplete", "empty", "refusal", "invalid-action"])
def test_invalid_or_incomplete_provider_response_is_rejected(model_environment, raw):
    with pytest.raises(InputError):
        choose_response(raw)


@pytest.mark.parametrize("exception", [TimeoutError("test-only-secret"),
    urllib.error.URLError("test-only-secret"), OSError("test-only-secret")])
def test_transport_failure_does_not_retry_or_disclose_details(model_environment, exception):
    calls = []

    def fail(*args, **kwargs):
        calls.append(True)
        raise exception

    policy = OpenAIPolicy(enabled=True, transport=fail)
    with pytest.raises(InputError, match="no automatic retry") as error:
        policy.choose({"instructions": "Test", "allowed_tools": ["catalog"], "remaining_seconds": 10})
    assert len(calls) == 1
    assert "test-only-secret" not in str(error.value)


def test_oversize_context_never_reaches_transport(model_environment):
    calls = []
    policy = OpenAIPolicy(enabled=True, transport=lambda *args, **kwargs: calls.append(True))
    with pytest.raises(InputError, match="request budget"):
        policy.choose({"instructions": "x" * 200_001, "allowed_tools": [], "remaining_seconds": 10})
    assert calls == []


def test_redirect_cannot_forward_authorization():
    with pytest.raises(InputError, match="redirect rejected"):
        NoRedirect().redirect_request(urllib.request.Request("https://api.openai.com/v1/responses"),
                                     None, 307, "Redirect", {}, "https://example.invalid/")


@pytest.mark.parametrize("missing", ["OPENAI_API_KEY", "OPENAI_MODEL"])
def test_model_mode_requires_explicit_environment(model_environment, monkeypatch, missing):
    monkeypatch.delenv(missing)
    with pytest.raises(InputError, match="environment"):
        OpenAIPolicy(enabled=True)


@pytest.mark.parametrize("field", ["config", "metric", "event_id"])
@pytest.mark.parametrize("value", [None, "", "   ", 42])
def test_invalid_event_identity_is_rejected_before_sql(field, value):
    bundle = sample_bundle()
    bundle.get("EV-demo-102-0")["data"][field] = value
    with pytest.raises(InputError, match="identity"):
        query_exposure(bundle, bundle.get("METRIC-demo-102"))


def test_parameterized_query_treats_sql_text_as_data():
    bundle = sample_bundle()
    metric = copy.deepcopy(bundle.get("METRIC-demo-102"))
    metric["data"]["config"] = "'; DROP TABLE exposure; --"
    actual = query_exposure(bundle, metric)
    assert (actual["numerator"], actual["denominator"]) == (0, 0)
    assert query_exposure(bundle, bundle.get("METRIC-demo-102"))["denominator"] == 20


def test_reordered_event_deliveries_produce_same_counts():
    bundle = sample_bundle()
    expected = query_exposure(bundle, bundle.get("METRIC-demo-102"))
    bundle.records.reverse()
    assert query_exposure(bundle, bundle.get("METRIC-demo-102")) == expected


@pytest.mark.parametrize("case", CASES)
def test_repeated_execution_preserves_inputs_and_decisions(case):
    bundle = sample_bundle(case)
    before = bundle.fingerprint
    expected = digest(run_all(bundle))
    for _ in range(10):
        assert digest(run_all(bundle)) == expected
        assert bundle.fingerprint == before


@pytest.mark.parametrize("workflow", ["AI1", "AI2", "AI3", "AI4", "AI5", "AI6", "AI7", "AI8"])
def test_empty_evidence_blocks_every_workflow(workflow):
    bundle = sample_bundle()
    bundle.records.clear()
    result = run_agent(bundle, workflow)
    assert result.status == "blocked"
    assert result.product_verdict == "unverified"


@pytest.mark.parametrize("missing", ["acknowledgement", "evidence", "current_build"])
def test_invalid_accepted_dependency_blocks_downstream_work(missing):
    bundle = sample_bundle("corrected-model")
    tasks = bundle.select("task")
    parent, child = tasks[:2]
    parent["data"].update(state="accepted", receiving_acknowledgement="Receiving QA", dependencies=[])
    parent["data"]["evidence"] = ["TRACE-1"]
    child["data"]["dependencies"] = [parent["id"]]
    if missing == "acknowledgement":
        parent["data"]["receiving_acknowledgement"] = ""
    elif missing == "evidence":
        parent["data"]["evidence"] = []
    else:
        parent["build"] = "stale-build"
    result = ANALYZERS["AI8"](bundle)
    child_row = next(row for row in result.details["task_register"] if row["source"] == child["id"])
    assert parent["id"] in child_row["blockers"]


@pytest.mark.parametrize("raw", [b"{}", b"[]", b"{bad", b"\xff", b"x" * 2_000_001],
                         ids=["empty-object", "list", "invalid-json", "invalid-encoding", "oversize"])
def test_invalid_bundle_file_is_rejected(tmp_path, raw):
    path = tmp_path / "invalid.json"
    path.write_bytes(raw)
    with pytest.raises(InputError):
        Bundle.load(path)


def test_cli_rejects_invalid_input_without_report_or_traceback(tmp_path, capsys):
    path = tmp_path / "invalid.json"
    path.write_text("{}")
    output = tmp_path / "output"
    with pytest.raises(SystemExit) as error:
        main(["run", "--input", str(path), "--output", str(output)])
    assert error.value.code == 2
    assert not output.exists()
    stderr = capsys.readouterr().err
    assert "Error:" in stderr and "Traceback" not in stderr


def test_existing_package_is_preserved(tmp_path):
    archive = tmp_path / "review.zip"
    archive.write_bytes(b"preserve previous package")
    with pytest.raises(InputError, match="already exists"):
        package_project(project_root(), archive)
    assert archive.read_bytes() == b"preserve previous package"


def test_valid_accepted_dependencies_remain_available():
    result = ANALYZERS["AI8"](sample_bundle("corrected-model"))
    assert all(row["blockers"] == [] for row in result.details["task_register"])


def test_dependency_blockers_propagate_indirectly_regardless_of_record_order():
    bundle = sample_bundle("corrected-model")
    bundle.get("TASK-1")["data"]["receiving_acknowledgement"] = False
    bundle.records.reverse()
    result = ANALYZERS["AI8"](bundle)
    rows = {row["source"]: row for row in result.details["task_register"]}
    assert "TASK-1" in rows["TASK-2"]["blockers"]
    assert "TASK-2" in rows["TASK-3"]["blockers"]
    assert "TASK-3" in rows["TASK-4"]["blockers"]


def test_accepted_task_with_stale_evidence_blocks_dependents():
    bundle = sample_bundle("corrected-model")
    bundle.get("TASK-1")["data"]["evidence"] = ["TRACE-1"]
    bundle.get("TRACE-1")["build"] = "stale-build"
    result = ANALYZERS["AI8"](bundle)
    assert "current-build task evidence" in result.details["task_register"][0]["blockers"]
    assert "TASK-1" in result.details["task_register"][1]["blockers"]


@pytest.mark.parametrize("usage", [{"input_tokens": -1}, {"output_tokens": True}, [], None])
def test_invalid_usage_cannot_be_masked_by_an_otherwise_valid_response(model_environment, usage):
    response = {"status": "completed", "usage": usage, "output": [{"type": "message", "content": [
        {"type": "output_text", "text": '{"tool":"catalog","argument":"","notes":[]}'}]}]}
    with pytest.raises(InputError, match="token accounting"):
        choose_response(json.dumps(response).encode())


@pytest.mark.parametrize("tool,argument", [("compare_telemetry", ""), ("read_evidence", "../private"),
    ("search_evidence", " "), ("catalog", "unexpected"), ("read_evidence", "x" * 201)])
def test_invalid_tool_requests_are_blocked_with_trace(tool, argument):
    class Policy:
        name, model = "mock_model", "test-double"

        def choose(self, context):
            return {"tool": tool, "argument": argument, "notes": []}

    result = run_agent(sample_bundle(), "AI6", Policy())
    assert result.status == "blocked" and result.product_verdict == "unverified"
    assert len(result.trace) == 1 and result.trace[0]["status"] == "error"


@pytest.mark.parametrize("steps,seconds", [(1, 120), (31, 120), (12, 0), (12, 601)])
def test_out_of_range_agent_budgets_are_rejected(steps, seconds):
    with pytest.raises(InputError, match="budget"):
        run_agent(sample_bundle(), "AI6", max_steps=steps, max_seconds=seconds)
