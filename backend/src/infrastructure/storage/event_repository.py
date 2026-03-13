"""Repository for task events."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.events import TaskEvent
from infrastructure.storage.json_store import JsonStore


class EventRepository:
    """File-backed repository for task events."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def append(self, event: TaskEvent) -> None:
        self._store.write(Path("events") / f"{event.id}.json", self._to_dict(event))

    def list_by_task_id(self, task_id: str) -> list[TaskEvent]:
        events_dir = self._store.base_dir / "events"
        if not events_dir.exists():
            return []

        items: list[TaskEvent] = []
        for path in sorted(events_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("task_id") == task_id:
                items.append(self._from_dict(payload))
        return items

    @staticmethod
    def _to_dict(event: TaskEvent) -> dict[str, object]:
        return {
            "id": event.id,
            "task_id": event.task_id,
            "type": event.type,
            "stage": event.stage,
            "message": event.message,
            "payload": event.payload,
            "created_at": event.created_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> TaskEvent:
        created_at = payload.get("created_at")
        return TaskEvent(
            id=str(payload["id"]),
            task_id=str(payload["task_id"]),
            type=str(payload["type"]),
            stage=str(payload["stage"]),
            message=str(payload["message"]),
            payload=dict(payload.get("payload", {})),
            created_at=(
                datetime.fromisoformat(str(created_at))
                if created_at
                else datetime.now(UTC)
            ),
        )
