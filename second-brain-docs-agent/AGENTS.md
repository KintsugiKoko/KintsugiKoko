# Codex Instructions For Second Brain Docs Agent

This project is a draft-only local documentation helper for turning Obsidian notes and local chat exports into structured Markdown drafts.

## Safety And Privacy

- Preserve privacy by default.
- Never publish externally without an explicit user request in the current conversation.
- Do not ask for, store, invent, or commit real API keys.
- Do not add real Confluence credentials.
- Keep generated drafts local under `docs/drafts/` unless the user explicitly asks otherwise.
- Treat sample data as mock content only.

## Development Style

- Keep the project beginner-friendly.
- Prefer simple working Python over clever architecture.
- Keep modules small and readable.
- Add tests for behavior changes.
- Use deterministic extraction first; do not add LLM API calls until explicitly requested.
- Leave clear TODO comments where future LLM summarization or publishing could plug in.

## Verification

For meaningful changes, run:

```powershell
python -m pytest
python -m src.main --obsidian-dir data/obsidian_sample --chatgpt-dir data/chatgpt_sample --output-dir docs/drafts
```

If a command cannot run, say that clearly and explain what still needs to be checked.

## Handoff Habit

End summaries with:

- what changed
- what checks ran
- what drafts were generated
- what remains local, draft-only, or placeholder
- a suggested commit message
- one next prompt for Codex
- one next prompt for ChatGPT
