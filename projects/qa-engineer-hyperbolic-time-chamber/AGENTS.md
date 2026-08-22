# QA Engineer Hyperbolic Time Chamber - Agent Guide

## Purpose

This project helps Keith grow from experienced Game QA / Technical QA into stronger QA tooling, automation, GitHub, documentation, and agent-supervised engineering habits.

Keith is a QA professional learning code in public. The work should create honest proof of growth through small QA-focused tools, tests, docs, examples, and portfolio artifacts.

## Core Identity

Keith's lane in this project:

- Game QA / Technical QA professional
- 8 years of game QA experience
- Strong QA judgment, bug communication, player-impact thinking, and systems validation
- Learning Python, pytest, Git / GitHub, GitHub Actions, Markdown docs/documentation, CLI tools, log triage, bug report tooling, community sentiment reporting, README/project documentation, learning logs, and agent-supervised workflows

## Project Boundaries

- Keep changes small, testable, and beginner-readable.
- Use fictional/sample data only.
- Do not use NDA, proprietary, or internal studio material.
- Do not describe tools as complete, enterprise-ready, or production-ready.
- Mark each project or feature as planned, concept, first working version, WIP prototype, or complete only when that status is supported by the files and verification.
- Prioritize practical QA usefulness over broad engineering architecture.

## ELO Prompt Rule

When creating prompts or next steps, separate ChatGPT prompts from Codex prompts and use ELO tiers when useful:

| ELO | Rank | Use Case |
|---:|---|---|
| 1000 | Wood | Explain, guide, review safely, teach the concept |
| 1400 | Gold | Make a scoped repo change with tests/docs |
| 1800 | Diamond | Audit architecture, risks, verification, and portfolio positioning |

## Agent Supervisor Workflow

Use the loop: Define → Delegate → Verify → Document → Reflect.

- Define: state the goal, files likely involved, and definition of done.
- Delegate: let Codex make focused edits while Keith supervises the direction.
- Verify: run tests, CLI commands, or documentation checks that match the change.
- Document: update README, examples, reports, learning logs, or PR summaries when behavior changes.
- Reflect: explain what Keith should learn from the diff and name the next smallest improvement.

## QA Tooling Standards

Each QA tool should aim to include:

- `README.md`
- `sample-data/`
- `src/`
- `tests/`
- `reports/` or output examples
- `pyproject.toml` when Python
- GitHub Actions when practical
- Example input
- Example output
- "What I Practiced"
- "Known Limitations"
- "Future Improvements"

## Verification Rules

- Run pytest when tests exist.
- Run CLI commands manually when practical.
- Confirm README commands match real behavior.
- List what was tested and what was not tested.
- Avoid claiming production readiness.
- If verification cannot be run, say why and identify the remaining risk.

## Documentation Rules

- Keep README instructions beginner-friendly and copy-ready.
- Update docs when behavior changes.
- Include sample input and output for QA tools.
- Keep learning logs honest about what was confusing, what worked, and what needs another pass.
- Use clear project status labels such as planned, WIP, first working version, or complete.

## Portfolio Positioning Rules

- Lead with evidence: tests, examples, commands, reports, screenshots, or devlogs.
- Connect work to QA strengths: repro clarity, validation, regression awareness, communication, risk thinking, and tool-building.
- Do not overstate coding, automation, engineering, or production readiness.
- Frame AI assistance as supervised workflow practice with human review.

## Standard Output After Meaningful Work

At the end of meaningful work, provide:

- Summary of files changed
- How to run or preview
- Tests run
- What was tested and what was not tested
- Known limitations
- What Keith should learn from the diff
- Suggested commit message
- ELO 1000 Wood ChatGPT prompt and Codex prompt
- ELO 1400 Gold ChatGPT prompt and Codex prompt
- ELO 1800 Diamond ChatGPT prompt and Codex prompt
