"""Research task aggregate and lifecycle transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from domain.enums import TaskStatus


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class ResearchTask:
    """Core execution unit for a business research request."""

    id: str
    project_id: str
    title: str
    question: str
    template_type: str
    background: str | None = None
    goal: str | None = None
    constraints: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.DRAFT
    plan_snapshot: dict[str, object] | None = None
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        project_id: str,
        title: str,
        question: str,
        template_type: str,
        background: str | None = None,
        goal: str | None = None,
        constraints: list[str] | None = None,
    ) -> "ResearchTask":
        return cls(
            id=f"task-{uuid4().hex[:12]}",
            project_id=project_id,
            title=title,
            question=question,
            template_type=template_type,
            background=background,
            goal=goal,
            constraints=list(constraints or []),
        )

    def start_planning(self) -> None:
        self._transition(TaskStatus.DRAFT, TaskStatus.PLANNING)

    def mark_pending_approval(self, *, plan_snapshot: dict[str, object]) -> None:
        self._transition(TaskStatus.PLANNING, TaskStatus.PENDING_APPROVAL)
        self.plan_snapshot = plan_snapshot

    def approve_plan(self) -> None:
        self._transition(TaskStatus.PENDING_APPROVAL, TaskStatus.RESEARCHING)
        self.started_at = self.started_at or _now()

    def start_research(self) -> None:
        self._transition(TaskStatus.RESEARCHING, TaskStatus.RESEARCHING)

    def start_review(self) -> None:
        self._transition(TaskStatus.RESEARCHING, TaskStatus.REVIEWING)

    def start_synthesis(self) -> None:
        self._transition(TaskStatus.REVIEWING, TaskStatus.SYNTHESIZING)

    def complete(self) -> None:
        self._transition(TaskStatus.SYNTHESIZING, TaskStatus.COMPLETED)
        self.completed_at = _now()

    def _transition(self, expected: TaskStatus, target: TaskStatus) -> None:
        if self.status is not expected:
            raise ValueError(
                f"Invalid transition from {self.status.value} to {target.value}; "
                f"expected {expected.value}."
            )
        self.status = target
        self.updated_at = _now()
