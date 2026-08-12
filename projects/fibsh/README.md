# Project Fibsh

Status: Private WIP Unreal game project.

Project Fibsh is a private WIP Unreal game project. The source repository, Unreal content, Blender files, packaged builds, commercial planning, gameplay details, and complete validation evidence remain private.

This public summary focuses on the QA and workflow systems used to supervise development. It is not a public build, source release, production-readiness statement, or store-readiness claim.

## Agent-Supervised Workflow

Fibsh uses a controlled workflow that separates planning, implementation, build generation, validation, and owner approval.

- Canonical product and ship-state documents establish scope, current evidence, known defects, and the next accepted action.
- Repository-level writer controls prevent overlapping production edits and require worktree and checkpoint agreement before recovery.
- Isolated build generations copy and hash scoped inputs before Unreal compile, data validation, cook, stage, package, and launch checks.
- Automated checks, deterministic packaged validation, and human-input smoke tests produce separate evidence instead of being treated as interchangeable.
- Public, financial, legal, platform, protected-branch, and final release decisions remain owner-gated.

## Recent Workflow Milestones

Recent committed work includes:

- A controlled agent workflow with explicit writer ownership and recovery checkpoints
- An isolated build lane that protects source stability while collecting compile, Unreal Data Validation, cook, stage, package, and launch evidence
- A WIP gameplay transaction with follow-up UX and persistence fixes
- Packaged-build automation checks kept separate from human-input smoke testing
- Quit/relaunch persistence validation and explicit defect ranking

Functional evidence is not presented as release quality. Character identity, visual presentation, audio, settings, broader progression, representative performance, and final release readiness still require additional work or validation.

## Senior QA / QAE Signal

- Converts product goals into bounded acceptance criteria and ranked risks
- Separates source stability, build success, automated checks, deterministic validation, and human usability review
- Tracks failures through reproducible evidence instead of relying on summary claims
- Protects unrelated WIP and private assets during build and verification work
- Uses agent assistance within explicit ownership, scope, and approval boundaries
- Reports what passed, what remains unverified, and what blocks release confidence

## Public Boundary

No private repository URL, Unreal source, binary content, Blender source, packaged build, credential, commercial detail, internal schedule, or unreleased production record is published here.
