"""Data model for structured bug reports."""

from dataclasses import dataclass, field


@dataclass
class BugReport:
    """A structured bug report created from rough QA notes."""

    title: str
    severity: str = "Not provided"
    priority: str = "Not provided"
    environment: str = "Not provided"
    steps_to_reproduce: list[str] = field(default_factory=list)
    expected_result: str = "Not provided"
    actual_result: str = "Not provided"
    repro_rate: str = "Not provided"
    notes: str = "No additional notes."
