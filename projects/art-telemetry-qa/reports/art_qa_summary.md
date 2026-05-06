# Art QA Telemetry Summary

> Portfolio-safe report generated from mock Unreal-style telemetry and validation data.

## Executive Summary

- Assets scanned: **6**
- Findings generated: **25**
- Total risk points: **115**
- This report supports human Art QA / Technical QA review; it is not final Tech Art, Performance, or Engineering sign-off.

## Risk By Asset

| Asset | Risk Points |
| --- | ---: |
| SM_Merchant_Caravan_Wagon | 45 |
| VFX_Starwell_Offering_Burst | 28 |
| SM_CosmicFish_SoulForm_01 | 16 |
| SK_Nyx_Cat_Merchant_WIP | 15 |
| T_MissingSlot_DebugMesh | 11 |

## Severity Counts

| Severity | Count |
| --- | ---: |
| Medium | 9 |
| High | 9 |
| Critical | 3 |
| Low | 4 |

## Likely Owner Routing

| Owner | Count |
| --- | ---: |
| Tech Art | 10 |
| Performance | 5 |
| Animation | 1 |
| VFX | 1 |
| QA | 5 |
| Art | 2 |
| Engineering | 1 |

## Findings

### Critical: SM_CosmicFish_SoulForm_01 - Texture size over critical review budget

- Rule: `ART-TEX-001`
- Likely owner: Tech Art
- Risk points: 10
- Asset path: `/Game/Nyx/Fish/SoulForms/SM_CosmicFish_SoulForm_01`
- Finding: Texture size is 8192px, which needs immediate budget review.
- Evidence: Static Mesh captured on Windows in Map_Fishing_Test from build Nyx-WIP-0.4.
- Suggested validation: Compare texture size, compression, mip behavior, and platform target before sign-off.

### Critical: SM_Merchant_Caravan_Wagon - Texture size over critical review budget

- Rule: `ART-TEX-001`
- Likely owner: Tech Art
- Risk points: 10
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Texture size is 8192px, which needs immediate budget review.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Compare texture size, compression, mip behavior, and platform target before sign-off.

### Critical: VFX_Starwell_Offering_Burst - Soak test warning spike

- Rule: `SOAK-WARN-001`
- Likely owner: Performance
- Risk points: 10
- Asset path: `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`
- Finding: 9 warning spike(s), 17 hitch(es), 248.2 MB memory growth over 90 minutes.
- Evidence: VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Suggested validation: Review timestamped soak evidence, streaming behavior, VFX loops, memory growth, and repeatability.

### High: SK_Nyx_Cat_Merchant_WIP - Skeletal mesh weighting warning

- Rule: `ANIM-WEIGHT-001`
- Likely owner: Animation
- Risk points: 6
- Asset path: `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`
- Finding: 3 weighting warning(s) were captured.
- Evidence: Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Suggested validation: Check deformation poses, vertex influence, affected bones, and animation preview coverage.

### High: SM_CosmicFish_SoulForm_01 - Alpha/translucency on high-density asset

- Rule: `ART-ALPHA-001`
- Likely owner: Tech Art
- Risk points: 6
- Asset path: `/Game/Nyx/Fish/SoulForms/SM_CosmicFish_SoulForm_01`
- Finding: 2 translucent material(s), 44.0% alpha coverage, and 118,000 triangles were captured together.
- Evidence: Static Mesh captured on Windows in Map_Fishing_Test from build Nyx-WIP-0.4.
- Suggested validation: Review overdraw, material setup, camera overlap, and whether a cheaper presentation is acceptable.

### High: SM_Merchant_Caravan_Wagon - Missing material slot assignment

- Rule: `ART-MAT-001`
- Likely owner: Art
- Risk points: 6
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Missing material slot(s): M_Caravan_Wood_Trim, M_Caravan_Wheel_Metal
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Open the asset in Unreal and verify slot assignment, defaults, and intended material overrides.

### High: SM_Merchant_Caravan_Wagon - Missing collision on gameplay asset

- Rule: `ENG-COLL-001`
- Likely owner: Engineering
- Risk points: 6
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Asset is marked as gameplay-facing but collision is missing.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Validate collision setup in PIE and confirm player, camera, projectile, or interaction expectations.

### High: SM_Merchant_Caravan_Wagon - Asset load warning

- Rule: `PERF-LOAD-001`
- Likely owner: Performance
- Risk points: 6
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: 5 load warning(s), 4200 ms asset load time.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

### High: SM_Merchant_Caravan_Wagon - Soak test warning spike

- Rule: `SOAK-WARN-001`
- Likely owner: Performance
- Risk points: 6
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: 5 warning spike(s), 10 hitch(es), 126.4 MB memory growth over 75 minutes.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Review timestamped soak evidence, streaming behavior, VFX loops, memory growth, and repeatability.

### High: T_MissingSlot_DebugMesh - Missing material slot assignment

- Rule: `ART-MAT-001`
- Likely owner: Art
- Risk points: 6
- Asset path: `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`
- Finding: Missing material slot(s): M_Debug_Default
- Evidence: Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Suggested validation: Open the asset in Unreal and verify slot assignment, defaults, and intended material overrides.

