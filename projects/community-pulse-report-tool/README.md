# Community Pulse Report Tool

## Status

Demo-ready local reporting prototype.

Community Pulse is a local CSV-based reporting support prototype for organizing fictional or manually prepared community feedback into QA-aware, human-reviewed Markdown summaries.

This project assumes feedback has already been collected or manually prepared by a human reviewer. It does not scrape platforms, monitor communities, discover conversations, ingest live data, or perform automated moderation. It does not connect to EA systems, Discord, Reddit, forums, social media APIs, private APIs, internal tools, proprietary data, scraped data, or live community sources.

## Goal

Turn fictional or manually prepared community feedback CSV data into a structured Markdown feedback review report.

The project models a real workflow problem: when a game has high engagement, manually prepared feedback notes can pile up across posts, accounts, forums, streams, or community discussions. This prototype practices organizing those local records into a reviewable shape with local CSV files, simple filters, transparent counts, exact representative quotes, and human follow-up notes.

It is not a social listening platform, not a scraper, not an automated moderation tool, not an automated decision-maker, and not a replacement for community judgment.

## What Problem This Models

A community manager, QA partner, or producer may need to answer questions like:

- What local feedback records came in under this fictional account or post?
- What topics are showing repeated concern?
- Are players split on the same feature?
- Which exact quotes should a human reviewer inspect?
- What follow-up should QA, design, production, or community review next?

This tool keeps that workflow portfolio-safe by using local CSV fields instead of live platform connections.

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

> Collect all feedback posted under these fictional accounts and fictional social posts, then summarize the themes, sentiment split, representative quotes, and suggested follow-ups.

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
python -m community_pulse sample-data/high-engagement-feedback-sample.csv --post-id mock-post-001 --output reports/high-engagement-report.md
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

The tool is designed to stay local, deterministic, and inexpensive to run. It parses the CSV once, normalizes rows once, then reuses that data for filtering, counts, quote selection, and Markdown formatting.

It does not use LLM calls, embeddings, vector databases, external search, scraping, or live integrations.

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

> Portfolio-safe prototype report generated from fictional sample data.

## Executive Summary

- Total local feedback records reviewed: **20**
- Strongest positive area: **Fishing timing** (3 items)
- Strongest mixed area: **Fishing timing** (2 items)
- Strongest negative area: **Onboarding clarity** (3 items)
- This report is a draft aid for human review, not an automated community decision.
```

## Use Your Own Local CSV

You can test the tool with your own local CSV if you manually prepare or export feedback into the documented format.

Use the template:

[sample-data/feedback-template.csv](sample-data/feedback-template.csv)

Important boundaries:

- Run the tool locally against a CSV file you are allowed to use.
- Do not paste private, proprietary, confidential, or NDA-covered feedback into a public repo.
- The tool does not fetch from live platforms.
- The tool does not scrape social media.
- The tool does not use private API access.
- You are responsible for permission, privacy, context, and human review when using your own data.

## What The Tool Does Not Do

- Does not connect to live community platforms.
- Does not scrape Discord, Reddit, forums, social media, or websites.
- Does not monitor live communities.
- Does not ingest live conversations.
- Does not discover posts.
- Does not connect to private APIs, internal systems, or company tools.
- Does not infer sentiment with AI or machine learning.
- Does not moderate communities.
- Does not make automated player decisions or decide product direction.
- Does not generate screenshots, visual evidence, art, avatars, or media.
- Does not replace community manager, QA, design, production, or leadership judgment.

## External QA Handoff Value

A future saved External QA handoff sample export would strengthen the portfolio story because it would show the tool doing more than summarizing feedback. It would turn community signals into a clean, reviewable artifact that QA partners can act on. For QA Lead and Technical QA roles, that would demonstrate cross-functional thinking, traceability, prioritization, evidence handling, and handoff discipline without needing live data, private systems, or extra explanation.

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
|   `-- test_report.py
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

Run tests from this project directory:

```powershell
python -m pytest
```

## Safety And Limitations

- Built-in sample data is fictional and created for portfolio practice.
- Optional account, post, keyword, topic, and conversation fields are local demo metadata only.
- Sentiment is read from the CSV label. The tool does not infer sentiment with AI or machine learning.
- Counts are simple summaries, not product decisions.
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

This project connects QA thinking with community management workflow awareness. It practices structured data parsing, input validation, filtering, sentiment summarization, conflicting opinion review, exact quote preservation, documentation, and visible limitations.

That makes it useful as a beginner Python project and as a small example of how tooling can support communication without pretending to automate the human parts of community work.
