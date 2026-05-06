# QA Tool Audit Report

Audit date: 2026-05-06

This report reviews the current portfolio tools and project documentation for Senior QA / Technical QA / Art QA signal. It focuses on evidence that is already present in the repository: tests, sample data, static pages, generated reports, and portfolio-safe documentation.

## Repository-Level Findings

- Primary deployment surface: GitHub Pages from `docs/`.
- Main portfolio page: `docs/index.html`.
- Live planning prototype: `docs/nyx-test-planner.html`.
- Root CI workflow: `.github/workflows/tests.yml`.
- Python projects in the root CI matrix: QA Bug Report Tool, Art Telemetry QA, Obsidian Conversation Sync Agent, Community Pulse Report Tool.
- Additional Python project with tests outside the root matrix: `second-brain-docs-agent`.
- No private studio data was found in the audited tool samples.
- Art QA / telemetry wording should continue to say mock, fictional, portfolio-safe, human-reviewed, and not a real Unreal plugin.

## Tool Inventory

| Tool / Project | Purpose | Current Status | Strongest Recruiter Evidence | Risky Or Unclear Wording | Test Coverage Status | Recommended Polish | Verification Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA Bug Report Tool | Converts rough QA notes into structured Markdown bug reports and triage summaries. | First working version / in progress. | Python CLI, sample notes, generated reports, JSON option, triage summary, 26 pytest tests. | Low risk. README clearly frames it as practice tooling separate from professional shipped-title work. | 26 tests passed. CLI smoke checks passed for single report, batch conversion, and triage summary. | Keep as first proof project because it shows QA fundamentals plus code/tests/docs. | Pass. |
| Art Telemetry QA | Parses mock Unreal-style Art QA telemetry and validation data into findings, risk scores, owner routing, reports, and Jira-ready drafts. | MVP portfolio prototype. | Mock telemetry parsing, validation rules, generated Markdown/CSV/Jira-ready reports, 14 pytest tests. | Must avoid implying real Unreal automation, real studio telemetry, or production readiness. Current wording is safe. | 14 tests passed. CLI scan generated 25 findings from 6 mock assets. | Add a top-level showcase page so recruiters can inspect the reporting model without digging into generated files. | Pass. |
| Nyx Test Planner | Browser-based QA planning board for Nyx scenarios, risk, status, validation type, and Markdown test plan drafting. | Live planning prototype. | Live GitHub Pages tool, scenario filters, local-only browser storage, Markdown export. | Must stay framed as planning, not an automated Unreal test runner. Current README says it does not connect to Unreal, Jira, private tools, or automated runners. | No automated JS tests present. Static browser smoke check should be used. | Link it near Unreal validation scenario docs so the planning workflow reads as intentional. | Pass with limitation: manual/static browser verification only. |
| Community Pulse Report Tool | Converts fictional community feedback CSVs into weekly sentiment reports. | First version / in progress. | Python CLI, fictional sample CSV, generated Markdown report, 9 pytest tests. | Low risk. README clearly says fictional sample data only and no live community/platform connections. | 9 tests passed. CLI smoke check generated a report from sample data. | Keep positioned as community/QA reporting practice, not live social listening. | Pass. |
| Obsidian Conversation Sync Agent | Syncs exported AI conversations into Obsidian-friendly Markdown notes. | First version, local-only practice project. | Local file parsing, dry-run mode, generated note structure, 6 pytest tests. | Must not imply account login, private chat access, or automatic summarization. Current README says exported files and human review. | 6 tests passed. Dry-run smoke command returned success. | Keep as documentation workflow support rather than core QA proof. | Pass. |
| Second Brain Docs Agent | Turns Obsidian notes and exported chat transcripts into draft Markdown documentation. | Early MVP, local-only, draft-only. | Draft generation from local samples, 14 pytest tests, no API keys. | Some wording says "agentic engineering"; keep it secondary so it does not distract from Senior QA / Technical QA signal. | 14 tests passed. Sample draft generation returned success. | Keep card wording focused on documentation discipline and human-reviewed drafts. | Pass. |
| QA Bug Report Portfolio | Stores practice bug reports and a reusable report format. | Planned / in progress. | Existing report archive with one completed link-fix report. | README says it is practice work, not professional QA evidence. That is honest. | No automated tests expected. | Useful as supporting documentation, not a primary proof project. | Pass as documentation project. |
| Unreal Project Showcase: Nyx | Documents the WIP Unreal C++ prototype, PIE checklists, save/load notes, and system notes. | Work in progress. | Save/load reliability notes, PIE smoke checklist, fishing/Starwell notes, WIP boundaries. | Must not sound like a finished game or completed vertical slice. Current WIP wording is mostly safe. | No Unreal build/test run from this portfolio repo. | Add a top-level Unreal test level/scenario showcase to connect the notes to QA planning and risk review. | Pass with limitation: documentation-only in this repo. |
| Project Nyx Folder | Placeholder operating guide for Nyx planning and docs. | Planned / placeholder. | Clear WIP boundary. | No implementation claim. | No tests expected. | Leave simple. | Pass. |
| QA Engineer Hyperbolic Time Chamber | Placeholder for QA-focused skill reps and operating guidance. | Planned / placeholder. | Honest scope and project-specific AGENTS guidance. | No implementation claim. | No tests expected. | Leave simple until real exercises exist. | Pass. |

## Existing Test Commands

Use the bundled or system Python from each project folder:

```powershell
python -m pytest
```

Projects verified this way:

- `projects/qa-bug-report-tool`
- `projects/art-telemetry-qa`
- `projects/obsidian-conversation-sync-agent`
- `projects/community-pulse-report-tool`
- `second-brain-docs-agent`

## Existing Build Commands

No package-level web build commands were found. The portfolio homepage and Nyx Test Planner are plain static HTML/CSS/JS under `docs/`.

## Existing Deployment Workflow

The repo deploys the static site through GitHub Pages from the `docs/` folder on `master`. No new deployment workflow is needed.

## Claim Safety Notes

- Art Telemetry QA is a mock-data Python CLI, not an Unreal plugin.
- Nyx Test Planner is a browser planning prototype, not an automated test runner.
- Unreal test levels and scenarios are portfolio-safe QA planning documentation unless a real Unreal project integration is explicitly present.
- Community Pulse uses fictional sample data only.
- Obsidian and Second Brain tools operate on local/exported files and human-reviewed drafts.
