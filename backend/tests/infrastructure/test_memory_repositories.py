from __future__ import annotations

from domain.idea_notes import IdeaNote
from domain.paper_cards import PaperCard
from domain.research_cards import ResearchCard
from domain.topic_notes import TopicNote
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.research_card_repository import ResearchCardRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository


def test_paper_card_repository_round_trips_card(tmp_path) -> None:
    repo = PaperCardRepository(base_dir=tmp_path)
    card = PaperCard.create(
        workspace_id="topic-1",
        title="Agentic RAG",
        authors=["A Researcher"],
        year=2025,
        venue="ICLR",
        source="arxiv",
        url="https://arxiv.org/pdf/1234.5678",
        abstract="An agentic retrieval method.",
        keywords=["rag"],
        problem="Improve agent search quality.",
        method="Planner-guided retrieval.",
    )

    repo.save(card)
    loaded = repo.get(card.id)

    assert loaded is not None
    assert loaded.url == "https://arxiv.org/pdf/1234.5678"


def test_topic_note_repository_round_trips_note(tmp_path) -> None:
    repo = TopicNoteRepository(base_dir=tmp_path)
    note = TopicNote.create(
        workspace_id="topic-1",
        title="Search synthesis",
        summary="Memory-heavy systems remain underexplored.",
        open_questions=["How should memory be evaluated?"],
        method_clusters=["memory"],
        last_updated_from_session_id="session-1",
    )

    repo.save(note)
    loaded = repo.get(note.id)

    assert loaded is not None
    assert loaded.open_questions == ["How should memory be evaluated?"]


def test_idea_note_repository_round_trips_note(tmp_path) -> None:
    repo = IdeaNoteRepository(base_dir=tmp_path)
    note = IdeaNote.create(
        workspace_id="topic-1",
        title="Planner plus memory",
        idea_type="hypothesis",
        content="A planning loop may benefit from durable memory.",
        related_paper_ids=["paper-1"],
    )

    repo.save(note)
    loaded = repo.get(note.id)

    assert loaded is not None
    assert loaded.related_paper_ids == ["paper-1"]


def test_research_card_repository_round_trips_card(tmp_path) -> None:
    repo = ResearchCardRepository(base_dir=tmp_path)
    card = ResearchCard.create(
        workspace_id="topic-1",
        session_id="session-1",
        problem_definition="How should we compare memory agents?",
        representative_papers=["paper-1"],
        main_method_tracks=["planner-based"],
        method_differences=["Planner-based methods are slower."],
        research_gaps=["Few benchmarks isolate memory quality."],
        improvement_directions=["Evaluate long-horizon memory recall."],
        reading_order=["paper-1"],
        citations=["https://arxiv.org/abs/1234.5678"],
    )

    repo.save(card)
    loaded = repo.get(card.id)

    assert loaded is not None
    assert loaded.improvement_directions == ["Evaluate long-horizon memory recall."]
