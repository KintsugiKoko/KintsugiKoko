from pathlib import Path

from obsidian_sync_agent.config import SyncConfig
from obsidian_sync_agent.sync import sync_conversations


def test_sync_writes_note_and_skips_unchanged_source(tmp_path):
    source = tmp_path / "source"
    vault = tmp_path / "vault"
    source.mkdir()
    (source / "conversation.json").write_text(
        """
        {
          "title": "Practice Note",
          "messages": [
            {"role": "user", "content": "Turn this into documentation."},
            {"role": "assistant", "content": "Add a summary and next steps."}
          ]
        }
        """,
        encoding="utf-8",
    )
    config = SyncConfig(source=source, vault=vault)

    first = sync_conversations(config)
    second = sync_conversations(config)

    notes = list((vault / "AI Conversation Notes" / "Conversations").glob("*.md"))
    index = vault / "AI Conversation Notes" / "AI Conversation Index.md"
    assert first.created == 1
    assert second.skipped == 1
    assert len(notes) == 1
    assert "Practice Note" in notes[0].read_text(encoding="utf-8")
    assert index.exists()
    assert "[[Conversations/" in index.read_text(encoding="utf-8")


def test_dry_run_does_not_write_files(tmp_path):
    source = tmp_path / "source"
    vault = tmp_path / "vault"
    source.mkdir()
    (source / "conversation.txt").write_text("A useful conversation.", encoding="utf-8")
    config = SyncConfig(source=source, vault=vault)

    result = sync_conversations(config, dry_run=True)

    assert result.planned == 1
    assert not vault.exists()


def test_sync_consolidates_repeated_titles_into_one_note(tmp_path):
    source = tmp_path / "source"
    vault = tmp_path / "vault"
    source.mkdir()

    (source / "daily-obsidian.json").write_text(
        """
        {
          "title": "Daily Obsidian conversation sync",
          "messages": [
            {"role": "user", "content": "First run."}
          ]
        }
        """,
        encoding="utf-8",
    )
    (source / "overnight-goal.json").write_text(
        """
        {
          "title": "Overnight portfolio goal",
          "messages": [
            {"role": "user", "content": "First goal."}
          ]
        }
        """,
        encoding="utf-8",
    )
    (source / "daily-obsidian-followup.json").write_text(
        """
        {
          "title": "Daily Obsidian conversation sync",
          "messages": [
            {"role": "user", "content": "Second run."}
          ]
        }
        """,
        encoding="utf-8",
    )

    config = SyncConfig(source=source, vault=vault)
    result = sync_conversations(config)

    notes = list((vault / "AI Conversation Notes" / "Conversations").glob("*.md"))
    index = (vault / "AI Conversation Notes" / "AI Conversation Index.md").read_text(encoding="utf-8")

    assert result.created == 2
    assert len(notes) == 2
    assert any("Daily Obsidian conversation sync" in note.read_text(encoding="utf-8") for note in notes)
    assert any("Overnight portfolio goal" in note.read_text(encoding="utf-8") for note in notes)
    assert index.count("[[Conversations/daily-obsidian-conversation-sync|Daily Obsidian conversation sync]]") == 1
    assert index.count("[[Conversations/overnight-portfolio-goal|Overnight portfolio goal]]") == 1
