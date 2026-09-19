# AI2: Regression test author

Workflow: **review_required**. Product assessment: **local_harness_pass**.
Execution: offline_policy. Review: pending.
Stopping reason: checks_complete_pending_review.

## Detection check: single_result

Info | observation | Owner: QA Engineering

Observed: Valid actual: 1; injected-fault actual: 2; expected: 1.

Expected: One score mutation for duplicate result delivery.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-01

## Detection check: stale_equip

Info | observation | Owner: QA Engineering

Observed: Valid actual: 'carbine'; injected-fault actual: 'old-tool'; expected: 'carbine'.

Expected: An obsolete completion cannot replace the current loadout.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-02

## Detection check: single_upgrade

Info | observation | Owner: QA Engineering

Observed: Valid actual: 15; injected-fault actual: 20; expected: 15.

Expected: One accepted upgrade changes power once.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-03

## Detection check: encounter_target

Info | observation | Owner: QA Engineering

Observed: Valid actual: False; injected-fault actual: True; expected: False.

Expected: A target in another encounter is ineligible.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-04

## Detection check: current_recovery

Info | observation | Owner: QA Engineering

Observed: Valid actual: 'carbine'; injected-fault actual: 'old-tool'; expected: 'carbine'.

Expected: Recovery rejects an obsolete snapshot.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-05

## Detection check: cleanup

Info | observation | Owner: QA Engineering

Observed: Valid actual: 1; injected-fault actual: 2; expected: 1.

Expected: Only current-encounter entities remain after cleanup.

Next action: Review the generated test candidate and integration boundary.

Evidence: RULE-06

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | author_and_test_regression | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
