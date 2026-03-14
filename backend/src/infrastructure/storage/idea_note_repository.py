"""Repository for idea notes."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.idea_notes import IdeaNote
from infrastructure.storage.json_store import JsonStore


class IdeaNoteRepository:
    """File-backed repository for idea notes."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, note: IdeaNote) -> None:
        self._store.write(Path("idea_notes") / f"{note.id}.json", self._to_dict(note))

    def get(self, note_id: str) -> IdeaNote | None:
        payload = self._store.read(Path("idea_notes") / f"{note_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_by_workspace_id(self, workspace_id: str) -> list[IdeaNote]:
        notes_dir = self._store.base_dir / "idea_notes"
        if not notes_dir.exists():
            return []
        notes: list[IdeaNote] = []
        for path in sorted(notes_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("workspace_id") == workspace_id:
                notes.append(self._from_dict(payload))
        return notes

    @staticmethod
    def _to_dict(note: IdeaNote) -> dict[str, object]:
        return {
            "id": note.id,
            "workspace_id": note.workspace_id,
            "title": note.title,
            "idea_type": note.idea_type,
            "content": note.content,
            "related_paper_ids": note.related_paper_ids,
            "confidence": note.confidence,
            "status": note.status,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> IdeaNote:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return IdeaNote(
            id=str(payload["id"]),
            workspace_id=str(payload["workspace_id"]),
            title=str(payload["title"]),
            idea_type=str(payload["idea_type"]),
            content=str(payload["content"]),
            related_paper_ids=list(payload.get("related_paper_ids", [])),
            confidence=float(payload.get("confidence", 0.5)),
            status=str(payload.get("status", "active")),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
