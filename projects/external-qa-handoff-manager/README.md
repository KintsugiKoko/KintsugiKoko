# External QA Handoff Manager

## Status

Working browser prototype for external QA planning and intake review.

External QA Handoff Manager turns a feature goal into an outsource-ready test packet with scenario coverage, bug-quality standards, evidence requirements, intake review, and Markdown handoff export.

The current browser build uses fictional scenarios and local sample data. Live Jira, vendor, and studio-system adapters remain outside this prototype's current scope.

## Live Demo

[Open the External QA Handoff Manager](https://kintsugikoko.github.io/KintsugiKoko/external-qa-handoff-manager.html)

## What It Demonstrates

- QA leadership around external/offsite test coordination
- Scenario coverage by area, risk, and readiness
- Bug-quality standards for useful incoming reports
- Evidence requirements for screenshot, clip, build, and pass/fail notes
- QA lead intake review before accepting a handoff as complete
- Review-ready Markdown export for handoff documentation

## Current Sample Flow

The sample handoff focuses on a fictional Nyx Starwell offering pass:

1. Review the feature goal and operating scope.
2. Scan the scenario matrix for high-risk and needs-setup items.
3. Review bug standards and evidence requirements.
4. Generate the Markdown handoff draft.
5. Export the reviewed handoff as Markdown for team circulation or further refinement.

## Current Operating Scope

The prototype demonstrates QA coordination judgment through fictional data, local browser state, manual intake decisions, and Markdown export. Production integrations, authentication, live build validation, and vendor-specific workflows would require separate project configuration and owner review.

## Known Limitations

- The sample data is hard-coded in the browser.
- The export is Markdown only.
- There is no account system, persistence, import, or Jira connection.
- Build validation and automated checks are separate from this planning prototype.
- A real handoff would need project-specific owner review, platform/build notes, and evidence storage.

## Future Improvements

- Add editable handoff fields.
- Add import/export JSON for sample packets.
- Add a small checklist print view.
- Add sample evidence pack links.
- Add reviewer notes for accepted, blocked, or follow-up-needed handoffs.
