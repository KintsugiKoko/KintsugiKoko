# Unreal Test Levels And Scenarios

This document is a recruiter-readable QA planning showcase for Unreal-style validation work. It describes test level patterns and scenarios that support Art QA / Technical QA judgment.

It is portfolio-safe documentation. It does not claim that this repository contains an Unreal Engine plugin, automated Unreal test runner, private studio tooling, or live telemetry integration.

## Test Level Types

## Asset Validation Level

Purpose: review imported assets in a controlled map before they are trusted in gameplay spaces.

Scenario setup:

- Place representative static meshes, skeletal meshes, materials, and VFX in a clean validation map.
- Use consistent lighting, camera angles, and scale references.
- Include known-good baseline assets beside WIP assets.

What QA observes:

- missing materials
- wrong scale or pivot
- broken normals or bounds
- missing LODs
- collision expectations
- naming/path hygiene

Telemetry/evidence captured:

- screenshots or capture clips
- asset path and map name
- material slot count
- texture size
- LOD count
- load warnings

Risk categories:

- visual defect
- performance risk
- collision/gameplay risk
- content organization risk

Likely owner routing: Art, Tech Art, Engineering, Performance, QA.

Pass/fail examples:

- Pass: asset has expected materials, LODs, collision, naming, and no load warnings.
- Fail: gameplay-facing prop has missing collision, missing LODs, or invalid material slots.

## Equipment Swap / Cosmetic Validation Level

Purpose: check equipment-facing content across repeated swaps, character states, and presentation contexts.

Scenario setup:

- Spawn a test character or mannequin with common equipment slots.
- Cycle weapons, armor, MTX cosmetics, dye/material variants, and attachment points.
- Include idle, movement, and preview poses when available.

What QA observes:

- clipping
- missing meshes or materials
- incorrect socket attachment
- VFX mismatch
- material override issues
- equipment state not clearing after swaps

Telemetry/evidence captured:

- item ID or asset path
- slot name
- material variant
- screenshot/video
- repro order
- load warnings or missing reference warnings

Risk categories:

- player-facing visual defect
- monetization/cosmetic risk
- regression risk
- data setup risk

Likely owner routing: Art, Tech Art, Animation, VFX, Engineering, QA.

Pass/fail examples:

- Pass: cosmetic swaps cleanly with expected materials, scale, sockets, and no lingering VFX.
- Fail: weapon VFX remains after unequip or armor material reverts to default after a preview swap.

## Mount / Vehicle Spawn Stress Level

Purpose: validate repeated mount or vehicle spawning under controlled stress.

Scenario setup:

- Spawn multiple mount or vehicle assets in a dedicated route or test pad.
- Repeat spawn/despawn, mount/dismount, camera movement, and nearby player movement.
- Include collision and pathing checks when relevant.

What QA observes:

- missing collision
- bad bounds
- load hitching
- animation or socket issues
- material streaming problems
- spawn cleanup failures

Telemetry/evidence captured:

- spawn count
- asset path
- map name
- load time
- warning spikes
- memory growth
- screenshots/video of failures

Risk categories:

- performance risk
- gameplay collision risk
- content streaming risk
- regression risk

Likely owner routing: Engineering, Performance, Art, Tech Art, Animation, QA.

Pass/fail examples:

- Pass: repeated spawns stay stable with expected collision and no warning spike pattern.
- Fail: a vehicle asset loads slowly, lacks collision, or produces repeat warning spikes during route testing.

## VFX Soak Test Level

Purpose: check visual effects over time for warning spikes, hitching, memory growth, and readability.

Scenario setup:

- Place VFX loops in a controlled map.
- Run the scene for a fixed duration.
- Vary camera distance, overlapping effects, and trigger frequency.

What QA observes:

- particle density
- readability
- hitching
- warning spikes
- memory growth
- loop cleanup

Telemetry/evidence captured:

- duration
- warning spike count
- hitch count
- memory growth
- average and p95 frame timing
- screenshots/video at repeat points

Risk categories:

- performance risk
- visual readability risk
- regression risk
- accessibility/readability risk

Likely owner routing: VFX, Tech Art, Performance, Engineering, QA.

Pass/fail examples:

- Pass: VFX remains readable and stable for the soak duration with no repeat warning pattern.
- Fail: repeated offering burst VFX produces warning spikes, hitches, and memory growth.

## Material / Alpha Risk Review Level

Purpose: review translucent, alpha-heavy, or material-slot-heavy assets in predictable camera and lighting conditions.

Scenario setup:

- Place high-risk materials near baseline opaque materials.
- Test camera overlap, movement, bright/dark lighting, and dense asset clusters.
- Include simple platform or quality-setting comparisons when available.

What QA observes:

- overdraw risk
- material flicker
- alpha sorting issues
- unreadable silhouettes
- too many material slots
- texture budget concerns

Telemetry/evidence captured:

- translucent material count
- alpha coverage percentage
- triangle count
- texture size
- material slot count
- screenshot comparisons

Risk categories:

- graphical defect
- performance risk
- readability risk
- content budget risk

Likely owner routing: Tech Art, Art, Performance, QA.

Pass/fail examples:

- Pass: alpha-heavy material stays readable and within budget in expected camera ranges.
- Fail: high-density soul-form fish uses large textures and high alpha coverage in a way that needs budget review.

## Performance Smoke Test Level

Purpose: provide a fast, repeatable pass that catches obvious performance or load regressions before deeper testing.

Scenario setup:

- Load key test maps from a clean start.
- Trigger representative asset groups, VFX, equipment swaps, and movement routes.
- Repeat the same steps after suspected fixes.

What QA observes:

- load warnings
- hitches
- memory growth
- visual pop-in
- obvious regression compared with baseline

Telemetry/evidence captured:

- build/config/platform
- map name
- route or scenario name
- load timing
- warning count
- before/after notes

Risk categories:

- build risk
- content streaming risk
- regression risk
- release readiness risk

Likely owner routing: Performance, Engineering, Tech Art, QA.

Pass/fail examples:

- Pass: key route loads and runs within expected baseline range.
- Fail: new asset group introduces repeat load warnings or visible hitching on the smoke route.

## Regression Replay Level

Purpose: replay known bug scenarios after fixes to verify the problem is resolved without creating nearby regressions.

Scenario setup:

- Keep a small library of known repro paths.
- Include setup data, expected behavior, actual historical failure, and validation evidence needed.
- Re-run the same steps after fixes and before release checkpoints.

What QA observes:

- original bug no longer reproduces
- nearby systems still behave correctly
- no new visual, content, or performance issue appears
- evidence is clear enough for closure notes

Telemetry/evidence captured:

- bug ID or report link
- repro steps
- build before/after
- screenshots/video
- telemetry notes
- fix-verification result

Risk categories:

- regression risk
- player-impact risk
- release readiness risk
- communication risk

Likely owner routing: QA, Engineering, Art, Tech Art, Performance, Design.

Pass/fail examples:

- Pass: original issue no longer reproduces and related smoke checks remain clean.
- Fail: fix removes one visual bug but creates a new missing material, collision, or presentation issue.

