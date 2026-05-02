# QA Bug Report Tool

## Status

First version, in progress as a beginner-friendly QA portfolio tool.

Done:

- Converts rough QA notes into structured Markdown bug reports
- Supports single-note input, stdin input, and batch conversion
- Includes sample notes, generated reports, pytest coverage, and README examples
- Supports JSON export for structured output review
- Supports optional evidence fields for screenshots, logs, videos, or attachment links

Next:

- Keep improving validation rules as more realistic QA note examples are added
- Add richer report templates later if they stay simple to maintain

## Goal

Turn rough QA notes into structured Markdown bug reports.

This project connects my interest in games with practical software habits. Games depend on clear feedback, reliable systems, and careful observation. This tool is a small way to practice writing QA notes clearly while I keep learning Python, GitHub, documentation, and AI-assisted workflows in public.

This is a practice coding project, separate from my professional shipped-title QA work. It is meant to show how I am connecting real QA habits with Python, testing, documentation, and AI-assisted workflow practice.

## Why This Matters for QA

This project shows a small but practical QA workflow: take messy notes, preserve important details, structure the report, validate common fields, and create output that another person could review or act on.

## AI Assistance

AI assistance was used as a learning and workflow support tool for this project. It helped with planning the file structure, drafting beginner-friendly documentation, checking edge cases, and writing pytest coverage.

I am still learning Python, testing, and command-line tool design. The goal is not to hide the use of AI or overstate my experience. The goal is to use AI responsibly while I practice reading code, asking better questions, testing behavior, and documenting what the project does.

## What It Does

The CLI accepts one plain text note, or a folder of plain text notes, and generates Markdown reports with:

- Title
- Severity
- Priority
- Environment
- Steps to reproduce
- Expected result
- Actual result
- Repro rate
- Evidence / attachments
- Notes

If a rough note leaves out a field, the tool marks it as `Not provided` instead of guessing.

Severity and priority values are cleaned up when they use common wording or shorthand. For example, `med` becomes `Medium`, and `P1` becomes `High`. If the tool does not recognize a value, it keeps the original text and adds a warning in the Notes section.

Evidence fields are optional. The parser accepts labels such as `Evidence`, `Attachments`, `Screenshots`, `Videos`, or `Logs` and keeps those items with the generated report.

Markdown is the default output format. JSON output is also available when a structured export is easier to inspect or reuse.

## Validation Reference

Severity values are normalized like this:

| Input values | Normalized value |
| --- | --- |
| `low`, `minor` | `Low` |
| `med`, `medium`, `moderate` | `Medium` |
| `high`, `major` | `High` |
| `blocker`, `crit`, `critical` | `Critical` |

Priority values are normalized like this:

| Input values | Normalized value |
| --- | --- |
| `p3`, `low` | `Low` |
| `p2`, `med`, `medium`, `normal` | `Medium` |
| `p1`, `high`, `urgent` | `High` |
| `p0`, `crit`, `critical` | `Critical` |

For a before-and-after example with unknown values, see [examples/unknown-validation-note.txt](examples/unknown-validation-note.txt) and [examples/unknown-validation-report.md](examples/unknown-validation-report.md).

## Project Structure

```text
qa-bug-report-tool/
|-- README.md
|-- CHANGELOG.md
|-- pyproject.toml
|-- examples/
|   |-- README.md
|   |-- unknown-validation-note.txt
|   `-- unknown-validation-report.md
|-- sample-data/
|   |-- 001-inventory-count-note.txt
|   |-- 002-settings-save-note.txt
|   |-- 003-profile-link-note.txt
|   |-- 004-quest-checklist-note.txt
|   `-- 005-mobile-menu-note.txt
|-- reports/
|   |-- 001-inventory-count.md
|   |-- 002-settings-save.md
|   |-- 003-profile-link.md
|   |-- 004-quest-checklist.md
|   `-- 005-mobile-menu.md
|-- src/
|   `-- bug_report_tool/
|       |-- __init__.py
|       |-- __main__.py
|       |-- cli.py
|       |-- json_output.py
|       |-- markdown.py
|       |-- models.py
|       `-- parser.py
`-- tests/
    |-- test_cli.py
    |-- test_markdown.py
    `-- test_parser.py
