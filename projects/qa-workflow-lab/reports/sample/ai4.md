# AI4: Defect triage agent

Workflow: **review_required**. Product assessment: **review_required**.
Execution: offline_policy. Review at execution: pending.
Stopping reason: checks_complete_pending_review.

## Workflow Pipeline

- Inputs: Defect reports, reproduction counts and linked evidence
- Checks: Validate fields, suggest severity, compare related reports
- Output: Defect proposals with missing-field requests
- Handoff: QA reviews ownership and duplicate differences

## Defect intake

| Source | Severity | Disposition | Missing fields | Related reports |
| --- | --- | --- | --- | --- |
| BUG-1 | Critical | draft ready | None | BUG-2 |
| BUG-2 | High | draft ready | None | BUG-1 |

## Repeated upgrade request changes authoritative power twice

Critical | observation | Owner: Gameplay Engineering

Observed: Report fields are complete. Candidate related reports: ['BUG-2'].

Expected: Distinct expected/actual behavior, attributable evidence, and valid repro counts.

Next action: Review severity, ownership, and duplicate differences before filing.

Evidence: BUG-1

## Upgrade icon briefly duplicates after recovery

High | observation | Owner: UI Engineering

Observed: Report fields are complete. Candidate related reports: ['BUG-1'].

Expected: Distinct expected/actual behavior, attributable evidence, and valid repro counts.

Next action: Review severity, ownership, and duplicate differences before filing.

Evidence: BUG-2

## Tool Trace

| Step | Tool | Status |
| --- | --- | --- |
| 1 | catalog | ok |
| 2 | prepare_defects | ok |
| 3 | finish | ok |

Full tool arguments, results, source records, and detailed outputs are in run.json.
