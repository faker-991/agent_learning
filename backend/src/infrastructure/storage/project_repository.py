"""Repository for projects."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.projects import Project
from infrastructure.storage.json_store import JsonStore


class ProjectRepository:
    """File-backed repository for projects."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, project: Project) -> None:
        self._store.write(Path("projects") / f"{project.id}.json", self._to_dict(project))

    def get(self, project_id: str) -> Project | None:
        payload = self._store.read(Path("projects") / f"{project_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_all(self) -> list[Project]:
        projects_dir = self._store.base_dir / "projects"
        if not projects_dir.exists():
            return []
        projects: list[Project] = []
        for path in sorted(projects_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload:
                projects.append(self._from_dict(payload))
        return projects

    @staticmethod
    def _to_dict(project: Project) -> dict[str, object]:
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "default_template_type": project.default_template_type,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> Project:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return Project(
            id=str(payload["id"]),
            name=str(payload["name"]),
            description=payload.get("description"),
            default_template_type=payload.get("default_template_type"),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
