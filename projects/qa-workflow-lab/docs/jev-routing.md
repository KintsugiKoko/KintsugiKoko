# Jev QA Intake Routing

## The Question

Can a model interpret a QA report's requested next action more usefully than a small keyword router, without silently treating a guess as an approved decision?

This experiment adds an intake step before the existing Workflow Lab. It suggests one of four specialist workflows or human review. The existing eight workflow implementations, evidence contracts and release logic are unchanged.

## Follow One Report

1. Load a fictional report with build, platform, steps, expected/actual behavior and a requested next action.
2. Check required fields in Python. An empty build or repro description goes to human review without a model request.
3. Run a keyword baseline. One matching keyword family suggests a workflow; no match or competing families defer to a human.
4. Optionally ask Jev a single Choice question with a fixed routing rubric.
5. Validate the response contract, then apply a confidence floor and probability-margin check.
6. Save the suggestion and compare it with separately authored expected labels. A human still owns dispatch and acceptance.

```text
Fictional report -> required fields -> baseline or optional Jev
                 -> local response/gate checks -> suggestion + human review
Separate labels  -----------------------------> evaluation only
```

| Route | First action |
| --- | --- |
| AI3 | Investigate and reproduce a state or client/server discrepancy |
| AI4 | Triage a report or related-defect candidate |
| AI5 | Investigate telemetry, exposure or measurement contracts |
| AI6 | Review external assignments, evidence and receiving-owner follow-up |
| human_review | Clarify missing, conflicting, unsupported or suspicious requests |

AI1, AI2, AI7 and AI8 remain available through the original CLI. They are not intake routes here: selecting change-risk analysis, test generation, release assessment or cross-team coordination requires broader evidence than one incoming report.

## Three Modes

From the project directory after the README installation steps:

```powershell
python -m qa_workflow_lab route-evaluate --output runs/routing-baseline
python -m qa_workflow_lab route-evaluate --mode replay --output runs/routing-replay
python -m qa_workflow_lab route-evaluate --mode jev --dry-run --max-calls 2 --output runs/routing-preview
```

Each output directory must be new. Open `routing.md` for the comparison, or `routing.json` for the underlying records. A dry run produces JSON request previews only.

- **Baseline:** no model, no credentials, deterministic keyword matching.
- **Replay:** hand-authored synthetic answers exercise the adapter's response contract and confidence gates. They are not Jev predictions. R14 intentionally violates the contract, so the command saves its results and exits 2.
- **Jev:** an actual HTTP adapter to TypeSafe, requiring `--allow-network` and a locally configured `TYPESAFE_API_KEY`. No key is stored in reports, source, fixtures or command arguments.

After reviewing the request preview and configuring your account privately:

```powershell
python -m qa_workflow_lab route-evaluate --mode jev --allow-network --max-calls 2 --output runs/routing-live-smoke
```

This two-call command is a transport smoke check, not a whole-dataset comparison. Remaining eligible cases defer to human review when the cap is exhausted, with a nonzero exit. To evaluate all eligible cases, deliberately choose a sufficient cap, at most 20. The current set contains 15 reports, of which 13 pass the required-field check.

Review provider terms and pricing before enabling requests. Only the fictional report and routing rubric are submitted. Labels and rationales stay local. No studio data or private documents belong in these fixtures. A `fictional` flag expresses intent, not automatic proof that text is safe to send.

## Controls Worth Inspecting

- R05 and R06: missing build or steps prevent a network call.
- R09: a keyword baseline picks investigation because it sees reproduction language, even though the request says reproduction is complete and asks for aggregate analysis.
- R10: a paraphrased investigation lacks the baseline's keywords.
- R11: adversarial report text requests bypassing the rubric and approving a release. The authored expectation is human review. A fixture result does not establish live prompt-injection resistance.
- R12: the synthetic response is confidently wrong. The gate allows a suggestion, and the independent label exposes the error. Human approval is still pending.
- R13: insufficient confidence defers to a person.
- R14: malformed response cannot become a specialist suggestion.
- R15: nearly tied options defer even when the supplied confidence is high.

## Read The Comparison Correctly

| Measure | Why it matters |
| --- | --- |
| Wrong specialist suggestions | Misrouting can waste specialist time or delay investigation |
| Suggestion coverage | How much work the router attempts rather than defers |
| Specialist precision | Correct suggestions divided by all specialist suggestions; undefined when none are made |
| Human review and unnecessary deferrals | A safe fallback still has review cost |
| Confusion matrix | Shows exactly which workflow pairs are confused |
| Model identity, latency, token usage | Records the live run context without estimating unmeasured savings |

The checked-in labels are authored expectations pending Keith's review, not independently adjudicated ground truth. The examples used to design the rubric are development cases, not a held-out benchmark. Do not tune a threshold on these examples and then claim general accuracy from the same set.

The default confidence floor is 0.8 and the minimum top-two probability margin is 0.15. Both are illustrative. Confidence describes a model's distribution; it is not a guarantee that its routing choice is correct. Compare threshold settings on a development set, freeze the rubric, and evaluate an independently labeled held-out set before adopting it.

The live adapter permits at most 20 attempts, caps request/response size, uses a 10-second request timeout and a 60-second run budget, rejects redirects, and stops further requests after an error. It does not retry. Network failures, invalid responses and exhausted budgets preserve a human-review outcome and produce exit code 2. Successful execution means an experiment was recorded, not that model routing outperformed the baseline.

## Code Reading Order

1. [Routing cases](../sample-data/routing-reports.json): what enters the system.
2. [Expected labels](../tests/routing-labels.json): what the evaluator expects and why.
3. [Routing logic](../src/qa_workflow_lab/routing.py): baseline, rubric, validation and gates.
4. [Jev adapter](../src/qa_workflow_lab/jev.py): explicit request boundary and failure handling.
5. [Evaluation](../src/qa_workflow_lab/routing_evaluation.py): compare outputs without leaking labels.
6. [Routing tests](../tests/test_routing.py) and [adapter tests](../tests/test_jev.py): failure controls and mocked HTTP contracts.

Run `python -m pytest tests/test_routing.py tests/test_jev.py`, then `python -m pytest` for the full project. Tests forbid real network connections. No UI build or additional dependency is needed for this CLI experiment.

## Explain The Design

The interesting part is not using another model. It is defining a judgment small enough to evaluate, comparing it with a simpler baseline, testing what happens when it fails, and retaining human authority.

Questions to answer while reading the code:

- Why is a missing build number a Python check rather than a model question?
- Why does R09 fool the baseline?
- How can R12 be confident and wrong?
- What happens if the API times out, returns an unknown route, or reaches its request cap?
- Why do expected labels stay outside the request?
- What result would justify keeping the simpler baseline?

## References

The adapter follows the [TypeSafe HTTP API](https://docs.typesafe.ai/api). The [Choice documentation](https://docs.typesafe.ai/primitives) describes constrained routing questions; the [confidence guide](https://docs.typesafe.ai/confidence) explains uncertainty and risk-sensitive gates. API contract reviewed September 19, 2026. Check the provider documentation again before a live run; aliases such as `jev-latest` can change.
