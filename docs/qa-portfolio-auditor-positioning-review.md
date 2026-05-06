# QA Portfolio Auditor Positioning Review

## Purpose

This review checks whether QA Portfolio Auditor is discoverable as a recruiter-facing Senior QA / Technical QA support artifact without making it compete with the primary QA project evidence.

## Where QA Portfolio Auditor Appears Now

- `README.md`
  - Listed in Featured Projects.
  - Mentioned as an optional item in Best First Review Path.
- `projects/README.md`
  - Listed in Current Project Folders.
  - Mentioned as an optional support layer in Good Starting Point.
- `docs/index.html`
  - Listed in the homepage Projects section.
  - Framed with an optional support-layer note before the project grid.
  - Card status uses "Portfolio-safe meta-QA prototype."
- `projects/qa-portfolio-auditor/README.md`
  - Status and portfolio role clarify it is a secondary/supporting artifact.

## Why It Is Secondary / Supporting

QA Portfolio Auditor is not the main proof of QA execution. It supports the portfolio by showing the review layer used before publishing: release-readiness thinking, evidence completeness, recruiter-safe wording review, overclaim control, tool/documentation readiness, and human-reviewed QA discipline.

It should be reviewed after the core tools, not before them.

## Main Recruiter Path After Update

1. QA Bug Report Tool - bug quality, repro discipline, severity/priority thinking, Markdown/JSON output, and pytest-backed validation.
2. Nyx Test Planner - QA planning judgment, risk notes, expected results, status tracking, and Markdown test-plan exports.
3. Art Telemetry QA - Art QA / Technical QA evidence using mock Unreal-style telemetry, risk summaries, owner routing, regression notes, and Jira-ready report drafting.
4. Community Pulse - mock player/playtest feedback grouping, repeated themes, risk notes, and human-reviewed QA follow-up reports.
5. External QA Handoff Manager - external QA coordination, scenario coverage, evidence requirements, intake checklist, and Markdown handoff exports.
6. Optional support layer: QA Portfolio Auditor - meta-QA review for tool readiness, documentation coverage, evidence completeness, recruiter-safe wording, and overclaim risk.

## Wording / Limitation Protections

The updated copy keeps QA Portfolio Auditor portfolio-safe by saying:

- It is a portfolio-safe meta-QA prototype.
- It uses static/mock portfolio metadata.
- It relies on human-reviewed checks.
- It checks local/static readiness signals and optional local artifact paths.
- It does not crawl the live site.
- It does not perform browser automation.
- It does not validate deployment health.
- It does not connect to Jira or Unreal.
- It does not replace manual review.

## Checks Run

- `node --check scripts\audit-portfolio-artifacts.js` - passed.
- `node --check projects\qa-portfolio-auditor\script.js` - passed.
- `node scripts\audit-portfolio-artifacts.js` - passed; checked 15 artifacts, found 1 intentional missing artifact, and 0 metadata mismatches.
- JavaScript smoke check for auditor export/model - passed.
- Local homepage HTTP check from `docs/` - passed; confirmed QA Portfolio Auditor, optional support-layer wording, meta-QA status, and limitation language are present.
- `python -m pytest` in `projects/qa-bug-report-tool` - 26 passed.
- `python -m pytest` in `projects/art-telemetry-qa` - 14 passed.
- `python -m pytest` in `projects/community-pulse-report-tool` - 9 passed.
- `python -m pytest` in `projects/obsidian-conversation-sync-agent` - 6 passed.
- `python -m pytest` in `second-brain-docs-agent` - 14 passed.
- No root `package.json` exists, so no `npm run build`, `npm test`, or `npm run lint` commands were available.

## Known Limitations

- This pass updates source files only; it is not pushed live yet.
- The homepage card links to the GitHub project README, not a live hosted auditor page.
- QA Portfolio Auditor still uses static/mock metadata in the browser UI.
- The local artifact script checks repo paths only and does not crawl the live site.
- Human review is still required before publishing.

## Ready To Commit / Push

Ready to commit after review. The changes are scoped to portfolio positioning, homepage copy/style, QA Portfolio Auditor README positioning, and this review report.
