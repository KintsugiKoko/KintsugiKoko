import io
import json
import urllib.error

import pytest

from qa_workflow_lab.cli import project_root
from qa_workflow_lab.jev import ENDPOINT, JevRouter
from qa_workflow_lab.models import InputError
from qa_workflow_lab.routing import ROUTES
from qa_workflow_lab.routing_evaluation import evaluate_routing, load_cases


@pytest.fixture
def report():
    return load_cases(project_root())[0]


@pytest.fixture
def environment(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-only-typesafe-key")


def envelope():
    return {"model": "jev-test", "usage": {"input_tokens": 100, "output_tokens": 0},
            "answers": {"route": {"type": "choice", "choice": "AI3", "confidence": 0.9,
            "probabilities": {route: 0.92 if route == "AI3" else 0.02 for route in ROUTES}}}}


def test_adapter_is_disabled_by_default_even_with_key(environment):
    with pytest.raises(InputError, match="allow-network"):
        JevRouter()


def test_enabled_requires_environment_key():
    with pytest.raises(InputError, match="TYPESAFE_API_KEY"):
        JevRouter(enabled=True)


def test_documented_http_contract_and_capped_attempts(environment, report):
    calls = []

    def transport(request, timeout):
        calls.append(request)
        assert request.full_url == ENDPOINT
        assert request.get_method() == "POST"
        assert request.get_header("Authorization") == "Bearer test-only-typesafe-key"
        assert timeout <= 10
        payload = json.loads(request.data)
        assert payload["state"] == {"report": report}
        assert payload["questions"]["route"]["type"] == "choice"
        assert set(payload["questions"]["route"]["criteria"]) == set(ROUTES)
        return io.BytesIO(json.dumps(envelope()).encode())

    router = JevRouter(enabled=True, max_calls=1, transport=transport)
    assert router.choose(report)["choice"] == "AI3"
    with pytest.raises(InputError, match="budget"):
        router.choose(report)
    assert len(calls) == 1
    assert router.usage == {"attempts": 1, "responses": 1, "input_tokens": 100, "output_tokens": 0}
    assert "test-only-typesafe-key" not in json.dumps(router.trace)


@pytest.mark.parametrize("raw", [b"not json", b"\xff", b"x" * 64_001, b"null", b"[]",
    b'{"model":"jev-test","usage":{},"answers":{}}',
    b'{"model":"jev-test","usage":{"input_tokens":true,"output_tokens":0},"answers":{}}',
    b'{"model":"jev-test","usage":{"input_tokens":-1,"output_tokens":0},"answers":{}}',
], ids=["invalid-json", "invalid-encoding", "oversize", "null", "list", "no-usage", "boolean-usage", "negative-usage"])
def test_invalid_responses_stop_circuit_and_sanitize(environment, report, raw):
    calls = []

    def transport(*args, **kwargs):
        calls.append(True)
        return io.BytesIO(raw)

    router = JevRouter(enabled=True, transport=transport)
    with pytest.raises(InputError, match="circuit stopped") as exc:
        router.choose(report)
    assert "test-only-typesafe-key" not in str(exc.value)
    with pytest.raises(InputError):
        router.choose(report)
    assert len(calls) == 1


@pytest.mark.parametrize("failure", [
    TimeoutError("test-only-typesafe-key"), urllib.error.URLError("test-only-typesafe-key"),
    urllib.error.HTTPError(ENDPOINT, 401, "test-only-typesafe-key", {}, None),
    urllib.error.HTTPError(ENDPOINT, 429, "test-only-typesafe-key", {}, None),
    InputError("Model endpoint redirect rejected."),
])
def test_transport_errors_preserve_review_fallback_without_retry(environment, failure):
    calls = []

    def transport(*args, **kwargs):
        calls.append(True)
        raise failure

    router = JevRouter(enabled=True, transport=transport)
    result = evaluate_routing(project_root(), mode="jev", router=router)
    assert len(calls) == 1
    assert result["selected_metrics"]["human_review"] == 15
    assert result["selected_metrics"]["specialist_precision"] is None
    assert result["model_evidence"] == "no_valid_model_response"
    assert "test-only-typesafe-key" not in json.dumps(result)


@pytest.mark.parametrize("change", [
    {"model": None}, {"model": "secret text with spaces"},
    {"answers": []}, {"answers": {"unexpected": {}}},
    {"answers": {"route": {"type": "choice", "choice": "AI8"}}},
])
def test_semantically_invalid_envelopes_are_not_counted_as_valid_responses(environment, report, change):
    body = envelope()
    body.update(change)
    router = JevRouter(enabled=True, transport=lambda *args, **kwargs: io.BytesIO(json.dumps(body).encode()))
    with pytest.raises(InputError, match="circuit stopped"):
        router.choose(report)
    assert router.usage["attempts"] == 1
    assert router.usage["responses"] == 0


def test_successful_adapter_is_used_by_evaluator_without_labels(environment):
    requests = []

    def transport(request, **kwargs):
        payload = json.loads(request.data)
        requests.append(payload)
        assert "expected_route" not in payload["state"]["report"]
        assert "rationale" not in payload["state"]["report"]
        return io.BytesIO(json.dumps(envelope()).encode())

    router = JevRouter(enabled=True, max_calls=2, transport=transport)
    result = evaluate_routing(project_root(), mode="jev", router=router)
    assert [r["state"]["report"]["id"] for r in requests] == ["R01", "R02"]
    assert result["usage"]["responses"] == 2
    assert result["selected_metrics"]["wrong_specialist"] == 1
    assert result["selected_metrics"]["human_review"] == 13
    assert result["requested_model"] == "jev-latest"


def test_budget_deadline_and_request_size_make_no_call(environment, report):
    router = JevRouter(enabled=True, transport=lambda *args, **kwargs: pytest.fail("Unexpected request"))
    router.deadline = 0
    with pytest.raises(InputError, match="budget"):
        router.choose(report)
    router = JevRouter(enabled=True, transport=lambda *args, **kwargs: pytest.fail("Unexpected request"))
    report["actual"] = "x" * 20_001
    with pytest.raises(InputError, match="request budget"):
        router.choose(report)