```

## Example Input

```text
Title: Inventory count does not update after using potion
Severity: Medium
Priority: Medium
Environment: Windows 11, Chrome, practice inventory page
Steps:
1. Open the inventory screen.
2. Use one health potion.
3. Look at the potion count.
Expected: Potion count decreases by one.
Actual: Potion count stays the same until the page refreshes.
Repro Rate: 3/3
Evidence:
- screenshots/inventory-count-before-after.png
- logs/inventory-ui-refresh.log
Notes: This could confuse a player because the UI suggests the item was not used.
```

## Example Output

```markdown
# Inventory count does not update after using potion

| Field | Details |
| --- | --- |
| Severity | Medium |
| Priority | Medium |
| Environment | Windows 11, Chrome, practice inventory page |
| Repro Rate | 3/3 |

## Steps to Reproduce

1. Open the inventory screen.
2. Use one health potion.
3. Look at the potion count.

## Expected Result

Potion count decreases by one.

## Actual Result

Potion count stays the same until the page refreshes.

## Evidence / Attachments

- screenshots/inventory-count-before-after.png
- logs/inventory-ui-refresh.log

## Notes

This could confuse a player because the UI suggests the item was not used.
```

## Demo

Command:

```powershell
python -m bug_report_tool sample-data/001-inventory-count-note.txt
```

Sample terminal output:

```text
# Inventory count does not update after using potion

| Field | Details |
| --- | --- |
| Severity | Medium |
| Priority | Medium |
| Environment | Windows 11, Chrome, practice inventory page |
| Repro Rate | 3/3 |

## Steps to Reproduce

1. Open the inventory screen.
2. Use one health potion.
3. Look at the potion count.
```

## Run the Tool

From this project folder:

```powershell
python -m pip install -e .
python -m bug_report_tool --help
python -m bug_report_tool sample-data/001-inventory-count-note.txt
```

Markdown is the default format. You can write it out explicitly:

```powershell
python -m bug_report_tool sample-data/001-inventory-count-note.txt --format markdown
```

Write the report to a file:

```powershell
python -m bug_report_tool sample-data/001-inventory-count-note.txt --output reports/new-report.md
```

Generate JSON instead of Markdown:

```powershell
python -m bug_report_tool sample-data/001-inventory-count-note.txt --format json
```

Convert every `.txt` note in `sample-data/` into matching `.md` files in `reports/`:

```powershell
python -m bug_report_tool --batch
```

Batch mode can also write JSON reports:

```powershell
python -m bug_report_tool --batch --format json
```

Use custom folders for batch mode:

```powershell
python -m bug_report_tool --batch --input-dir sample-data --output-dir reports
```

Batch mode keeps filenames readable. For example, `001-inventory-count-note.txt` becomes `001-inventory-count.md`.

Pass note text directly:

```powershell
python -m bug_report_tool --text "Title: Button does not respond`nSeverity: Low`nActual: Nothing happens after clicking."
```

## Run Tests

```powershell
python -m pip install -e . pytest
python -m pytest
```

The tests cover parsing, Markdown formatting, JSON output, CLI output, stdin input, batch mode, validation warnings, and help text examples.

## Sample Bugs

The `sample-data/` folder contains five rough practice notes. The `reports/` folder contains matching structured Markdown reports.

These samples are fictional practice data. They are here to make the project easier to test, explain, and improve.

## What I Practiced

- Building a small Python CLI that converts rough QA notes into structured Markdown bug reports
- Organizing the project with a simple `src/` layout, sample data, generated reports, and examples
- Supporting single-note conversion, batch conversion, and readable output filenames
- Adding JSON export while keeping Markdown as the default output
- Normalizing common severity and priority values while preserving unknown input with warning notes
- Adding optional evidence fields for screenshots, logs, videos, and attachment links
- Writing pytest validation for parser, formatter, CLI, batch mode, and help text behavior
- Practicing Git recovery workflow: rejected Git push, `git status`, rebase, README conflict resolution, pytest validation, and safe pushing
- Keeping the README clear, honest, and useful for a QA Engineer portfolio project

## Future Improvements

- Add a `--template` option for different report formats
- Add richer evidence metadata, such as evidence type or capture notes
