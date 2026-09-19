"""Fictional Relay Arena fixtures, authored for this executable demonstration."""

from .harness import CHECKS
from .models import Bundle


CASES = ("candidate", "evidence-gaps", "corrected-model")


def sample_data(case="candidate"):
    if case not in CASES:
        raise ValueError("Unknown sample case.")
    corrected = case == "corrected-model"
    rows = []
    meta = {"feature": "Relay Arena: upgrade and encounter transitions", "build": "demo-102", "baseline": "demo-101",
            "platforms": ["PC", "Console"], "rule_version": "rules-1", "owner": "Feature QA",
            "fictional": True, "case": case, "client_build": "demo-client-102", "server_build": "demo-server-102",
            "config": "arena-config-3", "mode": "multi-squad", "source_revision": "fixture-1"}

    def add(id, kind, data, build="demo-102", platform="PC"):
        rows.append({"id": id, "kind": kind, "build": build, "platform": platform, "data": data})

    for number, (check, (_, oracle)) in enumerate(CHECKS.items(), 1):
        rule_id = f"RULE-{number:02}"
        add(rule_id, "requirement", {"version": "rules-1", "approved": True, "oracle": oracle, "check": check,
            "risk": "Critical" if number in (1, 3, 4) else "High", "owner": "Gameplay Engineering"})
        for platform in meta["platforms"]:
            evidence = f"ART-{number}-{platform}"
            add(evidence, "artifact", {"type": "assertions", "run": f"run-{number}-{platform}", "readable": True,
                "content": f"Fictional fixture observation: {check}; reviewed rule rules-1. This record is sample data, not a real game test log."}, platform=platform)
            state = "failed" if number == 3 and not corrected else "passed"
            build = "demo-101" if platform == "Console" and number == 5 and not corrected else "demo-102"
            if case == "evidence-gaps" and platform == "Console" and number == 6:
                continue
            add(f"COV-{number}-{platform}", "coverage", {"requirement": rule_id, "rule_version": "rules-1", "result": state,
                "evidence": [evidence], "original_failure": "failure-upgrade-1" if number == 3 else "",
                "failure_disposition": "Reference-model fix reviewed in this fictional scenario" if corrected and number == 3 else ""}, build=build, platform=platform)

    add("CHANGE-1", "change", {"revision": "demo-diff-12", "surface": "upgrade transaction and recovery handoff",
        "diff": "Fixture diff: retry path now restores an upgrade request after the selection acknowledgement.",
        "requirements": ["RULE-03", "RULE-05"], "player_risk": "A repeated upgrade can change combat power or restore an obsolete loadout."})
    add("TRACE-1", "trace", {"session": "session-17", "clock": "server_tick", "expected_power": 15,
        "observed_power": 15 if corrected else 20, "ui_power": 15 if corrected else 20,
        "events": [{"tick": 10, "transaction": "upgrade-7", "action": "request"},
                   {"tick": 11, "transaction": "upgrade-7", "action": "mutation"},
                   {"tick": 12, "transaction": "upgrade-7", "action": "retry"},
                   {"tick": 13, "transaction": "upgrade-7", "action": "reject_duplicate" if corrected else "mutation"}]})
    add("BUG-1", "defect", {"title": "Repeated upgrade request changes authoritative power twice",
        "steps": ["Start with power 10.", "Apply upgrade request upgrade-7.", "Retry the same request after acknowledgement."],
        "expected": "Power remains 15 after duplicate delivery.", "actual": "Power reaches 20 in the failing fixture.",
        "attempts": 3, "failures": 3, "impact": "invalid_outcome", "signature": "upgrade-repeat", "owner": "Gameplay Engineering",
        "evidence": ["TRACE-1"], "state": "closed" if corrected else "open"})
    add("BUG-2", "defect", {"title": "Upgrade icon briefly duplicates after recovery", "steps": ["Recover after an accepted upgrade."],
        "expected": "One current icon.", "actual": "Two icons are described in a fictional report; authoritative state is unknown.",
        "attempts": 3, "failures": 1, "impact": "tactical_readability", "signature": "upgrade-repeat", "owner": "UI Engineering",
        "evidence": ["ART-3-PC"], "state": "closed" if corrected else "open"})

    for build, failures in (("demo-101", 1), ("demo-102", 1 if corrected else 4)):
        add(f"METRIC-{build}", "metric", {"metric": "duplicate_upgrade", "numerator": failures, "denominator": 20,
            "schema": "events-v1" if case != "evidence-gaps" or build == "demo-101" else "events-v2",
            "sample_rate": 1, "window_seconds": 60, "config": "arena-config-3", "complete": True,
            "sessions": [f"session-{build}-0"], "query": "approved_local_exposure_query"}, build=build)
        for number in range(20):
            add(f"EV-{build}-{number}", "metric_event", {"metric": "duplicate_upgrade", "event_id": f"commit-{number}",
                "eligible": True, "violation": number < failures, "config": "arena-config-3", "session": f"session-{build}-{number}",
                "second": number * 2}, build=build)
    add("ASSIGN-1", "assignment", {"owner": "External QA Lead", "setup": ["Use demo-102 and rules-1.", "Start an eligible upgrade with power 10."],
        "actions": ["Apply one upgrade.", "Retry the same transaction.", "Capture the authoritative parameter and UI at the same server tick."],
        "requirements": ["RULE-03"], "required_evidence": ["state", "trace"], "escalation": "Stop the affected scenario for an authoritative duplicate mutation; retain the failing record."})
    for number in (1, 2):
        for kind in ("state", "trace"):
            add(f"SUBART-{number}-{kind}", "artifact", {"type": kind, "run": f"remote-{number}", "readable": True,
                "content": f"Fictional {kind} excerpt for remote-{number}; expected power 15, observed {15 if corrected else 20}."})
        evidence = [f"SUBART-{number}-state", f"SUBART-{number}-trace"]
        if number == 2 and not corrected:
            evidence.pop()
        add(f"SUB-{number}", "submission", {"assignment": "ASSIGN-1", "run": f"remote-{number}", "rule_version": "rules-1",
            "result": "passed" if corrected or number == 2 else "failed", "expected": "Power 15 after duplicate delivery.",
            "actual": "Power 15." if corrected else "Reported power 20.", "expected_value": 15, "actual_value": 15 if corrected else 20, "evidence": evidence},
            build="demo-101" if case == "evidence-gaps" and number == 1 else "demo-102")

    for number, owner, deps, source, state, action in (
        (1, "Feature QA", [], "SUB-1", "accepted", "Confirm the assignment evidence contract."),
        (2, "Gameplay Engineering", ["TASK-1"], "TRACE-1", "accepted" if corrected else "running", "Review the duplicate guard and controlled comparison."),
        (3, "QA Engineering", ["TASK-2"], "RULE-03", "accepted" if corrected else "queued", "Review generated regression assertions and retest scope."),
        (4, "QA Lead", ["TASK-3"], "COV-3-PC", "queued", "Review candidate coverage and unresolved player risk."),
    ):
        add(f"TASK-{number}", "task", {"owner": owner, "dependencies": deps, "state": state, "priority": "High",
            "next_action": action, "checkpoint": "candidate review", "evidence": [source], "capacity": 1,
            "work_key": f"upgrade-task-{number}", "receiving_acknowledgement": state == "accepted"})
    return {"metadata": meta, "records": rows}


def sample_bundle(case="candidate"):
    return Bundle.from_dict(sample_data(case))
