"""Repository for conclusion cards."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.conclusion_cards import ConclusionCard
from infrastructure.storage.json_store import JsonStore


class ConclusionRepository:
    """File-backed repository for conclusion cards."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, card: ConclusionCard) -> None:
        self._store.write(Path("conclusion_cards") / f"{card.id}.json", self._to_dict(card))

    def find_by_task_id(self, task_id: str) -> ConclusionCard | None:
        cards_dir = self._store.base_dir / "conclusion_cards"
        if not cards_dir.exists():
            return None
        for path in cards_dir.glob("*.json"):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("task_id") == task_id:
                return self._from_dict(payload)
        return None

    @staticmethod
    def _to_dict(card: ConclusionCard) -> dict[str, object]:
        return {
            "id": card.id,
            "task_id": card.task_id,
            "project_id": card.project_id,
            "problem_definition": card.problem_definition,
            "core_conclusion": card.core_conclusion,
            "key_evidence": card.key_evidence,
            "alternative_views": card.alternative_views,
            "recommended_actions": card.recommended_actions,
            "risks_and_uncertainties": card.risks_and_uncertainties,
            "citations": card.citations,
            "version": card.version,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> ConclusionCard:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return ConclusionCard(
            id=str(payload["id"]),
            task_id=str(payload["task_id"]),
            project_id=str(payload["project_id"]),
            problem_definition=str(payload["problem_definition"]),
            core_conclusion=str(payload["core_conclusion"]),
            key_evidence=list(payload.get("key_evidence", [])),
            alternative_views=list(payload.get("alternative_views", [])),
            recommended_actions=list(payload.get("recommended_actions", [])),
            risks_and_uncertainties=list(payload.get("risks_and_uncertainties", [])),
            citations=list(payload.get("citations", [])),
            version=int(payload.get("version", 1)),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
