# Codex Instructions

This project is a portfolio-safe prototype for practicing community reporting workflows with fictional data.

## Scope

- Use fictional sample data only.
- Do not connect to EA systems, Discord, Reddit, forums, private APIs, internal tools, proprietary data, or scraped data.
- Keep the tool human-in-the-loop. It should assist reporting and triage, not replace community manager judgment.
- Keep the tone beginner-friendly, QA-aware, and community-management focused.

## Content Rules

- Do not imply the sample data came from real players, real communities, or real company systems.
- Label generated reports as based on fictional sample data.
- Keep limitations visible: sentiment is read from CSV labels, not inferred by AI or ML.
- Prefer small, clear Python modules over clever abstractions.
- Keep examples easy to inspect in Markdown and CSV.

## Review Checklist

- Required CSV columns are validated.
- Reports include method and limitations.
- Tests cover parsing, counts, area summaries, and Markdown generation.
- Any future integrations must remain mock/local unless explicitly approved and portfolio-safe.
