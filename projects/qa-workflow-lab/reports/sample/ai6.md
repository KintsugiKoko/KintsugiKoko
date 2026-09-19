# AI6: Remote QA coordinator

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review: pending.
Stopping reason: checks_complete_pending_review.

## Submission SUB-1: actionable

High | observation | Owner: External QA Lead

Observed: Reported failed. Required evidence identities and contents are present.

Expected: Complete assigned evidence on the correct build and configuration.

Next action: QA review: preserve the stated result and route the evidence.

Evidence: SUB-1, ASSIGN-1, SUBART-1-state, SUBART-1-trace

## Submission SUB-2: incomplete

High | gap | Owner: External QA Lead

Observed: Reported passed. Missing: reported pass contradicts supplied assertion values, trace evidence

Expected: Complete assigned evidence on the correct build and configuration.

Next action: Please reconcile the reported pass with the supplied assertion values. Please supply: trace evidence.

Evidence: SUB-2, ASSIGN-1, SUBART-2-state

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | review_submissions | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
