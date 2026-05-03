# Project Nyx - Agent Guide

## Purpose

Project Nyx is a cozy cosmic fishing prototype. Nyx is a tortoiseshell cat merchant/ferryman who appears during cosmic fishing runs, freezes the moment for story/dialogue, and offers upgrades or services. The player fishes soul-like fish variants from a cosmic river traffic jam inspired by Styx mythology. Starwell offerings connect fishing to cozy incremental progression.

Use this guide for Nyx planning, implementation notes, README updates, devlogs, PIE smoke test documentation, PR summaries, and portfolio-safe summaries.

## Tone Rules

- Cozy
- Cosmic
- Slightly silly
- Mythic but not grim
- Cat-forward
- Gentle incremental progression
- Inspired by goofy physics, chunky silhouettes, and cozy cats in space without leaning into horror

Avoid:

- Grimdark death obsession
- Horror framing
- Final-art claims
- Production-ready claims
- Giant unverified systems
- "Finish the whole game" scope

## Core Loop Direction

The intended prototype loop is:

- Enter a cosmic fishing run.
- Catch soul-fish variants from the cosmic river traffic jam.
- Encounter Nyx as a tortoiseshell merchant/ferryman who can freeze the moment for dialogue, upgrades, or services.
- Make Starwell offerings that convert fishing outcomes into cozy incremental progression.
- Return to the run with clearer feedback, readable UI, and safe reset/exit behavior.

## Weekly Workflow

Use the loop: Plan → Implement → Verify → Document → Summarize → Portfolio Update.

- Plan: choose one small weekly slice.
- Implement: keep the feature narrow and placeholder-safe.
- Verify: run PIE checks when practical and record what happened.
- Document: update README, devlog, testing note, or PR summary.
- Summarize: explain what changed and what remains WIP.
- Portfolio Update: only elevate work that has evidence and clear status.

## ELO Prompt Rule

When creating prompts or next steps, separate ChatGPT prompts from Codex prompts and use ELO tiers when useful:

- Beginner ELO: explicit, guided, low-risk, learning-focused.
- Intermediate ELO: scoped, practical, assumes basic repo/tool comfort.
- Expert ELO: production-style review style, including risks, acceptance criteria, verification, maintainability, and portfolio/recruiter framing.

## Good Weekly Slices

- Nyx merchant placeholder interaction
- Soul-fish variant data
- Starwell offering prototype
- Fishing feedback polish
- Cosmic river visual pass
- UI/shop readability pass
- Dialogue stub pass
- Upgrade/service menu placeholder
- PIE smoke test documentation
- Portfolio README polish

## Bad Or Vague Tasks To Avoid

- Finish the whole game.
- Build every Nyx system at once.
- Make final art, final animation, final VFX, or final audio claims.
- Add a giant unverified system without a small testable slice.
- Describe planned lore, endings, companions, cards, or economy depth as implemented.
- Use horror, grimdark, or heavy death framing when cozy mythic language fits better.

## Verification Rules

When possible, verify in PIE:

- Project opens
- Target map loads
- Player can enter fishing flow
- Weekly feature can be triggered
- Feature can be exited/reset
- Existing fishing loop still works
- No obvious crash
- No obvious softlock
- UI text is readable
- Placeholder content is clearly labeled

For each verification pass, record what was tested, what was not tested, what failed or looked risky, and what needs follow-up.

## Documentation Rules

For meaningful weekly slices, update or create:

- README section
- `docs/devlogs/YYYY-MM-DD-feature-name.md`
- `docs/testing/feature-name-pie-smoke-test.md`
- PR summary

Use prototype-safe language such as WIP, placeholder, first pass, partial validation, observed in PIE, needs follow-up, and planned. Keep devlogs short enough to maintain.

## Portfolio Safety Rules

- Clearly mark WIP and placeholder content.
- Do not claim a feature is complete unless implemented and verified.
- Explain what was tested and what was not tested.
- Use prototype-safe language.
- Do not claim production readiness.
- Do not present concept art, placeholder assets, planned systems, or future narrative paths as finished work.
- Keep recruiter-facing summaries focused on QA judgment, validation habits, documentation clarity, and practical iteration.

## Standard Output After Meaningful Work

At the end of meaningful work, provide:

- Summary of files changed
- How to run or preview
- Tests or PIE checks run
- What was tested and what was not tested
- Known limitations and WIP notes
- Portfolio-safe summary
- Suggested commit message
- Beginner ELO ChatGPT prompt and Codex prompt
- Intermediate ELO ChatGPT prompt and Codex prompt
- Expert ELO ChatGPT prompt and Codex prompt
