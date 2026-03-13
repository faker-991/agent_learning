"""Workflow service that advances approved tasks to completion."""

from __future__ import annotations

from dataclasses import dataclass

from agents.orchestrator import OrchestratorAgent
from domain.conclusion_cards import ConclusionCard
from domain.events import TaskEvent
from domain.tasks import ResearchTask
from infrastructure.storage.conclusion_repository import ConclusionRepository
from infrastructure.storage.event_repository import EventRepository
from infrastructure.storage.task_repository import TaskRepository


@dataclass(slots=True)
class WorkflowRunResult:
    """Aggregated workflow output after executing a task."""

    task: ResearchTask
    conclusion_card: ConclusionCard | None
    events: list[TaskEvent]


class ResearchWorkflow:
    """Advance a task through the post-approval workflow stages."""

    def __init__(
        self,
        *,
        task_repository: TaskRepository,
        conclusion_repository: ConclusionRepository,
        event_repository: EventRepository,
        orchestrator: OrchestratorAgent | None = None,
    ) -> None:
        self.task_repository = task_repository
        self.conclusion_repository = conclusion_repository
        self.event_repository = event_repository
        self.orchestrator = orchestrator or OrchestratorAgent()

    def generate_plan(self, task: ResearchTask) -> ResearchTask:
        task.start_planning()
        self.orchestrator.advance(
            task,
            plan_snapshot={
                "objective": task.question,
                "template_type": task.template_type,
            },
        )
        self.task_repository.save(task)
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="plan_generated",
                stage=task.status.value,
                message="Research plan generated and awaiting approval.",
            )
        )
        return task

    def approve(self, task: ResearchTask) -> ResearchTask:
        self.orchestrator.advance(task)
        self.task_repository.save(task)
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="task_approved",
                stage=task.status.value,
                message="Research plan approved.",
            )
        )
        return task

    def run(self, task: ResearchTask) -> WorkflowRunResult:
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="task_started",
                stage=task.status.value,
                message="Research execution started.",
            )
        )

        self.orchestrator.advance(task)
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="research_review",
                stage=task.status.value,
                message="Evidence collection complete, entering review.",
            )
        )

        self.orchestrator.advance(task)
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="synthesizing",
                stage=task.status.value,
                message="Synthesizing conclusion card.",
            )
        )

        card = ConclusionCard.create(
            task_id=task.id,
            project_id=task.project_id,
            problem_definition=task.question,
            core_conclusion="A focused pilot is the safest next move.",
            key_evidence=["Initial competitive scan suggests strong category momentum."],
            alternative_views=["Wait for more internal data before committing."],
            recommended_actions=["Launch a narrow validation sprint."],
            risks_and_uncertainties=["Evidence is still based on a lightweight V1 workflow."],
            citations=["internal://workflow-placeholder"],
        )
        self.conclusion_repository.save(card)

        self.orchestrator.advance(task)
        self.task_repository.save(task)
        self.event_repository.append(
            TaskEvent.create(
                task_id=task.id,
                type="task_completed",
                stage=task.status.value,
                message="Task completed with conclusion card output.",
            )
        )

        return WorkflowRunResult(
            task=task,
            conclusion_card=card,
            events=self.event_repository.list_by_task_id(task.id),
        )
