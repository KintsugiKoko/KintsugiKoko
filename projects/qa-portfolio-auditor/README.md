# QA Portfolio Auditor

## Status

Supporting meta-QA prototype.

QA Portfolio Auditor checks project metadata for demo readiness, documentation coverage, review clarity, evidence completeness, and claim accuracy before publishing.

The current model combines static portfolio metadata, local artifact checks, and a reviewer decision. It supports the release gate without replacing visual review, link verification, or owner sign-off.

## Portfolio Role

This is a supporting artifact rather than a primary proof project. The primary project path starts with Project Fibsh, External QA Handoff Manager, Community Pulse, QA Bug Report Tool, and the Game QA Field Guide.

QA Portfolio Auditor adds the meta-QA layer: release-readiness thinking, evidence completeness, documentation review, claim-accuracy control, tool verification, and explicit owner sign-off.

## What It Answers

Are my QA portfolio tools clearly documented, supported by reviewable evidence, scoped accurately, and easy to inspect?

## What It Demonstrates

- QA discipline applied to my own portfolio artifacts
- Release-readiness thinking before publishing
- Clear project scope and review paths
- Evidence completeness checks
- Data and source-boundary review
- Claim-quality checks around Unreal, Jira, private data, automation, and production-readiness language

## How To Run

Open `index.html` in a browser:

```powershell
start projects\qa-portfolio-auditor\index.html
```

The current prototype uses sample metadata defined in `script.js` and mirrored in `samples/portfolio_tools_sample.json` for review.

## What It Checks

For each portfolio tool, the auditor checks whether the tool has:

- A one-liner
- A status label
- A demo link or sample output
- A README/docs link
- Data and scope boundary language
- An evidence focus
- Known limitations or safe boundary language
- Expected local artifacts or link targets
- No flagged claim-quality phrases

## Artifact / Link Evidence

The auditor can track expected local artifacts and link targets for each portfolio tool, such as README files, demo pages, case studies, sample outputs, reports, and test files.

In the browser demo, artifact existence is represented through sample metadata with `Present`, `Missing`, or `Needs Review` status labels. A local filesystem script provides a separate check for listed repository paths.

A small local filesystem script can also check the listed repo paths directly and generate a saved report:

```powershell
node scripts\audit-portfolio-artifacts.js
```

That script writes `reports/local-artifact-check.md`. Live-page appearance, navigation, and deployment checks remain explicit review gates.

See `docs/artifact-link-check-model.md` for the metadata shape and limitations.

## Claim Quality Rules

The auditor flags wording that would require evidence beyond the current artifact, including:

- live Unreal automation
- Unreal plugin
- production-ready
- real studio telemetry
- private studio data
- real Jira integration
- automated engine validation
- replaces Tech Art review
- AI detects visual quality
- production pipeline integration

## Scope Language

The auditor encourages concrete scope labels such as:

- fictional sample data
- mock data
- mock Unreal-style telemetry
- owner-reviewed
- Markdown export
- Jira-ready reports
- risk summaries
- evidence packs
- external QA coordination

## Current Audit Model

This tool reviews static project metadata, expected local artifacts, wording rules, and recommended next actions. Browser rendering, external integrations, deployment health, and final publication approval are separate checks in the release workflow.

## Known Limitations

- Static browser prototype with an optional local filesystem report script.
- Artifact status in the browser demo is metadata-driven.
- Live link crawling, deployment checks, and repository-wide text parsing are future extensions.
- Sample data is intentionally small, and publication still requires owner review.

## Future Improvements

- Add import/export JSON.
- Add a repository text scan mode.
- Add screenshot-based manual review fields.
- Add saved audit history for before/after portfolio passes.
