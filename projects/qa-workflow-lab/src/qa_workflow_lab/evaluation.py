"""Labeled contract evaluation. Labels are never given to the agent policy."""

import json
from pathlib import Path
from .agents import run_agent
from .fixtures import sample_bundle
from .models import InputError


def evaluate(path, policy=None):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    for case in cases:
        bundle = sample_bundle("corrected-model")
        for edit in case["edits"]:
            target = bundle.get(edit["record"])
            keys = edit["path"].split(".")
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = edit["value"]
        result = run_agent(bundle, case["workflow"], policy)
        expected = case["expected"]
        observed = {"status": result.status, "product_verdict": result.product_verdict}
        if "submission" in expected:
            rows = result.details.get("submissions", [])
            row = next((r for r in rows if r["source"] == expected["submission"]), {})
            observed.update({"submission": row.get("source"), "disposition": row.get("disposition")})
        passed = all(observed.get(key) == value for key, value in expected.items())
        results.append({"case": case["id"], "workflow": case["workflow"], "passed": passed,
                        "expected": expected, "observed": observed, "stop_reason": result.stop_reason})
    return {"mode": policy.name if policy else "offline_policy", "case_count": len(results),
            "passed": sum(r["passed"] for r in results), "failed": sum(not r["passed"] for r in results),
            "scope": "Labeled local contract cases. Human effort and live model quality are not measured by this suite.", "cases": results}
