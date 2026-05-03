# Second Brain Docs Agent

Status: early MVP, local-only, draft-only.

Second Brain Docs Agent is a local-first documentation helper built to turn Obsidian notes and exported chat transcripts into structured Markdown drafts for human review.

This early MVP is intentionally conservative: it runs locally, requires no API keys, does not publish externally, and keeps all output in draft form. The goal is to help organize daily learning notes, project updates, decisions, action items, and portfolio-worthy proof into clearer documentation before anything is shared.

MVP boundaries:

- local-only
- draft-only
- no external publishing yet
- no API keys required
- no real Confluence credentials
- human review before anything is shared

## Short Project Summary

This tool reads notes from an Obsidian-style folder and chat exports from a local folder, extracts simple documentation signals, and writes Markdown drafts into `docs/drafts/`.

It can help turn raw learning material into first-pass drafts for:

- daily summaries
- weekly review summaries
- project updates
- portfolio updates
- Codex task prompts

The drafts are not final writing. They are a starting point for review.

## Project Card Description

Second Brain Docs Agent is a local-only documentation helper that turns Obsidian notes and exported chat transcripts into structured Markdown drafts for human review. This early MVP is intentionally draft-only, requires no API keys, and does not publish externally yet. It demonstrates QA-minded workflow design, documentation discipline, and practical agentic engineering for organizing project updates, decisions, tasks, and portfolio evidence.

## Recruiter-Friendly Project Summary

Second Brain Docs Agent is an early local-first documentation helper that turns Obsidian notes and exported chat transcripts into structured Markdown drafts. It is draft-only, requires no API keys, does not publish externally yet, and keeps human review before anything is shared.

As a portfolio project, it demonstrates QA-minded workflow design, documentation discipline, and practical agentic engineering by turning scattered learning notes, project decisions, action items, and conversation exports into reviewable documentation without pretending the drafts are final output.

## Resume / LinkedIn Summary

Resume bullet:

- Built a local-only, draft-only documentation automation MVP that converts Obsidian notes and exported chat transcripts into human-reviewed Markdown drafts, demonstrating QA-minded workflow design, documentation discipline, and practical agentic engineering without API keys or external publishing.

LinkedIn project blurb:

Second Brain Docs Agent is a local-first documentation automation MVP I built to support my QA/game-dev and agentic engineering workflow.

The tool turns Obsidian notes and exported chat transcripts into structured Markdown drafts for human review. It is intentionally conservative in this MVP stage: local-only, draft-only, no API keys, and no external publishing yet.

The project reflects how I approach tooling as a QA-minded builder: capture messy work, extract decisions and tasks, create reviewable documentation, and turn scattered learning into reusable project and portfolio evidence.

## Why I Built It

I use Obsidian to track Journey Journal entries, weekly reviews, project notes, prompt logs, and learning-in-public reflections. A lot of useful evidence starts in messy notes: what I built, what confused me, what I tested, what decisions I made, and what should happen next.

I built this MVP to practice turning that raw learning trail into clearer documentation without losing the original notes. It supports my QA/game-dev and agentic engineering workflow by turning scattered notes and conversations into reviewable project documentation, portfolio update drafts, and future Codex task prompts.

The goal is not to replace human judgment. The goal is to make review easier.

## What It Does Right Now

The MVP currently:

- reads local Markdown files from an Obsidian-style folder
- extracts simple frontmatter when present
- supports sample daily notes, weekly reviews, project pages, and prompt logs
- reads local `.md`, `.txt`, and `.json` chat export files
- normalizes notes and chat exports into Python objects
- extracts simple deterministic signals:
  - summary
  - action items
  - decisions
  - open questions
  - portfolio-worthy proof
  - suggested next Codex prompt
- renders structured Markdown drafts into `docs/drafts/`
- includes a Confluence placeholder that is disabled and dry-run only
- includes tests for the core behavior

This first version uses deterministic rules instead of an LLM API. That keeps it easier to inspect, easier to test, and safer for private notes.

## What Skills This Demonstrates

This project is small, but it shows practical workflow thinking.

QA skills:

- separating raw input from generated output
- writing tests for ingestion and rendering behavior
- reducing false positives in action item extraction
- keeping publishing disabled until there is a review step
- documenting known limitations clearly

Game-dev learning connection:

