# Handoff Ops Demo Design

## Demo Goal

Handoff Ops Demo gives a recruiter or reviewer a lightweight way to experience external QA intake review. The user acts as a QA lead reviewing mock bug cards for a fictional feature pass.

## User Flow

1. Read the feature goal.
2. Review build and test-window context.
3. Scan scenario coverage.
4. Review incoming bug cards.
5. Decide whether each bug is ready, needs more information, or matches a known issue.
6. Generate a QA Lead Intake Summary.

## Scoring Model

The demo uses a transparent readiness score based on reviewed bug cards. A bug is considered stronger signal when it includes build number, platform, clear repro steps, expected result, actual result, repro rate, evidence attachment, severity suggestion, owner routing, and no known issue match.

Known issue matches are routed away from dev review to avoid duplicate noise.

## Mock Data Structure

Bug cards include title, build, platform, scenario, steps, expected, actual, repro rate, evidence state, screenshot/video reference, severity suggestion, known issue match, suggested owner, and notes.

## Recruiter Walkthrough Script

"This prototype shows how I think about external QA handoffs. The first tab creates an outsource-ready packet with scope, scenarios, evidence expectations, and intake rules. The second tab simulates QA lead review: I check mock bug cards for build context, repro clarity, expected vs. actual behavior, evidence, duplicate risk, and owner routing before deciding whether the issue is ready for dev review."

## Overclaim Protections

- The demo does not connect to Jira.
- The demo does not use private studio workflows.
- The demo does not include real external QA data.
- The demo does not claim production pipeline integration.
- The demo simulates human-reviewed QA decision-making with mock data.
