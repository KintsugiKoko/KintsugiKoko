# QA Portfolio Auditor

**Status:** Portfolio-safe prototype  
**Live demo:** [QA Portfolio Auditor](../../docs/qa-portfolio-auditor.html)

QA Portfolio Auditor checks my portfolio tools for demo readiness, documentation coverage, recruiter-safe wording, evidence completeness, and overclaim risk before publishing.

## Purpose

This is a meta-QA tool for my Senior QA / Technical QA / Art QA portfolio. It answers:

> Are my QA portfolio tools working, clearly documented, safe from overclaiming, and easy for recruiters to review?

The tool audits portfolio tool metadata and wording for review readiness. It does not replace manual review, does not perform full browser automation, and does not claim perfect validation.

## What It Checks

- One-liner exists
- Status label exists
- Demo link or sample output exists
- README/docs link exists
- Portfolio-safe disclaimer exists
- Evidence focus exists
- Known limitations or safe boundary language exists
- Forbidden claims are avoided
- Required artifacts are present

## Portfolio-Safe Boundaries

- Uses sample portfolio metadata only.
- Does not use private studio data.
- Does not browse the web or perform full browser automation.
- Does not replace manual review.
- Does not claim perfect release readiness.
- Does not include Hearthstone in Art QA / telemetry scope.

## Local Preview

Open either file directly in a browser:

```text
projects/qa-portfolio-auditor/index.html
docs/qa-portfolio-auditor.html
```

The project page is kept near its README for source review. The `docs/` page is the GitHub Pages-facing demo used by the portfolio homepage.

## Sample Data

- [portfolio_tools_sample.json](samples/portfolio_tools_sample.json)

The sample data includes current portfolio tools and one watchlist entry for QA Capture Review Board because that project is not present on this branch.

## Documentation

- [Auditor Model](docs/auditor_model.md)
- [Sample Output](docs/sample_output.md)

## Known Limitations

- This is a static browser prototype.
- Link checks are metadata-based, not network or filesystem verification.
- Browser automation is not implemented.
- Manual review is still required before publishing.
- The current audit rules are intentionally simple and transparent.
