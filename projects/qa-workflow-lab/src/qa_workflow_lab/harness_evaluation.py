"""Bounded execution, separate authored labels, and inspectable harness evidence."""

import hashlib
import json
import re
from pathlib import Path

from .jev import ENDPOINT
from .jev_contracts import ACTIONS, REVIEW, RUBRIC_VERSION, questions, gate
from .models import InputError, digest
from .qa_harnesses import validate_cases, preflight, baseline_action, execute
from .routing_evaluation import cell


def _read(path):
    if path.stat().st_size > 200_000:
        raise InputError("Harness fixture exceeds the 200 KB budget.")
    return json.loads(path.read_text(encoding="utf-8"))


def load_inputs(root, harness="all", case_id=None):
    cases = validate_cases(_read(root / "sample-data/jev-harness-cases.json"))
    labels = _read(root / "tests/jev-harness-labels.json")
    if not isinstance(labels, dict) or set(labels) != {"status", "labels"} or labels["status"] != "authored_expectations_pending_owner_review":
        raise InputError("Keep authored harness labels explicitly pending owner review.")
    if not isinstance(labels["labels"], dict) or set(labels["labels"]) != {case["id"] for case in cases}:
        raise InputError("Labels must match fixture case IDs exactly.")
    for case in cases:
        label = labels["labels"][case["id"]]
        if not isinstance(label, dict) or set(label) != {"action", "rationale"}:
            raise InputError("Invalid harness label shape.")
        if not isinstance(label["action"], str) or label["action"] not in ACTIONS[case["harness"]] or not isinstance(label["rationale"], str) or not label["rationale"].strip():
            raise InputError("Invalid harness label action or rationale.")
    if harness not in ("all", *ACTIONS):
        raise InputError("Unknown harness.")
    selected = [case for case in cases if (harness == "all" or case["harness"] == harness) and (case_id is None or case["id"] == case_id)]
    if not selected:
        raise InputError("No matching harness cases.")
    return selected, labels


def preview(root, *, harness="all", case_id=None, model="jev-latest", max_calls=3):
    cases, _ = load_inputs(root, harness, case_id)
    if not isinstance(model, str) or not re.fullmatch(r"jev-[A-Za-z0-9_.-]{1,60}", model):
        raise InputError("Use a Jev model ID, not a URL or secret.")
    if type(max_calls) is not int or not 1 <= max_calls <= 20:
        raise InputError("Jev request cap must be between 1 and 20.")
    eligible = [case for case in cases if not preflight(case)]
    requests = [{"model": model, "state": {"case": case}, "questions": questions(case["harness"])}
                for case in eligible[:max_calls]]
    if any(len(json.dumps(request).encode("utf-8")) > 20_000 for request in requests):
        raise InputError("A harness request exceeds the 20 KB budget.")
    return {"mode": "dry_run", "network_calls": 0, "credentials_read": False, "endpoint": ENDPOINT,
            "max_calls": max_calls, "requests": requests,
            "local_deferrals": [case["id"] for case in cases if preflight(case)],
            "budget_deferrals": [case["id"] for case in eligible[max_calls:]]}


def evaluate(root, *, mode="baseline", harness="all", case_id=None, classifier=None):
    if mode not in ("baseline", "replay", "jev") or (mode == "jev" and classifier is None):
        raise InputError("Select a supported mode and explicitly enable Jev when requested.")
    cases, labels = load_inputs(root, harness, case_id)
    replay = None
    if mode == "replay":
        replay = _read(root / "sample-data/jev-harness-replay.json")
        all_cases, _ = load_inputs(root)
        expected = {case["id"] for case in all_cases if not preflight(case)}
        if not isinstance(replay, dict) or set(replay) != {"source", "answers"} or replay["source"] != "synthetic_contract_fixture_not_model_predictions":
            raise InputError("Replay must remain explicitly synthetic.")
        if not isinstance(replay["answers"], dict) or set(replay["answers"]) != expected:
            raise InputError("Replay must cover exactly the locally eligible cases.")
    rows = []
    for case in cases:
        simple = baseline_action(case)
        action, reason, answers = simple, "deterministic_baseline", None
        if preflight(case):
            action, reason = REVIEW, preflight(case)
        elif mode != "baseline":
            if mode == "jev" and classifier.stopped:
                action, reason = REVIEW, "circuit_stopped"
            elif mode == "jev" and classifier.usage["attempts"] >= classifier.max_calls:
                action, reason = REVIEW, "request_cap"
            else:
                try:
                    raw = replay["answers"][case["id"]] if mode == "replay" else classifier.classify(case)
                    action, reason = gate(raw, case["harness"])
                    answers = raw
                except InputError:
                    action, reason = REVIEW, "adapter_or_contract_error"
        outcome = execute(case, action)
        label = labels["labels"][case["id"]]
        rows.append({"id": case["id"], "harness": case["harness"], "title": case["title"],
                     "input": case, "input_sha256": digest(case), "baseline_action": simple,
                     "candidate": answers["action"]["choice"] if answers else None,
                     "answers": answers, "decision": action, "reason": reason, "outcome": outcome,
                     "expected_action": label["action"], "rationale": label["rationale"],
                     "action_matches_label": outcome["action"] == label["action"]})
    controls = [row["outcome"]["controls_passed"] for row in rows if row["outcome"]["controls_passed"] is not None]
    mismatches = [row for row in rows if not row["action_matches_label"]]
    metrics = {
        "cases": len(rows), "label_matches": len(rows) - len(mismatches),
        "wrong_non_review_actions": sum(row["outcome"]["action"] != REVIEW for row in mismatches),
        "deferrals": sum(row["outcome"]["action"] == REVIEW for row in rows),
        "control_pairs": len(controls), "failed_control_pairs": controls.count(False),
        "contract_errors": sum(row["reason"] == "adapter_or_contract_error" for row in rows),
        "release_holds": sum(row["outcome"]["product_verdict"] == "hold" for row in rows),
    }
    return {"schema_version": "1", "mode": mode, "rubric_version": RUBRIC_VERSION,
            "rubric_sha256": digest({name: questions(name) for name in ACTIONS}),
            "cases_sha256": digest(cases), "labels_sha256": digest(labels),
            "replay_sha256": digest(replay) if replay else None, "label_status": labels["status"],
            "review_status": "pending", "execution_scope": "local Python reference checks and fictional evidence metadata",
            "model_evidence": ("live_api_responses" if classifier.usage["responses"] else "no_valid_model_response") if mode == "jev" else "not_measured",
            "requested_model": classifier.model if mode == "jev" else None,
            "usage": dict(classifier.usage) if mode == "jev" else {"attempts": 0, "responses": 0},
            "transport_trace": list(classifier.trace) if mode == "jev" else [], "metrics": metrics, "rows": rows}


