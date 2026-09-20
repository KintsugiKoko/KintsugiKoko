"""Compare a baseline with gated suggestions; evaluation labels never enter requests."""

from collections import Counter
import json
from pathlib import Path

from .models import InputError, digest
from .routing import REVIEW, ROUTES, RUBRIC_VERSION, QUESTION, Suggestion, baseline, gate_answer
from .routing import missing_fields, request_payload, unit_number, validate_reports


def load_json(path):
    path = Path(path)
    if path.stat().st_size > 200_000:
        raise InputError("Routing fixture exceeds the 200 KB local budget.")
    return json.loads(path.read_text(encoding="utf-8"))


def load_cases(root):
    return validate_reports(load_json(root / "sample-data/routing-reports.json"))


def load_labels(root, reports):
    data = load_json(root / "tests/routing-labels.json")
    if not isinstance(data, dict) or data.get("status") != "authored_expectations_pending_owner_review":
        raise InputError("Routing labels must retain their authored-expectation review status.")
    labels = data.get("labels")
    if not isinstance(labels, dict) or set(labels) != {r["id"] for r in reports}:
        raise InputError("Evaluation labels must match the reports exactly.")
    for value in labels.values():
        if not isinstance(value, dict) or set(value) != {"route", "rationale"} or not isinstance(value["route"], str) or value["route"] not in ROUTES or not isinstance(value["rationale"], str) or not value["rationale"].strip():
            raise InputError("Invalid routing evaluation label.")
    return data


def metrics(rows, key):
    counts = Counter()
    confusion = {expected: {actual: 0 for actual in ROUTES} for expected in ROUTES}
    for row in rows:
        expected, actual = row["expected"], row[key]["route"]
        confusion[expected][actual] += 1
        counts["decision_matches"] += expected == actual
        if actual == REVIEW:
            counts["human_review"] += 1
            counts["unnecessary_deferrals"] += expected != REVIEW
        else:
            counts["specialist_suggestions"] += 1
            counts["correct_specialist"] += actual == expected
            counts["wrong_specialist"] += actual != expected
    total, suggested = len(rows), counts["specialist_suggestions"]
    return {"cases": total, "decision_matches": counts["decision_matches"],
            "specialist_suggestions": suggested, "wrong_specialist": counts["wrong_specialist"],
            "human_review": counts["human_review"], "unnecessary_deferrals": counts["unnecessary_deferrals"],
            "suggestion_coverage": suggested / total,
            "specialist_precision": counts["correct_specialist"] / suggested if suggested else None,
            "confusion_matrix": confusion}


def evaluate_routing(root, *, mode="baseline", threshold=0.8, router=None):
    if mode not in ("baseline", "replay", "jev") or not unit_number(threshold):
        raise InputError("Invalid routing mode or confidence threshold.")
    if mode == "jev" and router is None:
        raise InputError("Jev evaluation requires an explicitly enabled adapter.")
    reports = load_cases(root)
    labels = load_labels(root, reports)
    replay = {}
    if mode == "replay":
        fixture = load_json(root / "sample-data/routing-replay.json")
        if fixture.get("source") != "synthetic_contract_fixture_not_model_predictions":
            raise InputError("Replay must be explicitly labeled synthetic, not measured Jev output.")
        replay = fixture["answers"]
        if set(replay) != {r["id"] for r in reports if not missing_fields(r)}:
            raise InputError("Replay answers must cover exactly the eligible routing cases.")
    rows = []
    for report in reports:
        simple = baseline(report)
        result = simple
        if mode != "baseline" and not missing_fields(report):
            try:
                answer = replay[report["id"]] if mode == "replay" else router.choose(report)
                result = gate_answer(answer, threshold)
            except InputError:
                result = Suggestion(REVIEW, "adapter_or_contract_error")
        rows.append({"id": report["id"], "title": report["title"], "expected": labels["labels"][report["id"]]["route"],
                     "rationale": labels["labels"][report["id"]]["rationale"],
                     "baseline": simple.to_dict(), "selected": result.to_dict()})
    model_evidence = "not_measured"
    if mode == "jev":
        model_evidence = "live_api_responses" if router.usage.get("responses", 0) else "no_valid_model_response"
    return {"mode": mode, "rubric_version": RUBRIC_VERSION, "rubric_sha256": digest(QUESTION),
            "cases_sha256": digest(reports), "labels_sha256": digest(labels),
            "label_status": labels["status"], "threshold": threshold, "minimum_margin": 0.15,
            "scope": "Authored fictional cases, pending owner label review. Suggestions only; no dispatch or release decision.",
            "model_evidence": model_evidence,
            "requested_model": getattr(router, "model", None) if mode == "jev" else None,
            "replay_sha256": digest(replay) if mode == "replay" else None,
            "baseline_metrics": metrics(rows, "baseline"), "selected_metrics": metrics(rows, "selected"),
            "usage": dict(router.usage) if mode == "jev" else {"attempts": 0},
            "trace": list(router.trace) if mode == "jev" else [], "rows": rows}