- turning Nyx prototype notes into draft project updates
- capturing WIP systems without claiming they are finished
- connecting prototype work to verification notes and portfolio evidence

Agentic engineering skills:

- designing a local-first agent workflow
- keeping automation draft-only by default
- avoiding real credentials in the repo
- making future publishing an explicit, reviewed step
- using simple modules that can be improved over time

Documentation skills:

- converting raw notes into structured Markdown
- preserving human review before sharing
- making project status and limitations visible

## Draft-Only Mode

Draft-only means:

- generated files stay local in `docs/drafts/`
- nothing is sent to Confluence
- nothing is published to GitHub Pages
- no external APIs are called
- no API keys are required
- no real credentials are stored
- a human reviews the draft before it becomes public

## Project Structure

```text
second-brain-docs-agent/
+-- AGENTS.md
+-- README.md
+-- .env.example
+-- pyproject.toml
+-- data/
|   +-- obsidian_sample/
|   +-- chatgpt_sample/
+-- docs/
|   +-- drafts/
|   +-- templates/
+-- src/
|   +-- ingest/
|   +-- extract/
|   +-- render/
|   +-- publish/
|   +-- main.py
+-- tests/
```

## Setup

From this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

The runtime code uses only the Python standard library. `pytest` is needed for tests.

## Run The MVP Locally

```powershell
python -m src.main --obsidian-dir data/obsidian_sample --chatgpt-dir data/chatgpt_sample --output-dir docs/drafts
```

This generates local Markdown drafts from the sample Obsidian notes and sample chat transcript.

## Run Tests

```powershell
python -m pytest
```

## Add Obsidian Notes

For local testing, copy Markdown notes into `data/obsidian_sample/` or point the CLI at another local folder:

```powershell
python -m src.main --obsidian-dir "C:\Path\To\Your\Vault\Journey Journal" --chatgpt-dir data/chatgpt_sample --output-dir docs/drafts
```

Supported note styles:

- daily Journey Journal entries
- weekly reviews
- project pages
- prompt notes

Frontmatter is optional. When present, simple properties like `type`, `tags`, `project`, and `review_status` are extracted.

## ChatGPT Export Notes

Place local `.md`, `.txt`, or `.json` exports in `data/chatgpt_sample/` for testing. This is local-only. No export is uploaded anywhere.

## Current Limitations

- The extraction logic is simple and deterministic.
- Summaries are first-pass drafts, not polished writing.
- The tool can miss context that a human would understand.
- It may still need better rules for larger real Obsidian vaults.
- It does not publish to Confluence.
- It does not call an LLM API.
- It does not edit original Obsidian notes.
- It does not decide what should become public.

## Future Improvements

Possible next steps:

- add a local config file for selecting safe Obsidian folders
- improve note classification for real vault structures
- add more tests for empty notes, missing frontmatter, and unusual chat exports
- add a review-only mode that suggests links and tags without editing notes
- add a human approval checklist before any future publishing workflow
- add optional LLM summarization later, only after privacy and API-key handling are designed carefully
- keep Confluence publishing disabled until dry-run behavior and review gates are proven

## Future Confluence Publishing Plan

`src/publish/confluence.py` is a placeholder. It defaults to disabled and dry-run behavior.

Future publishing would need environment variables such as:

- `CONFLUENCE_BASE_URL`
- `CONFLUENCE_SPACE_KEY`
- `CONFLUENCE_PARENT_PAGE_ID`
- `CONFLUENCE_EMAIL`
- `CONFLUENCE_API_TOKEN`

Do not add real values to this repository. Use `.env.example` only as documentation.

## Next Recommended Codex Tasks

1. Add a local config file that points to selected folders without committing private paths.
2. Add richer note classification for Journey Journal, weekly review, project update, and prompt log notes.
3. Add a review-only mode that suggests tags and links without modifying original notes.
4. Add a human approval step before any future Confluence publishing code.
5. Add more tests for edge cases such as missing frontmatter, empty notes, and unusual ChatGPT JSON exports.

## Portfolio-Safe Summary

Second Brain Docs Agent is an early local-first documentation MVP. It shows practice with Python file ingestion, Markdown rendering, deterministic extraction, tests, and privacy-minded automation. It is useful as a workflow prototype, but it is not a publishing system yet.
