# AI7: Release evidence analyst

Workflow: **review_required**. Product assessment: **hold_for_evidence**.
Execution: offline_policy. Review: pending.
Stopping reason: checks_complete_pending_review.

## RULE-03 on PC: unresolved_original_failure

Critical | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: unresolved_original_failure

Expected: One accepted upgrade changes power once.

Next action: Resolve the gap and retain linked failure/retest evidence.

Evidence: RULE-03, COV-3-PC

## RULE-03 on Console: unresolved_original_failure

Critical | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: unresolved_original_failure

Expected: One accepted upgrade changes power once.

Next action: Resolve the gap and retain linked failure/retest evidence.

Evidence: RULE-03, COV-3-Console

## RULE-05 on Console: stale

High | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: stale

Expected: Recovery rejects an obsolete snapshot.

Next action: Resolve the gap and retain linked failure/retest evidence.

Evidence: RULE-05, COV-5-Console

## Open candidate defect

High | observation | Owner: QA

Observed: Repeated upgrade request changes authoritative power twice

Expected: Critical and High risks require verified correction or reviewed mitigation.

Next action: Review scope and fix/retest evidence.

Evidence: BUG-1

## Open candidate defect

High | observation | Owner: QA

Observed: Upgrade icon briefly duplicates after recovery

Expected: Critical and High risks require verified correction or reviewed mitigation.

Next action: Review scope and fix/retest evidence.

Evidence: BUG-2

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | assess_candidate | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
