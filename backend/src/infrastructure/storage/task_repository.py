"""Repository for persisting research tasks."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.enums import TaskStatus
from domain.tasks import ResearchTask
from infrastructure.storage.json_store import JsonStore


class TaskRepository:
    """File-backed repository for research tasks."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, task: ResearchTask) -> None:
        self._store.write(Path("tasks") / f"{task.id}.json", self._to_dict(task))

    def get(self, task_id: str) -> ResearchTask | None:
        payload = self._store.read(Path("tasks") / f"{task_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    @staticmethod
    def _to_dict(task: ResearchTask) -> dict[str, object]:
        return {
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "question": task.question,
            "template_type": task.template_type,
            "background": task.background,
            "goal": task.goal,
            "constraints": task.constraints,
            "status": task.status.value,
            "plan_snapshot": task.plan_snapshot,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "started_at": task.started_at,
            "completed_at": task.completed_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> ResearchTask:
        def parse_datetime(value: object) -> datetime | None:
            if value is None:
                return None
            return datetime.fromisoformat(str(value))

        return ResearchTask(
            id=str(payload["id"]),
            project_id=str(payload["project_id"]),
            title=str(payload["title"]),
            question=str(payload["question"]),
            template_type=str(payload["template_type"]),
            background=payload.get("background"),
            goal=payload.get("goal"),
            constraints=list(payload.get("constraints", [])),
            status=TaskStatus(str(payload["status"])),
            plan_snapshot=payload.get("plan_snapshot"),
            created_at=parse_datetime(payload.get("created_at")) or datetime.now(UTC),
            updated_at=parse_datetime(payload.get("updated_at")) or datetime.now(UTC),
            started_at=parse_datetime(payload.get("started_at")),
            completed_at=parse_datetime(payload.get("completed_at")),
        )
