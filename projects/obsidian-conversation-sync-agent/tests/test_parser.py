from pathlib import Path

from obsidian_sync_agent.parser import parse_file


def test_parse_chatgpt_export_sample():
    sample = Path(__file__).resolve().parents[1] / "sample-data" / "chatgpt-export-sample.json"

    conversations = parse_file(sample)

    assert len(conversations) == 1
    conversation = conversations[0]
    assert conversation.title == "Turn AI Conversations Into Notes"
    assert [message.role for message in conversation.messages] == ["user", "assistant"]
    assert "Obsidian notes" in conversation.messages[0].content


def test_parse_plain_text_file(tmp_path):
    source = tmp_path / "rough-codex-note.txt"
    source.write_text("Remember to document the workflow.", encoding="utf-8")

    conversations = parse_file(source)

    assert conversations[0].title == "Rough Codex Note"
    assert conversations[0].messages[0].role == "source"
    assert "document the workflow" in conversations[0].messages[0].content
