# Bounded Jev QA Harnesses

Three executable harnesses connect typed decisions to local QA operations. The implementation uses the existing TypeSafe HTTP adapter and Python standard library, with no LangChain runtime dependency.

The pattern follows [LangChain's Jev harness walkthrough](https://www.langchain.com/blog/building-a-harness-with-jev): use typed judgments for routing, then enforce the workflow in code. The [TypeSafe API contract](https://docs.typesafe.ai/api) defines the Choice, Noul and Score response shapes used here.

## Review Route

1. Run the clean investigation case below.
2. Open the generated Markdown and inspect its valid and fault-injected controls.
3. Run the full synthetic replay and inspect H03, H06 and H12.
4. Compare the report with [source code](../src/qa_workflow_lab/qa_harnesses.py), [regression tests](../tests/test_jev_harnesses.py) and [saved sample walkthrough](jev-harness-sample.md).

From the project directory, after the README's editable installation:

```powershell
python -m qa_workflow_lab harness-evaluate --mode replay --case H01 --output runs/harness-clean
python -m qa_workflow_lab harness-evaluate --output runs/harness-baseline
python -m qa_workflow_lab harness-evaluate --mode replay --output runs/harness-replay
python -m qa_workflow_lab harness-evaluate --mode replay --harness intake --output runs/harness-intake
python -m qa_workflow_lab harness-evaluate --mode jev --dry-run --max-calls 3 --output runs/harness-preview
python -m pytest
```

Every output path must be new. Open `harness-report.md` to review a run; `harness-results.json` contains the source records, typed answers, gates, local tool traces and hashes. `manifest.json` hashes the output files. Dry runs write `request-preview.json` instead.

## Harness Contracts

| Harness | Typed selection | Local operation | Independent constraint |
| --- | --- | --- | --- |
| Investigation | Duplicate upgrade, stale equipment, recovery, or human review | Runs a fixed Python reference check with valid and injected-fault controls | Literal expected results remain outside the model |
| External-evidence intake | Request evidence, prepare review, or human review | Builds a missing-evidence follow-up and checks required references | Missing fields, stale identity or absent references prevent a review-ready result |
| Release evidence | Coverage focus, blocker focus, or human review | Reviews three required critical-path checks with source IDs | Missing, failed, stale or conflicting evidence retains a hold; complete metadata still needs human review |

The investigation checks exercise a small fictional reference model. Intake and release checks evaluate supplied metadata, not screenshots, logs or game builds. A reference marked present is not proof that its underlying file exists or is valid.

## Decision Flow

1. Validate the complete fictional fixture and separate authored labels.
2. Defer cases missing build or platform before a model request.
3. Evaluate one decision bundle per case: Choice for the action, Noul for a possible bypass request, Score for advisory impact.
4. Validate types, option keys, probability sums, confidence, score legend and weighted score.
5. Defer if Choice confidence is below 0.8, the top probability margin is below 0.15, or bypass probability exceeds 0.2.
6. Dispatch only a hardcoded local function. Recheck mandatory evidence requirements.
7. Compare the effective action with separately authored expectations and preserve the trace.

The thresholds are illustrative policy settings, not calibrated accuracy guarantees. A Noul value near 0.5 means uncertainty about a proposition, not medium severity. Score is an advisory estimate; it cannot set a bug's verified severity or change a product verdict.

The bypass question is defense in depth, not a reliable prompt-injection detector. The actual authority boundary is the local operation allowlist: no supplied commands execute, no tickets are filed, no releases are approved.

## Offline and Live Modes

- **Baseline:** transparent local heuristics, including keyword selection for investigation. It does not understand all embedded instructions.
- **Replay:** synthetic typed responses exercise contracts and failure handling. They are not Jev predictions or an accuracy benchmark.
- **Jev:** optional TypeSafe requests. The same local gates, operations and reporting apply.

The full baseline deliberately produces two wrong non-review actions on adversarial requests and exits 1. The full replay includes one confidently wrong check and an invalid Score answer; it saves the report and exits 2. These are intentional negative fixtures, not a passing evaluation disguised as success.

| Exit | Meaning |
| --- | --- |
| 0 | Execution completed with no wrong non-review action, failed control or contract error; deferrals can remain |
| 1 | Wrong non-review action against authored labels, or a failed control pair |
| 2 | Input, adapter or typed-contract failure |

Always inspect the deferral count. Deferring every case is not useful classification. Authored labels are pending Keith's review, not independently validated ground truth. Labels are never included in request state.

A future live run requires an explicit choice to send the selected fictional fixtures to TypeSafe:

```powershell
python -m qa_workflow_lab harness-evaluate --mode jev --case H01 --dry-run --max-calls 1 --output runs/harness-live-preview
# Set TYPESAFE_API_KEY privately in the environment before explicitly enabling a paid request.
python -m qa_workflow_lab harness-evaluate --mode jev --case H01 --allow-network --max-calls 1 --output runs/harness-live
```

The default cap is three attempts, with an allowed range of 1 to 20, a 10-second per-request timeout and a 60-second transport budget. There are no retries or redirects. The circuit stops after a provider or contract error. Existing output directories are rejected before adapter initialization. Dry runs and offline modes never read credentials. No paid live run is included in this milestone.

## What To Explain

**A classifier is not a test oracle.** H03 selects the wrong investigation check with high synthetic confidence. That check's valid and fault-injected controls behave correctly, but the label comparison still identifies irrelevant selection.

**Required evidence cannot be voted away.** H06 asks for review-ready intake, but the local tool returns a missing-trace follow-up. H12 retains a release hold even when its typed decision fails validation.

**The trace separates responsibilities.** The candidate action, gate, effective action, fixed check output and product disposition are separate fields. This makes an incorrect decision inspectable instead of hiding it inside a polished summary.

## Current Boundaries

This is a portfolio-safe experiment using fictional records. It has no Unreal, Jira, studio or deployment connection. Typed transport tests use mocks. Live Jev reliability, latency, cost and model-version drift remain unmeasured. Input text is bounded, but a fictional flag is not a privacy scanner; review any future fixture additions before a network run.

Next step: review labels, add held-out paraphrases and contradictory reports, then compare a separately approved capped Jev run with the baseline. Adopt a model only if wrong actions, deferrals and review effort justify it.

## Verification Snapshot

Verified locally on September 19, 2026, using Python 3.12:

| Check | Result |
| --- | --- |
| Full project pytest suite | 387 passed, including 125 new harness tests |
| Clean H01 replay | Exit 0; valid and fault-injected controls behaved as expected |
| Intake-only replay | Exit 0; two human-review deferrals preserved |
| Full baseline | Expected exit 1; two wrong non-review actions exposed |
| Full synthetic replay | Expected exit 2; one wrong action and one invalid typed answer exposed |
| Jev dry run | Exit 0; three request previews, no credentials read or API calls |
| Source ZIP export | Passed; includes the generated harness report, JSON and manifest |
| Wheel build | Passed with the declared isolated setuptools build dependency |
| Local Markdown links | 17 checked, none missing |

The default pytest temporary directory was not writable in this Windows session. The suite passed with a fresh writable `--basetemp` directory outside the checkout. An initial wheel attempt without build isolation lacked setuptools; the standard isolated build passed. No application-code fix was needed for either environment issue.

CLI commands were executed from the source checkout with `PYTHONPATH=src` to isolate it from the older local installation. The README documents editable installation for reviewers. Fresh installation from the ZIP or wheel, other operating systems, live model behavior and browser rendering were not tested in this pass. This milestone changes CLI workflows and documentation, not the live portfolio page.
