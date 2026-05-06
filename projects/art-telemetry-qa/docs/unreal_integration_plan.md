# Unreal Integration Plan

This is a future-facing plan, not a completed Unreal plugin.

## Current State

The MVP reads mock Unreal-style CSV and JSON data from local sample files. It demonstrates the reporting and validation logic that could sit downstream of real capture workflows.

## Future Integration Direction

A future Unreal-facing version could:

- Export asset validation summaries from editor utility tools.
- Import Unreal Insights summary exports.
- Read cooked asset audit summaries.
- Compare captures before and after a suspected fix.
- Attach screenshot, log, or capture references to Jira-ready drafts.
- Store platform-specific threshold profiles.

## What Should Stay Human-Reviewed

- Whether a finding is a real bug.
- Whether a threshold applies to the asset's intended role.
- Whether Art, Tech Art, VFX, Animation, Engineering, Performance, or QA owns next action.
- Whether a fix is visually acceptable after performance or content changes.

## What This Tool Should Not Become

- A replacement for Unreal Insights.
- A replacement for Tech Art or Performance review.
- A private telemetry parser.
- An automatic Jira filing bot.
- A claim that every flagged asset is objectively broken.

The useful lane is Art QA evidence handling: capture, parse, isolate, report, verify, and keep the human reviewer in control.
