# Obsidian Conversation Sync Agent

Status: first version, local-only practice project

This is a small Python CLI agent that turns exported AI conversation files into Obsidian-friendly Markdown notes.

It fits this learning portfolio because it connects AI-assisted workflows, documentation habits, and the public rebuild after the Intrepid career reset. The goal is not to hide the AI assistance. The goal is to turn useful conversations into reviewable notes, action items, and learning documentation.

## What It Does

- Reads local conversation exports from a folder
- Supports `.json`, `.md`, and `.txt` source files
- Handles common ChatGPT export-style JSON with `mapping` message data
- Writes one Markdown note per conversation into a `Conversations/` folder
- Creates an `AI Conversation Index.md` hub note for review and navigation
- Adds YAML frontmatter, tags, source information, and a human-review reminder
- Adds Obsidian wikilinks for project, learning log, topic, and related-note connections
- Keeps a small sync index so unchanged conversations are skipped on later runs
- Includes a dry-run mode so I can preview what would happen before writing files

## What It Does Not Do Yet

- It does not directly log into ChatGPT, Codex, Discord, Slack, or any private account.
- It does not automatically summarize conversations with an AI model.
- It does not replace human review before notes become portfolio documentation.

Those boundaries are intentional for this first version. The safest beginner version starts with exported files that I control.

## Why I Built It

AI conversations can contain useful explanations, debugging notes, project decisions, and next steps. If they stay buried in chat history, I lose the learning trail.

This agent helps me practice:

- Python file handling
- Command line arguments
- JSON parsing
- Markdown generation
- Obsidian note organization
- Repeatable documentation workflows
- Honest AI-assisted learning habits

That matters because my learning portfolio is not just about finished code. It is also about showing how I think, document, test, and improve over time.

## Folder Structure

```text
obsidian-conversation-sync-agent/
  config.example.json
  sample-data/
  src/
    obsidian_sync_agent/
  tests/
```

## Quick Start

From this project folder:

```powershell
python -m pip install -e .
python -m obsidian_sync_agent --source sample-data --vault "C:\Path\To\Obsidian Vault" --dry-run
```

If the dry run looks right, remove `--dry-run`:

```powershell
python -m obsidian_sync_agent --source sample-data --vault "C:\Path\To\Obsidian Vault"
```

By default, notes are written to:

```text
AI Conversation Notes/
  AI Conversation Index.md
  Conversations/
    2026-05-02-example-title-abc12345.md
```

inside the Obsidian vault.

## Config File Option

Copy `config.example.json` and adjust the paths:

```powershell
python -m obsidian_sync_agent --config config.example.json --dry-run
```

The config file uses simple JSON:

```json
{
  "source": "sample-data",
  "vault": "C:/Path/To/Obsidian Vault",
  "folder": "AI Conversation Notes",
  "tags": ["ai-conversation", "learning-notes", "needs-review"]
}
```

For daily local use, keep a private `config.local.json` beside `config.example.json`. That file is ignored by Git so local paths do not get committed.

Example local setup:

```json
{
  "source": "C:/Users/YourName/Documents/AI Conversation Exports",
  "vault": "C:/Users/YourName/Documents/Obsidian Vault",
  "folder": "AI Conversation Notes",
  "tags": ["ai-conversation", "learning-notes", "needs-review"]
}
```

## Daily Run

This project includes a PowerShell runner for scheduled syncs:

```powershell
.\scripts\run-daily-sync.ps1
```

The runner:

- Uses `config.local.json`
- Sets the project `src/` folder so the module can run without installing the package
- Uses normal Python when available
- Falls back to the bundled Codex Python runtime when normal Python is not installed

To feed the daily sync, export or save conversation files into:

```text
C:\Users\YourName\Documents\AI Conversation Exports
```

The daily job writes reviewed-note drafts into:

```text
C:\Users\YourName\Documents\Obsidian Vault\AI Conversation Notes
```

The first run may only create the index if the export folder is empty. That is expected.

## Source Files

This agent can read:

- A folder of `.json`, `.md`, or `.txt` files
- A single `.json`, `.md`, or `.txt` file
- A ChatGPT-style `conversations.json` export
- A simpler JSON file with `title` and `messages`

Example simple JSON:

```json
{
  "title": "Learning Git Branches",
  "messages": [
    {
      "role": "user",
      "content": "Explain branches using a game save comparison."
    },
    {
      "role": "assistant",
      "content": "A branch is like a separate save file where you can try changes safely."
    }
  ]
}
```

## Output Note Shape

The sync folder is organized as a small Obsidian hub:

```text
AI Conversation Notes/
  AI Conversation Index.md
  Conversations/
    synced-conversation-notes.md
  .sync-index.json
```

Each synced note includes:

- Frontmatter for Obsidian metadata
- A backlink to `[[AI Conversation Index]]`
- A clear synced-source callout
- A placeholder summary section
- A connections section for project, learning log, topic, and related-note links
- A useful takeaways section
- A decisions, commands, or prompts section
- Follow-up checkboxes
- The conversation transcript

The summary is intentionally left for human review. That keeps the documentation honest and gives me a learning exercise after each sync.

The generated index note includes:

- A review queue of synced conversation notes
- Source file and sync-time details
- A short review workflow
- Common hub links like `[[Projects]]`, `[[Learning Journey]]`, and `[[AI-Assisted Workflows]]`

## Run Tests

From this project folder:

```powershell
python -m pip install -e . pytest
python -m pytest
```

## Next Improvements

- Add a command that imports directly from a chosen export file path
- Add optional conversation filters by date or tag
- Add an optional AI summarization step with clear review labels
- Add an Obsidian template setting
- Add a learning log entry about what was confusing while building this
