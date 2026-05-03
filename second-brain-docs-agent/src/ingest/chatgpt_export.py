"""Read local ChatGPT-style exports.

The MVP supports local `.md`, `.txt`, and `.json` files only. Nothing is sent
to an external service.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ChatMessage:
    """Normalized chat message."""

    role: str
    content: str


@dataclass(frozen=True)
class ChatSession:
    """Normalized local chat export."""

    title: str
    file_path: Path
    text: str
    messages: list[ChatMessage] = field(default_factory=list)
    modified_date: str | None = None


SUPPORTED_EXPORT_SUFFIXES = {".md", ".txt", ".json"}


def read_chatgpt_exports(folder: str | Path) -> list[ChatSession]:
    """Read local chat export files from a folder."""

    root = Path(folder)
    if not root.exists():
        raise FileNotFoundError(f"ChatGPT export folder does not exist: {root}")

    sessions: list[ChatSession] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXPORT_SUFFIXES:
            continue
        sessions.append(read_chatgpt_export(path))
    return sessions


def read_chatgpt_export(path: str | Path) -> ChatSession:
    """Read one local chat export."""

    export_path = Path(path)
    modified_date = datetime.fromtimestamp(export_path.stat().st_mtime).isoformat(timespec="seconds")
    suffix = export_path.suffix.lower()

    if suffix == ".json":
        return normalize_json_export(export_path, modified_date)

    text = export_path.read_text(encoding="utf-8").strip()
    return ChatSession(
        title=extract_text_title(text) or export_path.stem,
        file_path=export_path,
        text=text,
        messages=[ChatMessage(role="unknown", content=text)] if text else [],
        modified_date=modified_date,
    )


def normalize_json_export(path: Path, modified_date: str | None) -> ChatSession:
    """Normalize common JSON chat export shapes."""

    data = json.loads(path.read_text(encoding="utf-8"))
    title = path.stem
    messages: list[ChatMessage] = []

    if isinstance(data, dict):
        title = str(data.get("title") or title)
        if isinstance(data.get("messages"), list):
            messages = normalize_message_list(data["messages"])
        elif isinstance(data.get("mapping"), dict):
            messages = normalize_chatgpt_mapping(data["mapping"])
        elif isinstance(data.get("conversations"), list):
            for conversation in data["conversations"]:
                if isinstance(conversation, dict):
                    messages.extend(normalize_message_list(conversation.get("messages", [])))
    elif isinstance(data, list):
        messages = normalize_message_list(data)

    text = "\n\n".join(f"{message.role}: {message.content}" for message in messages if message.content)
    return ChatSession(title=title, file_path=path, text=text, messages=messages, modified_date=modified_date)


def normalize_message_list(raw_messages: list[Any]) -> list[ChatMessage]:
    """Normalize a list of simple message dictionaries."""

    messages: list[ChatMessage] = []
    for item in raw_messages:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or item.get("author") or "unknown")
        content = item.get("content", "")
        if isinstance(content, dict):
            content = " ".join(str(part) for part in content.get("parts", []) if part)
        messages.append(ChatMessage(role=role, content=str(content).strip()))
    return [message for message in messages if message.content]


def normalize_chatgpt_mapping(mapping: dict[str, Any]) -> list[ChatMessage]:
    """Normalize the mapping shape used by some ChatGPT data exports."""

    messages: list[ChatMessage] = []
    for node in mapping.values():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        author = message.get("author") or {}
        role = str(author.get("role") or "unknown")
        content = message.get("content") or {}
        parts = content.get("parts", []) if isinstance(content, dict) else []
        text = " ".join(str(part) for part in parts if part).strip()
        if text:
            messages.append(ChatMessage(role=role, content=text))
    return messages


def extract_text_title(text: str) -> str | None:
    """Return first Markdown heading or first non-empty line as a title."""

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped:
            return stripped[:80]
    return None