def dry_run(root, model, max_calls):
    reports = load_cases(root)
    load_labels(root, reports)
    if type(max_calls) is not int or not 1 <= max_calls <= 20:
        raise InputError("Jev request cap must be between 1 and 20.")
    eligible = [r for r in reports if not missing_fields(r)]
    return {"mode": "dry_run", "network_calls": 0, "credentials_read": False,
            "endpoint": "https://api.typesafe.ai/v1/systemone", "request_cap": max_calls,
            "eligible_cases": len(eligible), "deferred_missing_fields": [r["id"] for r in reports if missing_fields(r)],
            "budget_deferred": [r["id"] for r in eligible[max_calls:]],
            "requests": [request_payload(r, model) for r in eligible[:max_calls]]}


def cell(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def render_report(result):
    lines = ["# QA Intake Routing Experiment", "", f"Mode: **{result['mode']}**", "", result["scope"], ""]
    if result["mode"] == "replay":
        lines += ["Synthetic replay: these responses exercise gates, including a confidently wrong answer. They are not measured Jev predictions or accuracy.", ""]
    elif result["mode"] == "baseline":
        lines += ["Keyword baseline only. Jev was not called or measured.", ""]
    else:
        lines += ["Live API experiment on authored fixtures. Inspect transport errors and the returned model identities before interpreting results.", ""]
    lines += ["## Comparison", "", "| Method | Label matches | Suggestions | Wrong suggestions | Human review | Unnecessary deferrals |",
              "| --- | --- | --- | --- | --- | --- |"]
    methods = [("Keyword baseline", "baseline_metrics")]
    if result["mode"] != "baseline":
        methods.append((result["mode"], "selected_metrics"))
    for name, key in methods:
        m = result[key]
        lines.append(f"| {name} | {m['decision_matches']}/{m['cases']} | {m['specialist_suggestions']} | {m['wrong_specialist']} | {m['human_review']} | {m['unnecessary_deferrals']} |")
    lines += ["", "The JSON includes suggestion coverage, specialist precision and full confusion matrices. Deferring every case is not evidence of useful routing.",
              "", "## Case Review", "", "| Case | Expected | Baseline | Selected | Reason |", "| --- | --- | --- | --- | --- |"]
    for row in result["rows"]:
        lines.append(f"| {row['id']} | {row['expected']} | {row['baseline']['route']} | {row['selected']['route']} | {cell(row['selected']['reason'])} |")
    lines += ["", "## Reviewer Notes", "", "All suggestions remain pending human review. No workflow was executed, ticket filed or release approved.",
              f"Confidence threshold: {result['threshold']}; minimum probability margin: {result['minimum_margin']}. These are illustrative gates, not calibrated accuracy guarantees.",
              "Labels were authored separately from the inputs and never sent to the routing model. Keith must review them before using this as an accepted evaluation set.",
              "Use a held-out set before claiming improvement. Compare wrong routes, deferrals, coverage, latency and cost against the baseline.",
              f"Request attempts: {result['usage']['attempts']}.", ""]
    return "\n".join(lines)


def write_evaluation(result, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    with (output / "routing.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2, allow_nan=False) + "\n")
    if result["mode"] != "dry_run":
        with (output / "routing.md").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(render_report(result))
