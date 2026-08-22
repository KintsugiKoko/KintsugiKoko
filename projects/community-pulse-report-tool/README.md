# Community Pulse Report Tool

## Status

Demo-ready local reporting prototype.

Community Pulse is a local CSV-based reporting prototype that turns fictional, manually prepared, or permissioned feedback records into QA-aware Markdown summaries for review and routing.

The workflow begins after an authorized reviewer has collected or prepared the input. Analysis is local and deterministic, sentiment comes from the CSV label, and decisions remain with the community, QA, design, and production partners reviewing the report.

## Goal

Turn fictional or manually prepared community feedback CSV data into a structured Markdown feedback review report.

The project models a real workflow problem: when a game has high engagement, manually prepared feedback notes can pile up across posts, accounts, forums, streams, or community discussions. The tool organizes those local records with simple filters, transparent counts, exact representative quotes, and clear follow-up notes.

## What Problem This Models

A community manager, QA partner, or producer may need to answer questions like:

- What local feedback records came in under this fictional account or post?
- What topics are showing repeated concern?
- Are players split on the same feature?
- Which exact quotes should a human reviewer inspect?
- What follow-up should QA, design, production, or community review next?

The current implementation uses local CSV input so each record, filter, quote, and count stays auditable.

## What It Does

The CLI reads a CSV with these required columns:

- `date`
- `source`
- `game_area`
- `sentiment`
- `text`

It also accepts optional demo columns:

- `account`
- `post_id`
- `keyword`
- `topic`
- `conversation_id`

Older CSVs with only the required columns still work. Missing optional columns do not break the tool.

The generated Markdown report includes:

- Total feedback reviewed
- Filters applied, if any
- Sentiment snapshot
- Local feedback inputs
- Accounts and posts represented, when those fields exist
- Top mentioned topics or game areas
- Topic opinion splits when feedback is mixed across the same topic
- Positive, mixed, and negative themes
- Representative quotes copied exactly from the CSV `text` field
- Suggested human follow-ups
- Method and limitations

## Demo Workflow

The stronger demo file is:

[sample-data/high-engagement-feedback-sample.csv](sample-data/high-engagement-feedback-sample.csv)

It uses fictional accounts, fictional post IDs, repeated keywords, repeated topics, and positive, mixed, negative, and neutral sentiment labels.

Example scenario:

> Review all local feedback records tied to these fictional accounts and fictional post IDs, then summarize the themes, sentiment split, representative quotes, and suggested follow-ups.

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

## High-Engagement Demo Commands

Filter by a fictional keyword:

```powershell
python -m community_pulse sample-data/high-engagement-feedback-sample.csv --keyword onboarding
```

Filter by a fictional account and date range:

```powershell
python -m community_pulse sample-data/high-engagement-feedback-sample.csv --account mock-studio-account --start-date 2026-05-01 --end-date 2026-05-07
```

Filter by a fictional post ID and write a report:

```powershell
python -m community_pulse sample-data/high-engagement-feedback-sample.csv --post-id mock-post-001 --output reports/high-engagement-feedback-review-report.md
```

Available local filters:

- `--start-date`
- `--end-date`
- `--source`
- `--account`
- `--post-id`
- `--keyword`
- `--topic`

The source, account, post, keyword, and topic filters can be repeated.

## Output Limits And Lightweight Runtime

The tool is designed to stay local, deterministic, and inexpensive to run. It parses the CSV once, normalizes rows once, then reuses that data for filtering, counts, quote selection, and Markdown formatting. The current runtime is CSV input, deterministic Python analysis, and Markdown output.

Default report caps keep larger local CSVs readable:

| Option | Default | Purpose |
| --- | ---: | --- |
| `--max-quotes` | 8 | Limits representative quotes |
| `--max-topics` | 10 | Limits shown topics, sources, accounts, posts, and opinion splits |
| `--max-themes` | 5 | Limits positive, mixed, and negative theme lists |
| `--max-follow-ups` | 5 | Limits suggested human follow-ups |
| `--max-rows` | none | Optional demo/testing row limit for large local files |

Example:

```powershell
python -m community_pulse sample-data/high-engagement-feedback-sample.csv --max-quotes 6 --max-topics 5 --max-themes 3
```

When output is capped, the report says so with notes like:

- `Showing top 10 topics by mention count.`
- `Representative quotes limited to 8 for readability.`

## Example Output Snippet

