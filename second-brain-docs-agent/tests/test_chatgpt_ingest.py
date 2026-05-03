from pathlib import Path

from src.ingest.chatgpt_export import read_chatgpt_exports


def test_reads_chatgpt_json_sample():
    sessions = read_chatgpt_exports(Path("data/chatgpt_sample"))

    assert len(sessions) == 1
    session = sessions[0]
    assert session.title == "Nyx Docs Agent Planning Chat"
    assert len(session.messages) == 3
    assert "draft-only Second Brain Docs Agent" in session.text
    assert session.modified_date is not None
