"""Deterministic checks supply facts; agents choose tools and propose follow-up."""

from collections import Counter, defaultdict
from .harness import CHECKS, candidate_source, run_check
from .models import InputError, Result, finding
from .queries import query_exposure


TITLES = {
    "AI1": "Change risk analyst", "AI2": "Regression test author",
    "AI3": "Investigation agent", "AI4": "Defect triage agent",
    "AI5": "Telemetry analyst", "AI6": "Remote QA coordinator",
    "AI7": "Release evidence analyst", "AI8": "QA lead coordinator",
}


def required(data, *keys):
    missing = [key for key in keys if key not in data]
    if missing:
        raise InputError("Missing structured fields: " + ", ".join(missing))


def result_for(workflow):
    return Result(workflow, TITLES[workflow], status="review_required")


def rules(bundle):
    rows = bundle.select("requirement")
    if not rows:
        raise InputError("Approved requirements are missing.")
    for row in rows:
        data = row["data"]
        required(data, "version", "approved", "oracle", "check", "risk", "owner")
        if data["approved"] is not True or data["version"] != bundle.metadata["rule_version"] or not data["oracle"]:
            raise InputError(f"Requirement {row['id']} has an absent, stale, or unapproved oracle.")
        if data["check"] not in CHECKS or data["oracle"] != CHECKS[data["check"]][1]:
            raise InputError(f"Requirement {row['id']} differs from the reviewed local harness contract.")
    return rows


def change_risk(bundle):
    result = result_for("AI1")
    approved = {r["id"]: r for r in rules(bundle)}
    changes = bundle.select("change")
    if not changes:
        raise InputError("Versioned change evidence is missing.")
    coverage = bundle.select("coverage")
    mappings = []
    for record in changes:
        data = record["data"]
        required(data, "revision", "surface", "diff", "requirements", "player_risk")
        for rule_id in data["requirements"]:
            rule = approved.get(rule_id)
            current = [r["id"] for r in coverage if r["data"].get("requirement") == rule_id and r["build"] == bundle.metadata["build"]]
            mappings.append({"change": record["id"], "revision": data["revision"], "surface": data["surface"], "requirement": rule_id,
                             "current_evidence": current, "platforms": bundle.metadata["platforms"]})
            result.findings.append(finding(record, rule_id, f"Review {data['surface']}", data["player_risk"],
                rule["data"]["oracle"] if rule else "Rule owner must confirm expected behavior.",
                "Review current assertions and rerun affected configurations." if current else "Assign missing coverage before readiness review.",
                kind="risk", risk=rule["data"]["risk"] if rule else "High", owner=rule["data"]["owner"] if rule else "Design"))
            if rule:
                result.findings[-1].evidence.append(rule_id)
            else:
                result.status = "blocked"
    result.details = {"risk_to_test_map": mappings}
    return result


def regression(bundle):
    result = result_for("AI2")
    checks, runs = [], []
    for rule in rules(bundle):
        check = rule["data"]["check"]
        checks.append(check)
        valid = run_check(check)
        fault = run_check(check, faulty=True)
        detected = valid["passed"] and not fault["passed"]
        runs.append({"requirement": rule["id"], "valid": valid, "fault": fault, "detected": detected, "fresh_state_per_run": True})
        result.findings.append(finding(rule, "oracle", f"Detection check: {check}",
            f"Valid actual: {valid['actual']!r}; injected-fault actual: {fault['actual']!r}; expected: {valid['expected']!r}.",
            rule["data"]["oracle"], "Review the generated test candidate and integration boundary.", risk="Info", owner="QA Engineering"))
    result.product_verdict = "local_harness_pass" if all(r["detected"] for r in runs) else "local_harness_fail"
    result.details = {"runs": runs, "candidate_test": candidate_source(checks), "scope": "Executable Python reference model; porting requires a team's supported harness."}
    return result


