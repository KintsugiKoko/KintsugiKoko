# Coordination Variant Pack

Seven fictional variants challenge one mechanism: deriving work readiness from accepted dependencies and valid handoff evidence. Each starts from a known-valid parallel graph with controlled input changes that can be explained and tested.

```text
TASK-1 -> TASK-2 -> TASK-4
       -> TASK-3 -> TASK-4
```

## Expected Outcomes

| Variant | Change | Expected AI8 outcome |
| --- | --- | --- |
| `parallel-valid` | Valid parallel prerequisites and a join | All four tasks have no derived blockers. TASK-4 remains queued, not automatically approved. |
| `parallel-missing-ack` | Remove TASK-2 acknowledgement | TASK-2 is blocked; TASK-4 names TASK-2. TASK-1 and TASK-3 remain available. |
| `independent-blocker` | TASK-2 has zero capacity; TASK-4 depends only on TASK-3 | Only TASK-2 is blocked. The independent path is unchanged. |
| `duplicate-work-key` | TASK-2 and TASK-3 claim the same work key | Both conflicting tasks are blocked, regardless of input order. TASK-4 names both prerequisites. |
| `blank-owner` | TASK-1 owner is whitespace | TASK-1 needs a receiving owner. Both branches and their join retain dependency blockers. |
| `dependency-cycle` | TASK-1 depends on TASK-4 | AI8 stops as blocked/unverified. No available-task register is produced. |
| `missing-prerequisite` | TASK-3 refers to absent TASK-99 | AI8 stops as blocked/unverified and identifies the missing dependency. |

Variant definitions contain only input changes. Independent expected blocker maps live in [test_coordination_variants.py](../tests/test_coordination_variants.py), not in the evidence passed to the workflow.

## Run and Inspect

From the installed project directory, use fresh output paths:

```powershell
python -m qa_workflow_lab demo --variant parallel-missing-ack --output runs/missing-ack
python -m qa_workflow_lab demo --variant duplicate-work-key --output runs/duplicate-work
python -m qa_workflow_lab demo --variant dependency-cycle --output runs/cycle
python -m qa_workflow_lab showcase --variants --output runs/coordination-variants.html
python -m pytest tests/test_coordination_variants.py -v
```

Open `runs/coordination-variants.html`, select **AI8 / QA lead coordinator**, then switch evidence cases. Use **Work product** for the task register and **Tool trace** for rejected graphs. Individual run directories include Markdown, JSON, a browser view and file hashes.

The cycle and missing-prerequisite demos return exit code 2 because AI8 cannot evaluate the graph. Other variants return 0 when analysis completes, even if some tasks have blockers. Completion is not task approval or a product pass. The ordinary `showcase` command and the main three-case demo remain unchanged. `--case` and `--variant` cannot be combined.

## Input Rules

- Dependencies are a list of distinct, nonempty task IDs. Unknown IDs and cycles stop graph evaluation.
- Capacity is a nonnegative integer count of available task slots. Zero is a valid unavailable-capacity signal; strings, booleans, fractions and non-finite numbers are invalid.
- An empty, non-text or whitespace-only owner value creates a receiving-owner blocker. A missing required field stops contract validation.
- Optional work keys must be nonempty text. Surrounding whitespace is ignored when detecting conflicts. Every task claiming a duplicate key is blocked pending owner resolution.
- Existing build, evidence and receiving-acknowledgement checks still apply. Inputs and submitted task states remain unchanged.

## Critical Path Gate

Before a full regression pass, run the nine existing end-to-end checks that protect the primary review flow:

```powershell
python -m pytest tests/test_reports_cli.py tests/test_coordination_variants.py -k "cli_complete_flow or each_variant_cli or package_has_self_contained" -q
```

These exercise ordinary demo creation, expected blocked exits, hash-bound human review, all seven variant packets and package-local links. Then open the optional browser view and verify AI8 case switching, the valid control, blocked graph traces and an exact JSON export. Run the full suite before sharing a changed package.

## What the Tests Establish

Exact blocker maps cover the control, branch isolation, duplicate assignment and downstream propagation. Each of the five evaluable variants is checked under all 24 orderings of its four tasks, 120 graph executions. Repair tests restore acknowledgement or distinct work ownership and verify that blockers clear without altering the submitted state or earlier result.

New tests reproduced order-dependent duplicate detection and whitespace-owner acceptance before correction. Typed capacity and dependency contracts were tightened in the same pass. This is deterministic local coordination over fictional records, not an execution scheduler or validation of a real team's staffing decisions.
