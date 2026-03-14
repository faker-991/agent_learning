from __future__ import annotations

from domain.topic_notes import TopicNote


def test_topic_note_records_summary_and_open_questions() -> None:
    note = TopicNote.create(
        workspace_id="topic-1",
        title="RAG topic synthesis",
        summary="Retrieval quality remains the central bottleneck.",
        open_questions=["How to evaluate adaptive retrieval?"],
        method_clusters=["adaptive retrieval", "agentic retrieval"],
        last_updated_from_session_id="session-1",
    )

    assert note.summary.startswith("Retrieval quality")
    assert note.open_questions == ["How to evaluate adaptive retrieval?"]

