# External QA Handoff Model

External QA Handoff Manager models a portfolio-safe handoff packet for offsite QA coordination. It is not based on private studio workflows and does not connect to Jira.

## Purpose

The goal is to make a feature test pass executable before external QA starts work. A strong handoff reduces bug noise, clarifies evidence standards, and gives the QA lead a repeatable intake review path.

## Handoff Packet Model

A handoff packet should include feature area, build number, platform, test window, owner, external QA team, objective, setup steps, account/data requirements, scope, known issues, and escalation rules.

## Scenario Matrix Model

Each scenario row captures scenario name, priority, platform, evidence required, likely owner/routing, status, and notes. The matrix helps external testers see what matters most and helps the QA lead identify coverage gaps.

## Bug Evidence Model

Incoming bug reports are reviewed for build number, platform, exact repro steps, expected result, actual result, repro rate, screenshot/video reference, logs/telemetry if available, severity suggestion, and known issue/duplicate checks.

## Intake Review Model

The QA lead intake review classifies each incoming bug as:

- Ready for Dev Review
- Needs More Info
- Duplicate / Known Issue

The decision is based on evidence quality, duplicate checks, severity sanity, and whether the likely owner has enough information to act.

## Daily Summary Model

A daily summary should include tested coverage, blockers, high-risk bugs, duplicate trends, missing evidence patterns, coverage gaps, and release-readiness risk.

## Known Limitations

- This prototype uses mock data only.
- The scoring model is intentionally simple.
- It does not represent private outsource QA process ownership.
- It does not connect to Jira, Slack, Discord, or production tools.
- Human QA judgment is still required.
