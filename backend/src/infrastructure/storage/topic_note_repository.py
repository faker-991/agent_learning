"""Repository for topic notes."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.topic_notes import TopicNote
from infrastructure.storage.json_store import JsonStore


class TopicNoteRepository:
    """File-backed repository for topic notes."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, note: TopicNote) -> None:
        self._store.write(Path("topic_notes") / f"{note.id}.json", self._to_dict(note))

    def get(self, note_id: str) -> TopicNote | None:
        payload = self._store.read(Path("topic_notes") / f"{note_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_by_workspace_id(self, workspace_id: str) -> list[TopicNote]:
        notes_dir = self._store.base_dir / "topic_notes"
        if not notes_dir.exists():
            return []
        notes: list[TopicNote] = []
        for path in sorted(notes_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("workspace_id") == workspace_id:
                notes.append(self._from_dict(payload))
        return notes

    @staticmethod
    def _to_dict(note: TopicNote) -> dict[str, object]:
        return {
            "id": note.id,
            "workspace_id": note.workspace_id,
            "title": note.title,
            "summary": note.summary,
            "open_questions": note.open_questions,
            "method_clusters": note.method_clusters,
            "last_updated_from_session_id": note.last_updated_from_session_id,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> TopicNote:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return TopicNote(
            id=str(payload["id"]),
            workspace_id=str(payload["workspace_id"]),
            title=str(payload["title"]),
            summary=str(payload["summary"]),
            open_questions=list(payload.get("open_questions", [])),
            method_clusters=list(payload.get("method_clusters", [])),
            last_updated_from_session_id=payload.get("last_updated_from_session_id"),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
