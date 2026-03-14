"""Repository for paper cards."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.paper_cards import PaperCard
from infrastructure.storage.json_store import JsonStore


class PaperCardRepository:
    """File-backed repository for paper cards."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, card: PaperCard) -> None:
        self._store.write(Path("paper_cards") / f"{card.id}.json", self._to_dict(card))

    def get(self, card_id: str) -> PaperCard | None:
        payload = self._store.read(Path("paper_cards") / f"{card_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_by_workspace_id(self, workspace_id: str) -> list[PaperCard]:
        cards_dir = self._store.base_dir / "paper_cards"
        if not cards_dir.exists():
            return []
        cards: list[PaperCard] = []
        for path in sorted(cards_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("workspace_id") == workspace_id:
                cards.append(self._from_dict(payload))
        return cards

    @staticmethod
    def _to_dict(card: PaperCard) -> dict[str, object]:
        return {
            "id": card.id,
            "workspace_id": card.workspace_id,
            "title": card.title,
            "authors": card.authors,
            "year": card.year,
            "venue": card.venue,
            "source": card.source,
            "url": card.url,
            "abstract": card.abstract,
            "keywords": card.keywords,
            "problem": card.problem,
            "method": card.method,
            "contributions": card.contributions,
            "limitations": card.limitations,
            "relevance_score": card.relevance_score,
            "notes": card.notes,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> PaperCard:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return PaperCard(
            id=str(payload["id"]),
            workspace_id=str(payload["workspace_id"]),
            title=str(payload["title"]),
            authors=list(payload.get("authors", [])),
            year=int(payload["year"]),
            venue=str(payload["venue"]),
            source=str(payload["source"]),
            url=str(payload["url"]),
            abstract=str(payload["abstract"]),
            keywords=list(payload.get("keywords", [])),
            problem=str(payload["problem"]),
            method=str(payload["method"]),
            contributions=list(payload.get("contributions", [])),
            limitations=list(payload.get("limitations", [])),
            relevance_score=float(payload.get("relevance_score", 0.0)),
            notes=str(payload.get("notes", "")),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
