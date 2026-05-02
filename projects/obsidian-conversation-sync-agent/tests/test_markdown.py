from pathlib import Path

from obsidian_sync_agent.markdown import render_conversation_note, render_index_note
from obsidian_sync_agent.models import Conversation, Message


def test_render_conversation_note_marks_human_review():
    conversation = Conversation(
        title="Learning Branches",
        messages=[
            Message(role="user", content="Explain Git branches."),
            Message(role="assistant", content="A branch is a separate line of work."),
        ],
        source_path=Path("source.json"),
        source_id="source.json#1",
    )

    note = render_conversation_note(
        conversation,
        tags=["ai-conversation", "needs-review"],
        synced_at="2026-05-02T00:00:00Z",
    )

    assert 'status: "needs human review"' in note
    assert "- ai-conversation" in note
    assert "[[AI Conversation Index|Back to AI Conversation Index]]" in note
    assert "## Connections" in note
    assert "Project: [[Project - TODO]]" in note
    assert "## Useful Takeaways" in note
    assert "## Human Summary" in note
    assert "### User" in note
    assert "### Assistant" in note


def test_render_index_note_links_to_synced_conversations():
    note = render_index_note(
        [
            {
                "note_path": "Conversations/2026-05-02-learning-branches-abc12345.md",
                "source_path": "exports/conversations.json",
                "synced_at": "2026-05-02T00:00:00Z",
                "title": "Learning Branches",
            }
        ],
        folder_title="AI Conversation Notes",
        synced_at="2026-05-02T00:00:00Z",
    )

    assert "# AI Conversation Index" in note
    assert "[[Conversations/2026-05-02-learning-branches-abc12345|Learning Branches]]" in note
    assert "## Review Workflow" in note
    assert "[[AI-Assisted Workflows]]" in note
