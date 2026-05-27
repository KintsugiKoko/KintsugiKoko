# Local Maintenance Helpers

This folder is for local-only repair tools that support Keith's Codex workspace.

These helpers are not part of the public portfolio workflow, project roadmap, learning evidence, or recruiter-facing story. They exist only to repair local Codex Desktop state when recurring automations or session metadata create sidebar clutter.

Do not present this folder as proof of productivity, portfolio progress, product value, or a project feature. It is workspace hygiene only.

## Codex Automation Sidebar Policy

`codex_automation_sidebar_policy.py` consolidates repeated recurring automation sidebar rows for:

- `Daily Obsidian conversation sync`
- `Overnight portfolio goal`

The helper keeps one canonical active thread per automation title, archives older active session files when needed, and updates local automation prompts/config so ordinary recurring runs prefer concise inbox/status output.

This is a developer-only utility for automation clutter repair. It should stay out of portfolio evidence logs, showcase notes, badges, screenshots, and public-facing project documentation.

Dry-run is the default:

```powershell
python .\tools\local-maintenance\codex_automation_sidebar_policy.py
```

To write changes, use both explicit flags:

```powershell
python .\tools\local-maintenance\codex_automation_sidebar_policy.py --apply --confirm APPLY_LOCAL_CODEX_AUTOMATION_POLICY
```

Optional local hygiene flags:

```powershell
python .\tools\local-maintenance\codex_automation_sidebar_policy.py --date-active-rows --project-root "C:\Users\mcavo\OneDrive\Documents\Cron Jobs"
```

`--date-active-rows` prefixes matching sidebar rows with the row date, such as `2026-05-27 - Daily Obsidian conversation sync`, so recurring automation chats are easier to scan.

`--project-root` updates matching sidebar/project routing metadata for existing automation chats. It does not change the automation execution workspace, because the actual job may still need to run from the configured project repo.

Before any write, the helper creates backups under:

```text
C:\Users\mcavo\.codex\backups\
```

Do not add this helper to the main README unless the repository becomes specifically about Codex workspace management.
