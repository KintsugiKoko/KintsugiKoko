# Art Telemetry QA

## Status

Working Python QA prototype using fictional Unreal-style validation data.

Art Telemetry QA turns mock Unreal-style art telemetry and asset-validation data into structured findings, risk scores, owner-routing notes, and Jira-ready report drafts.

It demonstrates a technical QA workflow: capture, parse, isolate, report, and validate the fix. The current interface is a local Python CLI over fictional CSV and JSON fixtures, with Markdown and CSV output for reviewer inspection.

Unreal export adapters and Jira integration are separate future milestones rather than part of the current CLI.

## Portfolio Showcase

- [Art QA Telemetry Report Showcase](../../docs/art-qa-telemetry-report-showcase.md)
- [Tool Audit Report](../../docs/tool-audit-report.md)

## Why This Exists

Art QA can involve more than visual spot checks. Asset-heavy work often needs structured evidence: texture budgets, material slots, alpha/translucency risk, skeletal weighting warnings, LOD coverage, collision setup, VFX density, soak test behavior, load warnings, and naming/path hygiene.

This tool turns those signals into report drafts a human QA reviewer can inspect before filing bugs or asking Art, Tech Art, VFX, Animation, Engineering, Performance, or QA partners for follow-up.

## What It Generates

Run:

```bash
python -m art_telemetry_qa.cli scan --input samples --output reports
```

Generated files:

- `reports/art_qa_summary.md`
- `reports/art_qa_failures.csv`
- `reports/jira_ready_bugs.md`

## Inputs

The CLI expects:

- `samples/sample_art_telemetry.csv`
- `samples/sample_soak_results.json`
- `samples/sample_asset_validation.json`

All sample data is fictional and created for this project.

## Validation Rules

The MVP checks for:

- Missing material slots
- Texture size over budget
- Alpha/translucent material usage on high-density assets
- Skeletal mesh weighting warnings
- Material slot count over threshold
- Missing LODs
- Missing collision on gameplay assets
- Suspiciously large bounds
- VFX particle count over threshold
- Soak test warning spikes
- Invalid naming/path convention
- Asset load warnings

## Risk Scoring

| Severity | Points |
| --- | ---: |
| Critical | 10 |
| High | 6 |
| Medium | 3 |
| Low | 1 |

Risk points help sort the report. They are not an automatic pass/fail decision.

## Likely Owner Routing

Findings route to likely owners:

- Art
- Tech Art
- VFX
- Animation
- Engineering
- Performance
- QA

Owner routing is a draft triage aid. A human reviewer still owns final routing.

## Project Structure

```text
art-telemetry-qa/
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- art_telemetry_qa/
|       |-- __init__.py
|       |-- cli.py
|       |-- parser.py
|       |-- rules.py
|       |-- scoring.py
|       |-- report_writer.py
|       |-- jira_writer.py
|       `-- schemas.py
|-- tests/
|   |-- test_parser.py
|   |-- test_rules.py
|   |-- test_scoring.py
|   `-- test_report_writer.py
|-- samples/
|   |-- sample_art_telemetry.csv
|   |-- sample_soak_results.json
|   `-- sample_asset_validation.json
|-- reports/
|   `-- .gitkeep
`-- docs/
    |-- art_qa_validation_model.md
    |-- unreal_integration_plan.md
    `-- sample_output.md
```

## How To Run Tests

```bash
python -m pytest
```

## What This Demonstrates

- Direct Art QA / Technical QA validation thinking
- Telemetry/data parsing
- Rule-based asset validation
- Soak test interpretation
- Risk scoring
- Jira-ready reporting habits
- Clear separation between parsed signals, triage suggestions, and reviewer decisions

## Current Scope And Boundaries

- Local Python CLI using fictional CSV and JSON fixtures
- Rule-based findings, risk scoring, routing suggestions, and report drafts
- Reviewer-owned triage and fix-verification decisions
- Unreal export, live telemetry, Jira submission, and production threshold profiles remain future integrations

## Future Improvements

- Add configurable rule thresholds.
- Add baseline comparison between two captures.
- Add JSON export.
- Add evidence attachment references.
- Add platform-specific threshold profiles.
- Add real Unreal export support only with safe, public, non-proprietary schemas.
