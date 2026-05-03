# Unreal Project Showcase: Nyx

## Overview

Nyx is a work-in-progress Unreal C++ cozy cosmic fishing prototype starring a tuxedo-pattern cat. I am using it to practice game systems documentation, playtesting habits, and technical QA thinking.

The core loop is built around catching celestial fish, offering them to a Starwell, earning resources, unlocking thresholds, and saving persistent progress over time.

The goal of this page is to document the project as it develops: what I am practicing, what changes, what breaks, what I test, and what I learn from the process. It is not a finished game page, a shipped title, or a polished engineering portfolio.

Some details may stay general until they are safe and useful to share. I want this showcase to be honest, readable, and connected to real work instead of pretending the project is farther along than it is.

## Current Status

Status: Work in progress

Current focus:

- Organizing Unreal project notes around actual systems instead of only a broad idea
- Documenting small C++ and Unreal gameplay systems in clear, recruiter-readable language
- Connecting implementation notes to QA checks, edge cases, and player-facing risk
- Capturing screenshots or clips when they are ready and useful to share
- Writing QA and playtest notes as issues appear

## Project Areas Being Documented

These are the current areas I want to document as the project develops. Names and scope may change as the prototype changes.

| Area | What I am practicing | QA questions to ask |
| --- | --- | --- |
| Project structure | Keeping Unreal source notes organized around `Source/Nyx` and related gameplay systems | Can another person understand what each system is responsible for? |
| Fishing component | Documenting a focused gameplay feature with inputs, feedback, and result states | What happens when the action fails, repeats quickly, or receives unexpected input? |
| `AStarwell` / Starwell threshold notes | Tracking Starwell progression and unlock logic clearly | Are unlocks saved with stable IDs instead of fragile labels, ordering, or temporary names? |
| Economy component | Thinking through resources, costs, rewards, and balance-facing data | Are values readable, testable, and easy to validate after changes? |
| Deck component | Documenting a rules-based or collection-style system | Are card/deck states clear, recoverable, and testable? |
| SaveGame notes | Recording persistence behavior and save/load expectations | What data should persist, what should reset, and how can regressions be checked? |
| Validation helpers | Building notes around small checks that support reliability | What can be verified quickly before deeper playtesting? |
| PIE validation | Using Play in Editor sessions to check behavior while iterating | What should be tested every time a system changes? |

## Fishing Component System Note

`UFishingComponent` is the current C++ system note I want to explain first because it sits at the front of the Nyx gameplay loop. Its purpose is to manage the fishing interaction: starting a cast, selecting a fish, waiting for a bite, reeling, completing or failing a catch, recording catch progress, and optionally offering the completed catch to the Starwell.

This is still work-in-progress prototype documentation. The component is being presented as a focused gameplay system, not as finished player-facing fishing gameplay.

### Current Scope

The component currently represents the main fishing flow and related state:

- available fish definitions
- deterministic cast selection through seed and cast index
- active fishing state
- selected fish for the current cast
- bite timing
- reel tension
- catch completion and failure
- durable fishing progress such as discovered fish and catch counts
- Blueprint-facing events for presentation layers
- optional reward routing to `AStarwell` and economy systems

### Basic State Flow

The basic flow I am documenting is:

```text
Idle -> Casting -> FishBiting -> Reeling -> CatchComplete
```

There is also a failure path:

```text
Casting / FishBiting / Reeling -> CatchFailed
```

When loading saved progress, active runtime fishing state should return to `Idle` instead of trying to restore a half-finished cast.

### What This Component Should Own

`UFishingComponent` should own the gameplay rules directly tied to the fishing interaction:

- whether a cast can start
- which fish is selected for a cast
- when a bite occurs
- whether the player can start reeling
- how tension changes during the prototype loop
- when a catch resolves
- when catch progress is recorded
- when fishing state changes should notify Blueprint

Keeping those responsibilities together makes the system easier to reason about during testing.

### What Should Stay Outside It

The fishing component should not try to own the entire game.

Other systems should stay responsible for their own areas:

- `AStarwell` should own offering progress, threshold checks, and Starwell unlock state.
- Economy systems should own resources, costs, and rewards.
- UI, VFX, audio, and animation should respond through Blueprint events instead of being hard-coded into the component.
- Long-term save/load coordination should stay in save helpers instead of depending on live Actor state.
- Final content tuning and presentation should remain separate from the core C++ rules.

This separation is part of what I am practicing: keeping one gameplay component focused while still letting it connect to the rest of the loop.

### QA Questions

Useful questions for testing this component:

