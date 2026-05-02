from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import SyncConfig
from .markdown import render_conversation_note, render_index_note
from .models import Conversation
from .parser import iter_source_files, parse_file

CONVERSATIONS_FOLDER = "Conversations"
INDEX_FILE_NAME = "AI Conversation Index.md"


@dataclass(frozen=True)
class SyncAction:
    action: str
    title: str
    note_path: Path
    reason: str


@dataclass(frozen=True)
class SyncResult:
    actions: list[SyncAction]
    errors: list[str]

    @property
    def created(self) -> int:
        return sum(1 for action in self.actions if action.action == "created")

    @property
    def updated(self) -> int:
        return sum(1 for action in self.actions if action.action == "updated")

    @property
    def skipped(self) -> int:
        return sum(1 for action in self.actions if action.action == "skipped")

    @property
    def planned(self) -> int:
        return sum(1 for action in self.actions if action.action.startswith("would_"))


def sync_conversations(config: SyncConfig, *, dry_run: bool = False, force: bool = False) -> SyncResult:
    target_dir = config.vault / config.folder
    state_path = target_dir / ".sync-index.json"
    state = _load_state(state_path)
    actions: list[SyncAction] = []
    errors: list[str] = []
    synced_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    for source_file in iter_source_files(config.source):
        try:
            conversations = parse_file(source_file)
        except Exception as error:  # Keep one bad export from stopping the whole sync.
            errors.append(f"{source_file}: {error}")
            continue

        for conversation in conversations:
            checksum = _conversation_checksum(conversation)
            existing = state["sources"].get(conversation.source_id)
            note_path = _note_path(target_dir, conversation, existing)

            if existing and existing.get("checksum") == checksum and not force:
                actions.append(SyncAction("skipped", conversation.title, note_path, "unchanged"))
                continue

            action_name = "created" if not note_path.exists() else "updated"
            if dry_run:
                actions.append(SyncAction(f"would_{action_name}", conversation.title, note_path, "dry run"))
                continue

            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_text = render_conversation_note(
                conversation,
                tags=config.normalized_tags,
                synced_at=synced_at,
            )
            note_path.write_text(note_text, encoding="utf-8")

            state["sources"][conversation.source_id] = {
                "checksum": checksum,
                "note_path": str(note_path.relative_to(target_dir)),
                "source_path": str(conversation.source_path),
                "title": conversation.title,
                "synced_at": synced_at,
            }
            actions.append(SyncAction(action_name, conversation.title, note_path, "written"))

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        index_path = target_dir / INDEX_FILE_NAME
        index_path.write_text(
            render_index_note(
                _index_entries(state),
                folder_title=config.folder,
                synced_at=synced_at,
            ),
            encoding="utf-8",
        )
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")

    return SyncResult(actions=actions, errors=errors)


def _load_state(state_path: Path) -> dict[str, dict[str, dict[str, str]]]:
    if not state_path.exists():
        return {"sources": {}}
    try:
        with state_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {"sources": {}}
    if not isinstance(data, dict) or not isinstance(data.get("sources"), dict):
        return {"sources": {}}
    return data


def _note_path(target_dir: Path, conversation: Conversation, existing: dict[str, str] | None) -> Path:
    if existing and existing.get("note_path"):
        return target_dir / existing["note_path"]

    date_part = _date_part(conversation.created_at)
    slug = _slugify(conversation.title or "untitled conversation")
    short_id = hashlib.sha1(conversation.source_id.encode("utf-8")).hexdigest()[:8]
    return target_dir / CONVERSATIONS_FOLDER / f"{date_part}-{slug}-{short_id}.md"


def _date_part(value: str | None) -> str:
    if value and len(value) >= 10:
        return value[:10]
    return datetime.now(timezone.utc).date().isoformat()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:70] or "untitled-conversation"


def _conversation_checksum(conversation: Conversation) -> str:
    payload = {
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [asdict(message) for message in conversation.messages],
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _index_entries(state: dict[str, dict[str, dict[str, str]]]) -> list[dict[str, str]]:
    entries = []
    for source in state.get("sources", {}).values():
        if not isinstance(source, dict):
            continue
        entries.append(
            {
                "note_path": source.get("note_path", ""),
                "source_path": source.get("source_path", ""),
                "synced_at": source.get("synced_at", ""),
                "title": source.get("title", "Untitled Conversation"),
            }
        )
    return entries
