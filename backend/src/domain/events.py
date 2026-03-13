"""Event records for task progress and activity timelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class TaskEvent:
    """Timeline event generated during task execution."""

    id: str
    task_id: str
    type: str
    stage: str
    message: str
    payload: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        type: str,
        stage: str,
        message: str,
        payload: dict[str, object] | None = None,
    ) -> "TaskEvent":
        return cls(
            id=f"event-{uuid4().hex[:12]}",
            task_id=task_id,
            type=type,
            stage=stage,
            message=message,
            payload=dict(payload or {}),
        )
