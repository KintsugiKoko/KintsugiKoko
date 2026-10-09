# AI6: Remote QA coordinator

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Assignment requirements and external test submissions
- Checks: Verify build, run, rule version, assertions and artifacts
- Output: Assignment packet and evidence follow-ups
- Handoff: External QA Lead resolves incomplete submissions

## External QA intake

| Submission | Reported result | Disposition | Follow-up owner | Missing / conflicting evidence |
| --- | --- | --- | --- | --- |
| SUB-1 | failed | actionable | External QA Lead | None |
| SUB-2 | passed | incomplete | External QA Lead | reported pass contradicts supplied assertion values; trace evidence |

## Submission SUB-1: actionable

High | observation | Owner: External QA Lead

Observed: Reported failed. Required evidence identities and contents are present.

Expected: Complete assigned evidence on the correct build and configuration.

Next action: Route remote-1's failed result and attached evidence to the rule owner for fix verification.

Evidence: SUB-1, ASSIGN-1, SUBART-1-state, SUBART-1-trace

Verify: QA confirms remote-1's failed result against the attached evidence and retains the original capture.

## Submission SUB-2: incomplete

High | gap | Owner: External QA Lead

Observed: Reported passed. Missing: reported pass contradicts supplied assertion values, trace evidence

Expected: Complete assigned evidence on the correct build and configuration.

Next action: Please reconcile the reported pass with the supplied assertion values. Please supply: trace evidence.

Evidence: SUB-2, ASSIGN-1, SUBART-2-state

Verify: Resubmit remote-2 on demo-102 / PC with state, trace evidence and a result consistent with the assertion values.

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | review_submissions | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
