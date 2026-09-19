# Verification Scope

## Reproduce the Checks

From the project directory after editable installation:

```powershell
python -m pytest
python -m qa_workflow_lab demo --output runs/verification
python -m pytest runs/verification/test_regression_candidate.py
python -m qa_workflow_lab evaluate --output runs/contract-evaluation.json
python -m qa_workflow_lab showcase --output ../../docs/qa-workflow-lab.html
python -m qa_workflow_lab package --output packages/qa-workflow-lab.zip
```

## What the Tests Establish

- Six independent reference-model oracles pass valid behavior and detect their intended faults.
- Distinct legitimate upgrades and current-epoch recovery remain allowed.
- Missing evidence, wrong builds, wrong run IDs and contradictory pass labels remain visible.
- Telemetry queries reproduce counts, deduplicate deliveries and reject conflicting event identities.
- Stale coverage, unresolved failures and unapproved exclusions cannot become release readiness.
- Agent tool access, runtime/step budgets and citation retrieval rules are enforced in local code.
- Reports retain full traces and file hashes. Hostile HTML-like input is escaped in the standalone page.
- Optional model transport uses mocked responses in tests; secrets stay out of request bodies and reports.
- The package includes only the source, test, fixture, documentation and sample-output allowlist.

The labeled evaluation contains 12 contract cases, stored separately from demo inputs. Its labels are not passed to the policy. It measures expected local dispositions, not general model reasoning quality or efficiency gains.

## Recorded Local Verification

- Project test suite: 68 passing tests, including package link checks and mocked model transport.
- Generated regression candidate: six passing tests.
- Labeled contract evaluation: 12 of 12 expected dispositions matched.
- Browser review: installed Chrome at 1440px, 390px and 320px, all three cases and eight workflows checked for horizontal overflow.
- Interactions: evidence dialog, keyboard tab navigation, finding search, risk filter, Markdown download and JSON download checked.
- Homepage link and layout checked at the same three widths. No browser page errors observed.
- Generated artifacts use stable LF line endings so their recorded file hashes survive Git checkout.

These are local checks, not a deployment result. Live model execution was not part of this verification.

## Deliberate Limits

The browser shows saved offline-policy runs. The local harness exercises a reference model; fixture game-build observations are authored examples. Live model requests, real game execution, deployment integrations, human correction time and operational reliability require separate measured runs. A successful local evaluation supports this documented scope only.
