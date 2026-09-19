# Workflow Register

All outputs are review artifacts. Named owners approve consequential actions.

| ID | Trigger and inputs | Tool and acceptance | Receiving owner |
| --- | --- | --- | --- |
| AI1 | Changed surface, versioned diff, approved rules and coverage | `map_change_risks`: connect each risk to a rule or explicit gap, revision and current coverage | Embedded QA |
| AI2 | Stable approved rule and supported local fixture | `author_and_test_regression`: valid case passes, injected fault fails, candidate assertion retained, state reset per run | QA Engineering |
| AI3 | Failure trace with build, session and shared clock | `investigate_state`: retain observed state and timeline; separate causal hypotheses from local experiment results | QA and Gameplay Engineering |
| AI4 | Original defects, player impact and referenced evidence | `prepare_defects`: check required fields and counts; preserve differences between duplicate candidates | Feature QA |
| AI5 | Metric contract, exposure rows, candidate and baseline | `compare_telemetry`: query reproduces counts and denominator; measurement contract permits comparison | Data QA and metric owner |
| AI6 | Approved assignment and original submissions | `review_submissions`: inspect identity and readable fixture artifacts; list exact missing requirements | External QA Lead |
| AI7 | Required risks, platforms, candidate coverage and open defects | `assess_candidate`: every requirement/platform has current evidence or an explicit gap; failures remain visible | QA Lead and release owner |
| AI8 | Task ownership, capacity, dependencies and receiving acknowledgements | `coordinate_tasks`: detect missing dependencies, cycles, unavailable capacity and unacknowledged completion | QA Lead |

## Stop Conditions

- Missing or unapproved oracle: stop the affected rule-dependent workflow.
- Wrong build or missing required evidence: mark the submission incomplete and keep its original result.
- Unaligned trace clock: block event-order interpretation.
- Schema drift, invalid denominator or count disagreement: block trend comparison.
- Tool failure, out-of-scope action or exhausted step/runtime budget: preserve a blocked run.
- Unreviewed model proposal: retain pending status; do not convert it into an observed fact.

## Worked Handoff

The sample reports a repeated upgrade request. AI6 keeps the original failed submission and requests a missing trace from another tester. AI1 connects the retry path to upgrade and recovery rules. AI3 finds two mutation records for one transaction and proposes a guard investigation. AI2 runs a local duplicate-request assertion in both valid and fault-injected states. AI4 keeps a separate UI-only report as a possible related issue. AI5 measures 4 failures in 20 eligible candidate records against 1 in 20 baseline records. AI7 retains the failing upgrade and stale console recovery evidence. AI8 shows who owns the investigation, regression review and readiness decision.

The fixture narrative and the executed reference-model checks are separate evidence sources. Neither implies that a real game was tested.

## Acceptance Review

Use the cited record, tool trace and expected rule together. Check whether the evidence supports the conclusion, whether another platform or build is being implied, and whether the receiving owner has enough information to act. A completed agent run is a request for this review.
