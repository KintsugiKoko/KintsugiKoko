# Nyx Test Planner Case Study: Turning a Gameplay Idea into a QA Validation Pass

## Overview

This case study shows how one Nyx gameplay idea moves from planning into a human-reviewed QA validation path. It connects QA planning judgment, risk thinking, expected results, manual PIE/prototype validation notes, evidence capture, and pass/fail/follow-up decisions without claiming completed validation.

## Scenario

Scenario title: Starwell Offering Unlock Validation

The planned scenario checks whether offering a qualifying soul-fish to the Starwell advances the intended unlock or progression state in a clear, understandable way. The validation focus is not the full Nyx gameplay loop; it is the specific player-facing moment where a fish offering should create visible progress and leave enough evidence for review.

## Why This Scenario Matters

Player risk:

- The player may not understand whether the offering worked.
- Progress may feel lost, duplicated, or unclear if feedback is missing.
- A confusing unlock moment can weaken trust in the cozy progression loop.

Design risk:

- Unlock thresholds, reward timing, or Starwell feedback may not match the intended pacing.
- Placeholder presentation could imply a more finished system than actually exists.
- Missing feedback can hide whether the interaction supports the intended cozy cosmic fishing direction.

Technical / QA risk:

- The offering may update progress more than once.
- The interaction may fail silently if a required setup step is missing.
- Save/load or regression passes may need follow-up if the unlock state is durable.

## Planned Test Coverage

Nyx Test Planner captures the scenario as a structured planning item:

- Scenario title: Starwell Offering Unlock Validation
- Gameplay area: Starwell Offering
- Test type: Validation
- Risk level: High
- Status: Planned validation pass
- Steps / notes: setup state, fish offering action, observed feedback, progress check, follow-up questions
- Expected result: offering a qualifying fish advances the intended Starwell progress once and communicates the result clearly
- Follow-up notes: bug report, tuning note, missing setup dependency, regression check, save/load validation, or UI clarity note
- Markdown export: human-reviewed test-plan draft for the scenario and related risk notes

## Manual Validation Method

This scenario would be validated through a human-reviewed manual PIE validation or prototype review.

The reviewer would open the relevant Nyx prototype state, prepare or simulate the required fish / Starwell setup, perform the offering action, and observe the first visible result. Evidence capture should include a screenshot or short clip reference when practical, the exported Markdown test plan from Nyx Test Planner, and notes about the build or prototype version under review.

This method does not claim automated Unreal tests. Nyx Test Planner is a browser-based planning prototype and does not connect to Unreal, Jira, private tools, studio data, or automated test runners.

## Expected Result

- The Starwell offering interaction accepts the qualifying fish only when setup requirements are met.
- Starwell progress or unlock state advances once.
- The player-facing feedback communicates that the offering was accepted.
- Placeholder or WIP presentation remains clearly labeled.
- No duplicate reward, repeated unlock, immediate softlock, or unclear failure state is observed.
- Any missing setup dependency is recorded as a follow-up instead of treated as a passed validation.

## Actual Result

Pending manual PIE validation. This case study documents the planned validation path and expected evidence.

## Evidence to Capture

- Screenshot or short clip of the gameplay state
- Exported Markdown plan from Nyx Test Planner
- Notes on build / prototype version
- Pass/fail status
- Bug or follow-up note if needed

## Result / Decision

Pending manual PIE validation.

## Follow-Up

Possible follow-ups:

- Bug report
- Tuning note
- Missing implementation dependency
- Additional regression check
- Save/load validation
- UI clarity note

## Portfolio-Safe Note

This case study is a human-reviewed QA planning and validation artifact. It does not claim automated Unreal testing, live Jira integration, private studio tooling, or production pipeline integration.
