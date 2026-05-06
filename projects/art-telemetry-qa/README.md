# Art Telemetry QA

## Status

MVP portfolio prototype.

Art Telemetry QA is a portfolio-safe Python QA tooling prototype that turns mock Unreal-style art telemetry and asset validation data into human-reviewed Art QA findings, risk scores, and Jira-ready reports.

It demonstrates Art QA / Technical QA validation thinking: capture, parse, isolate, report, and validate-fix workflows. It uses mock data only and does not use private studio data, proprietary schemas, Unreal project files, internal telemetry, Jira, or studio tools.

This is not an Unreal plugin and does not automate Unreal. Any Unreal-facing work remains a future planning note that would need public, non-proprietary sample data and separate validation.

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

All sample data is fictional and portfolio-safe.

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
- Honest boundaries around mock data and human review

## What This Does Not Claim

- It is not a real Unreal plugin.
- It does not use private or proprietary studio data.
- It does not replace Unreal Insights, Tech Art, Performance, Engineering, or human QA judgment.
- It does not automatically file Jira tickets.
- It does not prove production readiness.

## Future Improvements

- Add configurable rule thresholds.
- Add baseline comparison between two captures.
- Add JSON export.
- Add evidence attachment references.
- Add platform-specific threshold profiles.
- Add real Unreal export support only with safe, public, non-proprietary schemas.
