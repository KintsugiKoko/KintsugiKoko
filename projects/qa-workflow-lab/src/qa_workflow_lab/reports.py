"""Inspectable Markdown, JSON and a self-contained browser review."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from .models import InputError, digest


def plain(text):
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "\\|")


def workflow_markdown(result):
    lines = [f"# {result['workflow']}: {result['title']}", "",
             f"Workflow: **{result['status']}**. Product assessment: **{result['product_verdict']}**.",
             f"Execution: {result['details']['execution']['mode']}. Review: {result['review_status']}.",
             f"Stopping reason: {result['stop_reason']}.", ""]
    for f in result["findings"]:
        lines += [f"## {plain(f['title'])}", "", f"{f['risk']} | {f['kind']} | Owner: {plain(f['owner'])}", "",
                  f"Observed: {plain(f['observation'])}", "", f"Expected: {plain(f['expected'])}", "",
                  f"Next action: {plain(f['next_action'])}", "", "Evidence: " + ", ".join(f["evidence"]), ""]
    for note in result["model_notes"]:
        lines += [f"Proposed {note['kind']}: {plain(note['text'])}", "Evidence: " + ", ".join(note["evidence"]), ""]
    lines += ["## Tool Trace", "", "| Step | Tool | Status |", "| --- | --- | --- |"]
    lines += [f"| {t['step']} | {t['tool']} | {t['status']} |" for t in result["trace"]]
    for step in result["trace"]:
        if step["status"] == "error":
            lines += ["", "Blocked: " + plain(step["output"]["error"])]
    lines += ["", "Full tool arguments, results, source records, and detailed outputs are in run.json.", ""]
    return "\n".join(lines)


def summary_markdown(run, *, linked=True):
    meta = run["metadata"]
    lines = ["# QA Workflow Lab: Review Packet", "", f"Feature: {plain(meta['feature'])}",
             f"Candidate: {meta['build']} | Baseline: {meta['baseline']} | Rules: {meta['rule_version']}",
             "", "Fictional Relay Arena evidence. Harness assertions execute against the included Python reference model.",
             "", "| Workflow | Artifact state | Product assessment |", "| --- | --- | --- |"]
    for r in run["workflows"]:
        name = f"{r['workflow']}: {r['title']}"
        label = f"[{name}]({r['workflow'].lower()}.md)" if linked else name
        lines.append(f"| {label} | {r['status']} | {r['product_verdict']} |")
    lines += ["", "## Review Route", "", "1. AI6: compare complete, incomplete and wrong-build submissions.",
              "2. AI3 and AI2: inspect the upgrade trace and the valid/fault assertion pair.",
              "3. AI5: reproduce the exposure rates using the recorded local query.",
              "4. AI7 and AI8: inspect stale coverage, dependencies and the receiving owner.",
              "", "Artifact completion and human acceptance remain separate from a product verdict.",
              "", f"Input SHA-256: {run['input_sha256']}", ""]
    return "\n".join(lines)


def jira_markdown(run):
    triage = next((r for r in run["workflows"] if r["workflow"] == "AI4"), {"details": {}})
    lines = ["# Defect Proposals", "", "Local drafts for QA review.", ""]
    for d in triage["details"].get("draft_defects", []):
        lines += [f"## {plain(d['title'])}", "", f"Source: {d['source']} | Build: {run['metadata']['build']}",
                  f"Severity suggestion: {d['severity_suggestion']} | Status: {d['disposition']}", "", "### Reproduction", ""]
        lines += [f"{i}. {plain(step)}" for i, step in enumerate(d["steps"], 1)]
        lines += ["", "Expected: " + plain(d["expected"]), "", "Actual: " + plain(d["actual"]), "",
                  "Evidence: " + ", ".join(d["evidence"]), "Possible related reports: " + ", ".join(d["duplicate_candidates"]),
                  "Missing: " + (", ".join(d["missing"]) or "None in the structured field check"), "",
                  "Fix verification: pending QA review and execution.", ""]
    return "\n".join(lines)


def handoff_markdown(run):
    remote = next((r for r in run["workflows"] if r["workflow"] == "AI6"), {"details": {}})
    lines = ["# Remote QA Assignment", "", "Fictional exercise. Assignment owner reviews this packet before distribution.", ""]
    for assignment in remote["details"].get("assignment_packets", []):
        d = assignment["data"]
        lines += [f"## {assignment['id']}", "", f"Build: {assignment['build']} | Owner: {d['owner']}", "", "### Setup", ""]
        lines += [f"- {plain(s)}" for s in d["setup"]]
        lines += ["", "### Execute", ""] + [f"{i}. {plain(s)}" for i, s in enumerate(d["actions"], 1)]
        lines += ["", "Required evidence: " + ", ".join(d["required_evidence"]), "Rules: " + ", ".join(d["requirements"]),
                  "Escalation: " + d["escalation"], "", "Record passed, failed, blocked or not run for each assigned case.", ""]
    for s in remote["details"].get("submissions", []):
        lines += [f"### {s['source']}: {s['disposition']}", "", s["followup_draft"], ""]
    return "\n".join(lines)


def render_showcase(runs, template):
    payload = [{"run": run, "markdown": summary_markdown(run, linked=False) + "\n" + "\n".join(workflow_markdown(r) for r in run["workflows"])} for run in runs]
    encoded = json.dumps(payload, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return Path(template).read_text(encoding="utf-8").replace("__RUN_DATA__", encoded)


def write_run(run, output, *, template=None):
    output = Path(output)
    if output.exists():
        raise InputError("Output already exists. Choose a new run directory to preserve prior evidence.")
    output.mkdir(parents=True)
    files = {"run.json": json.dumps(run, indent=2) + "\n", "README.md": summary_markdown(run),
             "defect-proposals.md": jira_markdown(run), "remote-assignment.md": handoff_markdown(run)}
    for result in run["workflows"]:
        files[result["workflow"].lower() + ".md"] = workflow_markdown(result)
        if "candidate_test" in result["details"]:
            files["test_regression_candidate.py"] = result["details"]["candidate_test"]
    if template:
        files["index.html"] = render_showcase([run], template)
    for name, content in files.items():
        (output / name).write_text(content, encoding="utf-8", newline="\n")
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "run_sha256": digest(run), "files": {
        name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in sorted(files)}}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest
