from __future__ import annotations

"""Local Codex workspace hygiene helper.

This script repairs local sidebar/session clutter from recurring automations.
It is not portfolio evidence, a project feature, or part of the public workflow.
"""

import argparse
import json
import re
import shutil
import sqlite3
import time
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_AUTOMATIONS = {
    "daily-obsidian-conversation-sync": "Daily Obsidian conversation sync",
    "overnight-portfolio-goal": "Overnight portfolio goal",
}

CONFIRMATION_PHRASE = "APPLY_LOCAL_CODEX_AUTOMATION_POLICY"
POLICY_MARKER = "Automation result delivery policy:"
POLICY_TEXT = (
    "Automation result delivery policy:\n"
    "- Routine successful runs, nothing-changed runs, no-content runs, and ordinary daily status reports should finish as a concise inbox/status item.\n"
    "- Do not create or request a new sidebar thread for routine outcomes.\n"
    "- Use or continue the canonical automation thread only for errors, debugging, decisions, unusual conditions, or long-form follow-up.\n"
    "- End with exactly one inbox-item directive."
)


@dataclass(frozen=True)
class IndexRecord:
    line: str
    id: str | None
    thread_name: str | None
    updated_at: datetime


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Local-only helper for consolidating recurring Codex automation sidebar rows. "
            "Dry-run is the default."
        )
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Path to the local Codex state directory. Defaults to ~/.codex.",
    )
    parser.add_argument("--apply", action="store_true", help="Write changes to local Codex state.")
    parser.add_argument(
        "--confirm",
        default="",
        help=f"Required with --apply. Must equal {CONFIRMATION_PHRASE}.",
    )
    args = parser.parse_args()

    if args.apply and args.confirm != CONFIRMATION_PHRASE:
        parser.error(f"--apply requires --confirm {CONFIRMATION_PHRASE}")

    summary = apply_policy(args.codex_home, dry_run=not args.apply)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def apply_policy(codex_home: Path, *, dry_run: bool = False, timestamp: str | None = None) -> dict[str, Any]:
    codex_home = codex_home.resolve()
    timestamp = timestamp or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_dir = codex_home / "backups" / f"automation-sidebar-policy-{timestamp}"
    archive_dir = codex_home / "archived_sessions"

    summary: dict[str, Any] = {
        "codex_home": str(codex_home),
        "dry_run": dry_run,
        "backup_dir": str(backup_dir),
        "canonical_threads": {},
        "session_index_rows_removed": 0,
        "session_files_moved": 0,
        "session_files_already_archived": 0,
        "missing_session_files": 0,
        "automation_runs_archived": 0,
        "toml_files_updated": [],
        "databases_updated": [],
        "backups_created": [],
    }

    index_result = consolidate_session_index(
        codex_home,
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    summary.update(index_result)

    policy_result = update_automation_policy(
        codex_home,
        canonical_threads=index_result["canonical_threads"],
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    summary["toml_files_updated"] = policy_result["toml_files_updated"]
    summary["databases_updated"] = policy_result["databases_updated"]

    automation_run_result = archive_duplicate_automation_runs(
        codex_home,
        canonical_threads=index_result["canonical_threads"],
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    summary["automation_runs_archived"] = automation_run_result["archived"]
    summary["databases_updated"] = sorted(
        set(policy_result["databases_updated"] + automation_run_result["databases_updated"])
    )
    summary["backups_created"] = (
        index_result["backups_created"] + policy_result["backups_created"] + automation_run_result["backups_created"]
    )

    has_changes = (
        summary["backups_created"]
        or summary["session_index_rows_removed"]
        or summary["session_files_moved"]
        or summary["state_threads_archived"]
        or summary["automation_runs_archived"]
        or summary["toml_files_updated"]
        or summary["databases_updated"]
    )
    if not dry_run and has_changes:
        manifest_path = backup_dir / "manifest.json"
        backup_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        summary["manifest"] = str(manifest_path)

    return summary


def consolidate_session_index(codex_home: Path, *, backup_dir: Path, dry_run: bool) -> dict[str, Any]:
    index_path = codex_home / "session_index.jsonl"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing session index: {index_path}")

    lines = index_path.read_text(encoding="utf-8-sig").splitlines()
    records = [_parse_index_line(line) for line in lines]
    canonical_by_title: dict[str, str] = {}
    archive_ids: set[str] = set()

    for automation_id, title in DEFAULT_AUTOMATIONS.items():
        matching = [record for record in records if record.thread_name == title and record.id]
        if not matching:
            continue

        configured_id = _read_configured_target_thread_id(codex_home / "automations" / automation_id / "automation.toml")
        configured = next((record for record in matching if record.id == configured_id), None)
        canonical = configured or max(matching, key=lambda record: record.updated_at)
        canonical_by_title[title] = canonical.id or ""

        for record in matching:
            if record.id != canonical.id and record.id:
                archive_ids.add(record.id)

    new_lines = [
        record.line
        for record in records
        if not (record.thread_name in DEFAULT_AUTOMATIONS.values() and record.id in archive_ids)
    ]

    backups_created: list[str] = []
    if len(new_lines) != len(lines) and not dry_run:
        backups_created.append(str(_backup_file(index_path, backup_dir)))
        index_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    move_result = archive_session_files(codex_home, archive_ids, backup_dir=backup_dir, dry_run=dry_run)
    db_archive_result = archive_state_threads(codex_home, archive_ids, backup_dir=backup_dir, dry_run=dry_run)

    return {
        "canonical_threads": canonical_by_title,
        "session_index_rows_removed": len(lines) - len(new_lines),
        "session_files_moved": move_result["moved"],
        "session_files_already_archived": move_result["already_archived"],
        "missing_session_files": move_result["missing"],
        "state_threads_archived": db_archive_result["archived"],
        "backups_created": backups_created + move_result["backups_created"] + db_archive_result["backups_created"],
    }


def archive_session_files(
    codex_home: Path,
    archive_ids: set[str],
    *,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    sessions_dir = codex_home / "sessions"
    archive_dir = codex_home / "archived_sessions"
    moved = 0
    already_archived = 0
    missing = 0

    for thread_id in sorted(archive_ids):
        active_files = list(sessions_dir.rglob(f"*{thread_id}*.jsonl")) if sessions_dir.exists() else []
        archived_files = list(archive_dir.glob(f"*{thread_id}*.jsonl")) if archive_dir.exists() else []

        if not active_files and archived_files:
            already_archived += 1
            continue
        if not active_files:
            missing += 1
            continue

        for source in active_files:
            destination = archive_dir / source.name
            if destination.exists():
                already_archived += 1
                continue
            moved += 1
            if not dry_run:
                archive_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))

    return {"moved": moved, "already_archived": already_archived, "missing": missing, "backups_created": []}


def archive_state_threads(
    codex_home: Path,
    archive_ids: set[str],
    *,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    db_path = codex_home / "state_5.sqlite"
    if not archive_ids or not db_path.exists():
        return {"archived": 0, "backups_created": []}

    placeholders = ",".join("?" for _ in archive_ids)
    connection = sqlite3.connect(db_path)
    try:
        rows = connection.execute(
            f"select id from threads where archived = 0 and id in ({placeholders})",
            sorted(archive_ids),
        ).fetchall()
        ids_to_archive = [row[0] for row in rows]
        if not ids_to_archive:
            return {"archived": 0, "backups_created": []}

        backups_created = []
        if not dry_run:
            backups_created.append(str(_backup_file(db_path, backup_dir)))
            now_ms = int(time.time() * 1000)
            placeholders = ",".join("?" for _ in ids_to_archive)
            connection.execute(
                f"update threads set archived = 1, archived_at = ? where id in ({placeholders})",
                [now_ms, *ids_to_archive],
            )
            connection.commit()
        return {"archived": len(ids_to_archive), "backups_created": backups_created}
    finally:
        connection.close()


def update_automation_policy(
    codex_home: Path,
    *,
    canonical_threads: dict[str, str],
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    backups_created: list[str] = []
    toml_files_updated: list[str] = []
    canonical_by_id = {automation_id: canonical_threads.get(title) for automation_id, title in DEFAULT_AUTOMATIONS.items()}

    for automation_id, canonical_thread_id in canonical_by_id.items():
        if not canonical_thread_id:
            continue
        toml_path = codex_home / "automations" / automation_id / "automation.toml"
        if not toml_path.exists():
            continue

        original = toml_path.read_text(encoding="utf-8")
        updated = _update_automation_toml(original, canonical_thread_id=canonical_thread_id)
        if updated != original:
            toml_files_updated.append(str(toml_path))
            if not dry_run:
                backups_created.append(str(_backup_file(toml_path, backup_dir)))
                toml_path.write_text(updated, encoding="utf-8")

    db_result = update_automation_database(codex_home, backup_dir=backup_dir, dry_run=dry_run)
    return {
        "toml_files_updated": toml_files_updated,
        "databases_updated": db_result["databases_updated"],
        "backups_created": backups_created + db_result["backups_created"],
    }


def archive_duplicate_automation_runs(
    codex_home: Path,
    *,
    canonical_threads: dict[str, str],
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    db_path = codex_home / "sqlite" / "codex-dev.db"
    if not db_path.exists():
        return {"archived": 0, "databases_updated": [], "backups_created": []}

    canonical_by_automation_id = {
        automation_id: canonical_threads.get(title)
        for automation_id, title in DEFAULT_AUTOMATIONS.items()
        if canonical_threads.get(title)
    }
    if not canonical_by_automation_id:
        return {"archived": 0, "databases_updated": [], "backups_created": []}

    connection = sqlite3.connect(db_path)
    try:
        if not _sqlite_table_exists(connection, "automation_runs"):
            return {"archived": 0, "databases_updated": [], "backups_created": []}

        rows_to_archive: list[tuple[str, str]] = []
        for automation_id, canonical_thread_id in canonical_by_automation_id.items():
            rows_to_archive.extend(
                connection.execute(
                    """
                    select automation_id, thread_id
                    from automation_runs
                    where automation_id = ?
                      and thread_id <> ?
                      and status <> 'ARCHIVED'
                    """,
                    (automation_id, canonical_thread_id),
                ).fetchall()
            )

        if not rows_to_archive:
            return {"archived": 0, "databases_updated": [], "backups_created": []}

        backups_created = []
        if not dry_run:
            backups_created.append(str(_backup_file(db_path, backup_dir)))
            now_ms = int(time.time() * 1000)
            for automation_id, thread_id in rows_to_archive:
                connection.execute(
                    """
                    update automation_runs
                    set status = 'ARCHIVED',
                        archived_reason = 'auto-sidebar-policy',
                        updated_at = ?
                    where automation_id = ?
                      and thread_id = ?
                    """,
                    (now_ms, automation_id, thread_id),
                )
            connection.commit()

        return {"archived": len(rows_to_archive), "databases_updated": [str(db_path)], "backups_created": backups_created}
    finally:
        connection.close()


def update_automation_database(codex_home: Path, *, backup_dir: Path, dry_run: bool) -> dict[str, Any]:
    db_path = codex_home / "sqlite" / "codex-dev.db"
    if not db_path.exists():
        return {"databases_updated": [], "backups_created": []}

    connection = sqlite3.connect(db_path)
    try:
        updates: list[tuple[str, str]] = []
        for automation_id in DEFAULT_AUTOMATIONS:
            row = connection.execute("select prompt from automations where id = ?", (automation_id,)).fetchone()
            if not row:
                continue
            prompt = row[0] or ""
            updated_prompt = _with_policy_text(prompt)
            if updated_prompt != prompt:
                updates.append((automation_id, updated_prompt))

        if not updates:
            return {"databases_updated": [], "backups_created": []}

        backups_created = []
        if not dry_run:
            backups_created.append(str(_backup_file(db_path, backup_dir)))
            now_ms = int(time.time() * 1000)
            for automation_id, updated_prompt in updates:
                connection.execute(
                    "update automations set prompt = ?, updated_at = ? where id = ?",
                    (updated_prompt, now_ms, automation_id),
                )
            connection.commit()

        return {"databases_updated": [str(db_path)], "backups_created": backups_created}
    finally:
        connection.close()


def _sqlite_table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    return (
        connection.execute(
            "select 1 from sqlite_master where type = 'table' and name = ?",
            (table_name,),
        ).fetchone()
        is not None
    )


def _parse_index_line(line: str) -> IndexRecord:
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return IndexRecord(line=line, id=None, thread_name=None, updated_at=datetime.min.replace(tzinfo=timezone.utc))

    return IndexRecord(
        line=line,
        id=data.get("id"),
        thread_name=data.get("thread_name"),
        updated_at=_parse_timestamp(data.get("updated_at")),
    )


def _parse_timestamp(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _read_configured_target_thread_id(toml_path: Path) -> str | None:
    if not toml_path.exists():
        return None
    try:
        data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return None
    value = data.get("target_thread_id")
    return value if isinstance(value, str) else None


def _update_automation_toml(text: str, *, canonical_thread_id: str) -> str:
    data = tomllib.loads(text)
    prompt = data.get("prompt", "")
    updated_prompt = _with_policy_text(prompt if isinstance(prompt, str) else "")
    updated = text

    if prompt != updated_prompt:
        updated = _replace_toml_string(updated, "prompt", updated_prompt)

    if data.get("target_thread_id") != canonical_thread_id:
        updated = _upsert_toml_string(updated, "target_thread_id", canonical_thread_id, after_key="name")

    if updated != text:
        updated = _replace_toml_integer(updated, "updated_at", int(time.time() * 1000))
    return updated


def _with_policy_text(prompt: str) -> str:
    if POLICY_MARKER in prompt:
        return prompt
    return f"{prompt}\n\n{POLICY_TEXT}".strip()


def _replace_toml_string(text: str, key: str, value: str) -> str:
    encoded = json.dumps(value)
    pattern = re.compile(rf"^{re.escape(key)}\s*=.*$", re.MULTILINE)
    replacement = f"{key} = {encoded}"
    if pattern.search(text):
        return pattern.sub(lambda _: replacement, text, count=1)
    return text.rstrip() + f"\n{replacement}\n"


def _replace_toml_integer(text: str, key: str, value: int) -> str:
    pattern = re.compile(rf"^{re.escape(key)}\s*=\s*\d+\s*$", re.MULTILINE)
    replacement = f"{key} = {value}"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return text.rstrip() + f"\n{replacement}\n"


def _upsert_toml_string(text: str, key: str, value: str, *, after_key: str) -> str:
    encoded = json.dumps(value)
    pattern = re.compile(rf"^{re.escape(key)}\s*=.*$", re.MULTILINE)
    replacement = f"{key} = {encoded}"
    if pattern.search(text):
        return pattern.sub(lambda _: replacement, text, count=1)

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(rf"^{re.escape(after_key)}\s*=", line):
            lines.insert(index + 1, replacement)
            return "\n".join(lines) + "\n"
    return text.rstrip() + f"\n{replacement}\n"


def _backup_file(path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination = backup_dir / f"{path.parent.name}__{path.name}"
    if destination.exists():
        suffix = 1
        while True:
            candidate = backup_dir / f"{path.name}.{suffix}.bak"
            if not candidate.exists():
                destination = candidate
                break
            suffix += 1
    shutil.copy2(path, destination)
    return destination


if __name__ == "__main__":
    raise SystemExit(main())