### High: VFX_Starwell_Offering_Burst - Asset load warning

- Rule: `PERF-LOAD-001`
- Likely owner: Performance
- Risk points: 6
- Asset path: `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`
- Finding: 4 load warning(s), 3100 ms asset load time.
- Evidence: VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Suggested validation: Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

### High: VFX_Starwell_Offering_Burst - VFX particle count over threshold

- Rule: `VFX-PART-001`
- Likely owner: VFX
- Risk points: 6
- Asset path: `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`
- Finding: Particle count is 4200, above the review threshold of 2000.
- Evidence: VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Suggested validation: Review spawn rate, lifetime, LOD behavior, and expected camera density.

### Medium: SK_Nyx_Cat_Merchant_WIP - Missing or insufficient LODs

- Rule: `ART-LOD-001`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`
- Finding: LOD count is 1.
- Evidence: Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Suggested validation: Verify imported LODs, screen-size transitions, and expected viewing distance.

### Medium: SK_Nyx_Cat_Merchant_WIP - Material slot count over threshold

- Rule: `ART-MAT-002`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`
- Finding: Material slot count is 8, above the review threshold of 6.
- Evidence: Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Suggested validation: Check whether material consolidation can reduce draw-call and maintenance risk.

### Medium: SK_Nyx_Cat_Merchant_WIP - Asset load warning

- Rule: `PERF-LOAD-001`
- Likely owner: Performance
- Risk points: 3
- Asset path: `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`
- Finding: 1 load warning(s), 1780 ms asset load time.
- Evidence: Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Suggested validation: Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

### Medium: SM_Merchant_Caravan_Wagon - Suspiciously large bounds

- Rule: `ART-BOUNDS-001`
- Likely owner: QA
- Risk points: 3
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Bounds extent is 62.0m.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Validate pivot, bounds setup, culling behavior, collision, and map placement.

### Medium: SM_Merchant_Caravan_Wagon - Missing or insufficient LODs

- Rule: `ART-LOD-001`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: LOD count is 0.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Verify imported LODs, screen-size transitions, and expected viewing distance.

### Medium: SM_Merchant_Caravan_Wagon - Material slot count over threshold

- Rule: `ART-MAT-002`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Material slot count is 10, above the review threshold of 6.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Check whether material consolidation can reduce draw-call and maintenance risk.

### Medium: T_MissingSlot_DebugMesh - Missing or insufficient LODs

- Rule: `ART-LOD-001`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`
- Finding: LOD count is 0.
- Evidence: Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Suggested validation: Verify imported LODs, screen-size transitions, and expected viewing distance.

### Medium: VFX_Starwell_Offering_Burst - Missing or insufficient LODs

- Rule: `ART-LOD-001`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`
- Finding: LOD count is 1.
- Evidence: VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Suggested validation: Verify imported LODs, screen-size transitions, and expected viewing distance.

### Medium: VFX_Starwell_Offering_Burst - Material slot count over threshold

- Rule: `ART-MAT-002`
- Likely owner: Tech Art
- Risk points: 3
- Asset path: `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`
- Finding: Material slot count is 9, above the review threshold of 6.
- Evidence: VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Suggested validation: Check whether material consolidation can reduce draw-call and maintenance risk.

### Low: SM_Merchant_Caravan_Wagon - Invalid naming or path convention

- Rule: `QA-NAME-001`
- Likely owner: QA
- Risk points: 1
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Naming valid: False; path valid: False.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Confirm naming and folder rules before content review or bug handoff.

### Low: SM_Merchant_Caravan_Wagon - Validation naming/path warning

- Rule: `QA-NAME-002`
- Likely owner: QA
- Risk points: 1
- Asset path: `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`
- Finding: Asset suffix does not match current vehicle naming convention.; Vehicle asset lives outside the current gameplay transport folder.
- Evidence: Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Suggested validation: Clean up naming/path convention before filing higher-cost technical issues.

### Low: T_MissingSlot_DebugMesh - Invalid naming or path convention

- Rule: `QA-NAME-001`
- Likely owner: QA
- Risk points: 1
- Asset path: `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`
- Finding: Naming valid: False; path valid: False.
- Evidence: Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Suggested validation: Confirm naming and folder rules before content review or bug handoff.

### Low: T_MissingSlot_DebugMesh - Validation naming/path warning

- Rule: `QA-NAME-002`
- Likely owner: QA
- Risk points: 1
- Asset path: `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`
- Finding: Temporary prefix is not valid for content review.; Temp folder should not be used for reviewed content.
- Evidence: Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Suggested validation: Clean up naming/path convention before filing higher-cost technical issues.


## Method / Limitations

- Uses mock Unreal-style data only.
- Does not use private studio data, proprietary schemas, internal telemetry, Jira, or Unreal project files.
- Thresholds are simple review triggers, not universal asset budgets.
- Findings are meant to support capture, parse, isolate, report, and validate-fix workflows.
- Human review is required before filing bugs or requesting cross-discipline follow-up.
