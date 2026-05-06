# QA Portfolio Auditor Model

## Purpose

QA Portfolio Auditor is a portfolio-safe self-audit prototype. It reviews sample metadata for portfolio tools and asks whether each tool is working, clearly documented, safe from overclaiming, and easy for recruiters to review.

This is not a production validation system, not a full browser automation suite, and not a replacement for manual review.

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
- Known limitations

## Checks

The prototype checks whether each portfolio tool has:

- One-liner
- Status label
- Demo link or sample output
- README/docs link
- Portfolio-safe disclaimer
- Evidence focus
- Known limitations or safe boundary language
- No forbidden overclaim phrases in the audited claim text

## Status Model

| Status | Meaning |
| --- | --- |
| Pass | Required metadata is present and no forbidden claim text was found. |
| Pass with Notes | The tool is reviewable but one or more safe-language or metadata items should be tightened. |
| Needs Review | A critical link/sample output is missing or forbidden claim language was found. |

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

The audit result is a draft signal. Keith still owns the final review before publishing portfolio claims. A passing card means the sample metadata looks ready for review, not that every live link, browser path, or project behavior has been perfectly validated.
