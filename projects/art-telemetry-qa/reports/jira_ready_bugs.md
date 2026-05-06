# Jira-Ready Art QA Bug Drafts

> Draft bug language from mock telemetry. A human QA reviewer should verify repro, impact, and owner before filing.

## 1. [Critical] SM_CosmicFish_SoulForm_01 - Texture size over critical review budget

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Fish/SoulForms/SM_CosmicFish_SoulForm_01`

**Summary**

SM_CosmicFish_SoulForm_01 triggered `ART-TEX-001` during mock Art QA telemetry validation.

**Observed Result**

Texture size is 8192px, which needs immediate budget review.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Fishing_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Compare texture size, compression, mip behavior, and platform target before sign-off.

## 2. [Critical] SM_Merchant_Caravan_Wagon - Texture size over critical review budget

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ART-TEX-001` during mock Art QA telemetry validation.

**Observed Result**

Texture size is 8192px, which needs immediate budget review.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Compare texture size, compression, mip behavior, and platform target before sign-off.

## 3. [Critical] VFX_Starwell_Offering_Burst - Soak test warning spike

**Likely owner:** Performance

**Asset path:** `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`

**Summary**

VFX_Starwell_Offering_Burst triggered `SOAK-WARN-001` during mock Art QA telemetry validation.

**Observed Result**

9 warning spike(s), 17 hitch(es), 248.2 MB memory growth over 90 minutes.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Review timestamped soak evidence, streaming behavior, VFX loops, memory growth, and repeatability.

## 4. [High] SK_Nyx_Cat_Merchant_WIP - Skeletal mesh weighting warning

**Likely owner:** Animation

**Asset path:** `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`

**Summary**

SK_Nyx_Cat_Merchant_WIP triggered `ANIM-WEIGHT-001` during mock Art QA telemetry validation.

**Observed Result**

3 weighting warning(s) were captured.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Check deformation poses, vertex influence, affected bones, and animation preview coverage.

## 5. [High] SM_CosmicFish_SoulForm_01 - Alpha/translucency on high-density asset

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Fish/SoulForms/SM_CosmicFish_SoulForm_01`

**Summary**

SM_CosmicFish_SoulForm_01 triggered `ART-ALPHA-001` during mock Art QA telemetry validation.

**Observed Result**

2 translucent material(s), 44.0% alpha coverage, and 118,000 triangles were captured together.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Fishing_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Review overdraw, material setup, camera overlap, and whether a cheaper presentation is acceptable.

## 6. [High] SM_Merchant_Caravan_Wagon - Missing material slot assignment

**Likely owner:** Art

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ART-MAT-001` during mock Art QA telemetry validation.

**Observed Result**

Missing material slot(s): M_Caravan_Wood_Trim, M_Caravan_Wheel_Metal

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Open the asset in Unreal and verify slot assignment, defaults, and intended material overrides.

## 7. [High] SM_Merchant_Caravan_Wagon - Missing collision on gameplay asset

**Likely owner:** Engineering

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ENG-COLL-001` during mock Art QA telemetry validation.

**Observed Result**

Asset is marked as gameplay-facing but collision is missing.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Validate collision setup in PIE and confirm player, camera, projectile, or interaction expectations.

## 8. [High] SM_Merchant_Caravan_Wagon - Asset load warning

**Likely owner:** Performance

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `PERF-LOAD-001` during mock Art QA telemetry validation.

**Observed Result**

5 load warning(s), 4200 ms asset load time.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

## 9. [High] SM_Merchant_Caravan_Wagon - Soak test warning spike

**Likely owner:** Performance

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `SOAK-WARN-001` during mock Art QA telemetry validation.

**Observed Result**

5 warning spike(s), 10 hitch(es), 126.4 MB memory growth over 75 minutes.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Review timestamped soak evidence, streaming behavior, VFX loops, memory growth, and repeatability.

## 10. [High] T_MissingSlot_DebugMesh - Missing material slot assignment

**Likely owner:** Art

**Asset path:** `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`

**Summary**

T_MissingSlot_DebugMesh triggered `ART-MAT-001` during mock Art QA telemetry validation.

**Observed Result**

Missing material slot(s): M_Debug_Default

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Open the asset in Unreal and verify slot assignment, defaults, and intended material overrides.

## 11. [High] VFX_Starwell_Offering_Burst - Asset load warning

**Likely owner:** Performance

**Asset path:** `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`

**Summary**

VFX_Starwell_Offering_Burst triggered `PERF-LOAD-001` during mock Art QA telemetry validation.

**Observed Result**

4 load warning(s), 3100 ms asset load time.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

## 12. [High] VFX_Starwell_Offering_Burst - VFX particle count over threshold

**Likely owner:** VFX

**Asset path:** `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`

**Summary**

VFX_Starwell_Offering_Burst triggered `VFX-PART-001` during mock Art QA telemetry validation.

**Observed Result**

Particle count is 4200, above the review threshold of 2000.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Review spawn rate, lifetime, LOD behavior, and expected camera density.

## 13. [Medium] SK_Nyx_Cat_Merchant_WIP - Missing or insufficient LODs

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`

**Summary**

SK_Nyx_Cat_Merchant_WIP triggered `ART-LOD-001` during mock Art QA telemetry validation.

**Observed Result**

