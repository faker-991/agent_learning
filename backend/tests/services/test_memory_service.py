from __future__ import annotations

from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository
from domain.idea_notes import IdeaNote
from domain.paper_cards import PaperCard
from domain.topic_notes import TopicNote
from services.memory_service import MemoryService


def test_memory_service_recalls_relevant_topic_state_and_writes_new_idea_note(tmp_path) -> None:
    paper_repo = PaperCardRepository(tmp_path)
    topic_note_repo = TopicNoteRepository(tmp_path)
    idea_repo = IdeaNoteRepository(tmp_path)

    paper_repo.save(
        PaperCard.create(
            workspace_id="topic-1",
            title="Planner Memory",
            authors=["A. Researcher"],
            year=2025,
            venue="ICLR",
            source="arxiv",
            url="https://arxiv.org/pdf/1111.2222.pdf",
            abstract="Memory-aware planning.",
            keywords=["memory", "planner"],
            problem="Improve agent memory.",
            method="Planner-guided memory retrieval.",
        )
    )
    topic_note_repo.save(
        TopicNote.create(
            workspace_id="topic-1",
            title="Topic summary",
            summary="Memory quality is still weak.",
            open_questions=["How to evaluate memory recall?"],
            method_clusters=["memory systems"],
            last_updated_from_session_id="session-1",
        )
    )
    idea_repo.save(
        IdeaNote.create(
            workspace_id="topic-1",
            title="Memory plus planning",
            idea_type="combination",
            content="Combine planner with durable memory.",
            related_paper_ids=[],
        )
    )

    service = MemoryService(
        paper_card_repository=paper_repo,
        topic_note_repository=topic_note_repo,
        idea_note_repository=idea_repo,
    )

    recalled = service.recall_for_question(
        workspace_id="topic-1",
        question="Can retrieval and planning be combined?",
    )

    assert recalled["paper_cards"]
    assert recalled["topic_notes"]
    assert recalled["idea_notes"]

    created = service.write_back_idea(
        workspace_id="topic-1",
        title="Combine retrieval and planning",
        content="Potential hybrid direction",
        related_paper_ids=["paper-1"],
    )

    assert created.related_paper_ids == ["paper-1"]
