# QA Bug Report Tool

## Status

First version. This is a beginner-friendly Python CLI practice project for a learning portfolio.

## Goal

Turn rough QA notes into a structured Markdown bug report.

This project connects my interest in games with practical software habits. Games depend on clear feedback, reliable systems, and careful observation. This tool is a small way to practice writing QA notes clearly while I keep learning Python, GitHub, documentation, and AI-assisted workflows in public.

This is a practice coding project, separate from my professional shipped-title QA work. It is meant to show how I am connecting real QA habits with Python, testing, documentation, and AI-assisted workflow practice.

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
- Notes

If a rough note leaves out a field, the tool marks it as `Not provided` instead of guessing.

Severity and priority values are cleaned up when they use common wording or shorthand. For example, `med` becomes `Medium`, and `P1` becomes `High`. If the tool does not recognize a value, it keeps the original text and adds a warning in the Notes section.

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

## Notes

This could confuse a player because the UI suggests the item was not used.
```

## Run the Tool

From this project folder:

```powershell
python -m pip install -e .
python -m bug_report_tool sample-data/001-inventory-count-note.txt
```

Write the report to a file:

```powershell
python -m bug_report_tool sample-data/001-inventory-count-note.txt --output reports/new-report.md
```

Convert every `.txt` note in `sample-data/` into matching `.md` files in `reports/`:

```powershell
python -m bug_report_tool --batch
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

## Sample Bugs

The `sample-data/` folder contains five rough practice notes. The `reports/` folder contains matching structured Markdown reports.

These samples are fictional practice data. They are here to make the project easier to test, explain, and improve.

## What I Practiced

- Building a small command-line tool with Python
- Organizing code with a simple `src/` package layout
- Turning unstructured notes into a repeatable Markdown format
- Converting a folder of rough notes with batch mode
- Normalizing common severity and priority values without hiding unknown input
- Writing pytest coverage for parser, formatter, and CLI behavior
- Keeping a project README clear enough for a beginner to maintain

## Future Improvements

- Add a `--template` option for different report formats
- Add screenshots or attachment links as optional report fields
