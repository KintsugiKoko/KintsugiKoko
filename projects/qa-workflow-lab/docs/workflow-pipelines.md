# QA Workflow Pipelines

The browser opens on the complete reference scenario, with AI8's pipeline overview selected. Each workflow has four stages: inputs, bounded checks, work product and human handoff. Select a specialist to inspect its own pipeline, then use Work product for readable result tables or Tool trace for exact arguments and outputs.

## Execution Flow

The evidence bundle supplies build identity, approved rules, changes, traces, exposure events, submissions and coverage. AI1 through AI7 analyze these records independently. AI8 receives their assessments and checks the task register. The implementation runs bounded tools over this shared bundle, with no recursive delegation.

| Workflow | Work product | Receiving reviewer |
| --- | --- | --- |
| AI1: Change risk | Changed-surface risk-to-test map | Feature QA |
| AI2: Regression | Executed valid/fault control pairs and pytest candidates | QA Engineering |
| AI3: Investigation | Ordered trace, state comparison and isolated control | Gameplay Engineering |
| AI4: Defect triage | Evidence-linked defect drafts and related-report candidates | QA |
| AI5: Telemetry | SQLite query counts and comparable exposure rates | Data QA |
| AI6: External QA | Assignment packet, submission checks and follow-up drafts | External QA Lead |
| AI7: Release evidence | Rule/platform coverage and candidate assessment | QA Lead and release owner |
| AI8: QA lead | Dependency register and specialist handoff brief | QA Lead |

## Recorded Scenario Results

These results come from local execution over fictional Relay Arena records. The Python controls execute against the included reference model. Coverage and reported game observations are supplied fixture records.

| Result | Complete walkthrough | Candidate with seeded failures |
| --- | --- | --- |
| Valid Python controls passed | 6/6 | 6/6 |
| Injected faults detected | 6/6 | 6/6 |
| Supplied candidate coverage passed | 12/12 | 9/12 |
| Coverage gaps | 0 | 3 |
| Blocked task handoffs | 0 | 2 |
| Exposure comparison | 1/20 baseline, 1/20 candidate, 0 percentage-point change | 1/20 baseline, 4/20 candidate, +15 percentage points |
| Candidate recommendation | QA lead review | Hold for evidence resolution |

The complete walkthrough is a separately authored reference scenario. Switching cases does not alter or resolve the original failing records. The evidence-gap case retains a blocked schema comparison and a missing Console test.

## Five-Minute Walkthrough

1. Open the complete scenario and explain the eight work products in the Pipeline view.
2. Select AI2 and open Work product. Compare the expected value with both executed control results.
3. Select AI5. Explain eligible exposure counts and the matched measurement contract. Inspect the SQL in the full work product.
4. Switch to the seeded-failure case. AI6 identifies a contradictory pass and missing trace. AI7 retains the stale and unresolved coverage. AI8 shows the resulting handoff blockers.
5. Export the summary. It includes owner actions, verification criteria and source references for the QA lead's review.

## Reproduce

From the project directory after installation:

```powershell
python -m qa_workflow_lab demo --case corrected-model --output runs/complete-walkthrough
python -m qa_workflow_lab demo --case candidate --output runs/seeded-failures
python -m pytest runs/complete-walkthrough/test_regression_candidate.py
python -m qa_workflow_lab showcase --output ../../docs/qa-workflow-lab.html
```

Use fresh output paths to retain earlier evidence. The complete walkthrough includes Keith's acceptance of the workflow artifact presentation in `reports/artifact-reviews.jsonl`. Each decision binds to the saved run's SHA-256. Changed evidence requires a fresh review. The seeded-failure case retains its pending reviews and hold assessment.
