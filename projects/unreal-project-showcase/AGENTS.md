# Nyx Codex Guide

This folder documents **Nyx**, a WIP Unreal Engine C++ cozy cosmic fishing prototype starring a tuxedo-pattern cat.

Use this guide for Nyx implementation notes, README updates, PR summaries, portfolio writing, and future source-repo work. Keep the language honest: do not claim final art, final gameplay, shipped features, or production-ready systems unless they are clearly implemented and verified.

## Current Focus

- Catch-to-Starwell vertical slice
- First uncommon fish Nyx encounter
- SaveGame reliability
- Blueprint post-load events
- Starwell stable threshold IDs
- UMG card pack opening flow
- Blender-to-Unreal PH asset workflow
- PIE smoke testing

For current project context, use `README.md` in this folder before inventing new wording.

## Unreal Rules

- Avoid editing binary `.uasset` files unless explicitly requested.
- Use the `PH_` prefix for placeholder assets.
- Preserve existing build, setup, and run instructions.
- Prefer small, reviewable changes over broad rewrites.
- Keep placeholder art, prototype Blueprints, and temporary validation helpers clearly labeled.

## Architecture Rules

- Data defines what things are.
- Gameplay logic decides what happens.
- UI and Blueprint show how it feels.
- SaveGame stores durable progress, not transient runtime state.
- Active runtime interactions, such as a fishing cast in progress, should restore to safe states instead of preserving fragile timers, animation locks, reel tension, bite state, or partially resolved catch data.
- Blueprint post-load events should refresh presentation without replaying one-time gameplay rewards.
- Starwell threshold progress should use stable IDs, not display text, array position, or temporary names.

## Documentation Rules

- Mark unfinished work as WIP, prototype, foundation, planned, or placeholder.
- Include what was tested and what still needs validation.
- Distinguish command-line automation or `-NullRHI` smoke tests from hands-on PIE, visual, UI, asset-scale, and player-facing validation.
- For PIE smoke test devlogs, separate observed results from planned checks. Use careful language such as "partial validation," "observed in PIE," and "needs follow-up" when the pass is not complete.
- Keep recruiter-facing language honest, portfolio-friendly, and evidence-based.
- Explain why a change matters for QA, iteration, reliability, or the Nyx vertical slice.
- Distinguish implemented behavior from planned systems such as future narrative paths, cards, companions, constellations, endings, or final art.
- Do not over-explain in `AGENTS.md`; reference the Nyx README or a focused devlog/checklist when details get long.

## PR Description Format

Use this structure for Nyx PRs and portfolio summaries:

```markdown
## Summary

## What Changed

## Why This Matters

## Testing / Validation

## Notes
```

In `Testing / Validation`, mention PIE smoke checks, manual QA passes, SaveGame checks, Blueprint refresh checks, or "not run" honestly.

In PR descriptions, do not describe Nyx systems as finished, production-ready, or fully validated unless the README/devlog evidence supports that exact claim.
