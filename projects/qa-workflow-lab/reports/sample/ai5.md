# AI5: Telemetry analyst

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Exposure events and baseline/candidate metric contracts
- Checks: Execute SQLite counts and validate comparable denominators
- Output: Exposure comparison with recorded SQL
- Handoff: Data QA reviews sessions and metric interpretation

## Executed SQLite counts

| Metric source | Violations | Eligible exposures |
| --- | --- | --- |
| METRIC-demo-101 | 1 | 20 |
| METRIC-demo-102 | 4 | 20 |

## Comparable exposure rates

| Metric / platform | Baseline | Candidate | Change (pp) |
| --- | --- | --- | --- |
| duplicate_upgrade / PC | 1/20 | 4/20 | +15.00 |

## Exposure: duplicate_upgrade

High | observation | Owner: Data QA

Observed: Candidate 4/20; baseline 1/20; change +15.00 percentage points.

Expected: Compare eligible exposures with matching schema, sampling, platform, configuration and duration.

Next action: Inspect the representative sessions and validate interpretation with the metric owner.

Evidence: METRIC-demo-102, METRIC-demo-101

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | compare_telemetry | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
