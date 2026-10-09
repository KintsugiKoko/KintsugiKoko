# AI3: Investigation agent

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Build, session, server-tick trace and approved values
- Checks: Order events, compare state, run an isolated control pair
- Output: Investigation timeline and testable hypothesis
- Handoff: Gameplay Engineering reviews the responsible guard

## Supplied trace: TRACE-1 (server_tick)

| Tick | Transaction | Action |
| --- | --- | --- |
| 10 | upgrade-7 | request |
| 11 | upgrade-7 | mutation |
| 12 | upgrade-7 | retry |
| 13 | upgrade-7 | mutation |

## Executed investigation control

| Variant | Expected | Actual | Assertion |
| --- | --- | --- | --- |
| Valid control | 15 | 15 | Passed |
| Injected fault | 15 | 20 | Failed as injected |

## Authoritative state comparison

Critical | observation | Owner: Gameplay Engineering

Observed: Authoritative power 20; approved expectation 15; UI 20. Repeated mutation IDs: ['upgrade-7'].

Expected: One mutation per accepted transaction and the approved effective parameter.

Next action: Compare duplicate delivery with a fresh valid transaction; engineering confirms the responsible guard.

Evidence: TRACE-1

Verify: Retry the same transaction: authoritative power remains 15 and only one mutation is recorded.

## Duplicate-request guard may be ineffective

High | hypothesis | Owner: Gameplay Engineering

Observed: The trace supports a repeated mutation; the responsible implementation has not been inspected.

Expected: An isolated comparison should distinguish server mutation from presentation duplication.

Next action: Run single_upgrade with a controlled repeated transaction.

Evidence: TRACE-1

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | investigate_state | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