def investigate(bundle):
    result = result_for("AI3")
    rules(bundle)
    traces = bundle.select("trace")
    if not traces:
        raise InputError("No trace was supplied for investigation.")
    timelines = []
    for record in traces:
        data = record["data"]
        required(data, "session", "clock", "events", "expected_power", "observed_power", "ui_power")
        events = data["events"]
        if record["build"] != bundle.metadata["build"] or data["clock"] != "server_tick" or not events:
            result.status = "blocked"
            result.findings.append(finding(record, "gap", "Trace identity needs review", "Build, clock, or event evidence is unsuitable for ordering.",
                "Current build with a shared clock and nonempty events.", "Request an aligned trace.", kind="gap"))
            continue
        for event in events:
            required(event, "tick", "transaction", "action")
            if type(event["tick"]) is not int:
                raise InputError("Trace ticks must be integers.")
        timeline = sorted(events, key=lambda e: e["tick"])
        mutations = Counter(e["transaction"] for e in timeline if e["action"] == "mutation")
        duplicate_ids = [key for key, count in mutations.items() if count > 1]
        timelines.append({"source": record["id"], "session": data["session"], "clock": data["clock"], "events": timeline})
        mismatch = data["observed_power"] != data["expected_power"]
        observation = f"Authoritative power {data['observed_power']}; approved expectation {data['expected_power']}; UI {data['ui_power']}. Repeated mutation IDs: {duplicate_ids}."
        result.findings.append(finding(record, "state", "Authoritative state comparison", observation,
            "One mutation per accepted transaction and the approved effective parameter.",
            "Compare duplicate delivery with a fresh valid transaction; engineering confirms the responsible guard.",
            risk="Critical" if mismatch else "Info", owner="Gameplay Engineering"))
        if mismatch:
            result.findings.append(finding(record, "hypothesis", "Duplicate-request guard may be ineffective",
                "The trace supports a repeated mutation; the responsible implementation has not been inspected.",
                "An isolated comparison should distinguish server mutation from presentation duplication.",
                "Run single_upgrade with a controlled repeated transaction.", kind="hypothesis", owner="Gameplay Engineering"))
    result.details = {"timelines": timelines, "experiment": {"control": run_check("single_upgrade"), "fault": run_check("single_upgrade", faulty=True),
                      "scope": "Local reference-model experiment, not a reproduction in the reported game build."}}
    return result


DEFECT_FIELDS = ("title", "steps", "expected", "actual", "attempts", "failures", "impact", "signature", "owner", "evidence")


def triage(bundle):
    result = result_for("AI4")
    drafts = []
    defects = bundle.select("defect")
    if not defects:
        raise InputError("No defect reports were supplied.")
    for record in defects:
        data = record["data"]
        missing = [k for k in DEFECT_FIELDS if k not in data or data[k] in (None, "", [])]
        if record["build"] != bundle.metadata["build"]:
            missing.append("current build confirmation")
        if type(data.get("attempts")) is not int or type(data.get("failures")) is not int or not 0 <= data.get("failures", -1) <= data.get("attempts", -1) or data.get("attempts", 0) <= 0:
            missing.append("valid repro counts")
        for evidence_id in data.get("evidence", []):
            evidence = bundle.get(evidence_id)
            if evidence["build"] != record["build"]:
                missing.append(f"matching build for {evidence_id}")
        candidates = [r["id"] for r in defects if r["id"] != record["id"] and data.get("signature") and r["data"].get("signature") == data["signature"]]
        severity = "Critical" if data.get("impact") == "invalid_outcome" else "High"
        drafts.append({"source": record["id"], "title": data.get("title", "Untitled submission"), "severity_suggestion": severity,
                       "priority": "QA and production review", "missing": missing, "duplicate_candidates": candidates,
                       "expected": data.get("expected", "Missing"), "actual": data.get("actual", "Missing"),
                       "steps": data.get("steps", []), "evidence": data.get("evidence", []), "disposition": "needs_info" if missing else "draft_ready"})
        result.findings.append(finding(record, "triage", data.get("title", "Incomplete report"),
            "Missing: " + ", ".join(missing) if missing else f"Report fields are complete. Candidate related reports: {candidates}.",
            "Distinct expected/actual behavior, attributable evidence, and valid repro counts.",
            "Request the listed fields." if missing else "Review severity, ownership, and duplicate differences before filing.",
            kind="gap" if missing else "observation", risk=severity, owner=data.get("owner") or "QA"))
    result.details = {"draft_defects": drafts}
    return result