- Can a cast start only when the fishing state allows it?
- What happens if the player tries to reel before a bite?
- Does a completed catch resolve once instead of duplicating rewards or progress?
- Does a failed catch clear temporary state safely?
- Does save/load preserve durable progress while returning active casts to `Idle`?
- Do Blueprint-facing events give presentation layers enough information without owning gameplay rules?
- Can debug tooling exercise the happy path and obvious failure paths in PIE?

### Known Limits

This note does not claim final fishing gameplay. The current documentation focuses on system boundaries and testable behavior.

Areas that may still change include final tuning, UI, VFX, audio, animation, fish content, full player controls, and how future cards or upgrades affect the fishing loop.

## Starwell Threshold System Note

`AStarwell` is the current world-facing actor for the offering side of the Nyx loop. Its purpose is to accept completed fish offerings, convert them into reward progress, track Starwell state, and broadcast threshold-related events that future presentation or story systems can respond to.

This is still work-in-progress prototype documentation. The Starwell is being presented as a gameplay systems anchor, not as finished narrative progression, final quest content, or complete player-facing unlock design.

### Current Scope

The Starwell currently represents the offering and threshold side of the prototype:

- accepted fish offerings
- Echo Scales generated from fish value
- total offering progress
- total fish accepted
- total Echo Scales generated
- configured offering thresholds
- reached story unlock IDs
- Blueprint-facing events for accepted fish, progress changes, threshold reaches, story unlock availability, and restored state
- validation support for threshold setup

### Offering To Threshold Flow

The basic flow I am documenting is:

```text
Caught fish -> offer to AStarwell -> grant reward value -> increase OfferingProgress -> check thresholds -> record reached StoryUnlockId
```

The important idea is that the Starwell sits between moment-to-moment fishing and longer-term progression. A catch is a short interaction; Starwell progress is the longer-running record of what those offerings have contributed to.

### Why Stable StoryUnlockId Values Matter

`FStarwellOfferingThreshold` includes a `StoryUnlockId` so reached thresholds can be tracked by a stable key.

That matters because content changes are normal during development. Threshold names, display text, order, reward tuning, and future narrative hooks may change. A save file should not break because a row moved in an array or a label was rewritten.

Using stable IDs keeps the saved `ReachedStoryUnlockIds` list easier to reason about across save/load, content edits, and future expansion.

### What The Starwell Should Own

`AStarwell` should own the gameplay rules directly tied to offerings and threshold progress:

- whether a fish offering is accepted
- how offering value contributes to Starwell progress
- when offering progress changes
- which threshold IDs have already been reached
- when threshold events should broadcast
- how Starwell progress restores from saved data
- whether threshold setup looks valid enough to test

Keeping those responsibilities on the Starwell makes the actor easier to explain as a world-facing progression object.

### What Should Stay Outside It

The Starwell should not try to own every part of the game loop.

Other systems should stay responsible for their own areas:

- `UFishingComponent` should own casting, bite, reel, catch, and fish progress state.
- Economy systems should own broader resource balances, costs, and upgrades.
- UI, VFX, audio, and world presentation should respond through Blueprint-facing events.
- Future story content should stay data-driven instead of being hard-coded into the actor.
- Save helpers should coordinate cross-system capture and restore rather than relying on direct live Actor references.

This separation keeps the Starwell connected to the loop without turning it into a catch-all system.

### QA Questions

Useful questions for testing this system:

- Does offering a valid fish increase Starwell progress once?
- Does the reward value stay understandable when fish values change?
- Does a threshold fire only once after its required progress is reached?
- Are empty or duplicate `StoryUnlockId` values caught before they become save/load problems?
- Does loading saved Starwell progress restore reached IDs without replaying rewards?
- Do Blueprint-facing events provide clean refresh points for presentation without owning the underlying rules?
- Can debug tooling validate offering progress and threshold setup during PIE testing?

### Known Limits

This note does not claim finished Starwell gameplay, finished narrative content, or final progression balance. The current documentation focuses on system responsibilities, threshold safety, and how the Starwell connects fishing rewards to longer-term progress.

Areas that may still change include final threshold content, story unlock design, reward tuning, UI, VFX, audio, level placement, and how future cards, upgrades, or narrative branches respond to Starwell progress.

## Save/Load Reliability Fix

One recent Nyx improvement focused on making save/load behavior more reliable while the project is still a gameplay systems prototype. This note explains the reliability reasoning behind the fix at a portfolio level.

### Active Fishing Casts Normalize To Idle On Load