```markdown
# Weekly Community Feedback Review Report

> Local prototype report generated from fictional sample data.

## Executive Summary

- Total local feedback records reviewed: **20**
- Strongest positive area: **Fishing timing** (3 items)
- Strongest mixed area: **Fishing timing** (2 items)
- Strongest negative area: **Onboarding clarity** (3 items)
- This report is prepared for human review, context checks, and follow-up routing.
```

## Use Your Own Local CSV

You can test the tool with your own local CSV if you manually prepare or export feedback into the documented format.

Use the template:

[sample-data/feedback-template.csv](sample-data/feedback-template.csv)

Input rules:

- Run the tool locally against a CSV file you are allowed to use.
- Do not paste private, proprietary, confidential, or NDA-covered feedback into a public repo.
- You are responsible for permission, privacy, context, and human review when using your own data.

## Current Scope

- Local CSV input from fictional, manually prepared, or permissioned records
- Deterministic filtering, counts, topic splits, and quote selection
- Exact quote preservation from the provided `text` field
- Markdown reports and saved handoff samples
- User-provided attribution and media references remain unchanged

Live collection, platform connectors, moderation, and product decisions remain outside the current tool scope.

## External QA Handoff Sample

Community Pulse includes a saved External QA handoff sample export:

[reports/external-qa-handoff-sample.md](reports/external-qa-handoff-sample.md)

The saved handoff shows how local feedback records become structured QA-ready context. It demonstrates cross-functional thinking, traceability, prioritization, evidence handling, and handoff discipline through a fictional review scenario.

## Project Structure

```text
community-pulse-report-tool/
|-- README.md
|-- AGENTS.md
|-- pyproject.toml
|-- sample-data/
|   |-- feedback-template.csv
|   |-- high-engagement-feedback-sample.csv
|   `-- weekly-feedback-sample.csv
|-- reports/
|   |-- external-qa-handoff-sample.md
|   |-- high-engagement-feedback-review-report.md
|   `-- weekly-sentiment-report.md
|-- src/
|   `-- community_pulse/
|       |-- __init__.py
|       |-- __main__.py
|       |-- analyzer.py
|       |-- cli.py
|       |-- filters.py
|       |-- models.py
|       |-- parser.py
|       `-- report.py
|-- tests/
|   |-- test_analyzer.py
|   |-- test_cli.py
|   |-- test_filters.py
|   |-- test_parser.py
|   |-- test_report.py
|   `-- test_user_facing_text.py
`-- .github/
    `-- workflows/
        `-- tests.yml
```

## What Was Tested

Pytest coverage includes:

- Parsing the original required-column CSV format
- Parsing newer CSVs with optional demo fields
- Missing optional fields do not fail
- Missing required columns fail clearly
- Empty required fields fail clearly
- Filtering by date range
- Filtering by source, account, post ID, keyword, and topic
- Optional `--max-rows` parsing limit
- Sentiment counts
- Topic/game-area counts
- Positive, mixed, and negative theme detection
- Topic opinion split counts
- Representative quotes preserve exact CSV text
- Representative quotes include negative and mixed feedback when present
- Configurable caps for quotes, topics, themes, and follow-ups
- Report sections for filters, accounts, posts, topic splits, follow-ups, and limitations
- CLI report generation from the high-engagement fictional sample
- Saved External QA handoff sample uses fictional data and visible limitations
- No em dash character in user-facing files or CLI help

Run tests from this project directory:

```powershell
python -m pytest
```

## Data Handling And Limitations

- Built-in sample data is fictional and created for this demonstration.
- Optional account, post, keyword, topic, and conversation fields are local demo metadata only.
- Sentiment is read from the supplied CSV label.
- Counts summarize the provided records and support, rather than determine, product decisions.
- Representative quotes are copied exactly from the CSV `text` field.
- A human reviewer should always decide what feedback is important, what needs escalation, and what context is missing.

## Future Improvements

- Add week-over-week comparison using two fictional CSV files
- Add CSV export for the summary counts
- Add reviewer notes to the generated report
- Add stricter sentiment label validation
- Add more fictional reporting scenarios
- Add a small static demo page if the portfolio needs a browser-based showcase later

## Why This Belongs In The Portfolio

This project connects QA systems thinking with community-management workflow awareness. It demonstrates structured data parsing, input validation, filtering, sentiment summaries, conflicting-opinion review, exact quote preservation, documentation, and clear routing boundaries.
