# Five-Minute Walkthrough

## 1. Start With the Quality Question

Open the browser showcase and select **Candidate with seeded failures**. The question is whether a retried upgrade can mutate the current build twice. The page starts on AI6 because a good investigation begins with usable evidence.

Open `SUB-1` to inspect the failed submission. Then compare `SUB-2`: its claimed pass lacks a trace and contradicts the supplied assertion values. The tool prepares a precise follow-up while retaining the original report.

## 2. Follow the Investigation

Select AI3 and open `TRACE-1`. One transaction has two mutation events. The observed authoritative parameter differs from the rule. The hypothesis is separate from the observation, and the next experiment distinguishes duplicate server mutation from a presentation-only symptom.

## 3. Prove the Assertion Has Value

Select AI2 and open **Work product**. The valid duplicate-upgrade case returns 15; the fault-injected variant returns 20. The intended assertion detects the difference. Review the generated candidate test, then run it through pytest from the CLI packet.

## 4. Assess Exposure and Readiness

AI5 records the exact local SQL and parameters. Candidate exposure is 4/20 versus 1/20 baseline, a 15 percentage-point difference in this fixture. This is a descriptive sample comparison.

AI7 retains stale console evidence and the unresolved upgrade failure. AI8 exposes the responsible owners and dependent regression work. A completed workflow cannot turn these risks into a green release.

## 5. Challenge the Framework

Choose **Missing evidence and schema drift**. Inspect the blocked telemetry result and its tool trace. Then choose **Corrected reference-model scenario**. Its coverage is ready for human review; the receiving owner still accepts the artifact and owns the next decision.

Export the summary or full run JSON. Run `python -m qa_workflow_lab evaluate --output runs/review-evaluation.json` to inspect the labeled contract cases. API-backed tool selection is optional and has its own evaluation needs.
