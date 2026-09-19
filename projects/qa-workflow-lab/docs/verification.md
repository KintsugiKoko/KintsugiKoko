# Verification Scope

## Technical Review Gate

Use the [Design Review Standard](design-review-standard.md) alongside automated verification. Acceptance requires a reproducible demonstration, a source-level explanation, a meaningful failure, a valid control, and a reasoned tradeoff. Test counts support that review; they do not replace it. Maintainer explanation and independent reviewer reproduction remain unassessed until observed.

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

- Expanded regression record: [2026-09-19 verification](regression-verification-2026-09-19.md).
- Project test suite: 190 passing tests after the [Coordination Variant Pack](coordination-variants.md), including negative contracts, graph-order invariance, package link checks and mocked model transport.
- Generated regression candidate: six passing tests.
- Labeled contract evaluation: 12 of 12 expected dispositions matched.
- Browser review: installed Chrome at 320, 390, 414, 768, 1024, 1440 and 2560px, all three cases, eight workflows and three views checked for horizontal overflow.
- Interactions: evidence dialog, keyboard tab navigation, finding search, risk filter, Markdown download and JSON download checked.
- Homepage link and layout checked at the same seven widths. No browser page errors observed.
- Coordination variants: 63 browser view states at 1440, 390 and 320px, with all seven JSON exports matching saved records.
- Critical-path gate: nine passing checks for demo creation, blocked exits, hash-bound review, variant packets and package links.
- Generated artifacts use stable LF line endings so their recorded file hashes survive Git checkout.

These are local checks, not a deployment result. Live model execution was not part of this verification.

## Optional Browser Regression

With Node.js, Playwright and Chrome installed, run from this project directory:

```powershell
node tests/browser_check.cjs ../../docs/qa-workflow-lab.html runs/browser-check ../../docs/index.html
```

Use a new output directory. The script saves screenshots and a JSON result, checks exact Markdown/JSON downloads, resolves evidence references and verifies keyboard tabs and modal focus return. `PLAYWRIGHT_MODULE` can point to an existing Playwright installation; `BROWSER_CHANNEL` defaults to `chrome`. In an extracted package, use `Showcase.html` and omit the homepage argument. No browser dependencies are required for the Python CLI or pytest suite.

## Deliberate Limits

The browser shows saved offline-policy runs. The local harness exercises a reference model; fixture game-build observations are authored examples. Live model requests, real game execution, deployment integrations, human correction time and operational reliability require separate measured runs. A successful local evaluation supports this documented scope only.
