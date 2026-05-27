from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("codex_automation_sidebar_policy.py")
SPEC = importlib.util.spec_from_file_location("codex_automation_sidebar_policy", MODULE_PATH)
policy = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["codex_automation_sidebar_policy"] = policy
SPEC.loader.exec_module(policy)


def test_consolidates_duplicates_and_preserves_newest_canonical(tmp_path):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-old",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-25T16:00:00Z",
            },
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
            {
                "id": "overnight-old",
                "thread_name": "Overnight portfolio goal",
                "updated_at": "2026-05-25T06:00:00Z",
            },
            {
                "id": "overnight-new",
                "thread_name": "Overnight portfolio goal",
                "updated_at": "2026-05-26T06:00:00Z",
            },
            {
                "id": "other-thread",
                "thread_name": "Cecil",
                "updated_at": "2026-05-26T07:00:00Z",
            },
        ],
    )
    _write_session_file(codex_home, "daily-old")
    _write_session_file(codex_home, "daily-new")
    _write_session_file(codex_home, "overnight-old")
    _write_session_file(codex_home, "overnight-new")

    summary = policy.apply_policy(codex_home, timestamp="test")

    rows = _read_session_index(codex_home)
    assert [row["id"] for row in rows if row["thread_name"] == "Daily Obsidian conversation sync"] == ["daily-new"]
    assert [row["id"] for row in rows if row["thread_name"] == "Overnight portfolio goal"] == ["overnight-new"]
    assert any(row["id"] == "other-thread" for row in rows)
    assert (codex_home / "archived_sessions" / "rollout-daily-old.jsonl").exists()
    assert (codex_home / "archived_sessions" / "rollout-overnight-old.jsonl").exists()
    assert (codex_home / "sessions" / "2026" / "05" / "rollout-daily-new.jsonl").exists()
    assert summary["session_index_rows_removed"] == 2
    assert summary["session_files_moved"] == 2
    assert summary["canonical_threads"]["Daily Obsidian conversation sync"] == "daily-new"
    assert summary["canonical_threads"]["Overnight portfolio goal"] == "overnight-new"


def test_updates_automation_policy_and_database_prompt(tmp_path):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
            {
                "id": "overnight-new",
                "thread_name": "Overnight portfolio goal",
                "updated_at": "2026-05-26T06:00:00Z",
            },
        ],
    )

    summary = policy.apply_policy(codex_home, timestamp="test")

    daily_toml = (codex_home / "automations" / "daily-obsidian-conversation-sync" / "automation.toml").read_text(
        encoding="utf-8"
    )
    overnight_toml = (codex_home / "automations" / "overnight-portfolio-goal" / "automation.toml").read_text(
        encoding="utf-8"
    )
    assert 'target_thread_id = "daily-new"' in daily_toml
    assert 'target_thread_id = "overnight-new"' in overnight_toml
    assert "Routine successful runs" in daily_toml
    assert "canonical automation thread only for errors" in overnight_toml
    assert len(summary["toml_files_updated"]) == 2

    connection = sqlite3.connect(codex_home / "sqlite" / "codex-dev.db")
    try:
        prompts = {
            row[0]: row[1]
            for row in connection.execute(
                "select id, prompt from automations where id in (?, ?)",
                ("daily-obsidian-conversation-sync", "overnight-portfolio-goal"),
            )
        }
    finally:
        connection.close()

    assert "Routine successful runs" in prompts["daily-obsidian-conversation-sync"]
    assert "Do not create or request a new sidebar thread" in prompts["overnight-portfolio-goal"]
    assert summary["databases_updated"] == [str(codex_home / "sqlite" / "codex-dev.db")]


def test_archives_duplicate_automation_runs_but_keeps_canonical(tmp_path):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-old",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-25T16:00:00Z",
            },
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
            {
                "id": "overnight-new",
                "thread_name": "Overnight portfolio goal",
                "updated_at": "2026-05-26T06:00:00Z",
            },
        ],
    )
    _write_automation_run(codex_home, "daily-obsidian-conversation-sync", "daily-old", "PENDING_REVIEW")
    _write_automation_run(codex_home, "daily-obsidian-conversation-sync", "daily-new", "PENDING_REVIEW")
    _write_automation_run(codex_home, "overnight-portfolio-goal", "overnight-new", "PENDING_REVIEW")

    summary = policy.apply_policy(codex_home, timestamp="test")

    rows = _read_automation_runs(codex_home)
    assert rows[("daily-obsidian-conversation-sync", "daily-old")] == "ARCHIVED"
    assert rows[("daily-obsidian-conversation-sync", "daily-new")] == "PENDING_REVIEW"
    assert rows[("overnight-portfolio-goal", "overnight-new")] == "PENDING_REVIEW"
    assert summary["automation_runs_archived"] == 1


def test_second_run_is_idempotent(tmp_path):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-old",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-25T16:00:00Z",
            },
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
        ],
    )
    _write_session_file(codex_home, "daily-old")
    _write_session_file(codex_home, "daily-new")

    first = policy.apply_policy(codex_home, timestamp="first")
    second = policy.apply_policy(codex_home, timestamp="second")

    assert first["session_index_rows_removed"] == 1
    assert second["session_index_rows_removed"] == 0
    assert second["session_files_moved"] == 0
    assert second["session_files_already_archived"] == 0
    assert _read_session_index(codex_home) == [
        {
            "id": "daily-new",
            "thread_name": "Daily Obsidian conversation sync",
            "updated_at": "2026-05-26T16:00:00Z",
        }
    ]
    assert len(list((codex_home / "archived_sessions").glob("*daily-old*.jsonl"))) == 1


