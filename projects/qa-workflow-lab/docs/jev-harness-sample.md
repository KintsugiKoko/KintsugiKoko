# Harness Sample Walkthrough

Input: [15 fictional cases](../sample-data/jev-harness-cases.json). Decisions: [synthetic replay](../sample-data/jev-harness-replay.json). Expectations: [separate authored labels](../tests/jev-harness-labels.json).

Generate the full packet:

```powershell
python -m qa_workflow_lab harness-evaluate --mode replay --output runs/harness-sample
```

The deliberate invalid Score response makes this command exit 2 after saving its report.

## H01: Duplicate Upgrade Investigation

Selected local check: `single_upgrade`.

| Control | Expected power | Actual power | Assertion |
| --- | --- | --- | --- |
| Valid transaction deduplication | 15 | 15 | Pass |
| Injected duplicate-application fault | 15 | 20 | Fail as intended |

The control pair succeeds because the assertion detects the injected fault. This is execution of the Python reference model, not a game-build result.

## H03: Confident but Wrong Selection

The report concerns recovery accepting an obsolete snapshot. The synthetic reply chooses `stale_equip` with 0.92 confidence. Both controls for the selected check behave as expected, but the authored label requires `current_recovery`.

The result records a wrong action. High confidence and correct test mechanics do not establish that the right investigation was chosen.

## H06: Missing External Evidence

Candidate: `review_ready`. Effective action: `request_evidence`.

The current repro-capture reference is present. The required event-trace reference is absent. Local intake checks produce:

> Request: event_trace:stale_or_missing

Human review remains pending.

## H12: Invalid Decision, Preserved Hold

The synthetic impact score is 8, outside the 0 to 2 rubric. The typed contract rejects it and defers the action.

Release coverage still runs. The current recovery record is marked fail, so the disposition remains **hold**. A classifier error cannot erase known evidence.

## Review Notes

The full JSON retains mock build/platform identity, source records, answer values, gate reasons, coverage matrices and executed control results. File hashes support artifact comparison, not authenticity certification. Keith reviews the authored labels and interpretations before using the result to judge a live model.