Active fishing casts are transient runtime interactions. When a save file is loaded, an active cast now normalizes back to an idle fishing state instead of trying to restore fragile mid-action state.

This is an intentional design choice, not a limitation. The save file should not need to preserve temporary runtime details such as timers, reel tension, bite state, animation locks, or partially resolved catch data. Those details belong to the live interaction, not long-term player progress.

Durable progress is the part that should persist. For Nyx, that means save/load work should protect progress such as discovered fish, catch counts, resources, upgrades, and Starwell progress.

### Blueprint Post-Load Events Matter

C++ can restore saved values, but Blueprint needs explicit restoration events so UI, VFX, audio, and world presentation can refresh after loading.

The important distinction is between gameplay events and restoration events. A gameplay event, such as offering a fish to the Starwell, should trigger one-time feedback, rewards, unlocks, and presentation. A post-load restoration event should refresh the world to match saved data without replaying one-time rewards or pretending the player just performed the action again.

That separation makes the system easier to test because loading a save should be visually accurate without duplicating rewards, replaying unlocks, or causing confusing side effects.

### Starwell Thresholds Need Stable Unique IDs

Starwell unlock thresholds should be tracked with stable unique IDs instead of display text, array index, or temporary asset names.

Stable IDs help protect save files when story text changes, thresholds are reordered, rewards are tuned, or assets are renamed. This matters for Nyx because the Starwell can become a long-term progression anchor rather than a single isolated feature.

Future-facing systems such as narrative branches, card unlocks, companions, constellations, and ending paths are still WIP unless documented elsewhere. The save/load lesson here is that those systems will be safer to build later if persistent progress is identified by stable IDs from the beginning.

## PIE Smoke Test Checklist

This is a work-in-progress validation checklist for testing Nyx's core loop in Play In Editor. It is meant to support manual QA and developer confidence while the Unreal C++ systems are still changing. It does not claim finished gameplay or full automated coverage.

The goal is to check that the loop can be exercised in a predictable way:

```text
Start cast -> bite -> reel -> catch -> offer to Starwell -> reward -> save -> load -> verify restored state
```

Suggested PIE smoke checks:

| Step | Check | What I am looking for |
| --- | --- | --- |
| 1 | Start a cast | The fishing system enters a clear cast state without errors or unclear feedback. |
| 2 | Force or wait for a bite | The bite state appears reliably, whether triggered through debug tooling or normal timing. |
| 3 | Start reeling | The system moves from bite to reel state without skipping or duplicating state changes. |
| 4 | Complete a catch | The catch resolves once, and any temporary fishing state is cleared safely. |
| 5 | Offer the fish to the Starwell | The Starwell accepts the offering without requiring fragile actor setup. |
| 6 | Confirm economy rewards | Expected resources increase once and do not duplicate unexpectedly. |
| 7 | Confirm Starwell progress | Offering progress updates and threshold checks remain understandable. |
| 8 | Save current progress | Durable progress is captured without relying on transient runtime state. |
| 9 | Load the save | Saved progress restores, while unsafe in-progress interactions return to a safe state such as `Idle`. |
| 10 | Review restored presentation | UI, VFX, audio, or world feedback can refresh through Blueprint-facing hooks when those presentation layers exist. |

This checklist connects the C++ architecture to QA practice. The important part is that I can describe how I would validate the player-facing loop, watch for regressions, and keep save/load behavior safe as the prototype grows.

## Beginner Blender Placeholder Task Plan

This PR/documentation note adds a beginner-friendly task plan for creating Blender placeholder assets for the Nyx vertical slice. The goal is not polished final art yet. The goal is to create readable PH assets and low-poly blockouts that can support gameplay testing while the prototype is still changing.

What this plan covers:

- Creating simple PH assets and low-poly blockouts in Blender
- Practicing a Blender-to-Unreal workflow for early prototype assets
- Checking scale, sockets, pivots, naming, and placement before assets are used in gameplay tests
- Using PIE testing to confirm placeholder assets support the intended interaction flow
- Keeping asset work clearly marked as WIP, prototype-focused, and safe to replace later

Why this matters for the vertical slice:

The Nyx vertical slice needs enough visual structure to test the fishing loop, Starwell interaction, reward feedback, save/load behavior, and basic world readability. Placeholder assets help make those systems testable without pretending that final models, animation, VFX, or presentation are complete.

Recruiter-facing value:

This plan shows how I am connecting beginner Blender practice to practical Unreal validation. It also keeps the scope honest: the asset work supports iteration, testing, sockets/pivots review, and clear documentation rather than claiming a finished art pipeline.

## What This Showcase Is Meant To Show

