# QA Portfolio Auditor Local Artifact Check

> Local filesystem check for portfolio-safe sample metadata. This does not crawl the live site, validate deployment health, connect to Jira, connect to Unreal, or replace manual review.

## Summary

- Artifacts checked: 15
- Present: 15
- Missing: 0
- Metadata mismatches: 0

## Results

### QA Bug Report Tool - README
- Type: documentation
- Path: projects/qa-bug-report-tool/README.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep README linked from the portfolio path.

### QA Bug Report Tool - Sample note data
- Type: sample-data
- Path: projects/qa-bug-report-tool/sample-data/001-inventory-count-note.txt
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep sample data fictional and portfolio-safe.

### QA Bug Report Tool - Generated Markdown report
- Type: sample-output
- Path: projects/qa-bug-report-tool/reports/001-inventory-count.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Re-run sample conversion after behavior changes.

### Nyx Test Planner - Planner page
- Type: demo
- Path: docs/nyx-test-planner.html
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep linked from the homepage project card.

### Nyx Test Planner - Planner README
- Type: documentation
- Path: projects/nyx-test-planner/README.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep limitations clear around manual PIE validation.

### Nyx Test Planner - Case study
- Type: case-study
- Path: docs/nyx-test-planner-case-study.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep result marked pending until manual PIE validation is run.

### Art Telemetry QA - README
- Type: documentation
- Path: projects/art-telemetry-qa/README.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep Unreal/plugin boundary language visible.

### Art Telemetry QA - Mock telemetry sample
- Type: sample-data
- Path: projects/art-telemetry-qa/samples/sample_art_telemetry.csv
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep sample data fictional and public.

### Art Telemetry QA - Report showcase
- Type: sample-output
- Path: docs/art-qa-telemetry-report-showcase.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep the showcase framed as mock Unreal-style telemetry.

### Community Pulse - README
- Type: documentation
- Path: projects/community-pulse-report-tool/README.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep mock/sample feedback boundary visible.

### Community Pulse - Sample feedback CSV
- Type: sample-data
- Path: projects/community-pulse-report-tool/sample-data/weekly-feedback-sample.csv
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep all feedback fictional.

### Community Pulse - Weekly sentiment report
- Type: sample-output
- Path: projects/community-pulse-report-tool/reports/weekly-sentiment-report.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Refresh sample output after report format changes.

### External QA Handoff Manager - Browser prototype page
- Type: demo
- Path: docs/external-qa-handoff-manager.html
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep the no-Jira/no-vendor-integration note visible.

### External QA Handoff Manager - Project README
- Type: documentation
- Path: projects/external-qa-handoff-manager/README.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep static MVP limitations clear.

### External QA Handoff Manager - Saved sample handoff export
- Type: sample-output
- Path: projects/external-qa-handoff-manager/reports/sample_handoff_packet.md
- Metadata status: Present
- Local filesystem status: Present
- Status matches metadata: Yes
- Recommended action: Keep the saved export aligned with the browser-generated Markdown sample.

## Limitations

- Checks local repository paths only.
- Does not crawl the live site.
- Does not validate external deployment health.
- Does not inspect the quality or accuracy of the artifact content.
- Human review is still required before publishing.