def telemetry(bundle):
    result = result_for("AI5")
    metrics = bundle.select("metric")
    if not metrics:
        raise InputError("No bounded metric results were supplied.")
    groups = defaultdict(dict)
    queries = []
    for record in metrics:
        data = record["data"]
        required(data, "metric", "numerator", "denominator", "schema", "sample_rate", "window_seconds", "config", "complete", "sessions", "query")
        if type(data["window_seconds"]) is not int or data["window_seconds"] <= 0 or type(data["sample_rate"]) not in (float, int) or not 0 < data["sample_rate"] <= 1:
            raise InputError("Metric window and sample rate must be positive and bounded.")
        measured = query_exposure(bundle, record)
        queries.append({"source": record["id"], **measured})
        if measured["numerator"] != data["numerator"] or measured["denominator"] != data["denominator"]:
            raise InputError("Supplied aggregate disagrees with the bounded local exposure query.")
        key = (data["metric"], record["platform"], data["config"])
        if record["build"] in groups[key]:
            raise InputError("Overlapping metric rows need an explicit aggregation rule.")
        groups[key][record["build"]] = record
    comparisons = []
    for key, builds in groups.items():
        current, baseline = builds.get(bundle.metadata["build"]), builds.get(bundle.metadata["baseline"])
        reference = current or baseline or next(iter(builds.values()))
        gaps = []
        if not current or not baseline:
            gaps.append("matched baseline and candidate")
        else:
            for row in (current, baseline):
                d = row["data"]
                if type(d["numerator"]) is not int or type(d["denominator"]) is not int or not 0 <= d["numerator"] <= d["denominator"] or d["denominator"] <= 0:
                    gaps.append("valid counts and nonzero denominator")
                if d["complete"] is not True:
                    gaps.append("complete event stream")
                if not isinstance(d["query"], str) or not d["query"].strip():
                    gaps.append("recorded query")
            for field in ("schema", "sample_rate", "window_seconds"):
                if current["data"][field] != baseline["data"][field]:
                    gaps.append(f"matched {field}")
        if gaps:
            result.status = "blocked"
            result.findings.append(finding(reference, "measurement", "Trend comparison blocked", ", ".join(sorted(set(gaps))),
                "Comparable measurement contracts and eligible exposure.", "Ask the metric owner for corrected inputs.", kind="gap", owner="Data QA"))
            continue
        cd, bd = current["data"], baseline["data"]
        delta = cd["numerator"] / cd["denominator"] - bd["numerator"] / bd["denominator"]
        comparisons.append({"metric": key[0], "platform": key[1], "config": key[2], "candidate": cd, "baseline": bd,
                            "delta_percentage_points": round(delta * 100, 4), "evidence": [baseline["id"], current["id"]]})
        f = finding(current, "rate", f"Exposure: {key[0]}",
            f"Candidate {cd['numerator']}/{cd['denominator']}; baseline {bd['numerator']}/{bd['denominator']}; change {delta * 100:+.2f} percentage points.",
            "Compare eligible exposures with matching schema, sampling, platform, configuration and duration.",
            "Inspect the representative sessions and validate interpretation with the metric owner.", risk="High" if delta > 0 else "Info", owner="Data QA")
        f.evidence.append(baseline["id"])
        result.findings.append(f)
    result.details = {"comparisons": comparisons, "queries": queries, "calculation": "numerator / eligible denominator, candidate minus baseline",
                      "interpretation": "Descriptive comparison of supplied aggregate counts; not a statistical or causal conclusion."}
    return result


