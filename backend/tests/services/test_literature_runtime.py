from __future__ import annotations

from domain.paper_cards import PaperCard
from domain.research_sessions import ResearchSession
from domain.topic_workspaces import TopicWorkspace
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository
from services.literature_runtime import LiteratureAgentRuntime
from services.memory_service import MemoryService


class FakeRetrievalService:
    def retrieve(self, *, question: str, time_window_years: int, research_domain: str):
        return type(
            "RetrievalResult",
            (),
            {
                "queries": [question, f"{question} survey"],
                "candidate_papers": [
                    {
                        "paper_id": "paper-1",
                        "title": "Agentic RAG",
                        "authors": ["A. Researcher"],
                        "year": 2025,
                        "venue": "ICLR",
                        "source": "arxiv",
                        "url": "https://arxiv.org/abs/1234.5678",
                        "pdf_url": "https://arxiv.org/pdf/1234.5678",
                        "abstract": "Agentic retrieval system.",
                        "keywords": ["agent", "rag"],
                        "problem": "Improve retrieval quality.",
                    }
                ],
            },
        )()


class FakeScreeningService:
    def select_representative_papers(self, *, question: str, candidates: list[dict[str, object]], max_results: int):
        return candidates[:max_results]


class FakeAnalysisService:
    def build_paper_card(self, *, workspace_id: str, paper: dict[str, object]) -> PaperCard:
        return PaperCard.create(
            workspace_id=workspace_id,
            title=str(paper["title"]),
            authors=list(paper["authors"]),
            year=int(paper["year"]),
            venue=str(paper["venue"]),
            source=str(paper["source"]),
            url="https://arxiv.org/pdf/1234.5678.pdf",
            abstract=str(paper["abstract"]),
            keywords=list(paper["keywords"]),
            problem=str(paper["problem"]),
            method="Planner-guided retrieval.",
        )


def test_literature_runtime_builds_research_card_and_writes_paper_memory(tmp_path) -> None:
    memory_service = MemoryService(
        paper_card_repository=PaperCardRepository(tmp_path),
        topic_note_repository=TopicNoteRepository(tmp_path),
        idea_note_repository=IdeaNoteRepository(tmp_path),
    )
    runtime = LiteratureAgentRuntime(
        retrieval_service=FakeRetrievalService(),
        screening_service=FakeScreeningService(),
        analysis_service=FakeAnalysisService(),
        memory_service=memory_service,
    )
    workspace = TopicWorkspace.create(
        title="Agent Search",
        description="Track recent papers.",
        research_domain="ai",
    )
    session = ResearchSession.create(
        workspace_id=workspace.id,
        question="What are the recent representative papers for agent search?",
        intent_type="find_representative_papers",
        time_window_years=2,
    )

    plan = runtime.generate_plan(session, workspace)
    result = runtime.execute(session, workspace, {"paper_cards": [], "topic_notes": [], "idea_notes": []})

    assert len(plan["queries"]) == 2
    assert result.research_card.representative_papers
    assert result.events
    stored_cards = memory_service.paper_card_repository.list_by_workspace_id(workspace.id)
    assert len(stored_cards) == 1
