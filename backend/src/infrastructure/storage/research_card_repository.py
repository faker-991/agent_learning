"""Repository for research guidance cards."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.research_cards import ResearchCard
from infrastructure.storage.json_store import JsonStore


class ResearchCardRepository:
    """File-backed repository for research guidance cards."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, card: ResearchCard) -> None:
        self._store.write(Path("research_cards") / f"{card.id}.json", self._to_dict(card))

    def get(self, card_id: str) -> ResearchCard | None:
        payload = self._store.read(Path("research_cards") / f"{card_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def find_by_session_id(self, session_id: str) -> ResearchCard | None:
        cards_dir = self._store.base_dir / "research_cards"
        if not cards_dir.exists():
            return None
        for path in cards_dir.glob("*.json"):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("session_id") == session_id:
                return self._from_dict(payload)
        return None

    @staticmethod
    def _to_dict(card: ResearchCard) -> dict[str, object]:
        return {
            "id": card.id,
            "workspace_id": card.workspace_id,
            "session_id": card.session_id,
            "problem_definition": card.problem_definition,
            "representative_papers": card.representative_papers,
            "main_method_tracks": card.main_method_tracks,
            "method_differences": card.method_differences,
            "research_gaps": card.research_gaps,
            "improvement_directions": card.improvement_directions,
            "reading_order": card.reading_order,
            "citations": card.citations,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> ResearchCard:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return ResearchCard(
            id=str(payload["id"]),
            workspace_id=str(payload["workspace_id"]),
            session_id=str(payload["session_id"]),
            problem_definition=str(payload["problem_definition"]),
            representative_papers=list(payload.get("representative_papers", [])),
            main_method_tracks=list(payload.get("main_method_tracks", [])),
            method_differences=list(payload.get("method_differences", [])),
            research_gaps=list(payload.get("research_gaps", [])),
            improvement_directions=list(payload.get("improvement_directions", [])),
            reading_order=list(payload.get("reading_order", [])),
            citations=list(payload.get("citations", [])),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
