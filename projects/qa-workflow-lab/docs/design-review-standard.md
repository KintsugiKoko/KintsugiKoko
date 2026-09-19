# Design Review Standard

## Review Objective

Demonstrate a working QA mechanism, explain the decisions behind it, and show how a targeted test distinguishes correct behavior from a meaningful failure. Start with one complete investigation rather than a tour of every workflow.

Test totals are supporting evidence. The review must establish what the implementation does, why the expected result is correct, and which decision the result supports.

## Required Gates

| Gate | Demonstrate | Acceptance |
| --- | --- | --- |
| Working implementation | Run from a versioned local input and inspect the produced artifact. | The reviewer can reproduce the result from the documented command and connect it to the relevant source. Saved browser output is identified as a saved run. |
| Technical explanation | Trace input validation, tool selection, calculation, output and human review. | The maintainer can locate each step in code, explain the boundary, and distinguish deterministic execution from optional model proposals. |
| Substantive failure | Show an actual reproduced defect or a clearly identified fault injection. | Explain the causal mechanism, the misleading result a shallow check would accept, and the observable consequence. Do not relabel a fictional fixture as a production incident. |
| Test discrimination | Use an independent expected result, a failing variant and a valid control. | The test catches the targeted fault without rejecting legitimate behavior. State reset and input identity are explicit. |
| Judgment and tradeoff | Explain the chosen fix and one reasonable alternative. | Tie the choice to correctness, inspection effort or maintenance cost. Identify what observation would change the decision. |
| Reproducible handoff | Retain the input, revision, command, expected/actual result and evidence reference. | A second reviewer can repeat the demonstration, inspect the result, and name the remaining question. |

Record each gate as **Pass**, **Needs work**, or **Not assessed**. A green test suite does not assess the maintainer's explanation or a second reviewer's reproducibility. Those gates require an observed review. This standard is a technical review gate, separate from product release approval.

## Primary Worked Example: Invalid Accepted Dependencies

**Risk:** a receiving task can appear available even though an upstream handoff is invalid.

The reproduced defect was in the coordinator's dependency check: it consulted the prerequisite's `accepted` label without propagating that prerequisite's own evidence, acknowledgement or build blockers. The corrected implementation validates each task, then propagates blockers in dependency order. Submitted status labels remain intact; the derived blockers determine whether work is available for review.

| Review question | Source or test |
| --- | --- |
| Why is an accepted label insufficient? | `coordinate()` in [analysis.py](../src/qa_workflow_lab/analysis.py), local blockers and dependency propagation |
| Does the fix catch an invalid direct handoff? | `test_invalid_accepted_dependency_blocks_downstream_work` in [failure-boundary tests](../tests/test_failure_boundaries.py) |
| Does it work through a chain and with reordered input? | `test_dependency_blockers_propagate_indirectly_regardless_of_record_order` in the same test file |
| Does a valid handoff still work? | `test_valid_accepted_dependencies_remain_available` in the same test file |
| Does current task status conceal stale evidence? | `test_accepted_task_with_stale_evidence_blocks_dependents` in the same test file |

**Tradeoff:** dependency-order propagation uses the existing cycle-checked graph and a small derived blocker register. It avoids adding a scheduler or modifying owners' submitted statuses. A separate receiving-owner review remains necessary because a populated acknowledgement field is not proof that a person meaningfully reviewed the work.

## Test Design Discussion

The [Coordination Variant Pack](coordination-variants.md) provides runnable challenges for this review, including a valid parallel control, isolated failure and input-order checks.

For the primary example, be able to answer:

1. Which invariant is protected? Downstream work cannot be available while a prerequisite is incomplete or invalid.
2. What would a shallow test miss? All tasks may have nonempty owners and `accepted` labels while the root task lacks an acknowledgement.
3. Why is the oracle independent? The tests assert specific blocked dependency IDs and a known-valid control, rather than deriving expected blockers with the coordinator itself.
4. What prevents a reject-everything fix? The valid accepted chain must produce no blockers.
5. What remains outside this check? The truth of an owner's acknowledgement and the semantic sufficiency of submitted evidence still require review.
6. What is the next useful challenge? Propose a changed dependency graph or evidence mutation, predict the result, and test that prediction without changing the expected result to match the implementation.

For a second mechanism, use the duplicate-upgrade assertion in [harness.py](../src/qa_workflow_lab/harness.py): repeated delivery of one transaction leaves power at 15; a distinct legitimate transaction can increase it to 20. Explain why duplicate suppression and rejecting all subsequent upgrades are different behaviors.

## Review Record

Keep completed review notes with the local verification evidence. Record:

- Revision and exact input.
- Command and actual output location.
- Invariant, failure mechanism and valid control.
- Expected result stated before execution, then observed result.
- Reviewer question and the source/test used to answer it.
- Tradeoff, unresolved question and next experiment.
- Gate results, reviewer and date.

Use the [walkthrough](walkthrough.md) for the demonstration and [verification record](regression-verification-2026-09-19.md) for the recorded automated results. Live model reliability needs its own measured evaluation; passing offline contracts does not establish it.
