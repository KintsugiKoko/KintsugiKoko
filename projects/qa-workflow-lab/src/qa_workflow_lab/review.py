"""Readable review products derived from recorded tool results."""


PIPELINES = {
    "AI1": {"inputs": "Approved rules, change records, candidate coverage", "checks": "Map changed surfaces to player risk and current coverage", "output": "Risk-to-test map", "handoff": "Feature QA confirms missing test scope"},
    "AI2": {"inputs": "Approved rules and independent test oracles", "checks": "Execute valid controls and injected faults with fresh state", "output": "Regression tests and assertion results", "handoff": "QA Engineering reviews the test candidates"},
    "AI3": {"inputs": "Build, session, server-tick trace and approved values", "checks": "Order events, compare state, run an isolated control pair", "output": "Investigation timeline and testable hypothesis", "handoff": "Gameplay Engineering reviews the responsible guard"},
    "AI4": {"inputs": "Defect reports, reproduction counts and linked evidence", "checks": "Validate fields, suggest severity, compare related reports", "output": "Defect proposals with missing-field requests", "handoff": "QA reviews ownership and duplicate differences"},
    "AI5": {"inputs": "Exposure events and baseline/candidate metric contracts", "checks": "Execute SQLite counts and validate comparable denominators", "output": "Exposure comparison with recorded SQL", "handoff": "Data QA reviews sessions and metric interpretation"},
    "AI6": {"inputs": "Assignment requirements and external test submissions", "checks": "Verify build, run, rule version, assertions and artifacts", "output": "Assignment packet and evidence follow-ups", "handoff": "External QA Lead resolves incomplete submissions"},
    "AI7": {"inputs": "Rule/platform coverage, failure history and open defects", "checks": "Retain stale, conflicting and unresolved coverage", "output": "Candidate assessment and coverage matrix", "handoff": "QA Lead recommends, release owner decides"},
    "AI8": {"inputs": "Task register, dependency graph and specialist assessments", "checks": "Check owners, capacity, acknowledgements and prerequisites", "output": "Handoff register and candidate review brief", "handoff": "QA Lead assigns actions and records the review"},
}


def readable(value):
    return str(value).replace("_", " ")


def work_product_tables(result):
    data = result["details"]
    tables = []

    def add(title, columns, rows):
        if rows:
            tables.append({"title": title, "columns": columns, "rows": rows})

    add("Change coverage", ["Change / rule", "Surface", "Current records", "Platforms"], [
        [f"{r['change']} / {r['requirement']}", r["surface"], ", ".join(r["current_evidence"]) or "None",
         ", ".join(r["platforms"])] for r in data.get("risk_to_test_map", [])])
    add("Executed Python controls", ["Rule / check", "Expected", "Valid actual", "Fault actual", "Detection"], [
        [f"{r['requirement']} / {r['valid']['check']}", repr(r["valid"]["expected"]), repr(r["valid"]["actual"]),
         repr(r["fault"]["actual"]), "Detected" if r["detected"] else "FAILED"] for r in data.get("runs", [])])
    for timeline in data.get("timelines", []):
        add(f"Supplied trace: {timeline['source']} ({timeline['clock']})", ["Tick", "Transaction", "Action"], [
            [e["tick"], e["transaction"], e["action"]] for e in timeline["events"]])
    experiment = data.get("experiment")
    if experiment:
        add("Executed investigation control", ["Variant", "Expected", "Actual", "Assertion"], [
            [label, repr(experiment[key]["expected"]), repr(experiment[key]["actual"]),
             ("Passed" if key == "control" else "FAILED: fault missed") if experiment[key]["passed"]
             else "Failed as injected" if key == "fault" else "FAILED: valid control"]
            for key, label in (("control", "Valid control"), ("fault", "Injected fault"))])
    add("Defect intake", ["Source", "Severity", "Disposition", "Missing fields", "Related reports"], [
        [d["source"], d["severity_suggestion"], readable(d["disposition"]), ", ".join(d["missing"]) or "None",
         ", ".join(d["duplicate_candidates"]) or "None"] for d in data.get("draft_defects", [])])
    add("Executed SQLite counts", ["Metric source", "Violations", "Eligible exposures"], [
        [q["source"], q["numerator"], q["denominator"]] for q in data.get("queries", [])])
    add("Comparable exposure rates", ["Metric / platform", "Baseline", "Candidate", "Change (pp)"], [
        [f"{c['metric']} / {c['platform']}", f"{c['baseline']['numerator']}/{c['baseline']['denominator']}",
         f"{c['candidate']['numerator']}/{c['candidate']['denominator']}", f"{c['delta_percentage_points']:+.2f}"]
        for c in data.get("comparisons", [])])
    add("External QA intake", ["Submission", "Reported result", "Disposition", "Follow-up owner", "Missing / conflicting evidence"], [
        [s["source"], s["reported_result"], s["disposition"], s["owner"], "; ".join(s["gaps"]) or "None"]
        for s in data.get("submissions", [])])
    add("Candidate coverage (supplied records)", ["Rule", "Platform", "State", "Owner", "Source records"], [
        [r["requirement"], r["platform"], readable(r["state"]), r["owner"], ", ".join(r["sources"]) or "None"]
        for r in data.get("coverage_matrix", [])])
    add("QA task handoffs", ["Task / owner", "Recorded state", "Blockers", "Next action", "Checkpoint"], [
        [f"{r['source']} / {r['owner']}", r["state"], ", ".join(r["blockers"]) or "None",
         r["next_action"], r["checkpoint"]] for r in data.get("task_register", [])])
    add("Specialist assessments", ["Workflow", "Execution", "Assessment", "Review at execution"], [
        [r["workflow"], readable(r["status"]), readable(r["product_verdict"]), r["review_status"]]
        for r in data.get("workflow_handoffs", [])])
    return tables


