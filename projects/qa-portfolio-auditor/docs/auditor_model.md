# QA Portfolio Auditor Model

QA Portfolio Auditor is a portfolio-safe self-audit tool for reviewing public QA portfolio projects before publishing.

## Purpose

The auditor answers:

> Are my QA portfolio tools working, clearly documented, safe from overclaiming, and easy for recruiters to review?

It demonstrates QA discipline applied to portfolio artifacts: release-readiness thinking, evidence completeness, recruiter clarity, and overclaim control.

## Metadata Model

Each tool record includes:

- Tool name
- Project category
- Demo link or sample output path
- README/docs link
- One-liner
- Status label
- Evidence focus
- Required phrases
- Forbidden phrases
- Required artifacts
- Known limitations

## Check Model

The browser prototype checks:

- Has one-liner
- Has status label
- Has demo link or sample output
- Has README/docs link
- Has portfolio-safe disclaimer
- Has evidence focus
- Has known limitations or safe boundary language
- Avoids forbidden claims

## Status Model

- `Pass`: the project has core review signals and no forbidden claim hits.
- `Pass with Notes`: the project is reviewable but should tighten one or more signals.
- `Needs Review`: the project is missing basic review artifacts or has overclaim risk.

## Forbidden Claim Model

The auditor flags wording such as:

- live Unreal automation
- Unreal plugin
- production-ready
- real studio telemetry
- private studio data
- real Jira integration
- automated engine validation
- replaces Tech Art review
- AI detects visual quality
- production pipeline integration

## Known Limitations

- The tool checks sample metadata and wording, not live websites.
- It does not perform full browser automation.
- It does not replace manual review.
- It does not guarantee perfect recruiter-readiness.
