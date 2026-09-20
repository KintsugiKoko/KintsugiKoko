# QA Workflow Lab

Eight bounded QA workflows connect change risk, regression checks, investigation, telemetry, external test evidence, and release review in one traceable packet.

Built by Keith McAvoy as an independent QA engineering project. The fictional **Relay Arena** scenario follows an upgrade retry across an encounter transition. A reviewer can follow the same issue from its original submission to a controlled test, an exposure query, and a candidate assessment.

**Start with the [browser showcase](../../docs/qa-workflow-lab.html), then inspect the [sample review packet](reports/sample/README.md).** The browser opens locally and displays saved executions with searchable findings, source records, tool traces, and Markdown/JSON exports.

## What Runs

| Workflow | Implemented work product |
| --- | --- |
| AI1: Change risk analyst | Versioned risk-to-test map, changed surfaces and current coverage |
| AI2: Regression test author | Python test candidates plus valid and injected-fault assertion pairs |
| AI3: Investigation agent | Ordered trace, authoritative/presentation comparison, hypothesis and controlled model experiment |
| AI4: Defect triage agent | Field checks, distinct related-report candidates and local defect proposals |
| AI5: Telemetry analyst | Allowlisted SQLite query, deduplicated exposure counts and matched rate comparison |
| AI6: Remote QA coordinator | Assignment packet, submission identity checks and precise missing-evidence follow-ups |
| AI7: Release evidence analyst | Rule/platform coverage matrix retaining stale, conflicting and unresolved evidence |
| AI8: QA lead coordinator | Dependency register, capacity and receiving-owner checks, specialist handoff states |

Two execution modes use the same tools and output contracts:

- **Offline policy:** deterministic tool selection. Works locally, without credentials or a model call. The checked-in showcase uses this mode.
- **Model tool loop:** an optional OpenAI Responses adapter lets a model select bounded retrieval and analysis operations. Hypotheses and next actions require retrieved source IDs. The adapter is tested with mocked responses; live model quality requires a separately recorded evaluation.

The local harness actually executes six independent rule checks, each against a valid and fault-injected case. Reported game-build observations are explicitly fictional fixtures. The harness scope is a Python reference model.

## Run Locally

