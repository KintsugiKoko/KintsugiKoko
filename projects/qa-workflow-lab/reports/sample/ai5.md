# AI5: Telemetry analyst

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review: pending.
Stopping reason: checks_complete_pending_review.

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
