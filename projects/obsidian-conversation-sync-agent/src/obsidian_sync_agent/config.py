from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_FOLDER = "AI Conversation Notes"
DEFAULT_TAGS = ["ai-conversation", "learning-notes", "needs-review"]


@dataclass(frozen=True)
class SyncConfig:
    source: Path
    vault: Path
    folder: str = DEFAULT_FOLDER
    tags: list[str] | None = None

    @property
    def normalized_tags(self) -> list[str]:
        if self.tags is None:
            return DEFAULT_TAGS.copy()
        return self.tags


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("Config file must contain a JSON object.")
    return data


def config_from_values(
    *,
    source: str | None,
    vault: str | None,
    folder: str | None = None,
    tags: list[str] | None = None,
    config_path: Path | None = None,
) -> SyncConfig:
    data: dict[str, Any] = {}
    base_dir = Path.cwd()

    if config_path is not None:
        data = load_config(config_path)
        base_dir = config_path.parent

    source_value = source or data.get("source")
    vault_value = vault or data.get("vault")

    if not source_value:
        raise ValueError("Missing source folder or file. Use --source or set source in the config file.")
    if not vault_value:
        raise ValueError("Missing Obsidian vault path. Use --vault or set vault in the config file.")

    folder_value = folder or data.get("folder") or DEFAULT_FOLDER
    tags_value = tags if tags is not None else data.get("tags")

    if tags_value is not None and not isinstance(tags_value, list):
        raise ValueError("Config tags must be a list of strings.")

    return SyncConfig(
        source=_resolve_path(base_dir, str(source_value)),
        vault=_resolve_path(base_dir, str(vault_value)),
        folder=str(folder_value),
        tags=[str(tag) for tag in tags_value] if tags_value is not None else None,
    )


def _resolve_path(base_dir: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()