Use Python 3.10 or later from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e . pytest
python -m qa_workflow_lab demo --output runs/candidate
python -m qa_workflow_lab run --input sample-data/candidate.json --workflow AI6 --output runs/remote-review
python -m pytest
```

On macOS/Linux, activate with `source .venv/bin/activate`. Open `runs/candidate/index.html` to inspect the packet. A new output directory is required for each run so earlier failures remain available.

Explore the contrasting cases:

```powershell
python -m qa_workflow_lab demo --case evidence-gaps --output runs/gaps
python -m qa_workflow_lab demo --case corrected-model --output runs/corrected
python -m qa_workflow_lab evaluate --output runs/evaluation.json
python -m pytest runs/candidate/test_regression_candidate.py
```

`evidence-gaps` intentionally returns exit code 2: schema drift blocks the telemetry workflow. Exit code 0 means the workflows completed their contracts, not that the candidate passed. The original candidate correctly retains a hold recommendation. The corrected scenario is separately authored fixture data, not a claim that an external game defect was fixed.

For a focused dependency challenge, run `python -m qa_workflow_lab demo --variant parallel-missing-ack --output runs/parallel-review`. The [Coordination Variant Pack](docs/coordination-variants.md) adds seven runnable cases covering parallel handoffs, isolated blockers, duplicate assignments and invalid graphs. Build a switchable browser view with `python -m qa_workflow_lab showcase --variants --output runs/coordination-variants.html`, then select AI8.

## Outputs

- `README.md`: review route and workflow disposition table
- `ai1.md` through `ai8.md`: observations, expectations, next actions and source IDs
- `run.json`: full records, calculated results, hypotheses, tool arguments and outputs
- `remote-assignment.md`: executable assignment and follow-up drafts
- `defect-proposals.md`: local ticket drafts with evidence and duplicate candidates
- `test_regression_candidate.py`: fixed-template tests for review and execution
- `index.html`: standalone browser review
- `manifest.json`: run and file hashes

## Record Human Review

```powershell
python -m qa_workflow_lab review --run runs/candidate/run.json --workflow AI6 --reviewer "Keith McAvoy" --decision accepted --note "Reviewed source records and the missing-trace follow-up."
```

This appends to `reviews.jsonl` with the immutable run hash. Artifact acceptance leaves the product verdict unchanged. The receiving owner still decides what to send, file, retest or escalate.

## Optional Model Execution

Set `OPENAI_API_KEY` and `OPENAI_MODEL` through your local environment, then explicitly enable network mode:

```powershell
python -m qa_workflow_lab run --input sample-data/candidate.json --workflow AI6 --mode model --allow-network --output runs/model-review
```

The selected fictional bundle and retrieved tool results are sent to the configured model. API usage may incur cost. Defaults cap each workflow at 12 steps, 120 seconds, a 200 KB request body and 1,600 output tokens per request. Requests use `store=false`, a fixed HTTPS endpoint, no redirects and no automatic retry. Credentials stay in request headers and are excluded from reports. Offline runs never read credentials.

The adapter follows [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs). The model proposes a structured action; local code validates it and invokes the allowlisted operation. A model cannot change the computed verdict or execute arbitrary code.

## Optional Jev Intake Routing Experiment

Compare a transparent keyword baseline with an optional Jev routing suggestion before any workflow executes. Fifteen fictional reports cover clear ownership, missing fields, conflicting requests, paraphrases, negation, and adversarial instructions. Local checks handle missing build/platform/repro context. The model can suggest AI3, AI4, AI5, AI6, or human review; it cannot dispatch tools or change a product verdict.

```powershell
python -m qa_workflow_lab route-evaluate --output runs/routing-baseline
python -m qa_workflow_lab route-evaluate --mode replay --output runs/routing-replay
python -m qa_workflow_lab route-evaluate --mode jev --dry-run --max-calls 2 --output runs/routing-preview
```

The synthetic replay deliberately includes a malformed response and returns exit code 2 after saving the report. It tests the fallback, not Jev accuracy. The dry run saves request bodies without reading credentials or contacting a service. Both modes work offline.

With `TYPESAFE_API_KEY` set privately in your environment, `--mode jev --allow-network` enables the TypeSafe adapter. Review the dry run first: the selected fictional reports leave your computer and API usage may incur cost. A 1 to 20 request-attempt cap, 10-second request timeout, 60-second run budget, no redirects, and a stop-on-error circuit bound the experiment. No automatic retry occurs. Existing output directories are rejected before requests.

`routing.md` and `routing.json` show the baseline comparison, wrong specialist suggestions, human-review deferrals, coverage, confusion matrices, input/rubric/label hashes, and live usage when applicable. Labels are authored test expectations kept separate from request inputs, pending Keith's review. A confidence threshold is an experimental gate, not proof that a suggestion is correct.

Read the [Jev routing walkthrough](docs/jev-routing.md) for the request flow, failure cases, commands and evaluation boundaries. No live Jev accuracy result is included in the checked-in project.

## Bounded Jev QA Harnesses

Three runnable harnesses extend the routing experiment into investigation-check selection, external-evidence intake and release-evidence review. Jev supplies typed Choice, Noul and Score judgments; local code validates the response, runs allowlisted checks and preserves evidence gaps. The offline replay includes confident misrouting, missing evidence and invalid responses so reviewers can inspect how the workflow handles failure.

```powershell
python -m qa_workflow_lab harness-evaluate --mode replay --case H01 --output runs/harness-clean
python -m qa_workflow_lab harness-evaluate --mode replay --output runs/harness-replay
```

The clean case runs a valid and fault-injected Python control pair. The full replay intentionally exits 2 after saving its report because it contains a malformed answer. No API is called in either command. Read the [harness walkthrough](docs/jev-harnesses.md) and [sample results](docs/jev-harness-sample.md) for the three contracts, critical-path gates and opt-in Jev request preview.

## Package and Rebuild

```powershell
python -m qa_workflow_lab package --output packages/qa-workflow-lab.zip
python -m qa_workflow_lab showcase --output ../../docs/qa-workflow-lab.html
```

The ZIP includes source, tests, fixtures, docs, a freshly generated sample packet, a synthetic harness replay packet under `reports/jev-harnesses/`, and a standalone `Showcase.html` with all three main cases. Packaging uses an explicit project-file allowlist. Extract the ZIP before opening the showcase or installing the project.

## Design and Verification

- [Architecture and tool contracts](docs/architecture.md)
- [Workflow register and acceptance criteria](docs/workflow-register.md)
- [Game-system scenario design](docs/game-system-scenarios.md)
- [Five-minute walkthrough](docs/walkthrough.md)
- [Verification and evaluation scope](docs/verification.md)

## What I Practiced

I translated a QA operating framework into bounded tools, independent test oracles, source-linked reports, failure handling and evaluation cases. The design preserves the distinction between a valid artifact, a passing assertion and a release decision.

## Known Limitations

This is an independent portfolio prototype using fictional game-system data. The package has no game-engine, studio, issue-tracker or build-farm connection. Source retrieval operates on supplied records. Model notes carry source references but still need semantic review. The interface displays saved executions; CLI runs produce new evidence. Human effort savings, live model reliability and production integration have not been measured.

## Future Improvements

Review the routing labels, run a capped live Jev experiment, then test a separate held-out set before deciding whether model routing earns a place in the workflow. Evaluate one model-driven AI6 assignment against independently labeled cases, record reviewer correction time, and compare it with the deterministic baseline. Add further integrations only after their evidence contracts and access boundaries are defined.