def exit_code(result):
    if result["metrics"]["contract_errors"]:
        return 2
    return 1 if result["metrics"]["failed_control_pairs"] or result["metrics"]["wrong_non_review_actions"] else 0


def render_report(result):
    m = result["metrics"]
    lines = ["# Bounded QA Harness Review", "", f"Mode: **{result['mode']}**",
             "", "Scope: local Python reference checks and fictional evidence metadata. Human review is pending.",
             "Baseline is deterministic. Replay responses are synthetic contract fixtures, not measured Jev predictions.",
             "", "## Run Summary", "",
             f"- Label matches: {m['label_matches']}/{m['cases']} authored expectations.",
             f"- Wrong non-review actions: {m['wrong_non_review_actions']}; deferrals: {m['deferrals']}.",
             f"- Control pairs: {m['control_pairs']}; failed control pairs: {m['failed_control_pairs']}.",
             f"- Contract errors: {m['contract_errors']}; release holds: {m['release_holds']}.",
             f"- API attempts: {result['usage']['attempts']}; model evidence: {result['model_evidence']}.",
             "", "A passing control pair proves that its fixed assertion detects its injected fault. It does not prove the chosen check was relevant to the report.",
             "", "## Case Review", "",
             "| Case | Harness | Expected action | Effective action | Gate | Label match |",
             "| --- | --- | --- | --- | --- | --- |"]
    for row in result["rows"]:
        outcome = row["outcome"]
        reason = outcome.get("local_gate", row["reason"])
        lines.append("| " + " | ".join(cell(v) for v in (row["id"], row["harness"], row["expected_action"],
                     outcome["action"], reason, row["action_matches_label"])) + " |")
    for row in result["rows"]:
        outcome = row["outcome"]
        lines += ["", "## " + row["id"] + ": " + cell(row["title"]), "",
                  "Build: " + cell(row["input"]["build"].strip() or "missing") + ". Platform: " + cell(row["input"]["platform"].strip() or "missing") + ".",
                  "Authored expectation: " + cell(row["rationale"]),
                  "Disposition: **" + outcome["product_verdict"] + "**. Reviewer: pending."]
        if row["answers"]:
            answers = row["answers"]
            lines += [f"Choice confidence: {answers['action']['confidence']}; bypass probability: {answers['bypass']['noul']}; advisory impact score: {answers['impact']['score']}/2."]
        if outcome.get("gaps"):
            lines += ["Missing or unresolved: " + cell(", ".join(outcome["gaps"])) + "."]
        if outcome.get("coverage"):
            lines += ["", "| Required check | Disposition | Supplied source IDs | Current source IDs |",
                      "| --- | --- | --- | --- |"]
            for item in outcome["coverage"]:
                lines.append("| " + " | ".join(cell(v) for v in (item["check"], item["disposition"],
                             ", ".join(item["source_ids"]) or "none", ", ".join(item["current_source_ids"]) or "none")) + " |")
            lines.append("")
        for operation in outcome["trace"]:
            if operation["tool"] == "blocker_focus":
                lines.append("Blocker focus: " + cell(", ".join(operation["source_ids"]) or "no current blocker reference") + ".")
            if operation["tool"] == "reference_check":
                for control in operation["controls"]:
                    lines.append(f"- {control['check']} ({control['variant']}): expected {control['expected']!r}, actual {control['actual']!r}, assertion passed: {control['passed']}.")
        if outcome.get("intake_draft"):
            lines += ["Follow-up: " + cell(outcome["intake_draft"])]
    lines += ["", "## Review Boundaries", "",
              "Labels are separately authored and pending owner review. Confidence and impact are advisory, not calibrated correctness or verified severity.",
              "Evidence references are mock metadata; files are not opened or inspected. Full source records, local tool traces and hashes are in harness-results.json.",
              "No engine connection, ticket submission or release approval occurs. Review mismatches and deferrals before any live experiment.", ""]
    return "\n".join(lines)


def write_results(result, output):
    output = Path(output)
    files = {"request-preview.json" if result["mode"] == "dry_run" else "harness-results.json":
             json.dumps(result, indent=2, allow_nan=False) + "\n"}
    if result["mode"] != "dry_run":
        files["harness-report.md"] = render_report(result)
    manifest = {"files": {name: hashlib.sha256(text.encode("utf-8")).hexdigest() for name, text in files.items()}}
    files["manifest.json"] = json.dumps(manifest, indent=2) + "\n"
    output.mkdir(parents=True, exist_ok=False)
    for name, text in files.items():
        with (output / name).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