def remote_review(bundle):
    result = result_for("AI6")
    approved = {r["id"] for r in rules(bundle)}
    assignments = {r["id"]: r for r in bundle.select("assignment")}
    submissions = bundle.select("submission")
    if not assignments or not submissions:
        raise InputError("An assignment and at least one submission are required.")
    dispositions = []
    for record in submissions:
        data = record["data"]
        required(data, "assignment", "run", "rule_version", "result", "expected", "actual", "evidence")
        assignment = assignments.get(data["assignment"])
        if not assignment:
            raise InputError("Submission refers to an unknown assignment.")
        contract = assignment["data"]
        required(contract, "setup", "actions", "requirements", "required_evidence", "escalation", "owner")
        if not contract["requirements"] or any(r not in approved for r in contract["requirements"]):
            raise InputError("Assignment contains an unknown or absent rule reference.")
        if not contract["setup"] or not contract["actions"] or not contract["required_evidence"] or not contract["owner"]:
            raise InputError("Assignment setup, actions, evidence contract and owner are required.")
        gaps = []
        if record["build"] != bundle.metadata["build"] or record["build"] != assignment["build"]:
            gaps.append("matching assigned build")
        if record["platform"] not in bundle.metadata["platforms"]:
            gaps.append("supported platform")
        if data["rule_version"] != bundle.metadata["rule_version"]:
            gaps.append("current rule version")
        for key in ("run", "expected", "actual"):
            if not data[key]:
                gaps.append(key)
        if data["result"] not in ("passed", "failed", "blocked", "not_run"):
            gaps.append("valid result state")
        if data.get("expected_value") != data.get("actual_value") and data["result"] == "passed":
            gaps.append("reported pass contradicts supplied assertion values")
        evidence_types = set()
        for evidence_id in data["evidence"]:
            artifact = bundle.get(evidence_id)
            ad = artifact["data"]
            if artifact["kind"] != "artifact" or not ad.get("content") or ad.get("readable") is not True:
                gaps.append(f"readable artifact {evidence_id}")
            elif ad.get("run") != data["run"] or artifact["build"] != record["build"] or artifact["platform"] != record["platform"]:
                gaps.append(f"matching artifact identity {evidence_id}")
            else:
                evidence_types.add(ad.get("type"))
        gaps += [f"{kind} evidence" for kind in contract["required_evidence"] if kind not in evidence_types]
        disposition = "incomplete" if gaps else ("blocked" if data["result"] in ("blocked", "not_run") else "actionable")
        requests = [g for g in gaps if g != "reported pass contradicts supplied assertion values"]
        followup = "Please supply: " + ", ".join(requests) + "." if requests else ""
        if "reported pass contradicts supplied assertion values" in gaps:
            followup = "Please reconcile the reported pass with the supplied assertion values. " + followup
        followup = followup.strip() or "QA review: preserve the stated result and route the evidence."
        dispositions.append({"source": record["id"], "assignment": assignment["id"], "reported_result": data["result"], "disposition": disposition,
                             "gaps": gaps, "followup_draft": followup, "owner": contract["owner"]})
        f = finding(record, "intake", f"Submission {record['id']}: {disposition}",
            f"Reported {data['result']}. " + ("Missing: " + ", ".join(gaps) if gaps else "Required evidence identities and contents are present."),
            "Complete assigned evidence on the correct build and configuration.", followup,
            kind="gap" if gaps else "observation", risk="High" if gaps or data["result"] == "failed" else "Info", owner=contract["owner"])
        f.evidence += [assignment["id"], *data["evidence"]]
        result.findings.append(f)
    result.details = {"assignment_packets": list(assignments.values()), "submissions": dispositions,
                      "calibration": "Review one submission with the execution lead before expanding the assignment."}
    return result


