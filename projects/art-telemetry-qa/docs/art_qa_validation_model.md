# Art QA Validation Model

This project models a portfolio-safe Art QA / Technical QA workflow:

1. Capture mock Unreal-style art telemetry.
2. Parse the capture data into consistent records.
3. Evaluate focused validation rules.
4. Score risk by severity.
5. Route likely ownership.
6. Generate Markdown and CSV reports for human review.

## Input Types

- `sample_art_telemetry.csv`: asset-level telemetry signals such as texture size, material slots, triangle count, alpha coverage, particle count, bounds, naming/path validity, and load warnings.
- `sample_soak_results.json`: longer-running soak signals such as warning spikes, hitch count, memory growth, and frame timings.
- `sample_asset_validation.json`: validation observations such as missing material slots, missing collision, LOD count, skeletal weighting warnings, and naming/path warnings.

## Validation Areas

The MVP rules cover:

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

Risk score is a triage helper. It is not a universal budget, automatic failure, or substitute for human QA/Tech Art review.

## Owner Routing

Findings are routed to likely owners:

- Art
- Tech Art
- VFX
- Animation
- Engineering
- Performance
- QA

Owner routing is intentionally conservative. It helps start the conversation; it does not decide final assignment.

## Portfolio Boundary

This model uses mock data only. It does not use private studio data, proprietary schemas, Unreal project files, Jira, internal dashboards, or real telemetry captures.
