"""Application service for business research tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from domain.tasks import ResearchTask
from infrastructure.storage.conclusion_repository import ConclusionRepository
from infrastructure.storage.event_repository import EventRepository
from infrastructure.storage.task_repository import TaskRepository
from workflows.research_workflow import ResearchWorkflow, WorkflowRunResult


@dataclass(slots=True)
class TaskApplicationService:
    """High-level API for creating, approving, and running tasks."""

    base_dir: str | Path
    task_repository: TaskRepository = field(init=False)
    conclusion_repository: ConclusionRepository = field(init=False)
    event_repository: EventRepository = field(init=False)
    workflow: ResearchWorkflow = field(init=False)

    def __post_init__(self) -> None:
        self.task_repository = TaskRepository(self.base_dir)
        self.conclusion_repository = ConclusionRepository(self.base_dir)
        self.event_repository = EventRepository(self.base_dir)
        self.workflow = ResearchWorkflow(
            task_repository=self.task_repository,
            conclusion_repository=self.conclusion_repository,
            event_repository=self.event_repository,
        )

    def create_task(
        self,
        *,
        project_id: str,
        title: str,
        question: str,
        template_type: str,
    ) -> ResearchTask:
        task = ResearchTask.create(
            project_id=project_id,
            title=title,
            question=question,
            template_type=template_type,
        )
        self.task_repository.save(task)
        return task

    def generate_plan(self, task_id: str) -> ResearchTask:
        task = self._require_task(task_id)
        return self.workflow.generate_plan(task)

    def approve_plan(self, task_id: str) -> ResearchTask:
        task = self._require_task(task_id)
        return self.workflow.approve(task)

    def run(self, task_id: str) -> WorkflowRunResult:
        task = self._require_task(task_id)
        return self.workflow.run(task)

    def _require_task(self, task_id: str) -> ResearchTask:
        task = self.task_repository.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        return task
