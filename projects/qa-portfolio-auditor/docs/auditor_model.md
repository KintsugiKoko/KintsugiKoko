# QA Portfolio Auditor Model

## Purpose

QA Portfolio Auditor is a portfolio-safe self-audit prototype. It reviews local/static sample metadata for portfolio tools and asks whether each tool is working, clearly documented, safe from overclaiming, and easy for recruiters to review.

This is not a production validation system, not a full browser automation suite, not a live-site crawler, and not a replacement for manual review.

## Inputs

Each tool record includes:

- Tool name
- Project category
- Demo link or sample output
- README/docs link
- One-liner
- Status label
- Evidence focus
- Required safe phrases
- Forbidden phrases
- Required artifacts
- Expected artifact/link evidence
- Known limitations

Expected artifact/link evidence uses this shape:

- `label`: human-readable artifact name
- `path`: local repo path or portfolio page path
- `type`: documentation, demo, case-study, sample-output, tests, reports, or similar
- `status`: Present, Missing, or Needs Review
- `recommendedAction`: the next small cleanup step if the artifact is missing or needs review

## Checks

The prototype checks whether each portfolio tool has:

- One-liner
- Status label
- Demo link or sample output
- README/docs link
- Portfolio-safe disclaimer
- Evidence focus
- Known limitations or safe boundary language
- Expected artifact/link evidence metadata
- Present / Missing / Needs Review status for expected artifacts
- No forbidden overclaim phrases in the audited claim text

## Status Model

| Status | Meaning |
| --- | --- |
| Pass | Required metadata is present and no forbidden claim text was found. |
| Pass with Notes | The tool is reviewable but one or more safe-language or metadata items should be tightened. |
| Needs Review | A critical link/sample output is missing or forbidden claim language was found. |

Artifact status is intentionally separate from live deployment validation:

| Artifact Status | Meaning |
| --- | --- |
| Present | The sample metadata says the expected local artifact or link target exists. |
| Missing | The sample metadata says the expected artifact has not been created or saved yet. |
| Needs Review | The artifact is listed, but a human should confirm it is current, accurate, or useful for recruiter review. |

## Forbidden Claim Examples

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

## Safe Language Examples

- portfolio-safe
- mock data
- mock Unreal-style telemetry
- human-reviewed
- Markdown export
- Jira-ready reports
- risk summaries
- evidence packs
- external QA coordination

## Human Review Boundary

The audit result is a draft signal. Keith still owns the final review before publishing portfolio claims. A passing card means the sample metadata looks ready for review, not that every live link, browser path, artifact, deployment, or project behavior has been perfectly validated.

In the browser demo, artifact existence is metadata-driven. The repo also includes `scripts/audit-portfolio-artifacts.js`, which checks the listed local paths and writes `reports/local-artifact-check.md`. That script is still a local artifact check rather than live-site crawling or production deployment validation.
