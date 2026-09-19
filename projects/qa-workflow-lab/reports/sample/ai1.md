# AI1: Change risk analyst

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review: pending.
Stopping reason: checks_complete_pending_review.

## Review upgrade transaction and recovery handoff

Critical | risk | Owner: Gameplay Engineering

Observed: A repeated upgrade can change combat power or restore an obsolete loadout.

Expected: One accepted upgrade changes power once.

Next action: Review current assertions and rerun affected configurations.

Evidence: CHANGE-1, RULE-03

## Review upgrade transaction and recovery handoff

High | risk | Owner: Gameplay Engineering

Observed: A repeated upgrade can change combat power or restore an obsolete loadout.

Expected: Recovery rejects an obsolete snapshot.

Next action: Review current assertions and rerun affected configurations.

Evidence: CHANGE-1, RULE-05

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | map_change_risks | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
