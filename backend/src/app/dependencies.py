"""Dependency wiring for literature topic/session routes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent import DeepResearchAgent
from config import Configuration
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository
from services.literature_retrieval_service import LiteratureRetrievalService
from services.literature_runtime import LiteratureAgentRuntime
from services.literature_sources.arxiv_client import ArxivClient
from services.literature_sources.semantic_scholar_client import SemanticScholarClient
from services.memory_service import MemoryService
from services.paper_analysis_service import PaperAnalysisService
from services.paper_screening_service import PaperScreeningService
from services.topic_research_application_service import TopicResearchApplicationService


@dataclass(slots=True)
class AppContainer:
    """Shared service container for the API."""

    config: Configuration
    topic_service: TopicResearchApplicationService


def build_container(config: Configuration) -> AppContainer:
    base_dir = Path(config.storage_workspace)
    paper_card_repository = PaperCardRepository(base_dir)
    topic_note_repository = TopicNoteRepository(base_dir)
    idea_note_repository = IdeaNoteRepository(base_dir)
    memory_service = MemoryService(
        paper_card_repository=paper_card_repository,
        topic_note_repository=topic_note_repository,
        idea_note_repository=idea_note_repository,
    )
    llm = DeepResearchAgent(config).llm
    return AppContainer(
        config=config,
        topic_service=TopicResearchApplicationService(
            base_dir=base_dir,
            runtime=LiteratureAgentRuntime(
                retrieval_service=LiteratureRetrievalService(
                    arxiv_client=ArxivClient(),
                    semantic_scholar_client=SemanticScholarClient(),
                ),
                screening_service=PaperScreeningService(),
                analysis_service=PaperAnalysisService(llm=llm),
                memory_service=memory_service,
            ),
        ),
    )