LOD count is 1.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Verify imported LODs, screen-size transitions, and expected viewing distance.

## 14. [Medium] SK_Nyx_Cat_Merchant_WIP - Material slot count over threshold

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`

**Summary**

SK_Nyx_Cat_Merchant_WIP triggered `ART-MAT-002` during mock Art QA telemetry validation.

**Observed Result**

Material slot count is 8, above the review threshold of 6.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Check whether material consolidation can reduce draw-call and maintenance risk.

## 15. [Medium] SK_Nyx_Cat_Merchant_WIP - Asset load warning

**Likely owner:** Performance

**Asset path:** `/Game/Nyx/Characters/Nyx/SK_Nyx_Cat_Merchant_WIP`

**Summary**

SK_Nyx_Cat_Merchant_WIP triggered `PERF-LOAD-001` during mock Art QA telemetry validation.

**Observed Result**

1 load warning(s), 1780 ms asset load time.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Skeletal Mesh captured on Windows in Map_Merchant_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Compare warm/cold load captures and check whether streaming or asset dependency cost changed.

## 16. [Medium] SM_Merchant_Caravan_Wagon - Suspiciously large bounds

**Likely owner:** QA

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ART-BOUNDS-001` during mock Art QA telemetry validation.

**Observed Result**

Bounds extent is 62.0m.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Validate pivot, bounds setup, culling behavior, collision, and map placement.

## 17. [Medium] SM_Merchant_Caravan_Wagon - Missing or insufficient LODs

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ART-LOD-001` during mock Art QA telemetry validation.

**Observed Result**

LOD count is 0.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Verify imported LODs, screen-size transitions, and expected viewing distance.

## 18. [Medium] SM_Merchant_Caravan_Wagon - Material slot count over threshold

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `ART-MAT-002` during mock Art QA telemetry validation.

**Observed Result**

Material slot count is 10, above the review threshold of 6.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Check whether material consolidation can reduce draw-call and maintenance risk.

## 19. [Medium] T_MissingSlot_DebugMesh - Missing or insufficient LODs

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`

**Summary**

T_MissingSlot_DebugMesh triggered `ART-LOD-001` during mock Art QA telemetry validation.

**Observed Result**

LOD count is 0.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Verify imported LODs, screen-size transitions, and expected viewing distance.

## 20. [Medium] VFX_Starwell_Offering_Burst - Missing or insufficient LODs

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`

**Summary**

VFX_Starwell_Offering_Burst triggered `ART-LOD-001` during mock Art QA telemetry validation.

**Observed Result**

LOD count is 1.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Verify imported LODs, screen-size transitions, and expected viewing distance.

## 21. [Medium] VFX_Starwell_Offering_Burst - Material slot count over threshold

**Likely owner:** Tech Art

**Asset path:** `/Game/Nyx/VFX/Starwell/VFX_Starwell_Offering_Burst`

**Summary**

VFX_Starwell_Offering_Burst triggered `ART-MAT-002` during mock Art QA telemetry validation.

**Observed Result**

Material slot count is 9, above the review threshold of 6.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- VFX captured on Windows in Map_Starwell_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Check whether material consolidation can reduce draw-call and maintenance risk.

## 22. [Low] SM_Merchant_Caravan_Wagon - Invalid naming or path convention

**Likely owner:** QA

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `QA-NAME-001` during mock Art QA telemetry validation.

**Observed Result**

Naming valid: False; path valid: False.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Confirm naming and folder rules before content review or bug handoff.

## 23. [Low] SM_Merchant_Caravan_Wagon - Validation naming/path warning

**Likely owner:** QA

**Asset path:** `/Game/Nyx/Vehicles/Caravan/SM_Merchant_Caravan_Wagon`

**Summary**

SM_Merchant_Caravan_Wagon triggered `QA-NAME-002` during mock Art QA telemetry validation.

**Observed Result**

Asset suffix does not match current vehicle naming convention.; Vehicle asset lives outside the current gameplay transport folder.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Route_Test from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Clean up naming/path convention before filing higher-cost technical issues.

## 24. [Low] T_MissingSlot_DebugMesh - Invalid naming or path convention

**Likely owner:** QA

**Asset path:** `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`

**Summary**

T_MissingSlot_DebugMesh triggered `QA-NAME-001` during mock Art QA telemetry validation.

**Observed Result**

Naming valid: False; path valid: False.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Confirm naming and folder rules before content review or bug handoff.

## 25. [Low] T_MissingSlot_DebugMesh - Validation naming/path warning

**Likely owner:** QA

**Asset path:** `/Game/Nyx/Temp/T_MissingSlot_DebugMesh`

**Summary**

T_MissingSlot_DebugMesh triggered `QA-NAME-002` during mock Art QA telemetry validation.

**Observed Result**

Temporary prefix is not valid for content review.; Temp folder should not be used for reviewed content.

**Expected Result**

Asset should meet the agreed visual, technical, naming, collision, loading, and performance expectations for its role.

**Evidence To Attach / Verify**

- Static Mesh captured on Windows in Map_Debug_ArtQA from build Nyx-WIP-0.4.
- Screenshot or capture from the reviewed map, if available.
- Repeat capture after the suspected fix, if this becomes a filed issue.

**Suggested Validation**

Clean up naming/path convention before filing higher-cost technical issues.
