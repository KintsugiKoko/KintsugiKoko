# AI7: Release evidence analyst

Workflow: **review_required**. Product assessment: **hold_for_evidence**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Rule/platform coverage, failure history and open defects
- Checks: Retain stale, conflicting and unresolved coverage
- Output: Candidate assessment and coverage matrix
- Handoff: QA Lead recommends, release owner decides

## Candidate coverage (supplied records)

| Rule | Platform | State | Owner | Source records |
| --- | --- | --- | --- | --- |
| RULE-01 | PC | passed | Gameplay Engineering | COV-1-PC |
| RULE-01 | Console | passed | Gameplay Engineering | COV-1-Console |
| RULE-02 | PC | passed | Gameplay Engineering | COV-2-PC |
| RULE-02 | Console | passed | Gameplay Engineering | COV-2-Console |
| RULE-03 | PC | unresolved original failure | Gameplay Engineering | COV-3-PC |
| RULE-03 | Console | unresolved original failure | Gameplay Engineering | COV-3-Console |
| RULE-04 | PC | passed | Gameplay Engineering | COV-4-PC |
| RULE-04 | Console | passed | Gameplay Engineering | COV-4-Console |
| RULE-05 | PC | passed | Gameplay Engineering | COV-5-PC |
| RULE-05 | Console | stale | Gameplay Engineering | COV-5-Console |
| RULE-06 | PC | passed | Gameplay Engineering | COV-6-PC |
| RULE-06 | Console | passed | Gameplay Engineering | COV-6-Console |

## RULE-03 on PC: unresolved_original_failure

Critical | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: unresolved_original_failure

Expected: One accepted upgrade changes power once.

Next action: Link the original failure to a reviewed disposition and a current retest.

Evidence: RULE-03, COV-3-PC

Verify: RULE-03 / PC: current candidate evidence passes the oracle, with any original failure disposition retained.

## RULE-03 on Console: unresolved_original_failure

Critical | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: unresolved_original_failure

Expected: One accepted upgrade changes power once.

Next action: Link the original failure to a reviewed disposition and a current retest.

Evidence: RULE-03, COV-3-Console

Verify: RULE-03 / Console: current candidate evidence passes the oracle, with any original failure disposition retained.

## RULE-05 on Console: stale

High | gap | Owner: Gameplay Engineering

Observed: Candidate coverage: stale

Expected: Recovery rejects an obsolete snapshot.

Next action: Rerun this rule on the candidate build; retain the old result as baseline evidence.

Evidence: RULE-05, COV-5-Console

Verify: RULE-05 / Console: current candidate evidence passes the oracle, with any original failure disposition retained.

## Open candidate defect

Critical | observation | Owner: Gameplay Engineering

Observed: Repeated upgrade request changes authoritative power twice

Expected: Critical and High risks require verified correction or reviewed mitigation.

Next action: Review the reproduction and player impact; link a fix/retest record or an explicit mitigation decision.

Evidence: BUG-1

Verify: QA confirms the recorded expected result on the candidate, or the release owner records an accepted mitigation.

## Open candidate defect

High | observation | Owner: UI Engineering

Observed: Upgrade icon briefly duplicates after recovery

Expected: Critical and High risks require verified correction or reviewed mitigation.

Next action: Review the reproduction and player impact; link a fix/retest record or an explicit mitigation decision.

Evidence: BUG-2

Verify: QA confirms the recorded expected result on the candidate, or the release owner records an accepted mitigation.

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | assess_candidate | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