def review_summary(run):
    workflows = {r["workflow"]: r for r in run["workflows"]}
    controls = workflows.get("AI2", {}).get("details", {}).get("runs", [])
    coverage = workflows.get("AI7", {}).get("details", {}).get("coverage_matrix", [])
    submissions = workflows.get("AI6", {}).get("details", {}).get("submissions", [])
    tasks = workflows.get("AI8", {}).get("details", {}).get("task_register", [])
    blocked = [r for r in run["workflows"] if r["status"] == "blocked"]
    control_failures = sum(not r["detected"] for r in controls)
    gaps = sum(r["state"] not in ("passed", "not_applicable") for r in coverage)
    task_blockers = sum(bool(r["blockers"]) for r in tasks)
    release = workflows.get("AI7")
    holds = bool(blocked or control_failures or gaps or task_blockers or
                 any(s["disposition"] != "actionable" for s in submissions) or
                 (release and release["product_verdict"] == "hold_for_evidence"))
    assessment = "hold" if holds else "review_required" if release and coverage else "incomplete_scope"
    reasons = []
    if blocked:
        reasons.append(f"{len(blocked)} workflow(s) could not complete their checks.")
    if control_failures:
        reasons.append(f"{control_failures} local control pair(s) did not detect the expected behavior.")
    if gaps:
        reasons.append(f"{gaps} of {len(coverage)} required rule/platform combinations need evidence resolution.")
    open_defects = sum(f["id"].endswith("-open") for f in release["findings"]) if release else 0
    if open_defects:
        reasons.append(f"{open_defects} candidate defect(s) remain open in the supplied records.")
    incomplete = sum(s["disposition"] != "actionable" for s in submissions)
    if incomplete:
        reasons.append(f"{incomplete} external submission(s) need follow-up.")
    if task_blockers:
        reasons.append(f"{task_blockers} task handoff(s) have unresolved prerequisites.")
    if not reasons:
        reasons.append("Recorded checks are ready for QA lead review." if assessment == "review_required"
                       else "Run the release-evidence workflow before a candidate assessment.")

    actions = []
    for r in run["workflows"]:
        if r["status"] == "blocked" and (not r["findings"] or any(t["status"] == "error" for t in r["trace"])):
            errors = [t["output"].get("error", "") for t in r["trace"] if t["status"] == "error"]
            actions.append({"workflow": r["workflow"], "title": "Restore workflow evidence contract", "risk": "High",
                            "owner": r["title"], "action": "; ".join(errors) or readable(r["stop_reason"]),
                            "verify": "Rerun this workflow successfully on the same candidate identity.", "evidence": []})
        for f in r["findings"]:
            if f["kind"] == "hypothesis" or f["risk"] == "Info" or r["workflow"] in ("AI1", "AI4"):
                continue
            if r["workflow"] == "AI8" and f["kind"] != "gap":
                continue
            actions.append({"workflow": r["workflow"], "title": f["title"], "risk": f["risk"], "owner": f["owner"],
                            "action": f["next_action"], "verify": f.get("verification") or f["expected"], "evidence": f["evidence"]})
    actions.sort(key=lambda a: {"Critical": 0, "High": 1}.get(a["risk"], 2))
    return {"assessment": assessment, "reasons": reasons, "control_pairs": len(controls),
            "valid_controls_passed": sum(r["valid"]["passed"] for r in controls),
            "injected_faults_detected": sum(not r["fault"]["passed"] for r in controls),
            "control_failures": control_failures, "coverage_total": len(coverage),
            "coverage_passed": sum(r["state"] == "passed" for r in coverage),
            "coverage_excluded": sum(r["state"] == "not_applicable" for r in coverage),
            "coverage_gaps": gaps, "blocked_workflows": len(blocked), "blocked_tasks": task_blockers,
            "actions": actions, "scope": "Executed Python and SQLite checks over fictional Relay Arena records."}
