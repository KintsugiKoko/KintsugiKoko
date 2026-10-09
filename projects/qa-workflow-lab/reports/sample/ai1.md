# AI1: Change risk analyst

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Approved rules, change records, candidate coverage
- Checks: Map changed surfaces to player risk and current coverage
- Output: Risk-to-test map
- Handoff: Feature QA confirms missing test scope

## Change coverage

| Change / rule | Surface | Current records | Platforms |
| --- | --- | --- | --- |
| CHANGE-1 / RULE-03 | upgrade transaction and recovery handoff | COV-3-PC, COV-3-Console | PC, Console |
| CHANGE-1 / RULE-05 | upgrade transaction and recovery handoff | COV-5-PC | PC, Console |

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
