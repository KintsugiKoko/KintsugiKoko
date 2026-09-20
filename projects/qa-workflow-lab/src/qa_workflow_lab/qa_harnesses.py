"""Three small harnesses over fictional records and fixed Python reference checks."""

import re

from .harness import run_check
from .jev_contracts import ACTIONS, REVIEW
from .models import InputError

CASE_FIELDS = {"id", "harness", "title", "build", "platform", "steps", "expected", "actual", "request", "evidence"}
EVIDENCE_FIELDS = {"id", "check", "build", "platform", "status", "reference"}
RELEASE_CHECKS = ("single_upgrade", "stale_equip", "current_recovery")
INTAKE_CHECKS = ("repro_capture", "event_trace")


def validate_cases(data):
    if not isinstance(data, dict) or set(data) != {"fictional", "cases"} or data["fictional"] is not True:
        raise InputError("Harness fixtures must explicitly identify fictional data.")
    cases = data["cases"]
    if not isinstance(cases, list) or not 1 <= len(cases) <= 20:
        raise InputError("Provide 1 to 20 fictional harness cases.")
    seen = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != CASE_FIELDS:
            raise InputError("Unexpected or missing harness case fields.")
        for key in CASE_FIELDS - {"evidence"}:
            if not isinstance(case[key], str) or len(case[key]) > 2000:
                raise InputError("Case text fields must be strings of at most 2000 characters.")
        if not re.fullmatch(r"H[0-9]{2}", case["id"]) or case["id"] in seen or case["harness"] not in ACTIONS:
            raise InputError("Invalid or duplicate harness case identity.")
        seen.add(case["id"])
        if not case["title"].strip() or not isinstance(case["evidence"], list) or len(case["evidence"]) > 20:
            raise InputError("Case needs a title and a bounded evidence list.")
        record_ids = set()
        for record in case["evidence"]:
            if not isinstance(record, dict) or set(record) != EVIDENCE_FIELDS:
                raise InputError("Unexpected or missing evidence fields.")
            if any(not isinstance(value, str) or len(value) > 500 for value in record.values()):
                raise InputError("Evidence values must be bounded strings.")
            if not re.fullmatch(r"E[0-9]{2}", record["id"]) or record["id"] in record_ids:
                raise InputError("Evidence IDs must be unique within a case.")
            record_ids.add(record["id"])
            if record["status"] not in ("pass", "fail", "blocked", "present", "missing"):
                raise InputError("Unknown evidence status.")
    return cases


def preflight(case):
    missing = [key for key in ("build", "platform") if not case[key].strip()]
    return "missing_identity:" + ",".join(missing) if missing else None


def coverage(case, required, acceptable):
    """Preserve every supplied row; stale or contradictory evidence cannot hide a gap."""
    matrix = []
    for check in required:
        records = [r for r in case["evidence"] if r["check"] == check]
        current = [r for r in records if r["build"] == case["build"] and r["platform"] == case["platform"]]
        statuses = {r["status"] for r in current}
        if not current:
            disposition = "stale_or_missing"
        elif len(statuses) > 1:
            disposition = "conflicting"
        elif not all(r["reference"].strip() for r in current):
            disposition = "missing_reference"
        elif statuses != {acceptable}:
            disposition = "not_accepted"
        else:
            disposition = "covered"
        matrix.append({"check": check, "disposition": disposition, "source_ids": [r["id"] for r in records],
                       "current_source_ids": [r["id"] for r in current]})
    return matrix


def intake_gaps(case):
    missing = [key for key in ("steps", "expected", "actual") if not case[key].strip()]
    matrix = coverage(case, INTAKE_CHECKS, "present")
    missing += [r["check"] + ":" + r["disposition"] for r in matrix if r["disposition"] != "covered"]
    return missing, matrix


def baseline_action(case):
    if preflight(case):
        return REVIEW
    if case["harness"] == "intake":
        return "request_evidence" if intake_gaps(case)[0] else "review_ready"
    if case["harness"] == "release":
        blocked = any(r["status"] in ("fail", "blocked") and r["build"] == case["build"]
                      and r["platform"] == case["platform"] for r in case["evidence"])
        return "blocker_review" if blocked else "coverage_review"
    text = " ".join(case[key] for key in ("title", "actual", "request")).lower()
    families = {
        "single_upgrade": ("upgrade", "power twice"),
        "stale_equip": ("equip", "loadout"),
        "current_recovery": ("recovery", "snapshot"),
    }
    matches = [action for action, words in families.items() if any(word in text for word in words)]
    return matches[0] if len(matches) == 1 else REVIEW


def execute(case, action):
    if action not in ACTIONS[case["harness"]]:
        raise InputError("An unlisted operation cannot execute.")
    result = {"action": action, "review_status": "pending", "product_verdict": "review_required",
              "trace": [], "controls_passed": None}
    if preflight(case):
        result.update(action=REVIEW, local_gate=preflight(case))
        if case["harness"] == "release":
            result.update(product_verdict="hold", gaps=[preflight(case)])
        return result

    # Release coverage is mandatory, even if the model defers or the transport fails.
    if case["harness"] == "release":
        matrix = coverage(case, RELEASE_CHECKS, "pass")
        gaps = [r["check"] + ":" + r["disposition"] for r in matrix if r["disposition"] != "covered"]
        result.update(coverage=matrix, gaps=gaps, product_verdict="hold" if gaps else "review_required")
        result["trace"].append({"tool": "release_coverage", "required_checks": list(RELEASE_CHECKS), "matrix": matrix})
        if action == "blocker_review":
            blockers = [r["id"] for r in case["evidence"] if r["build"] == case["build"]
                        and r["platform"] == case["platform"] and r["status"] in ("fail", "blocked")]
            result["trace"].append({"tool": "blocker_focus", "source_ids": blockers,
                                    "next_action": "Review current failures and contradictions with the receiving owner."})
        return result

    if action == REVIEW:
        return result
    if case["harness"] == "investigation":
        controls = [run_check(action), run_check(action, faulty=True)]
        result["trace"].append({"tool": "reference_check", "check": action, "controls": controls})
        result["controls_passed"] = controls[0]["passed"] is True and controls[1]["passed"] is False
        return result

    gaps, matrix = intake_gaps(case)
    effective = "request_evidence" if gaps else action
    result.update(action=effective, gaps=gaps, coverage=matrix,
                  intake_draft="Request: " + ", ".join(gaps) if gaps else "Complete local metadata; human intake review pending.")
    if effective != action:
        result["local_gate"] = "required_evidence_missing"
    result["trace"].append({"tool": "intake_checklist", "missing_items": gaps, "matrix": matrix})
    return result