- How I explain unfinished technical work without overstating it
- How I connect gameplay systems to QA thinking
- How I break a larger game project into smaller testable areas
- How I document expected behavior, observed behavior, and follow-up questions
- How I use project notes to support learning, testing, and future portfolio updates

## Skills I Am Practicing

- Unreal Editor navigation and project organization
- Gameplay prototyping and iteration
- C++ or Blueprint systems thinking, depending on the feature being built
- Level, interaction, or tool documentation
- QA observation, repro notes, and playtest feedback
- Screenshot capture and portfolio presentation
- Explaining unfinished work professionally
- Writing clear system summaries for technical and non-technical readers

## QA Documentation Format

For each system I add to this showcase, I want to keep the writeup small and practical:

| Field | Purpose |
| --- | --- |
| System | Name of the feature, component, or test area |
| Goal | What the system is supposed to support |
| Current state | What works, what is placeholder, and what is unknown |
| Test notes | What I checked in editor or during playtesting |
| Risks | Bugs, edge cases, confusing behavior, or player-facing concerns |
| Next step | The next small improvement or validation pass |

## Development Log

| Date | Update | Notes |
| --- | --- | --- |
| 2026-05-02 | Showcase page created | Added a place to document the Unreal project while it is still in progress. |
| 2026-05-02 | Added Nyx project details | Moved useful Unreal project details into this showcase while keeping the page honest about work-in-progress status. |
| 2026-05-02 | Documented save/load reliability fix | Added notes on active cast restoration, Blueprint post-load events, and stable Starwell threshold IDs. |
| 2026-05-02 | Added PIE smoke test checklist | Added a WIP manual validation checklist for the fishing, Starwell, economy, save, and load loop. |
| 2026-05-02 | Added fishing component system note | Documented the purpose, state flow, boundaries, QA questions, and limits for `UFishingComponent`. |
| 2026-05-02 | Added Starwell threshold system note | Documented `AStarwell` responsibilities, threshold flow, stable `StoryUnlockId` values, QA questions, and limits. |
| 2026-05-02 | Added first PIE smoke test result | Recorded a partial validation result for save/load behavior, active cast restoration, and follow-up Blueprint presentation checks. |
| 2026-05-02 | Added Beginner Blender Placeholder Task Plan | Captured a WIP plan for PH assets, low-poly blockouts, Blender-to-Unreal workflow practice, sockets/pivots checks, and PIE validation support for the Nyx vertical slice. |

Future entries can track:

- Features tested
- Design changes
- Bugs found
- Screenshots added
- Playtest observations
- Questions to revisit
- Validation passes run in PIE

## QA and Playtest Notes

This section will track practical observations from testing the project.

### Recent Result

Date: 2026-05-02

Result: Partial

What worked:

- The save/load flow restored durable progress without trying to resume the active fishing cast.

What failed or looked risky:

- Blueprint presentation refresh still needs a follow-up pass to confirm UI, VFX, and audio update cleanly after load.

Any bugs found:

- None confirmed yet.

Next action:

- Run another PIE pass focused on post-load presentation and Starwell threshold refresh behavior.

Suggested note format:

| Date | Area Tested | Observation | Next Action |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

Examples of useful notes:

- A feature does not respond the way I expected
- A camera, UI, control, or interaction feels unclear
- A level section creates confusion or friction
- A bug needs clearer repro steps
- A test pass reveals a small improvement for player experience
- A save/load pass reveals missing or incorrect persisted data
- A validation helper catches a setup issue before playtesting

## Visual Evidence

Screenshots or short clips can be added once they show a useful tested state. Until then, the QA notes and system documentation are the main evidence for this work-in-progress showcase.

## Next Steps

- Run a follow-up PIE pass focused on post-load presentation and Starwell threshold refresh behavior
- Add class-level references from `Source/Nyx` if the source is shared publicly and the names can be verified directly
- Add a short economy component system note
- Create the first PH asset checklist for Blender-to-Unreal import, sockets, pivots, scale, and PIE placement checks
- Decide which screenshot or clip would help explain the project without overselling it
- Add a simple "known issues" table once there are real observations to track
- Keep future updates specific, small, and tied to what was actually tested

## Reflection

This showcase is part of learning in public. The project is still developing, and that is the point. I want to practice explaining work while it is in motion: what I tried, what I noticed, what confused me, and what I improved.

Games are the reason this kind of documentation matters to me. Building in Unreal connects the creative side of games with the practical habits I am trying to strengthen: testing, iteration, clear notes, honest scope, and steady follow-through.