def test_cli_defaults_to_dry_run(tmp_path, monkeypatch, capsys):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-old",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-25T16:00:00Z",
            },
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
        ],
    )
    _write_session_file(codex_home, "daily-old")
    _write_session_file(codex_home, "daily-new")
    monkeypatch.setattr(sys, "argv", ["policy", "--codex-home", str(codex_home)])

    assert policy.main() == 0

    output = json.loads(capsys.readouterr().out)
    assert output["dry_run"] is True
    assert output["session_index_rows_removed"] == 1
    assert [row["id"] for row in _read_session_index(codex_home)] == ["daily-old", "daily-new"]
    assert not (codex_home / "archived_sessions" / "rollout-daily-old.jsonl").exists()


def test_cli_requires_confirmation_before_apply(tmp_path, monkeypatch):
    codex_home = _make_codex_home(tmp_path)
    _write_session_index(
        codex_home,
        [
            {
                "id": "daily-old",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-25T16:00:00Z",
            },
            {
                "id": "daily-new",
                "thread_name": "Daily Obsidian conversation sync",
                "updated_at": "2026-05-26T16:00:00Z",
            },
        ],
    )
    monkeypatch.setattr(sys, "argv", ["policy", "--codex-home", str(codex_home), "--apply"])

    with pytest.raises(SystemExit):
        policy.main()

    assert [row["id"] for row in _read_session_index(codex_home)] == ["daily-old", "daily-new"]


def _make_codex_home(tmp_path: Path) -> Path:
    codex_home = tmp_path / ".codex"
    (codex_home / "sessions" / "2026" / "05").mkdir(parents=True)
    (codex_home / "archived_sessions").mkdir()
    (codex_home / "automations" / "daily-obsidian-conversation-sync").mkdir(parents=True)
    (codex_home / "automations" / "overnight-portfolio-goal").mkdir(parents=True)
    (codex_home / "sqlite").mkdir()

    _write_automation_toml(codex_home, "daily-obsidian-conversation-sync", "Daily Obsidian conversation sync")
    _write_automation_toml(codex_home, "overnight-portfolio-goal", "Overnight portfolio goal")
    _write_automation_db(codex_home)
    return codex_home


def _write_automation_toml(codex_home: Path, automation_id: str, name: str) -> None:
    toml_path = codex_home / "automations" / automation_id / "automation.toml"
    toml_path.write_text(
        "\n".join(
            [
                "version = 1",
                f'id = "{automation_id}"',
                'kind = "cron"',
                f'name = "{name}"',
                f'prompt = "Run {name}."',
                'status = "ACTIVE"',
                'rrule = "FREQ=DAILY"',
                "updated_at = 1",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_automation_db(codex_home: Path) -> None:
    connection = sqlite3.connect(codex_home / "sqlite" / "codex-dev.db")
    try:
        connection.execute(
            "create table automations (id TEXT, name TEXT, prompt TEXT, status TEXT, next_run_at INTEGER, last_run_at INTEGER, cwds TEXT, rrule TEXT, model TEXT, reasoning_effort TEXT, created_at INTEGER, updated_at INTEGER)"
        )
        connection.execute(
            "create table automation_runs (thread_id TEXT, automation_id TEXT, status TEXT, read_at INTEGER, thread_title TEXT, source_cwd TEXT, inbox_title TEXT, inbox_summary TEXT, created_at INTEGER, updated_at INTEGER, archived_user_message TEXT, archived_assistant_message TEXT, archived_reason TEXT)"
        )
        for automation_id, name in policy.DEFAULT_AUTOMATIONS.items():
            connection.execute(
                "insert into automations (id, name, prompt, status, updated_at) values (?, ?, ?, ?, ?)",
                (automation_id, name, f"Run {name}.", "ACTIVE", 1),
            )
        connection.commit()
    finally:
        connection.close()


def _write_automation_run(codex_home: Path, automation_id: str, thread_id: str, status: str) -> None:
    connection = sqlite3.connect(codex_home / "sqlite" / "codex-dev.db")
    try:
        connection.execute(
            "insert into automation_runs (thread_id, automation_id, status, thread_title, created_at, updated_at) values (?, ?, ?, ?, ?, ?)",
            (thread_id, automation_id, status, policy.DEFAULT_AUTOMATIONS[automation_id], 1, 1),
        )
        connection.commit()
    finally:
        connection.close()


def _read_automation_runs(codex_home: Path) -> dict[tuple[str, str], str]:
    connection = sqlite3.connect(codex_home / "sqlite" / "codex-dev.db")
    try:
        return {
            (automation_id, thread_id): status
            for automation_id, thread_id, status in connection.execute(
                "select automation_id, thread_id, status from automation_runs"
            )
        }
    finally:
        connection.close()


def _write_session_index(codex_home: Path, rows: list[dict[str, str]]) -> None:
    (codex_home / "session_index.jsonl").write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )


def _read_session_index(codex_home: Path) -> list[dict[str, str]]:
    return [
        json.loads(line)
        for line in (codex_home / "session_index.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_session_file(codex_home: Path, thread_id: str) -> None:
    session_path = codex_home / "sessions" / "2026" / "05" / f"rollout-{thread_id}.jsonl"
    session_path.write_text(f'{{"id": "{thread_id}"}}\n', encoding="utf-8")