def release_review(bundle):
    result = result_for("AI7")
    coverage = bundle.select("coverage")
    matrix = []
    for rule in rules(bundle):
        for platform in bundle.metadata["platforms"]:
            relevant = [r for r in coverage if r["data"].get("requirement") == rule["id"] and r["platform"] == platform]
            current = [r for r in relevant if r["build"] == bundle.metadata["build"] and r["data"].get("rule_version") == bundle.metadata["rule_version"]]
            states = {r["data"].get("result") for r in current}
            invalid = states - {"passed", "failed", "blocked", "not_run", "not_applicable"}
            if invalid:
                raise InputError("Coverage contains an unknown result state.")
            unresolved = any(r["data"].get("original_failure") and not r["data"].get("failure_disposition") for r in current)
            if not current:
                state = "stale" if relevant else "not_run"
            elif len(states) > 1:
                state = "conflicting"
            elif unresolved:
                state = "unresolved_original_failure"
            elif "not_applicable" in states:
                state = "not_applicable" if all(r["data"].get("exclusion_approved") is True and r["data"].get("exclusion_reason") for r in current) else "unapproved_exclusion"
            else:
                state = next(iter(states))
            if current and any(not r["data"].get("evidence") for r in current):
                state = "missing_evidence"
            for row in current:
                for evidence_id in row["data"].get("evidence", []):
                    evidence = bundle.get(evidence_id)
                    if evidence["build"] != row["build"] or evidence["platform"] != platform:
                        state = "mismatched_evidence"
                    elif evidence["kind"] != "artifact" or evidence["data"].get("readable") is not True or not evidence["data"].get("content"):
                        state = "unreadable_evidence"
            matrix.append({"requirement": rule["id"], "platform": platform, "risk": rule["data"]["risk"], "state": state,
                           "sources": [r["id"] for r in relevant], "owner": rule["data"]["owner"]})
            if state not in ("passed", "not_applicable"):
                f = finding(rule, platform, f"{rule['id']} on {platform}: {state}",
                    "Candidate coverage: " + state, rule["data"]["oracle"], "Resolve the gap and retain linked failure/retest evidence.",
                    kind="gap", risk=rule["data"]["risk"], owner=rule["data"]["owner"])
                f.evidence += [r["id"] for r in relevant]
                result.findings.append(f)
    open_defects = [r for r in bundle.select("defect") if r["build"] == bundle.metadata["build"] and r["data"].get("state", "open") != "closed"]
    for defect in open_defects:
        result.findings.append(finding(defect, "open", "Open candidate defect", defect["data"].get("title", "Untitled"),
            "Critical and High risks require verified correction or reviewed mitigation.", "Review scope and fix/retest evidence.", risk="High"))
    result.product_verdict = "hold_for_evidence" if result.findings else "ready_for_human_review"
    result.details = {"coverage_matrix": matrix, "options": ["Hold affected scope until gaps are resolved.", "Propose reduced scope only with dependency and fallback validation."],
                      "decision_owner": "QA lead recommends; release owner decides."}
    return result


def coordinate(bundle):
    result = result_for("AI8")
    tasks = bundle.select("task")
    if not tasks:
        raise InputError("Task register is missing.")
    by_id = {r["id"]: r for r in tasks}
    visiting, visited = set(), set()

    def visit(task_id):
        if task_id in visiting:
            raise InputError("Task dependencies contain a cycle.")
        if task_id in visited:
            return
        if task_id not in by_id:
            raise InputError("Task dependency is missing from the register.")
        visiting.add(task_id)
        required(by_id[task_id]["data"], "owner", "dependencies", "state", "priority", "next_action", "checkpoint", "evidence", "capacity")
        for dependency in by_id[task_id]["data"]["dependencies"]:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task in tasks:
        visit(task["id"])
    register, seen_work = [], set()
    for record in tasks:
        data = record["data"]
        blockers = [dep for dep in data["dependencies"] if by_id[dep]["data"]["state"] != "accepted"]
        if not data["owner"]:
            blockers.append("receiving owner")
        if record["build"] != bundle.metadata["build"]:
            blockers.append("candidate build")
        if data["capacity"] <= 0:
            blockers.append("owner capacity")
        work = data.get("work_key")
        if work and work in seen_work:
            blockers.append("duplicate work key")
        seen_work.add(work)
        for evidence_id in data["evidence"]:
            bundle.get(evidence_id)
        if data["state"] == "accepted" and (not data["evidence"] or not data.get("receiving_acknowledgement")):
            blockers.append("receiving acknowledgement and evidence")
        register.append({"source": record["id"], **data, "blockers": blockers})
        result.findings.append(finding(record, "task", f"{record['id']}: " + ("blocked" if blockers else "available for review"),
            "Dependencies: " + (", ".join(blockers) or "satisfied"), "A named owner, compatible evidence and accepted dependencies.",
            data["next_action"], kind="gap" if blockers else "observation", risk=data["priority"], owner=data["owner"] or "QA Lead"))
    result.details = {"task_register": register, "delegation_depth": 0, "priority_owner": "QA Lead"}
    return result


ANALYZERS = {"AI1": change_risk, "AI2": regression, "AI3": investigate, "AI4": triage,
             "AI5": telemetry, "AI6": remote_review, "AI7": release_review, "AI8": coordinate}
