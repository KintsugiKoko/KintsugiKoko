from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Message:
    role: str
    content: str
    created_at: str | None = None


@dataclass(frozen=True)
class Conversation:
    title: str
    messages: list[Message]
    source_path: Path
    source_id: str
    created_at: str | None = None
    updated_at: str | None = None
