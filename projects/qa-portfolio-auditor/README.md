# QA Portfolio Auditor

## Status

Portfolio-safe prototype.

QA Portfolio Auditor checks my portfolio tools for demo readiness, documentation coverage, recruiter-safe wording, evidence completeness, and overclaim risk before publishing.

This is a self-audit tool for a Senior QA / Technical QA / Art QA portfolio. It checks portfolio tool metadata and wording for review readiness, but it does not replace manual review, perform full browser automation, connect to private tools, or claim perfect validation.

## What It Answers

Are my QA portfolio tools working, clearly documented, safe from overclaiming, and easy for recruiters to review?

## What It Demonstrates

- QA discipline applied to my own portfolio artifacts
- Release-readiness thinking before publishing
- Recruiter-readable project positioning
- Evidence completeness checks
- Portfolio-safe disclaimer review
- Overclaim control around Unreal, Jira, private data, automation, and production-readiness language

## How To Run

Open `index.html` in a browser:

```powershell
start projects\qa-portfolio-auditor\index.html
```

The current prototype uses sample metadata defined in `script.js` and mirrored in `samples/portfolio_tools_sample.json` for review.

## What It Checks

For each portfolio tool, the auditor checks whether the tool has:

- A one-liner
- A status label
- A demo link or sample output
- A README/docs link
- Portfolio-safe disclaimer language
- An evidence focus
- Known limitations or safe boundary language
- No forbidden overclaim phrases

## Forbidden Claim Examples

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

## Required Safe Language Examples

The auditor encourages portfolio-safe phrases such as:

- portfolio-safe
- mock data
- mock Unreal-style telemetry
- human-reviewed
- Markdown export
- Jira-ready reports
- risk summaries
- evidence packs
- external QA coordination

## Portfolio-Safe Boundary

This tool reviews sample portfolio metadata. It does not use private studio data, connect to Unreal, connect to Jira, run automated browser checks, or replace human review. Its value is showing the audit model: clear evidence, safe wording, missing-item checks, and recommended next actions.

## Known Limitations

- Static browser prototype only.
- No full browser automation.
- No live link crawling.
- No repository-wide text parsing yet.
- Sample data is intentionally small and portfolio-safe.
- Human review is still required before publishing.

## Future Improvements

- Add import/export JSON.
- Add optional live link status checks.
- Add a repository text scan mode.
- Add screenshot-based manual review fields.
- Add saved audit history for before/after portfolio passes.
