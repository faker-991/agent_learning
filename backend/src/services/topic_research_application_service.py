"""Application service for topic workspaces and research sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from infrastructure.storage.event_repository import EventRepository
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.research_card_repository import ResearchCardRepository
from infrastructure.storage.research_session_repository import ResearchSessionRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository
from infrastructure.storage.topic_workspace_repository import TopicWorkspaceRepository
from domain.research_sessions import ResearchSession
from domain.topic_workspaces import TopicWorkspace
from services.memory_service import MemoryService
from workflows.literature_workflow import (
    LiteratureRuntime,
    LiteratureWorkflow,
    LiteratureWorkflowRunResult,
)


@dataclass(slots=True)
class TopicResearchApplicationService:
    """High-level API for topic workspaces and literature sessions."""

    base_dir: str | Path
    runtime: LiteratureRuntime
    workspace_repository: TopicWorkspaceRepository = field(init=False)
    session_repository: ResearchSessionRepository = field(init=False)
    research_card_repository: ResearchCardRepository = field(init=False)
    event_repository: EventRepository = field(init=False)
    memory_service: MemoryService = field(init=False)
    workflow: LiteratureWorkflow = field(init=False)

    def __post_init__(self) -> None:
        self.workspace_repository = TopicWorkspaceRepository(self.base_dir)
        self.session_repository = ResearchSessionRepository(self.base_dir)
        self.research_card_repository = ResearchCardRepository(self.base_dir)
        self.event_repository = EventRepository(self.base_dir)
        self.memory_service = MemoryService(
            paper_card_repository=PaperCardRepository(self.base_dir),
            topic_note_repository=TopicNoteRepository(self.base_dir),
            idea_note_repository=IdeaNoteRepository(self.base_dir),
        )
        self.workflow = LiteratureWorkflow(
            session_repository=self.session_repository,
            research_card_repository=self.research_card_repository,
            event_repository=self.event_repository,
            memory_service=self.memory_service,
            runtime=self.runtime,
        )

    def create_workspace(
        self,
        *,
        title: str,
        description: str,
        research_domain: str,
    ) -> TopicWorkspace:
        workspace = TopicWorkspace.create(
            title=title,
            description=description,
            research_domain=research_domain,
        )
        self.workspace_repository.save(workspace)
        return workspace

    def create_session(
        self,
        *,
        workspace_id: str,
        question: str,
        intent_type: str,
        time_window_years: int,
    ) -> ResearchSession:
        session = ResearchSession.create(
            workspace_id=workspace_id,
            question=question,
            intent_type=intent_type,
            time_window_years=time_window_years,
        )
        self.session_repository.save(session)
        return session

    def generate_plan(self, session_id: str) -> ResearchSession:
        session = self._require_session(session_id)
        workspace = self._require_workspace(session.workspace_id)
        return self.workflow.generate_plan(session=session, workspace=workspace)

    def run_session(self, session_id: str) -> LiteratureWorkflowRunResult:
        session = self._require_session(session_id)
        workspace = self._require_workspace(session.workspace_id)
        return self.workflow.run(session=session, workspace=workspace)

    def _require_workspace(self, workspace_id: str) -> TopicWorkspace:
        workspace = self.workspace_repository.get(workspace_id)
        if workspace is None:
            raise ValueError(f"Workspace not found: {workspace_id}")
        return workspace

    def _require_session(self, session_id: str) -> ResearchSession:
        session = self.session_repository.get(session_id)
        if session is None:
            raise ValueError(f"Session not found: {session_id}")
        return session
