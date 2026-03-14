"""Workflow service for literature research sessions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from domain.events import TaskEvent
from domain.research_cards import ResearchCard
from domain.research_sessions import ResearchSession
from domain.topic_workspaces import TopicWorkspace
from infrastructure.storage.event_repository import EventRepository
from infrastructure.storage.research_card_repository import ResearchCardRepository
from infrastructure.storage.research_session_repository import ResearchSessionRepository
from services.memory_service import MemoryService


@dataclass(slots=True)
class LiteratureRuntimeResult:
    """Structured output returned by a literature runtime."""

    research_card: ResearchCard
    events: list[TaskEvent]


class LiteratureRuntime(Protocol):
    """Capability contract for topic research execution."""

    def generate_plan(
        self,
        session: ResearchSession,
        workspace: TopicWorkspace,
    ) -> dict[str, object]:
        """Generate a plan snapshot for the session."""

    def execute(
        self,
        session: ResearchSession,
        workspace: TopicWorkspace,
        recalled_memory: dict[str, list[object]],
    ) -> LiteratureRuntimeResult:
        """Execute the literature workflow and return the output card plus events."""


@dataclass(slots=True)
class LiteratureWorkflowRunResult:
    """Aggregated workflow output for a literature session."""

    session: ResearchSession
    research_card: ResearchCard | None
    events: list[TaskEvent]


class LiteratureWorkflow:
    """Coordinates a topic research session with memory recall and write-back."""

    def __init__(
        self,
        *,
        session_repository: ResearchSessionRepository,
        research_card_repository: ResearchCardRepository,
        event_repository: EventRepository,
        memory_service: MemoryService,
        runtime: LiteratureRuntime,
    ) -> None:
        self.session_repository = session_repository
        self.research_card_repository = research_card_repository
        self.event_repository = event_repository
        self.memory_service = memory_service
        self.runtime = runtime

    def generate_plan(
        self,
        *,
        session: ResearchSession,
        workspace: TopicWorkspace,
    ) -> ResearchSession:
        plan_snapshot = self.runtime.generate_plan(session, workspace)
        session.attach_plan(plan_snapshot)
        self.session_repository.save(session)
        self.event_repository.append(
            TaskEvent.create(
                task_id=session.id,
                type="plan_generated",
                stage="planning",
                message="Literature plan generated.",
            )
        )
        return session

    def run(
        self,
        *,
        session: ResearchSession,
        workspace: TopicWorkspace,
    ) -> LiteratureWorkflowRunResult:
        recalled_memory = self.memory_service.recall_for_question(
            workspace_id=workspace.id,
            question=session.question,
        )
        runtime_result = self.runtime.execute(session, workspace, recalled_memory)
        self.research_card_repository.save(runtime_result.research_card)
        session.attach_research_card(runtime_result.research_card.id)
        session.complete()
        self.session_repository.save(session)

        for event in runtime_result.events:
            self.event_repository.append(event)

        self.event_repository.append(
            TaskEvent.create(
                task_id=session.id,
                type="session_completed",
                stage="synthesizing",
                message="Literature session completed.",
            )
        )

        return LiteratureWorkflowRunResult(
            session=session,
            research_card=runtime_result.research_card,
            events=self.event_repository.list_by_task_id(session.id),
        )
