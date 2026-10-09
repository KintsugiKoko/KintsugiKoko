# QA Workflow Lab: Review Packet

Feature: Relay Arena: upgrade and encounter transitions
Candidate: demo-102 | Baseline: demo-101 | Rules: rules-1

Fictional Relay Arena evidence. Harness assertions execute against the included Python reference model.

## Run Assessment

Recommendation: **hold**.

- 3 of 12 required rule/platform combinations need evidence resolution.
- 2 candidate defect(s) remain open in the supplied records.
- 1 external submission(s) need follow-up.
- 2 task handoff(s) have unresolved prerequisites.

Executed controls: 6/6 valid controls passed; 6/6 injected faults detected.
Supplied candidate coverage: 9/12 passed; 0 approved exclusions; 3 gaps.

## Priority Actions

| Risk / workflow | Owner | Next action | Verification | Evidence |
| --- | --- | --- | --- | --- |
| Critical / AI3 | Gameplay Engineering | Compare duplicate delivery with a fresh valid transaction; engineering confirms the responsible guard. | Retry the same transaction: authoritative power remains 15 and only one mutation is recorded. | TRACE-1 |
| Critical / AI7 | Gameplay Engineering | Link the original failure to a reviewed disposition and a current retest. | RULE-03 / PC: current candidate evidence passes the oracle, with any original failure disposition retained. | RULE-03, COV-3-PC |
| Critical / AI7 | Gameplay Engineering | Link the original failure to a reviewed disposition and a current retest. | RULE-03 / Console: current candidate evidence passes the oracle, with any original failure disposition retained. | RULE-03, COV-3-Console |
| Critical / AI7 | Gameplay Engineering | Review the reproduction and player impact; link a fix/retest record or an explicit mitigation decision. | QA confirms the recorded expected result on the candidate, or the release owner records an accepted mitigation. | BUG-1 |
| High / AI5 | Data QA | Inspect the representative sessions and validate interpretation with the metric owner. | Compare eligible exposures with matching schema, sampling, platform, configuration and duration. | METRIC-demo-102, METRIC-demo-101 |
| High / AI6 | External QA Lead | Route remote-1's failed result and attached evidence to the rule owner for fix verification. | QA confirms remote-1's failed result against the attached evidence and retains the original capture. | SUB-1, ASSIGN-1, SUBART-1-state, SUBART-1-trace |
| High / AI6 | External QA Lead | Please reconcile the reported pass with the supplied assertion values. Please supply: trace evidence. | Resubmit remote-2 on demo-102 / PC with state, trace evidence and a result consistent with the assertion values. | SUB-2, ASSIGN-1, SUBART-2-state |
| High / AI7 | Gameplay Engineering | Rerun this rule on the candidate build; retain the old result as baseline evidence. | RULE-05 / Console: current candidate evidence passes the oracle, with any original failure disposition retained. | RULE-05, COV-5-Console |
| High / AI7 | UI Engineering | Review the reproduction and player impact; link a fix/retest record or an explicit mitigation decision. | QA confirms the recorded expected result on the candidate, or the release owner records an accepted mitigation. | BUG-2 |
| High / AI8 | QA Engineering | Resolve TASK-2; then Review generated regression assertions and retest scope. | Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted. | TASK-3, RULE-03 |
| High / AI8 | QA Lead | Resolve TASK-3; then Review candidate coverage and unresolved player risk. | Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted. | TASK-4, COV-3-PC |

## Workflow Dispositions

| Workflow | Artifact state | Product assessment |
| --- | --- | --- |
| [AI1: Change risk analyst](ai1.md) | review_required | review_required |
| [AI2: Regression test author](ai2.md) | review_required | local_harness_pass |
| [AI3: Investigation agent](ai3.md) | review_required | review_required |
| [AI4: Defect triage agent](ai4.md) | review_required | review_required |
| [AI5: Telemetry analyst](ai5.md) | review_required | review_required |
| [AI6: Remote QA coordinator](ai6.md) | review_required | review_required |
| [AI7: Release evidence analyst](ai7.md) | review_required | hold_for_evidence |
| [AI8: QA lead coordinator](ai8.md) | review_required | hold_for_evidence |

## Review Route

1. AI6: compare complete, incomplete and wrong-build submissions.
2. AI3 and AI2: inspect the upgrade trace and the valid/fault assertion pair.
3. AI5: reproduce the exposure rates using the recorded local query.
4. AI7 and AI8: inspect stale coverage, dependencies and the receiving owner.

Artifact completion and human acceptance remain separate from a product verdict.

Input SHA-256: 2f3f9cda4100677369ffc5e849a6d0e5ad638df9bfe368dcc3fa1257bb9a240a
