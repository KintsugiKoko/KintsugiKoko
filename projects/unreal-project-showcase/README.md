# Unreal Project Showcase: Nyx

## Overview

Nyx is a work-in-progress Unreal project I am using to practice game systems documentation, playtesting habits, and technical QA thinking.

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
| AStarwell / pathing notes | Tracking navigation or pathfinding-related experiments clearly | Are edge cases, blocked paths, and confusing player outcomes recorded? |
| Economy component | Thinking through resources, costs, rewards, and balance-facing data | Are values readable, testable, and easy to validate after changes? |
| Deck component | Documenting a rules-based or collection-style system | Are card/deck states clear, recoverable, and testable? |
| SaveGame notes | Recording persistence behavior and save/load expectations | What data should persist, what should reset, and how can regressions be checked? |
| Validation helpers | Building notes around small checks that support reliability | What can be verified quickly before deeper playtesting? |
| PIE validation | Using Play in Editor sessions to check behavior while iterating | What should be tested every time a system changes? |

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

Future entries can track:

- Features tested
- Design changes
- Bugs found
- Screenshots added
- Playtest observations
- Questions to revisit
- Validation passes run in PIE

## Screenshots Placeholder

Screenshots or short clips can be added here when they are ready and safe to share.

Suggested format:

```markdown
![Short screenshot description](path-to-screenshot.png)
```

For now, this section is intentionally a placeholder.

## QA and Playtest Notes

This section will track practical observations from testing the project.

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

## Next Steps

- Add one short system note for the fishing component
- Add one QA note from a PIE validation pass
- Decide which screenshot or clip would help explain the project without overselling it
- Add a simple "known issues" table once there are real observations to track
- Keep future updates specific, small, and tied to what was actually tested

## Reflection

This showcase is part of learning in public. The project is still developing, and that is the point. I want to practice explaining work while it is in motion: what I tried, what I noticed, what confused me, and what I improved.

Games are the reason this kind of documentation matters to me. Building in Unreal connects the creative side of games with the practical habits I am trying to strengthen: testing, iteration, clear notes, honest scope, and steady follow-through.
