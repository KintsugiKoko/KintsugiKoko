# QA Portfolio Auditor Homepage Placement Review

## Purpose

This review checks whether QA Portfolio Auditor is discoverable as a recruiter-facing Senior QA / Technical QA support artifact without making it compete with the primary QA project evidence on the live homepage.

## Where QA Portfolio Auditor Appears Now

- `README.md`
  - Mentioned as an optional support layer in Best First Review Path.
  - Removed from the equal-weight Featured Projects table.
- `projects/README.md`
  - Mentioned as an optional support layer in Good Starting Point.
  - Removed from the equal-weight Current Project Folders table.
- `docs/index.html`
  - Appears as a linked optional support-layer note above the project grid.
  - Links to the live `qa-portfolio-auditor.html` page.
  - Removed from the main Featured Projects card grid.
- `projects/qa-portfolio-auditor/README.md`
  - Status and portfolio role clarify it is a secondary/supporting artifact.

## Why It Is Secondary / Supporting

QA Portfolio Auditor is not the main proof of QA execution. It supports the portfolio by showing the review layer used before publishing: release-readiness thinking, evidence completeness, recruiter-safe wording review, overclaim control, tool/documentation readiness, and human-reviewed QA discipline.

It should be reviewed after the core tools, not before them.

## Main Recruiter Path After Update

1. QA Bug Report Tool - bug quality, repro discipline, severity/priority thinking, Markdown/JSON output, and pytest-backed validation.
2. Art Telemetry QA - Art QA / Technical QA evidence using mock Unreal-style telemetry, risk summaries, owner routing, regression notes, and Jira-ready report drafting.
3. Nyx Test Planner - QA planning judgment, risk notes, expected results, status tracking, and Markdown test-plan exports.
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
- Local homepage HTTP check from `docs/` - passed; confirmed QA Portfolio Auditor appears as a linked optional support layer, not as a project card.
- Static homepage check - passed; confirmed the QA Portfolio Auditor card was removed from the project grid.
- `python -m pytest` in `projects/qa-bug-report-tool` - 26 passed.
- `python -m pytest` in `projects/art-telemetry-qa` - 14 passed.
- `python -m pytest` in `projects/community-pulse-report-tool` - 9 passed.
- `python -m pytest` in `projects/obsidian-conversation-sync-agent` - 6 passed.
- `python -m pytest` in `second-brain-docs-agent` - 14 passed.
- No root `package.json` exists, so no `npm run build`, `npm test`, or `npm run lint` commands were available.

## Known Limitations

- This pass updates source files only; it is not pushed live yet.
- The homepage links to the live auditor page, but the auditor remains a supporting link rather than a project card.
- QA Portfolio Auditor still uses static/mock metadata in the browser UI.
- The local artifact script checks repo paths only and does not crawl the live site.
- Human review is still required before publishing.

## Ready To Commit / Push

Ready to commit after review. The changes are scoped to homepage placement, README/project index positioning, and this review report.
