# Artifact / Link Check Model

## Purpose

The artifact/link check helps QA Portfolio Auditor answer a practical portfolio question: does each tool claim evidence that is actually listed as a local artifact or reviewable link target?

This is a portfolio-safe prototype check for demo readiness, documentation coverage, evidence completeness, and overclaim control. It supports human review; it does not replace it.

## Metadata Fields

Each expected artifact can include:

- `label`: clear name for the artifact
- `path`: local repo path or portfolio page path
- `type`: artifact category, such as documentation, demo, case-study, sample-output, tests, or reports
- `status`: Present, Missing, or Needs Review
- `recommendedAction`: small next step for cleanup or verification

## Example Artifact Entries

```json
{
  "label": "README",
  "path": "projects/nyx-test-planner/README.md",
  "type": "documentation",
  "status": "Present",
  "recommended_action": "Keep the README linked from the homepage and project index."
}
```

```json
{
  "label": "Saved sample handoff export",
  "path": "projects/external-qa-handoff-manager/docs/sample-handoff-output.md",
  "type": "sample-output",
  "status": "Missing",
  "recommended_action": "Optional next step: save one Markdown export as a reviewable sample output."
}
```

## Local Filesystem Check

The browser demo stays metadata-driven, but the repo also includes a small local filesystem check:

```powershell
node scripts\audit-portfolio-artifacts.js
```

The script reads `samples/portfolio_tools_sample.json`, checks each listed local path with `fs.existsSync`, and writes `reports/local-artifact-check.md`.

## What The Check Can Prove

- A tool has expected evidence listed in the portfolio metadata.
- A local path listed in the sample metadata currently exists or is missing in the repo when the local script is run.
- Each listed artifact has a clear path, type, status, and cleanup action.
- Missing or uncertain evidence is visible before publishing.
- Recruiter-facing claims can be checked against local/static evidence labels.

## What The Check Cannot Prove

- It does not crawl the live site.
- It does not validate external deployment health.
- It does not perform full browser automation.
- It does not connect to Jira, Unreal, private tools, or studio data.
- It does not prove that every linked file is current or high quality.
- It does not replace manual review.

## Next Future Step

A future iteration could add a repo text scan mode for forbidden overclaim phrases across README and docs files. That should stay local and human-reviewed unless live-site crawling or browser automation is intentionally added later and documented honestly.
