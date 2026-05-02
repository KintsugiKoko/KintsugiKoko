"""Create a reusable QA workspace folder."""

from __future__ import annotations

from pathlib import Path

QA_SUBFOLDERS = ("notes", "reports", "checklists", "test-runs")

QA_README = """# QA Workflow

This folder is a lightweight QA workspace for a project.

## Folder Map

- `notes/` - rough notes captured while testing
- `reports/` - structured bug reports generated from notes
- `checklists/` - repeatable test passes, smoke checks, or release checks
- `test-runs/` - short records of test commands, results, and follow-up items

## Suggested Workflow

1. Capture rough observations in `notes/`.
2. Convert notes into structured reports in `reports/`.
3. Use `checklists/` for repeatable coverage.
4. Save important test run summaries in `test-runs/`.
5. Check `git status` before committing QA artifacts.

## Useful Commands

```powershell
python -m bug_report_tool qa/notes/example-note.txt --output qa/reports/example-report.md
python -m bug_report_tool --batch --input-dir qa/notes --output-dir qa/reports
python -m pytest
```

This folder is meant to support clear QA habits. It is not a production-grade QA system.
"""


def init_qa_workspace(qa_dir: str | Path = "qa") -> Path:
    """Create a beginner-friendly QA folder structure."""

    qa_path = Path(qa_dir)
    qa_path.mkdir(parents=True, exist_ok=True)

    for folder_name in QA_SUBFOLDERS:
        (qa_path / folder_name).mkdir(exist_ok=True)

    readme_path = qa_path / "README.md"
    if not readme_path.exists():
        readme_path.write_text(QA_README, encoding="utf-8")

    return qa_path
