# External QA Handoff Manager

## Status

First working browser prototype for portfolio review.

External QA Handoff Manager demonstrates how a QA lead can turn a feature goal into an outsource-ready test packet with scenario coverage, bug-quality standards, evidence requirements, intake review, and Markdown handoff export.

It uses mock data only. It does not connect to Jira, vendor portals, private studio workflows, internal test plans, outsourcing systems, or live production data.

## Live Demo

[Open the External QA Handoff Manager](https://kintsugikoko.github.io/KintsugiKoko/external-qa-handoff-manager.html)

## What It Demonstrates

- QA leadership around external/offsite test coordination
- Scenario coverage by area, risk, and readiness
- Bug-quality standards for useful incoming reports
- Evidence requirements for screenshot, clip, build, and pass/fail notes
- QA lead intake review before accepting a handoff as complete
- Human-reviewed Markdown export for portfolio-safe documentation

## Current Sample Flow

The sample handoff focuses on a fictional Nyx Starwell offering pass:

1. Review the feature goal and portfolio-safe boundary.
2. Scan the scenario matrix for high-risk and needs-setup items.
3. Review bug standards and evidence requirements.
4. Generate the Markdown handoff draft.
5. Treat the output as a human-reviewed planning artifact, not a live Jira or vendor-system export.

## Portfolio-Safe Boundary

This project is meant to show QA coordination judgment. It does not claim:

- Real studio data
- Live vendor integration
- Jira automation
- Private outsourcing workflows
- Production pipeline ownership
- Automated Unreal or engine validation

## Known Limitations

- The sample data is hard-coded in the browser.
- The export is Markdown only.
- There is no account system, persistence, import, or Jira connection.
- It does not validate a real build or run automated checks.
- A real handoff would need project-specific owner review, platform/build notes, and evidence storage.

## Future Improvements

- Add editable handoff fields.
- Add import/export JSON for sample packets.
- Add a small checklist print view.
- Add sample evidence pack links.
- Add reviewer notes for accepted, blocked, or follow-up-needed handoffs.
