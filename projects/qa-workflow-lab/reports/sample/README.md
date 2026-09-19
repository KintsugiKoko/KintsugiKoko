# QA Workflow Lab: Review Packet

Feature: Relay Arena: upgrade and encounter transitions
Candidate: demo-102 | Baseline: demo-101 | Rules: rules-1

Fictional Relay Arena evidence. Harness assertions execute against the included Python reference model.

| Workflow | Artifact state | Product assessment |
| --- | --- | --- |
| [AI1: Change risk analyst](ai1.md) | review_required | review_required |
| [AI2: Regression test author](ai2.md) | review_required | local_harness_pass |
| [AI3: Investigation agent](ai3.md) | review_required | review_required |
| [AI4: Defect triage agent](ai4.md) | review_required | review_required |
| [AI5: Telemetry analyst](ai5.md) | review_required | review_required |
| [AI6: Remote QA coordinator](ai6.md) | review_required | review_required |
| [AI7: Release evidence analyst](ai7.md) | review_required | hold_for_evidence |
| [AI8: QA lead coordinator](ai8.md) | review_required | review_required |

## Review Route

1. AI6: compare complete, incomplete and wrong-build submissions.
2. AI3 and AI2: inspect the upgrade trace and the valid/fault assertion pair.
3. AI5: reproduce the exposure rates using the recorded local query.
4. AI7 and AI8: inspect stale coverage, dependencies and the receiving owner.

Artifact completion and human acceptance remain separate from a product verdict.

Input SHA-256: 2f3f9cda4100677369ffc5e849a6d0e5ad638df9bfe368dcc3fa1257bb9a240a
