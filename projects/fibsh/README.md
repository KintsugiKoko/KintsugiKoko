# Project Fibsh

Status: Active private Unreal Engine game development with selected public documentation and evidence.

Project Fibsh is an original game about a city cat's strange fishing vacation at Lake Glorp. I direct the product scope, systems design, visual development, PH asset workflow, build validation, and release decisions that move the project from concept into a playable prototype.

This summary showcases selected character concepts, level planning, Blender PH assets, the canon Master landscape in Unreal, packaged-build captures, persistence validation, and the controlled workflow behind the project. Core source and editable production assets remain private.

## Published Visual Development

[![Approved Project Fibsh city-cat gameplay concept](../../docs/assets/fibsh/fibsh-character-gameplay-concept.png)](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence)

The public [Game Design Portfolio](https://kintsugikoko.github.io/KintsugiKoko/game-design.html#visual-evidence) includes:

- approved city-cat gameplay and inventory concepts
- an orthographic Lake Glorp level plan
- environment-scale and player-view Lake Glorp concept explorations, labeled separately from current implementation
- the canon Master landscape in Unreal, showing the mountain silhouette, river route, terrain scale, and forest coverage
- a Blender PH environment pass for terrain, shoreline, approach, and camera review
- a Blender PH rig stress render for fishing-arm deformation and pose-range review
- a packaged Unreal smoke-test contact sheet covering the current fishing flow

Artifact labels carry the maturity signal: concepts establish direction, PH assets support iteration, Unreal captures show current implementation, and packaged captures document observed behavior.

## Controlled Development Workflow

Fibsh uses a controlled workflow that separates planning, implementation, build generation, validation, and owner approval.

- Canonical product and ship-state documents establish scope, current evidence, known defects, and the next accepted action.
- Repository-level writer controls prevent overlapping production edits and require worktree and checkpoint agreement before recovery.
- Isolated build generations copy and hash scoped inputs before Unreal compile, data validation, cook, stage, package, and launch checks.
- Automated checks, deterministic packaged validation, and human-input smoke tests produce separate evidence instead of being treated as interchangeable.
- Public, financial, legal, platform, protected-branch, and release decisions remain owner-gated.

## Recent Workflow Milestones

Recent committed work includes:

- A controlled implementation workflow with explicit writer ownership and recovery checkpoints
- An isolated build lane that protects source stability while collecting compile, Unreal Data Validation, cook, stage, package, and launch evidence
- A scoped gameplay transaction with follow-up UX and persistence fixes
- Packaged-build automation checks kept separate from human-input smoke testing
- Quit/relaunch persistence validation and explicit defect ranking

A current validation record includes 25 successful automation checks with no recorded failures. A packaged human-input smoke reached a natural bite, completed the catch-and-store flow, updated the journal, and preserved the same catch after quit and relaunch.

The current validated scope covers the core transaction and persistence contract. PH character work, presentation, audio, settings, progression, representative performance, and broader release gates remain active development areas.

## Senior QA / QAE Signal

- Converts product goals into bounded acceptance criteria and ranked risks
- Separates source stability, build success, automated checks, deterministic validation, and human usability review
- Tracks failures through reproducible evidence instead of relying on summary claims
- Protects unrelated WIP and private assets during build and verification work
- Directs tool-assisted implementation through explicit ownership, scope, and verification gates
- Reports what passed, what remains unverified, and what blocks release confidence

## Public Boundary

Selected flat images, workflow summaries, and validation outcomes are published. The private repository, Unreal source and content, Blender source, packaged builds, credentials, commercial details, schedules, and unreleased production records remain private.
