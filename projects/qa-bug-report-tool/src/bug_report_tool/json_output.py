"""Format bug reports as JSON."""

from __future__ import annotations

import json
from dataclasses import asdict

from bug_report_tool.models import BugReport


def format_json(report: BugReport) -> str:
    """Return a JSON bug report."""

    return json.dumps(asdict(report), indent=2)
