from __future__ import annotations

from domain.idea_notes import IdeaNote


def test_idea_note_tracks_related_papers_and_status() -> None:
    note = IdeaNote.create(
        workspace_id="topic-1",
        title="Combine planner with retrieval",
        idea_type="combination",
        content="Use planning to decide when retrieval should happen.",
        related_paper_ids=["paper-1", "paper-2"],
    )

    assert note.idea_type == "combination"
    assert note.related_paper_ids == ["paper-1", "paper-2"]
    assert note.status == "active"

