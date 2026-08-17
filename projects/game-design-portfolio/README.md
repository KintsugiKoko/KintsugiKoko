# Game Design Portfolio

This section collects public-safe examples of how I think about gameplay systems, player understanding, iteration, and design validation.

My primary professional lane is Senior QA / QAE. The design work shown here is narrower and clearly labeled: professional content and systems-design contributions from Ashes of Creation, plus current private work on Project Fibsh. The Fibsh showcase includes selected concept boards, Blender results, packaged Unreal captures, and validation summaries while source files and unreleased production material remain private.

- [Open the live Game Design Portfolio](https://kintsugikoko.github.io/KintsugiKoko/game-design.html)
- [Review the public Project Fibsh summary](../fibsh/README.md)

## Design Focus

- Interconnected gameplay systems
- Equipment, economy, and progression relationships
- Player-facing clarity and feedback
- Character and visual-direction review
- Level composition and spatial readability
- Product scope and acceptance criteria
- Persistence and safe state behavior
- Playtest planning and iteration
- Translating design intent into observable behavior

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

## Current WIP Design Work

### Project Fibsh

**Status:** Current private WIP Unreal game project with selected public-safe visual and validation evidence.

Project Fibsh is a WIP project about a city cat's strange fishing vacation at Lake Glorp. Its public design evidence shows how that premise moves through visual direction, spatial planning, Blender development, Unreal implementation, packaged smoke testing, and owner-reviewed iteration.

Detailed mechanics, Unreal source and content, Blender source files, packaged builds, commercial planning, and the complete validation record remain private.

## Published Project Fibsh Evidence

The public page already contains evidence across four distinct stages. Each artifact is labeled so a visual target is not confused with an implemented result.

### Character And Gameplay Direction

[![Approved Project Fibsh city-cat gameplay concept](../../docs/assets/fibsh/fibsh-character-gameplay-concept.png)](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)

This approved, human-reviewed concept board establishes the city-cat silhouette, Lake Glorp mood, fishing posture, and cast-ready readability. It is concept direction, not an in-engine screenshot.

### Lake Glorp Level Concept

[![Lake Glorp orthographic level concept](../../docs/assets/fibsh/lake-glorp-level-concept.png)](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)

The orthographic plan supports design decisions about the dock approach, shoreline loop, central fishing focus, readable landmarks, and supporting activity spaces.

### Blender Environment And Character Work

[![Lake Glorp Blender environment work in progress](../../docs/assets/fibsh/lake-glorp-blender-environment-wip.png)](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)

The Lake Glorp structural pass tests terrain tiers, shoreline shape, approach paths, lighting anchors, and camera coverage. A separate [Parry rig stress render](../../docs/assets/fibsh/parry-blender-rig-stress-wip.png) records fishing-arm deformation and pose-range review. Parry is a WIP validation character, not the final player identity.

### Packaged Unreal Validation

[![Project Fibsh packaged smoke-test contact sheet](../../docs/assets/fibsh/fibsh-packaged-smoke-test-wip.jpg)](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)

The packaged contact sheet records a real WIP flow through menu, movement, cast, wait, bite, reel, result, journal, and pause states. It is functional proof, not release-quality presentation.

## Design And Validation Loop

```text
Define the goal -> bound the scope -> implement one change -> validate the result -> decide the next action
```

| Design area | Purpose | Current public status |
| --- | --- | --- |
| Product and ship-state intent | Establish the current goal, accepted scope, known evidence, ranked risks, and next action | Workflow documented, product details private |
| Gameplay transaction | Keep one WIP player-facing change bounded enough to iterate and verify | Follow-up UX and persistence fixes documented at a high level |
| Persistence behavior | Preserve understandable durable state across quit and relaunch | Validation evidence summarized, implementation private |
| System boundaries | Prevent one feature from silently owning unrelated rules or release decisions | Public workflow principle |
| Release evidence | Separate build success, automated checks, deterministic validation, and human usability review | Evidence types documented separately, no release-readiness claim |

## Product Scope And Acceptance Criteria

Canonical product and ship-state documents establish what the current change is trying to achieve, which behavior is accepted, what remains unknown, and which risks block the next decision.

That structure supports design iteration because it keeps the player-facing goal connected to observable behavior without treating a successful build or automated check as proof of a complete experience.

Questions used during review include:

- What should the player understand after this interaction?
- Which system owns the state change, feedback, and persistence rule?
- What evidence would show that the change works as intended?
- Which defects block the next milestone, and which are known WIP limits?
- What still requires human play or usability review?

## Public / Private Boundary

### What Is Public

- Scope-control and acceptance-criteria habits
- Agent-supervised writer and recovery controls
- Isolated build and validation stages
- Separation of automated, deterministic, and human evidence
- High-level gameplay, UX, and persistence iteration milestones
- Selected flattened concept boards, Blender renders, and packaged Unreal captures
- Ranked defects, residual risk, and owner-gated decisions

### What Remains Private

- Detailed mechanics and unreleased design records
- Unreal source, content, and project internals
- Blender files and final source assets
- Packaged builds and complete validation evidence
- Commercial plans, schedules, credentials, and platform details

## Design And Iteration Process

1. State the player-facing or product goal.
2. Map the systems and content responsibilities.
3. Define acceptance criteria, failure states, and known risks.
4. Implement or document the smallest controlled change.
5. Run the appropriate build, deterministic, automated, and human checks separately.
6. Distinguish observed evidence from assumptions.
7. Rank defects and approve the next action through owner review.

## Evidence And Artifacts

- [Project Fibsh Public Summary](../fibsh/README.md)
- [Agent-Supervised Workflow](../fibsh/README.md#agent-supervised-workflow)
- [Recent Workflow Milestones](../fibsh/README.md#recent-workflow-milestones)
- [Published Visual Development Evidence](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)
- [Senior QA / QAE Signal](../fibsh/README.md#senior-qa--qae-signal)

## What This Section Does Not Claim

- Sole ownership of Ashes of Creation quests, world events, recipes, or the equipment rework
- Publication of confidential studio documentation or proprietary tuning
- Public access to Project Fibsh source, assets, builds, mechanics, or commercial records
- Finished Project Fibsh gameplay, final art, production readiness, store readiness, or release quality
- That automation replaces human play, usability review, or owner approval

## Evidence Maintenance

- Keep concept, Blender, Unreal, and validation artifacts labeled by their actual maturity.
- Add only owner-reviewed flat exports, never private source files or packaged builds.
- Keep the public summary aligned with current verified milestones.
- Preserve the distinction between functional validation and release presentation.
