# AI2: Regression test author

Workflow: **review_required**. Product assessment: **local_harness_pass**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Approved rules and independent test oracles
- Checks: Execute valid controls and injected faults with fresh state
- Output: Regression tests and assertion results
- Handoff: QA Engineering reviews the test candidates

## Executed Python controls

| Rule / check | Expected | Valid actual | Fault actual | Detection |
| --- | --- | --- | --- | --- |
| RULE-01 / single_result | 1 | 1 | 2 | Detected |
| RULE-02 / stale_equip | 'carbine' | 'carbine' | 'old-tool' | Detected |
| RULE-03 / single_upgrade | 15 | 15 | 20 | Detected |
| RULE-04 / encounter_target | False | False | True | Detected |
| RULE-05 / current_recovery | 'carbine' | 'carbine' | 'old-tool' | Detected |
| RULE-06 / cleanup | 1 | 1 | 2 | Detected |

## Detection check: single_result

Info | observation | Owner: QA Engineering

Observed: Valid actual: 1; injected-fault actual: 2; expected: 1.

Expected: One score mutation for duplicate result delivery.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-01

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Detection check: stale_equip

Info | observation | Owner: QA Engineering

Observed: Valid actual: 'carbine'; injected-fault actual: 'old-tool'; expected: 'carbine'.

Expected: An obsolete completion cannot replace the current loadout.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-02

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Detection check: single_upgrade

Info | observation | Owner: QA Engineering

Observed: Valid actual: 15; injected-fault actual: 20; expected: 15.

Expected: One accepted upgrade changes power once.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-03

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Detection check: encounter_target

Info | observation | Owner: QA Engineering

Observed: Valid actual: False; injected-fault actual: True; expected: False.

Expected: A target in another encounter is ineligible.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-04

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Detection check: current_recovery

Info | observation | Owner: QA Engineering

Observed: Valid actual: 'carbine'; injected-fault actual: 'old-tool'; expected: 'carbine'.

Expected: Recovery rejects an obsolete snapshot.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-05

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Detection check: cleanup

Info | observation | Owner: QA Engineering

Observed: Valid actual: 1; injected-fault actual: 2; expected: 1.

Expected: Only current-encounter entities remain after cleanup.

Next action: Run the exported pytest candidate and review the assertion against this rule.

Evidence: RULE-06

Verify: Valid behavior passes, the injected fault fails, and a fresh-state rerun passes.

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | author_and_test_regression | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
