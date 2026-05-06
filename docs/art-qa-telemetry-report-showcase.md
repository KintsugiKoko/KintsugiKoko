# Art QA Telemetry Report Showcase

This showcase explains the Art Telemetry QA tool as portfolio-safe Art QA / Technical QA evidence work.

The data is fictional. It is mock Unreal-style asset telemetry and sample validation data. It does not use private studio data, internal telemetry, proprietary schemas, or live Unreal Engine automation.

## What The Tool Demonstrates

The MVP demonstrates a practical QA reporting loop:

1. Capture mock asset and soak-test data.
2. Parse structured CSV and JSON inputs.
3. Evaluate asset risk rules.
4. Assign simple severity and risk points.
5. Route likely owners for review.
6. Generate readable QA reports and Jira-ready bug drafts.
7. Keep human QA judgment in the loop before filing or escalating.

## Mock Inputs

The sample flow uses:

- `projects/art-telemetry-qa/samples/sample_art_telemetry.csv`
- `projects/art-telemetry-qa/samples/sample_soak_results.json`
- `projects/art-telemetry-qa/samples/sample_asset_validation.json`

Sample asset areas include:

- Starwell blockout
- Nyx cat merchant skeletal mesh
- Starwell offering VFX
- Soul-form fish material risk
- Merchant caravan vehicle asset
- Debug asset naming/path example

## Parsing Summary

Current generated sample output:

| Metric | Result |
| --- | ---: |
| Assets scanned | 6 |
| Findings generated | 25 |
| Total risk points | 115 |
| Output formats | Markdown summary, CSV failures, Jira-ready bug drafts |

## Severity Snapshot

| Severity | Count |
| --- | ---: |
| Critical | 3 |
| High | 9 |
| Medium | 9 |
| Low | 4 |

## Likely Owner Routing

| Likely Owner | Count |
| --- | ---: |
| Tech Art | 10 |
| Performance | 5 |
| QA | 5 |
| Art | 2 |
| Animation | 1 |
| VFX | 1 |
| Engineering | 1 |

Owner routing is a starting point for triage, not a final assignment. A human QA reviewer should verify repro, expected behavior, asset ownership, and player impact before filing bugs.

## Validation Checks Covered

The current MVP includes checks for:

- alpha/translucency risk on high-density assets
- material slot count over threshold
- missing material slots
- texture budget warnings
- missing or insufficient LODs
- missing collision on gameplay-facing assets
- skeletal mesh weighting warnings
- VFX particle count over threshold
- suspiciously large bounds
- soak-test warning spikes
- asset load warnings
- suspicious naming/path conventions

## Jira-Ready Example

Example generated bug draft:

```text
[Critical] VFX_Starwell_Offering_Burst - Soak test warning spike

Likely owner: Performance
Asset path: /Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst

Observed Result:
9 warning spikes, 17 hitches, and 248.2 MB memory growth over 90 minutes.

Expected Result:
Asset should meet agreed visual, technical, loading, and performance expectations for its role.

Evidence To Attach / Verify:
- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.
```

## Human-Reviewed Validation Notes

This tool helps organize evidence, but it does not replace Art, Tech Art, VFX, Animation, Engineering, Performance, or QA review.

Before filing a real issue, a QA reviewer would still check:

- whether the asset belongs in the reviewed map or scenario
- whether the threshold is correct for the asset type and platform target
- whether the issue reproduces after a clean load or repeat capture
- whether there is a player-facing impact
- whether screenshots, video, logs, or capture files are needed
- whether a fix should be verified through smoke, regression, or soak coverage

## Portfolio Boundary

This is a Python QA tooling MVP. It is not production-ready, not integrated with Unreal Engine, not connected to Jira, and not based on real studio telemetry. Its value is showing Art QA / Technical QA thinking: capture, parse, isolate, risk-rank, report, and verify with human judgment.

