# External QA Handoff Manager

**Status:** Portfolio-safe prototype  
**Live demo:** [Handoff Ops Demo](../../docs/external-qa-handoff-manager.html)

External QA Handoff Manager turns feature goals into outsource-ready QA packets with setup steps, scenario coverage, bug-quality standards, evidence requirements, daily summaries, and QA lead intake review checklists.

Handoff Ops Demo lets reviewers walk through a lightweight external QA intake scenario, triage mock bug cards, check evidence quality, and generate a QA lead summary.

## What This Demonstrates

- External QA handoff planning
- Bug-quality standards that reduce noisy reports
- Evidence requirements before developer review
- QA lead intake review discipline
- Owner routing for QA, Art, Tech Art, Engineering, Performance, Design, and Production partners
- Markdown packet and summary exports

## Portfolio-Safe Boundaries

- Uses mock feature data and mock incoming bug cards only.
- Does not use private studio data, private workflows, real Jira data, or proprietary schemas.
- Does not connect to Jira or any production tracking system.
- Does not claim production pipeline integration.
- Simulates QA lead intake review behavior for portfolio review and learning.

## Demo Flow

1. Open the [Handoff Ops Demo](../../docs/external-qa-handoff-manager.html).
2. Review the mock **Mount Equipment Visual Validation** handoff.
3. Check the scenario matrix, bug standards, evidence requirements, and intake checklist.
4. Switch to Handoff Ops Demo.
5. Review the mock external QA bug cards.
6. Mark each card as `Ready for Dev Review`, `Needs More Info`, or `Duplicate / Known Issue`.
7. Generate a QA Lead Intake Summary.

## Local Preview

Open either file directly in a browser:

```text
projects/external-qa-handoff-manager/index.html
docs/external-qa-handoff-manager.html
```

The project page is kept near its README for source review. The `docs/` page is the GitHub Pages-facing copy used by the portfolio homepage.

## Included Outputs

- Handoff Overview
- Setup Instructions
- Scope
- Scenario Matrix
- Bug Standards
- Evidence Requirements
- Escalation Rules
- Daily Summary Template
- QA Lead Intake Review Checklist
- QA Lead Intake Summary

## Sample Data

- [sample_handoff.json](samples/sample_handoff.json)
- [sample_incoming_bugs.json](samples/sample_incoming_bugs.json)

These files are fictional and intentionally small so the workflow is easy to inspect.

## Documentation

- [Handoff Model](docs/handoff_model.md)
- [External QA Process Notes](docs/external_qa_process_notes.md)
- [Handoff Ops Demo Design](docs/handoff_ops_demo_design.md)
- [Sample Output](docs/sample_output.md)

## Known Limitations

- This is a browser prototype, not a production task tracker.
- Markdown export is client-side only.
- Bug scoring is intentionally transparent and simple.
- No Jira, Slack, Discord, internal tools, or private studio systems are connected.
- Review decisions still require human QA judgment.

## Future Improvements

- Import/export JSON handoff packets.
- Add more scenario templates for combat, UI, localization, and platform checks.
- Add optional CSV export for reviewed bug cards.
- Add accessibility checks for the demo UI.
- Add a small automated smoke test for browser interactions.
