# QA Portfolio Gap Review

## What The Portfolio Proves Now

The portfolio now shows a coherent Senior QA / Technical QA / Art QA path:

- Bug-quality writing through QA Bug Report Tool.
- Scenario planning and risk/status tracking through Nyx Test Planner.
- Mock telemetry parsing and Art QA evidence reporting through Art Telemetry QA.
- Mock player/playtest feedback summarization through Community Pulse.
- External/offsite QA coordination through External QA Handoff Manager.
- Human-reviewed Markdown exports and clear WIP boundaries across the strongest tools.

This is not presented as production engineering. It is stronger as QA evidence: turning ambiguous inputs into structured reports, risk summaries, validation plans, and reviewer-friendly documentation.

## What Still Feels Light

- Static browser tools do not have automated UI tests yet.
- External QA Handoff Manager is a first static MVP with hard-coded mock data.
- QA Capture Review Board is not present on `master`, so it should stay out of the main review path until it exists.
- The CLI tools have strong README/report evidence, but a hiring manager may still need the homepage to point them clearly at the right first projects.

## Senior QA Evidence

- Clear bug report structure and triage fields.
- Repro quality, expected/actual result discipline, severity/priority normalization, and review notes.
- Test planning before implementation gets messy.
- Pass/fail/follow-up thinking in case studies and smoke-test docs.
- Release/readiness style summaries without pretending the tools replace human judgment.

## Technical QA Evidence

- Python CLIs with pytest coverage.
- Markdown and JSON output paths where useful.
- Mock data parsing and report generation.
- GitHub Actions test matrix for Python projects.
- CLI smoke checks that confirm exports and reports work at MVP level.

## Art QA Evidence

- Art Telemetry QA uses mock Unreal-style art validation data.
- The tool converts sample asset data into risk summaries, owner-routing notes, regression notes, and Jira-ready report drafts.
- Wording stays clear that this is not an Unreal plugin, not live Unreal automation, and not real studio telemetry.

## QA Leadership Evidence

- External QA Handoff Manager shows handoff packet thinking: feature goal, scenario matrix, bug standards, evidence requirements, and intake checklist.
- Community Pulse shows how player/playtest feedback can be grouped into risk notes and human-reviewed follow-up reports.
- The root README and homepage now give recruiters a faster first review path.

## Build Later, Not Now

These are useful later, but should not block the current portfolio polish:

- QA Capture Review Board as a separate working tool.
- Editable External QA Handoff Manager fields.
- Import/export JSON for static browser tools.
- Automated browser smoke tests for the static pages.
- More visual evidence examples or screenshots.
- A single dashboard that compares report outputs across tools.

## Gap Review Verdict

The portfolio is ready for a live review pass as a QA-focused public-development portfolio. The strongest evidence is QA judgment, risk communication, structured documentation, and tool-assisted reporting. The remaining gaps are reasonable next iterations rather than blockers.
