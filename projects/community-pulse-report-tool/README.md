# Community Pulse Report Tool

## Status

First version, in progress as a beginner-friendly Python portfolio project.

This tool uses fictional sample data only. It does not connect to EA systems, Discord, Reddit, forums, private APIs, internal tools, proprietary data, or live community sources.

## Goal

Turn fictional weekly community feedback CSV data into a structured Markdown sentiment report.

The project models a real workflow problem: community managers often need to turn scattered player feedback into readable summaries for production, QA, design, and leadership partners. This prototype practices the shape of that workflow with safe sample data, simple counts, and a human-in-the-loop report.

It is not a social listening platform, not an automated moderation tool, and not a replacement for community judgment. It is a small practice tool for understanding reporting bottlenecks, triage thinking, and clear communication.

## What It Does

The CLI reads a CSV with these required columns:

- `date`
- `source`
- `game_area`
- `sentiment`
- `text`

It then generates a Markdown report with:

- Total feedback item count
- Sentiment totals
- Feedback counts by source
- Feedback counts by game area
- Top positive areas
- Top negative areas
- Representative quotes
- Suggested human follow-ups
- Method and limitations

## Project Structure

```text
community-pulse-report-tool/
|-- README.md
|-- AGENTS.md
|-- pyproject.toml
|-- sample-data/
|   `-- weekly-feedback-sample.csv
|-- reports/
|   `-- weekly-sentiment-report.md
|-- src/
|   `-- community_pulse/
|       |-- __init__.py
|       |-- __main__.py
|       |-- analyzer.py
|       |-- cli.py
|       |-- models.py
|       |-- parser.py
|       `-- report.py
|-- tests/
|   |-- test_analyzer.py
|   |-- test_parser.py
|   `-- test_report.py
`-- .github/
    `-- workflows/
        `-- tests.yml
```

The portfolio repository also includes this project in the root GitHub Actions test matrix so pytest can run from the real repo structure.

## Example Input CSV

```csv
date,source,game_area,sentiment,text
2026-05-01,fictional-feedback-form,Fishing,positive,"The casting loop felt relaxing and easy to understand after the first try."
2026-05-01,mock-playtest-note,Onboarding,negative,"I did not understand why the first soul-form fish mattered until later."
2026-05-02,mock-community-digest,Merchant,positive,"Nyx being a merchant and ferryman sounds cozy and gives the run a personality."
```

The full fictional sample lives in [sample-data/weekly-feedback-sample.csv](sample-data/weekly-feedback-sample.csv).

## Example Output Snippet

```markdown
# Weekly Community Sentiment Report

> Portfolio-safe prototype report generated from fictional sample data.

## Executive Summary

- Total feedback items reviewed: **12**
- Strongest positive area: **Fishing** (1 item)
- Strongest negative area: **Onboarding** (2 items)
- This report is a draft aid for human review, not an automated community decision.
```

The generated sample report lives in [reports/weekly-sentiment-report.md](reports/weekly-sentiment-report.md).

## How To Run

From this project directory:

```powershell
python -m pip install -e .
python -m community_pulse sample-data/weekly-feedback-sample.csv --output reports/weekly-sentiment-report.md
```

You can also print the report to the terminal by leaving off `--output`:

```powershell
python -m community_pulse sample-data/weekly-feedback-sample.csv
```

## What Was Tested

Pytest coverage includes:

- CSV parsing with required columns
- Missing-column validation
- Empty required-field validation
- Sentiment counts
- Game area counts
- Top positive and negative area detection
- Representative quote selection
- Markdown report section generation
- Markdown report counts, quotes, and limitations

Run tests from this project directory:

```powershell
python -m pytest
```

## Safety And Limitations

- Sample data is fictional and created for portfolio practice.
- The tool does not fetch, scrape, or connect to live communities.
- Sentiment is read from the CSV label. The tool does not infer sentiment with AI or machine learning.
- Counts are simple summaries, not product decisions.
- A human reviewer should always decide what feedback is important, what needs escalation, and what context is missing.

## Future Improvements

- Add week-over-week comparison using two fictional CSV files
- Add optional topic tags for feedback themes
- Add a reviewer-notes section for human interpretation
- Add stricter sentiment label validation
- Add CSV export for the summary counts
- Add a small known-limitations table to the report
- Add more fictional samples that model different community reporting scenarios

## Why This Belongs In The Portfolio

This project connects QA thinking with community management workflow awareness. It practices reading structured data, validating inputs, summarizing patterns, preserving representative quotes, documenting limitations, and keeping human judgment visible.

That makes it useful as a beginner Python project and as a small example of how tooling can support communication without pretending to automate the human parts of community work.
