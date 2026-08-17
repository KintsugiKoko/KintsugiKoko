# Game Design Portfolio

This section collects public-safe examples of how I think about gameplay systems, progression, player understanding, iteration, and design validation.

My professional background is primarily Senior QA / QAE. The design work shown here is narrower and clearly labeled: professional content and systems-design contributions from Ashes of Creation, plus original work-in-progress systems and documentation from Nyx. I do not claim sole ownership of team work, finished level-design experience, or completed commercial game-design systems that are not supported by public evidence.

- [Open the live Game Design Portfolio](https://kintsugikoko.github.io/KintsugiKoko/game-design.html)
- [Review the Nyx Unreal showcase](../unreal-project-showcase/README.md)
- [Open the Nyx Test Planner](https://kintsugikoko.github.io/KintsugiKoko/nyx-test-planner.html)
- [Read the Nyx Test Planner case study](../../docs/nyx-test-planner-case-study.md)

## Design Focus

- Interconnected gameplay systems
- Equipment, economy, and progression relationships
- Player-facing clarity and feedback
- Core-loop structure
- Persistent progression and safe state restoration
- Playtest planning and iteration
- Translating design intent into testable behavior

## Professional Design Contribution

### Ashes of Creation Content And Systems Design

**Status:** Professional team contributions. Public summary only.

At Intrepid Studios, I contributed directly to content and systems design while working across Narrative Design and the Ashes of Creation Economy team. I was preparing to transition formally into design when the unexpected studio closure interrupted that path.

My contribution included:

- designing quest and world-event content with the Narrative Design team
- designing equipment recipes with the Economy team
- helping translate system goals, item behavior, and progression changes for an equipment rework across two milestones
- reviewing interactions between equipment, economy, progression, rewards, UI, tools, and supporting data
- identifying implementation gaps and player-facing risk during iteration
- using test coverage, playtest findings, and cross-discipline discussion to support design decisions
- communicating with design, engineering, production, art, and QA partners

This is not presented as sole design ownership. Proprietary requirements, internal documentation, tuning values, unreleased implementation details, and team-authored assets remain private.

## Original WIP Design Work

### Nyx Core Loop

Nyx is a work-in-progress cozy cosmic fishing prototype. The current design loop is:

```text
Catch a soul-form fish -> offer it to the Starwell -> earn rewards -> unlock progress -> save persistent progress
```

The loop is designed to connect a short, readable fishing interaction to a longer progression goal. Each system has a focused responsibility so the player can understand what happened and the prototype can be tested in smaller pieces.

| System | Design purpose | Current public status |
| --- | --- | --- |
| Fishing state flow | Give the player a readable cast, wait, bite, reel, and catch sequence | WIP C++ prototype and system documentation |
| Starwell offerings | Turn caught fish into visible longer-term progress | WIP actor and threshold documentation |
| Stable threshold IDs | Protect progression when display text, ordering, or rewards change | Save/load reliability design documented |
| Nyx merchant / ferryman | Add personality, services, and a bridge into future-run progression | Concept and planning foundation, not finished gameplay |
| Upgrades and deck foundations | Create future choices that can change later runs | Scaffolding and future-facing documentation |

### Starwell As A Progression Anchor

The Starwell sits between moment-to-moment fishing and persistent progress:

```text
Caught fish -> offering value -> Starwell progress -> threshold check -> stable unlock record
```

The design goal is not just to grant a reward. It is to make every catch contribute to a larger, understandable purpose while keeping one-time rewards separate from save/load restoration.

Questions used during iteration include:

- Does the player understand why an offering matters?
- Is reward feedback distinct from restored presentation after loading?
- Can thresholds change without making old saves fragile?
- Does the Starwell feel like a world-facing progression object rather than a menu with extra steps?

### Fishing System Boundaries

The fishing component owns the interaction state flow and catch outcome. It should not own the full economy, Starwell progression, final presentation, or unrelated world rules.

That boundary supports design iteration because fishing timing can change without turning one component into the owner of every reward, unlock, UI, VFX, and save decision.

## Levels And Spaces

### Prototype Test Area And Interaction Path

**Status:** Planning and Play In Editor validation evidence. Not a finished authored level.

The current public design work uses a simple interaction path for prototype validation:

```text
Fishing area -> catch feedback -> Starwell offering point -> Nyx merchant / service beat -> return to the loop
```

The purpose is to test readability, pacing, interaction distance, placement, and return-to-loop clarity before claiming a polished level or encounter.

Current public evidence includes placeholder-asset planning, interaction placement questions, test-area checks, and PIE smoke-test scenarios. It does not yet include a finished whitebox walkthrough, final environment art, authored mission flow, or a completed playable vertical slice.

## Design And Iteration Process

1. State the player-facing goal.
2. Map the systems and content responsibilities.
3. Identify the decision, feedback, and failure states the player needs to understand.
4. Build or document the smallest testable version.
5. Run focused PIE, playtest, or scenario checks.
6. Separate observed behavior from assumptions.
7. Revise the design, documentation, or implementation boundary.

## Evidence And Artifacts

- [Fishing Component System Note](../unreal-project-showcase/README.md#fishing-component-system-note)
- [Starwell Threshold System Note](../unreal-project-showcase/README.md#starwell-threshold-system-note)
- [Save/Load Reliability Fix](../unreal-project-showcase/README.md#saveload-reliability-fix)
- [PIE Smoke Test Checklist](../unreal-project-showcase/README.md#pie-smoke-test-checklist)
- [Beginner Blender Placeholder Asset Checklist](../unreal-project-showcase/README.md#beginner-blender-placeholder-asset-checklist)
- [Nyx Test Planner](../../docs/nyx-test-planner.html)
- [Nyx Test Planner Case Study](../../docs/nyx-test-planner-case-study.md)

## What This Section Does Not Claim

- Sole ownership of Ashes of Creation quests, world events, recipes, or the equipment rework
- Publication of confidential studio documentation or proprietary tuning
- Finished Nyx gameplay, final art, or production readiness
- Finished public mission, encounter, or level-design artifacts beyond the contributions documented here
- Public access to private Fibsh or Nyx source repositories and assets

## Next Portfolio Evidence

- Add an annotated Nyx whitebox showing player route, interaction beats, and iteration notes
- Add before-and-after examples from one verified design change
- Add screenshots or short video only after public-safe assets and presentation are reviewed
- Add a compact design brief for one self-contained Nyx interaction
