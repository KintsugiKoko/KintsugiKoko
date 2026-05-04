# Post-Load Presentation PIE Checklist

Status: planned manual validation

This checklist turns the Journey Journal project audit into one small Nyx follow-up task. It focuses only on post-load presentation after a save/load pass, so the validation stays narrow, observable, and portfolio-safe.

## Goal

Verify whether the current Nyx prototype can restore durable progress after loading while keeping presentation refresh behavior understandable.

This pass should not claim finished gameplay, final UI, final VFX, or complete save/load coverage.

## Context

The current showcase notes say that durable save/load progress restored without trying to resume an active fishing cast. The remaining follow-up is to check whether Blueprint-facing presentation refreshes clearly after load.

## Definition Of Done

- Run one focused PIE pass if the project is available.
- Save after reaching or simulating a known fishing / Starwell progress state.
- Load the save.
- Record what restored correctly.
- Record any confusing, missing, duplicated, or stale presentation.
- Leave unverified areas marked as not tested.

## Checklist

| Step | Check | Result | Notes |
| --- | --- | --- | --- |
| 1 | Open the Nyx project in Unreal Editor | Not run |  |
| 2 | Load the target test map | Not run |  |
| 3 | Reach or simulate a fishing / Starwell progress state | Not run |  |
| 4 | Save the current progress | Not run |  |
| 5 | Load the saved progress | Not run |  |
| 6 | Confirm active fishing state returns to a safe state such as `Idle` | Not run |  |
| 7 | Confirm durable progress still appears present after load | Not run |  |
| 8 | Check whether Starwell progress or threshold state refreshes visibly | Not run |  |
| 9 | Check whether UI text or feedback is readable after load | Not run |  |
| 10 | Watch for duplicate rewards, replayed one-time events, crashes, or softlocks | Not run |  |

## Evidence To Capture

- Date of the pass
- Unreal version or branch, if available
- Map name used
- Short notes on what was actually observed
- Screenshot or short clip only if it shows a useful tested state
- Any bugs or follow-up questions

## Result Template

```markdown
Date:
Result: Not run / Partial / Pass / Fail

What was tested:
-

What worked:
-

What failed or looked risky:
-

What was not tested:
-

Next action:
-
```

## Portfolio-Safe Summary

This checklist is evidence of a planned QA validation pass for a WIP Unreal prototype. It should become stronger only after a real PIE pass records observed results.
