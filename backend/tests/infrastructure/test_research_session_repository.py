from __future__ import annotations

from domain.research_sessions import ResearchSession
from infrastructure.storage.research_session_repository import ResearchSessionRepository


def test_research_session_repository_round_trips_session(tmp_path) -> None:
    repo = ResearchSessionRepository(base_dir=tmp_path)
    session = ResearchSession.create(
        workspace_id="topic-1",
        question="What are the best recent agent memory papers?",
        intent_type="find_representative_papers",
        time_window_years=2,
    )
    session.record_retrieved_papers(["paper-1"])
    session.record_selected_papers(["paper-1"])

    repo.save(session)
    loaded = repo.get(session.id)

    assert loaded is not None
    assert loaded.retrieved_paper_ids == ["paper-1"]
    assert loaded.selected_paper_ids == ["paper-1"]

