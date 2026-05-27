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
WORKSPACE_ROUTING_MARKER = "Automation workspace routing note:"
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2} - (.+)$")
DATE_SUFFIX_RE = re.compile(r"^(.+) - \d{4}-\d{2}-\d{2}$")
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
    parser.add_argument(
        "--date-active-rows",
        action="store_true",
        help="Prefix matching active sidebar rows with their updated date for easier scanning.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Optional local project root to use for matching automation thread sidebar routing metadata.",
    )
    parser.add_argument(
        "--future-project-root",
        type=Path,
        default=None,
        help="Optional local project root to write into matching automation configs for future run routing.",
    )
    args = parser.parse_args()

    if args.apply and args.confirm != CONFIRMATION_PHRASE:
        parser.error(f"--apply requires --confirm {CONFIRMATION_PHRASE}")

    summary = apply_policy(
        args.codex_home,
        dry_run=not args.apply,
        date_active_rows=args.date_active_rows,
        project_root=args.project_root,
        future_project_root=args.future_project_root,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def apply_policy(
    codex_home: Path,
    *,
    dry_run: bool = False,
    timestamp: str | None = None,
    date_active_rows: bool = False,
    project_root: Path | None = None,
    future_project_root: Path | None = None,
) -> dict[str, Any]:
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
        "session_index_rows_dated": 0,
        "project_root": str(project_root.resolve()) if project_root else None,
        "future_project_root": str(future_project_root.resolve()) if future_project_root else None,
        "project_thread_hints_updated": 0,
        "project_saved_roots_updated": 0,
        "state_thread_cwds_updated": 0,
        "automation_run_source_cwds_updated": 0,
        "future_toml_files_updated": [],
        "future_database_rows_updated": 0,
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

    if date_active_rows:
        date_result = date_session_index_rows(codex_home, backup_dir=backup_dir, dry_run=dry_run)
        summary["session_index_rows_dated"] = date_result["dated"]
        summary["backups_created"] += date_result["backups_created"]

    if project_root:
        project_result = route_automation_threads_to_project(
            codex_home,
            project_root=project_root,
            backup_dir=backup_dir,
            dry_run=dry_run,
        )
        summary["project_thread_hints_updated"] = project_result["thread_hints_updated"]
        summary["project_saved_roots_updated"] = project_result["saved_roots_updated"]
        summary["state_thread_cwds_updated"] = project_result["state_thread_cwds_updated"]
        summary["automation_run_source_cwds_updated"] = project_result["automation_run_source_cwds_updated"]
        summary["databases_updated"] = sorted(
            set(summary["databases_updated"] + project_result["databases_updated"])
        )
        summary["backups_created"] += project_result["backups_created"]

    if future_project_root:
        future_result = route_future_automations_to_project(
            codex_home,
            project_root=future_project_root,
            backup_dir=backup_dir,
            dry_run=dry_run,
        )
        summary["future_toml_files_updated"] = future_result["toml_files_updated"]
        summary["future_database_rows_updated"] = future_result["database_rows_updated"]
        summary["databases_updated"] = sorted(
            set(summary["databases_updated"] + future_result["databases_updated"])
        )
        summary["backups_created"] += future_result["backups_created"]

    has_changes = (
        summary["backups_created"]
        or summary["session_index_rows_removed"]
        or summary["session_files_moved"]
        or summary["state_threads_archived"]
        or summary["automation_runs_archived"]
        or summary["session_index_rows_dated"]
        or summary["project_thread_hints_updated"]
        or summary["project_saved_roots_updated"]
        or summary["state_thread_cwds_updated"]
        or summary["automation_run_source_cwds_updated"]
        or summary["future_toml_files_updated"]
        or summary["future_database_rows_updated"]
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
        matching = [record for record in records if _automation_title_base(record.thread_name) == title and record.id]
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
        if not (_automation_title_base(record.thread_name) in DEFAULT_AUTOMATIONS.values() and record.id in archive_ids)
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


def date_session_index_rows(codex_home: Path, *, backup_dir: Path, dry_run: bool) -> dict[str, Any]:
    index_path = codex_home / "session_index.jsonl"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing session index: {index_path}")

    lines = index_path.read_text(encoding="utf-8-sig").splitlines()
    updated_lines: list[str] = []
    dated = 0

    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            updated_lines.append(line)
            continue

        base_title = _automation_title_base(data.get("thread_name"))
        updated_at = _parse_timestamp(data.get("updated_at"))
        if base_title and updated_at != datetime.min.replace(tzinfo=timezone.utc):
            desired_title = f"{updated_at.date().isoformat()} - {base_title}"
            if data.get("thread_name") != desired_title:
                data["thread_name"] = desired_title
                line = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                dated += 1

        updated_lines.append(line)

    backups_created: list[str] = []
    if dated and not dry_run:
        backups_created.append(str(_backup_file(index_path, backup_dir)))
        index_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")

    return {"dated": dated, "backups_created": backups_created}


def route_automation_threads_to_project(
    codex_home: Path,
    *,
    project_root: Path,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    project_root_text = str(project_root.resolve())
    project_root_for_threads = _sqlite_cwd_for_project(project_root_text)
    thread_ids = _collect_automation_thread_ids(codex_home)
    backups_created: list[str] = []
    databases_updated: list[str] = []

    state_result = _route_global_state_threads(
        codex_home,
        thread_ids=thread_ids,
        project_root=project_root_text,
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    backups_created.extend(state_result["backups_created"])

    thread_result = _route_state_thread_cwds(
        codex_home,
        thread_ids=thread_ids,
        project_root=project_root_for_threads,
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    backups_created.extend(thread_result["backups_created"])
    databases_updated.extend(thread_result["databases_updated"])

    run_result = _route_automation_run_source_cwds(
        codex_home,
        project_root=project_root_text,
        backup_dir=backup_dir,
        dry_run=dry_run,
    )
    backups_created.extend(run_result["backups_created"])
    databases_updated.extend(run_result["databases_updated"])

    return {
        "thread_hints_updated": state_result["thread_hints_updated"],
        "saved_roots_updated": state_result["saved_roots_updated"],
        "state_thread_cwds_updated": thread_result["updated"],
        "automation_run_source_cwds_updated": run_result["updated"],
        "databases_updated": sorted(set(databases_updated)),
        "backups_created": backups_created,
    }


def route_future_automations_to_project(
    codex_home: Path,
    *,
    project_root: Path,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    project_root_text = str(project_root.resolve())
    backups_created: list[str] = []
    toml_files_updated: list[str] = []

    for automation_id in DEFAULT_AUTOMATIONS:
        toml_path = codex_home / "automations" / automation_id / "automation.toml"
        if not toml_path.exists():
            continue

        original = toml_path.read_text(encoding="utf-8")
        updated = _update_future_automation_toml(original, project_root=project_root_text)
        if updated != original:
            toml_files_updated.append(str(toml_path))
            if not dry_run:
                backups_created.append(str(_backup_file(toml_path, backup_dir)))
                toml_path.write_text(updated, encoding="utf-8")

    db_result = _route_future_automation_database(
        codex_home,
        project_root=project_root_text,
        backup_dir=backup_dir,
        dry_run=dry_run,
    )

    return {
        "toml_files_updated": toml_files_updated,
        "database_rows_updated": db_result["updated"],
        "databases_updated": db_result["databases_updated"],
        "backups_created": backups_created + db_result["backups_created"],
    }


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


def _collect_automation_thread_ids(codex_home: Path) -> set[str]:
    thread_ids: set[str] = set()
    index_path = codex_home / "session_index.jsonl"
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8-sig").splitlines():
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if _automation_title_base(data.get("thread_name")) and data.get("id"):
                thread_ids.add(data["id"])

    db_path = codex_home / "sqlite" / "codex-dev.db"
    if db_path.exists():
        connection = sqlite3.connect(db_path)
        try:
            if _sqlite_table_exists(connection, "automation_runs"):
                placeholders = ",".join("?" for _ in DEFAULT_AUTOMATIONS)
                rows = connection.execute(
                    f"select thread_id from automation_runs where automation_id in ({placeholders})",
                    sorted(DEFAULT_AUTOMATIONS),
                ).fetchall()
                thread_ids.update(row[0] for row in rows if row[0])
        finally:
            connection.close()

    state_db_path = codex_home / "state_5.sqlite"
    if state_db_path.exists():
        connection = sqlite3.connect(state_db_path)
        try:
            if _sqlite_table_exists(connection, "threads"):
                rows = connection.execute(
                    """
                    select id from threads
                    where title in (?, ?)
                       or title like 'Automation: Daily Obsidian conversation sync%'
                       or title like 'Automation: Overnight portfolio goal%'
                    """,
                    tuple(DEFAULT_AUTOMATIONS.values()),
                ).fetchall()
                thread_ids.update(row[0] for row in rows if row[0])
        finally:
            connection.close()

    return thread_ids


def _route_global_state_threads(
    codex_home: Path,
    *,
    thread_ids: set[str],
    project_root: str,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    state_path = codex_home / ".codex-global-state.json"
    if not state_path.exists():
        return {"thread_hints_updated": 0, "saved_roots_updated": 0, "backups_created": []}

    state = json.loads(state_path.read_text(encoding="utf-8"))
    saved_roots_updated = 0
    for key in ("project-order", "electron-saved-workspace-roots"):
        roots = state.get(key)
        if isinstance(roots, list) and project_root not in roots:
            roots.insert(0, project_root)
            saved_roots_updated += 1

    hints = state.setdefault("thread-workspace-root-hints", {})
    thread_hints_updated = 0
    for thread_id in sorted(thread_ids):
        if hints.get(thread_id) != project_root:
            hints[thread_id] = project_root
            thread_hints_updated += 1

    backups_created: list[str] = []
    if (thread_hints_updated or saved_roots_updated) and not dry_run:
        backups_created.append(str(_backup_file(state_path, backup_dir)))
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "thread_hints_updated": thread_hints_updated,
        "saved_roots_updated": saved_roots_updated,
        "backups_created": backups_created,
    }


def _route_state_thread_cwds(
    codex_home: Path,
    *,
    thread_ids: set[str],
    project_root: str,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    db_path = codex_home / "state_5.sqlite"
    if not thread_ids or not db_path.exists():
        return {"updated": 0, "databases_updated": [], "backups_created": []}

    connection = sqlite3.connect(db_path)
    try:
        if not _sqlite_table_exists(connection, "threads"):
            return {"updated": 0, "databases_updated": [], "backups_created": []}

        placeholders = ",".join("?" for _ in thread_ids)
        ids = sorted(thread_ids)
        updated = connection.execute(
            f"select count(*) from threads where id in ({placeholders}) and cwd <> ?",
            [*ids, project_root],
        ).fetchone()[0]

        backups_created: list[str] = []
        if updated and not dry_run:
            backups_created.append(str(_backup_sqlite_database(db_path, backup_dir)))
            connection.execute(
                f"update threads set cwd = ? where id in ({placeholders})",
                [project_root, *ids],
            )
            connection.commit()

        return {
            "updated": updated,
            "databases_updated": [str(db_path)] if updated else [],
            "backups_created": backups_created,
        }
    finally:
        connection.close()


def _route_automation_run_source_cwds(
    codex_home: Path,
    *,
    project_root: str,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    db_path = codex_home / "sqlite" / "codex-dev.db"
    if not db_path.exists():
        return {"updated": 0, "databases_updated": [], "backups_created": []}

    connection = sqlite3.connect(db_path)
    try:
        if not _sqlite_table_exists(connection, "automation_runs"):
            return {"updated": 0, "databases_updated": [], "backups_created": []}

        placeholders = ",".join("?" for _ in DEFAULT_AUTOMATIONS)
        automation_ids = sorted(DEFAULT_AUTOMATIONS)
        updated = connection.execute(
            f"""
            select count(*) from automation_runs
            where automation_id in ({placeholders})
              and (source_cwd is null or source_cwd <> ?)
            """,
            [*automation_ids, project_root],
        ).fetchone()[0]

        backups_created: list[str] = []
        if updated and not dry_run:
            backups_created.append(str(_backup_sqlite_database(db_path, backup_dir)))
            connection.execute(
                f"update automation_runs set source_cwd = ? where automation_id in ({placeholders})",
                [project_root, *automation_ids],
            )
            connection.commit()

        return {
            "updated": updated,
            "databases_updated": [str(db_path)] if updated else [],
            "backups_created": backups_created,
        }
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


def _update_future_automation_toml(text: str, *, project_root: str) -> str:
    data = tomllib.loads(text)
    original_cwds = data.get("cwds")
    execution_workspace = _execution_workspace_from_cwds(original_cwds, project_root)
    prompt = data.get("prompt", "")
    updated_prompt = _with_workspace_routing_note(prompt if isinstance(prompt, str) else "", execution_workspace)
    updated = text

    if prompt != updated_prompt:
        updated = _replace_toml_string(updated, "prompt", updated_prompt)

    if original_cwds != [project_root]:
        updated = _replace_toml_array_of_strings(updated, "cwds", [project_root])

    if updated != text:
        updated = _replace_toml_integer(updated, "updated_at", int(time.time() * 1000))
    return updated


def _route_future_automation_database(
    codex_home: Path,
    *,
    project_root: str,
    backup_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    db_path = codex_home / "sqlite" / "codex-dev.db"
    if not db_path.exists():
        return {"updated": 0, "databases_updated": [], "backups_created": []}

    connection = sqlite3.connect(db_path)
    try:
        if not _sqlite_table_exists(connection, "automations"):
            return {"updated": 0, "databases_updated": [], "backups_created": []}

        updates: list[tuple[str, str, str]] = []
        for automation_id, cwds, prompt in connection.execute(
            "select id, cwds, prompt from automations where id in (?, ?)",
            tuple(sorted(DEFAULT_AUTOMATIONS)),
        ):
            existing_cwds = _parse_json_string_list(cwds)
            execution_workspace = _execution_workspace_from_cwds(existing_cwds, project_root)
            updated_cwds = json.dumps([project_root])
            updated_prompt = _with_workspace_routing_note(prompt or "", execution_workspace)
            if cwds != updated_cwds or prompt != updated_prompt:
                updates.append((automation_id, updated_cwds, updated_prompt))

        backups_created: list[str] = []
        if updates and not dry_run:
            backups_created.append(str(_backup_sqlite_database(db_path, backup_dir)))
            now_ms = int(time.time() * 1000)
            for automation_id, updated_cwds, updated_prompt in updates:
                connection.execute(
                    "update automations set cwds = ?, prompt = ?, updated_at = ? where id = ?",
                    (updated_cwds, updated_prompt, now_ms, automation_id),
                )
            connection.commit()

        return {
            "updated": len(updates),
            "databases_updated": [str(db_path)] if updates else [],
            "backups_created": backups_created,
        }
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


def _automation_title_base(thread_name: str | None) -> str | None:
    if not isinstance(thread_name, str):
        return None

    value = thread_name.strip()
    for pattern in (DATE_PREFIX_RE, DATE_SUFFIX_RE):
        match = pattern.match(value)
        if match:
            value = match.group(1).strip()
            break

    return value if value in DEFAULT_AUTOMATIONS.values() else None


def _execution_workspace_from_cwds(cwds: Any, project_root: str) -> str | None:
    if not isinstance(cwds, list):
        return None
    for cwd in cwds:
        if isinstance(cwd, str) and cwd and cwd != project_root:
            return cwd
    return None


def _parse_json_string_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [item for item in parsed if isinstance(item, str)]


def _with_workspace_routing_note(prompt: str, execution_workspace: str | None) -> str:
    if WORKSPACE_ROUTING_MARKER in prompt or not execution_workspace:
        return prompt
    note = (
        f"{WORKSPACE_ROUTING_MARKER}\n"
        "- This automation is listed under the Cron Jobs project for sidebar hygiene.\n"
        f"- When repository files are needed, use `{execution_workspace}` as the working directory with absolute paths."
    )
    return f"{prompt}\n\n{note}".strip()


def _sqlite_cwd_for_project(project_root: str) -> str:
    if project_root.startswith("\\\\?\\"):
        return project_root
    return f"\\\\?\\{project_root}"


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


def _replace_toml_array_of_strings(text: str, key: str, values: list[str]) -> str:
    encoded = ", ".join(json.dumps(value) for value in values)
    pattern = re.compile(rf"^{re.escape(key)}\s*=.*$", re.MULTILINE)
    replacement = f"{key} = [{encoded}]"
    if pattern.search(text):
        return pattern.sub(lambda _: replacement, text, count=1)
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


def _backup_sqlite_database(path: Path, backup_dir: Path) -> Path:
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

    source = sqlite3.connect(path)
    backup = sqlite3.connect(destination)
    try:
        source.backup(backup)
    finally:
        backup.close()
        source.close()
    return destination


if __name__ == "__main__":
    raise SystemExit(main())
