from __future__ import annotations

from domain.research_sessions import ResearchSession, SessionStatus


def test_research_session_tracks_selected_and_retrieved_papers() -> None:
    session = ResearchSession.create(
        workspace_id="topic-1",
        question="What are the strongest recent retrieval-augmented generation papers?",
        intent_type="find_representative_papers",
        time_window_years=2,
    )

    session.record_retrieved_papers(["paper-1", "paper-2"])
    session.record_selected_papers(["paper-2"])
    session.attach_research_card("card-1")
    session.complete()

    assert session.retrieved_paper_ids == ["paper-1", "paper-2"]
    assert session.selected_paper_ids == ["paper-2"]
    assert session.research_card_id == "card-1"
    assert session.status is SessionStatus.COMPLETED

