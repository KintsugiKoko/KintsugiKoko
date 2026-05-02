from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Conversation, Message

SUPPORTED_EXTENSIONS = {".json", ".md", ".txt"}


def iter_source_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source] if source.suffix.lower() in SUPPORTED_EXTENSIONS else []

    if not source.exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")

    return sorted(
        path
        for path in source.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def parse_file(path: Path) -> list[Conversation]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _parse_json_file(path)
    if suffix in {".md", ".txt"}:
        return [_parse_text_file(path)]
    return []


def _parse_json_file(path: Path) -> list[Conversation]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and isinstance(data.get("conversations"), list):
        return [_parse_json_conversation(item, path, index) for index, item in enumerate(data["conversations"], 1)]

    if isinstance(data, list) and any(_looks_like_conversation(item) for item in data):
        return [_parse_json_conversation(item, path, index) for index, item in enumerate(data, 1)]

    if isinstance(data, dict):
        return [_parse_json_conversation(data, path, 1)]

    if isinstance(data, list):
        return [
            Conversation(
                title=path.stem.replace("-", " ").replace("_", " ").title(),
                messages=_parse_message_list(data),
                source_path=path,
                source_id=f"{path.resolve()}#messages",
            )
        ]

    raise ValueError(f"Unsupported JSON shape in {path}")


def _looks_like_conversation(value: Any) -> bool:
    return isinstance(value, dict) and (
        "mapping" in value
        or "messages" in value
        or "title" in value
        or "conversation" in value
    )


def _parse_json_conversation(data: Any, path: Path, index: int) -> Conversation:
    if not isinstance(data, dict):
        return Conversation(
            title=f"{path.stem} {index}",
            messages=[],
            source_path=path,
            source_id=f"{path.resolve()}#{index}",
        )

    title = str(data.get("title") or data.get("name") or f"{path.stem} {index}").strip()
    created_at = _normalize_datetime(data.get("create_time") or data.get("created_at") or data.get("created"))
    updated_at = _normalize_datetime(data.get("update_time") or data.get("updated_at") or data.get("updated"))
    source_key = data.get("id") or data.get("conversation_id") or index

    if isinstance(data.get("mapping"), dict):
        messages = _parse_chatgpt_mapping(data["mapping"])
    elif isinstance(data.get("messages"), list):
        messages = _parse_message_list(data["messages"])
    elif isinstance(data.get("conversation"), list):
        messages = _parse_message_list(data["conversation"])
    else:
        content = _extract_content(data.get("content") or data.get("text") or data)
        messages = [Message(role="source", content=content)] if content else []

    return Conversation(
        title=title or "Untitled Conversation",
        messages=messages,
        source_path=path,
        source_id=f"{path.resolve()}#{source_key}",
        created_at=created_at,
        updated_at=updated_at,
    )


def _parse_chatgpt_mapping(mapping: dict[str, Any]) -> list[Message]:
    dated_messages: list[tuple[str, Message]] = []

    for node in mapping.values():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue

        role = _extract_role(message)
        if role in {"system", "tool"}:
            continue

        content = _extract_content(message.get("content"))
        if not content:
            continue

        created_at = _normalize_datetime(message.get("create_time") or message.get("created_at"))
        dated_messages.append((created_at or "", Message(role=role, content=content, created_at=created_at)))

    return [message for _, message in sorted(dated_messages, key=lambda item: item[0])]


def _parse_message_list(messages: list[Any]) -> list[Message]:
    parsed: list[Message] = []
    for item in messages:
        if not isinstance(item, dict):
            content = _extract_content(item)
            if content:
                parsed.append(Message(role="source", content=content))
            continue

        role = str(item.get("role") or item.get("author") or item.get("speaker") or "source").strip().lower()
        content = _extract_content(item.get("content") or item.get("text") or item.get("message"))
        created_at = _normalize_datetime(item.get("created_at") or item.get("create_time") or item.get("time"))

        if role not in {"system", "tool"} and content:
            parsed.append(Message(role=role, content=content, created_at=created_at))

    return parsed


def _parse_text_file(path: Path) -> Conversation:
    text = path.read_text(encoding="utf-8").strip()
    return Conversation(
        title=path.stem.replace("-", " ").replace("_", " ").title(),
        messages=[Message(role="source", content=text)] if text else [],
        source_path=path,
        source_id=f"{path.resolve()}#text",
    )


def _extract_role(message: dict[str, Any]) -> str:
    author = message.get("author")
    if isinstance(author, dict):
        return str(author.get("role") or "source").strip().lower()
    return str(message.get("role") or "source").strip().lower()


def _extract_content(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n\n".join(filter(None, (_extract_content(item) for item in value))).strip()
    if isinstance(value, dict):
        if isinstance(value.get("parts"), list):
            return _extract_content(value["parts"])
        if "text" in value:
            return _extract_content(value["text"])
        if "content" in value:
            return _extract_content(value["content"])
        return json.dumps(value, indent=2, sort_keys=True)
    return str(value).strip()


def _normalize_datetime(value: Any) -> str | None:
    if value in {None, ""}:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value)
