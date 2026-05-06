# QA Portfolio Auditor Placement Audit

## Current Placement

QA Portfolio Auditor appears in:

- `README.md`
- `docs/index.html`
- `projects/README.md`
- `projects/qa-portfolio-auditor/README.md`
- `docs/qa-portfolio-auditor.html`

## Placement Decision

**Decision: keep QA Portfolio Auditor as an optional/supporting review layer.**

The main recruiter path remains:

1. QA Bug Report Tool
2. Nyx Test Planner
3. Art Telemetry QA
4. External QA Handoff Manager
5. Community Pulse, where relevant
6. QA Portfolio Auditor as the optional self-audit layer

This preserves the story:

> Bug quality -> test planning -> Art QA telemetry -> external QA leadership -> self-audit discipline.

## Primary Or Secondary?

QA Portfolio Auditor should read as **secondary/supporting**, not primary.

It strengthens the portfolio because it shows release-readiness discipline, artifact evidence checks, documentation review, recruiter-safe wording review, evidence completeness, and overclaim control. It should not compete with the stronger first-review projects that demonstrate direct QA tool-building, test planning, telemetry parsing, or external QA handoff judgment.

## Crowding Risk

The homepage now introduces QA Portfolio Auditor as an optional support layer before the cards, and its card uses the `supporting-card` treatment. That keeps it discoverable without making it the primary hero.

## Recruiter-Safe Wording

The current wording avoids unsafe claims:

- It does not claim live-site crawling.
- It does not claim full browser automation.
- It does not claim all links are automatically checked.
- It does not claim production-readiness validation.
- It does not claim deployment health validation.
- It does not replace manual review.

Safe terms used:

- `portfolio-safe`
- `meta-QA prototype`
- `local/static metadata`
- `human-reviewed`
- `artifact evidence`
- `evidence completeness`
- `recruiter-safe wording`
- `overclaim risk`
- `tool readiness`

## Changes Made In This Pass

- Added a GitHub Pages-facing `docs/qa-portfolio-auditor.html` demo page with matching CSS and JS.
- Updated the homepage card to link directly to the live Auditor page.
- Updated the README and project roadmap to mention the live Auditor link.
- Added this placement audit.
- Added a live readiness report.

## Result

**Pass with notes.** QA Portfolio Auditor is discoverable, but clearly supporting. It reinforces the portfolio maturity story without turning the project section into a pile of unrelated tools.

Known note: the repository still has an existing root-level `python -m pytest` aggregation limitation because multiple Python projects are tested from their own roots. This placement pass does not change that test structure.
