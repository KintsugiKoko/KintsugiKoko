# Five-Minute Walkthrough

Follow the [Design Review Standard](design-review-standard.md): run one mechanism, explain its implementation, expose a meaningful failure, and show a valid control. Use the first five sections for the short overview, then choose the dependency deep dive when a reviewer asks how the framework handles misleading completion signals.

## 1. Start With the Quality Question

Open the browser showcase and select **Candidate with seeded failures**. The question is whether a retried upgrade can mutate the current build twice. The page starts on AI6 because a good investigation begins with usable evidence.

Open `SUB-1` to inspect the failed submission. Then compare `SUB-2`: its claimed pass lacks a trace and contradicts the supplied assertion values. The tool prepares a precise follow-up while retaining the original report.

## 2. Follow the Investigation

Select AI3 and open `TRACE-1`. One transaction has two mutation events. The observed authoritative parameter differs from the rule. The hypothesis is separate from the observation, and the next experiment distinguishes duplicate server mutation from a presentation-only symptom.

## 3. Prove the Assertion Has Value

Select AI2 and open **Work product**. The valid duplicate-upgrade case returns 15; the fault-injected variant returns 20. The intended assertion detects the difference. Review the generated candidate test, then run it through pytest from the CLI packet.

## 4. Assess Exposure and Readiness

AI5 records the exact local SQL and parameters. Candidate exposure is 4/20 versus 1/20 baseline, a 15 percentage-point difference in this fixture. This is a descriptive sample comparison.

AI7 retains stale console evidence and the unresolved upgrade failure. AI8 exposes the responsible owners and dependent regression work. A completed workflow cannot turn these risks into a green release.

## 5. Challenge the Framework

Choose **Missing evidence and schema drift**. Inspect the blocked telemetry result and its tool trace. Then choose **Corrected reference-model scenario**. Its coverage is ready for human review; the receiving owner still accepts the artifact and owns the next decision.

Export the summary or full run JSON. Run `python -m qa_workflow_lab evaluate --output runs/review-evaluation.json` to inspect the labeled contract cases. API-backed tool selection is optional and has its own evaluation needs.

## Dependency Deep Dive

Start with the specific question: **Can an accepted task make its dependents look ready when the handoff was never acknowledged?** This is a reproduced coordinator defect, not a hypothetical production story.

From the project directory, run the focused regression checks:

```powershell
python -m pytest tests/test_failure_boundaries.py -k "dependency or dependencies or dependents" -v
```

Then run this Python example with the project installed. Predict the output before executing it:

```python
from qa_workflow_lab.analysis import coordinate
from qa_workflow_lab.fixtures import sample_bundle

bundle = sample_bundle("corrected-model")
control = coordinate(bundle)
assert all(not row["blockers"] for row in control.details["task_register"])

bundle.get("TASK-1")["data"]["receiving_acknowledgement"] = False
challenged = coordinate(bundle)
for row in challenged.details["task_register"]:
    print(row["source"], row["state"], row["blockers"])
```

Expected: TASK-1 retains its submitted `accepted` state but gains an acknowledgement/evidence blocker. TASK-2 names TASK-1 as a blocker, TASK-3 names TASK-2, and TASK-4 names TASK-3. The input's status label and the coordinator's readiness assessment are deliberately different.

Open `coordinate()` in [analysis.py](../src/qa_workflow_lab/analysis.py) and trace three steps: dependency validation and ordering, local evidence checks, then blocker propagation. Explain why changing an `accepted` label is less useful than retaining it alongside the reason it cannot be trusted for downstream work.

For the control, use a fresh `corrected-model` bundle. Its accepted prerequisites remain available. Reverse the record order in the challenged bundle to test whether the result depends on incidental input ordering; the regression test asserts that the same dependency chain stays blocked.

Close by naming the next question: what would establish that the owner's acknowledgement represents a substantive review? The local field check alone does not answer that. This connects an implemented mechanism to the human QA decision it supports.
