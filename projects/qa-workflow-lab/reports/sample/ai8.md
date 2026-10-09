# AI8: QA lead coordinator

Workflow: **review_required**. Product assessment: **hold_for_evidence**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Task register, dependency graph and specialist assessments
- Checks: Check owners, capacity, acknowledgements and prerequisites
- Output: Handoff register and candidate review brief
- Handoff: QA Lead assigns actions and records the review

## QA task handoffs

| Task / owner | Recorded state | Blockers | Next action | Checkpoint |
| --- | --- | --- | --- | --- |
| TASK-1 / Feature QA | accepted | None | Confirm the assignment evidence contract. | candidate review |
| TASK-2 / Gameplay Engineering | running | None | Review the duplicate guard and controlled comparison. | candidate review |
| TASK-3 / QA Engineering | queued | TASK-2 | Review generated regression assertions and retest scope. | candidate review |
| TASK-4 / QA Lead | queued | TASK-3 | Review candidate coverage and unresolved player risk. | candidate review |

## Specialist assessments

| Workflow | Execution | Assessment | Review at execution |
| --- | --- | --- | --- |
| AI1 | review required | review required | pending |
| AI2 | review required | local harness pass | pending |
| AI3 | review required | review required | pending |
| AI4 | review required | review required | pending |
| AI5 | review required | review required | pending |
| AI6 | review required | review required | pending |
| AI7 | review required | hold for evidence | pending |

## TASK-1: acknowledged

Info | observation | Owner: Feature QA

Observed: Recorded state: accepted. Evidence: SUB-1. Unresolved prerequisites: none.

Expected: A named owner, current-build evidence and accepted prerequisites before the next handoff.

Next action: Confirm the assignment evidence contract.

Evidence: TASK-1, SUB-1

Verify: Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted.

## TASK-2: running

High | observation | Owner: Gameplay Engineering

Observed: Recorded state: running. Evidence: TRACE-1. Unresolved prerequisites: none.

Expected: A named owner, current-build evidence and accepted prerequisites before the next handoff.

Next action: Review the duplicate guard and controlled comparison.

Evidence: TASK-2, TRACE-1

Verify: Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted.

## TASK-3: blocked

High | gap | Owner: QA Engineering

Observed: Recorded state: queued. Evidence: RULE-03. Unresolved prerequisites: TASK-2.

Expected: A named owner, current-build evidence and accepted prerequisites before the next handoff.

Next action: Resolve TASK-2; then Review generated regression assertions and retest scope.

Evidence: TASK-3, RULE-03

Verify: Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted.

## TASK-4: blocked

High | gap | Owner: QA Lead

Observed: Recorded state: queued. Evidence: COV-3-PC. Unresolved prerequisites: TASK-3.

Expected: A named owner, current-build evidence and accepted prerequisites before the next handoff.

Next action: Resolve TASK-3; then Review candidate coverage and unresolved player risk.

Evidence: TASK-4, COV-3-PC

Verify: Checkpoint: candidate review. Receiving owner acknowledges the current-build evidence; prerequisites are accepted.

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | coordinate_tasks | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
