"""Repository for topic workspaces."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.topic_workspaces import TopicWorkspace
from infrastructure.storage.json_store import JsonStore


class TopicWorkspaceRepository:
    """File-backed repository for topic workspaces."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, workspace: TopicWorkspace) -> None:
        self._store.write(Path("topics") / f"{workspace.id}.json", self._to_dict(workspace))

    def get(self, workspace_id: str) -> TopicWorkspace | None:
        payload = self._store.read(Path("topics") / f"{workspace_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_all(self) -> list[TopicWorkspace]:
        topics_dir = self._store.base_dir / "topics"
        if not topics_dir.exists():
            return []
        workspaces: list[TopicWorkspace] = []
        for path in sorted(topics_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload:
                workspaces.append(self._from_dict(payload))
        return workspaces

    @staticmethod
    def _to_dict(workspace: TopicWorkspace) -> dict[str, object]:
        return {
            "id": workspace.id,
            "title": workspace.title,
            "description": workspace.description,
            "research_domain": workspace.research_domain,
            "default_time_window": workspace.default_time_window,
            "created_at": workspace.created_at,
            "updated_at": workspace.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> TopicWorkspace:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return TopicWorkspace(
            id=str(payload["id"]),
            title=str(payload["title"]),
            description=payload.get("description"),
            research_domain=str(payload["research_domain"]),
            default_time_window=int(payload.get("default_time_window", 2)),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
