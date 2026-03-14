"""Repository for literature research sessions."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from domain.research_sessions import ResearchSession, SessionStatus
from infrastructure.storage.json_store import JsonStore


class ResearchSessionRepository:
    """File-backed repository for research sessions."""

    def __init__(self, base_dir: str | Path) -> None:
        self._store = JsonStore(base_dir)

    def save(self, session: ResearchSession) -> None:
        self._store.write(Path("sessions") / f"{session.id}.json", self._to_dict(session))

    def get(self, session_id: str) -> ResearchSession | None:
        payload = self._store.read(Path("sessions") / f"{session_id}.json")
        if payload is None:
            return None
        return self._from_dict(payload)

    def list_by_workspace_id(self, workspace_id: str) -> list[ResearchSession]:
        sessions_dir = self._store.base_dir / "sessions"
        if not sessions_dir.exists():
            return []
        sessions: list[ResearchSession] = []
        for path in sorted(sessions_dir.glob("*.json")):
            payload = self._store.read(path.relative_to(self._store.base_dir))
            if payload and payload.get("workspace_id") == workspace_id:
                sessions.append(self._from_dict(payload))
        return sessions

    @staticmethod
    def _to_dict(session: ResearchSession) -> dict[str, object]:
        return {
            "id": session.id,
            "workspace_id": session.workspace_id,
            "question": session.question,
            "intent_type": session.intent_type,
            "time_window_years": session.time_window_years,
            "status": session.status.value,
            "plan_snapshot": session.plan_snapshot,
            "retrieved_paper_ids": session.retrieved_paper_ids,
            "selected_paper_ids": session.selected_paper_ids,
            "research_card_id": session.research_card_id,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }

    @staticmethod
    def _from_dict(payload: dict[str, object]) -> ResearchSession:
        def parse_datetime(value: object) -> datetime:
            return datetime.fromisoformat(str(value)) if value else datetime.now(UTC)

        return ResearchSession(
            id=str(payload["id"]),
            workspace_id=str(payload["workspace_id"]),
            question=str(payload["question"]),
            intent_type=str(payload["intent_type"]),
            time_window_years=int(payload["time_window_years"]),
            status=SessionStatus(str(payload["status"])),
            plan_snapshot=dict(payload.get("plan_snapshot") or {}) or None,
            retrieved_paper_ids=list(payload.get("retrieved_paper_ids", [])),
            selected_paper_ids=list(payload.get("selected_paper_ids", [])),
            research_card_id=payload.get("research_card_id"),
            created_at=parse_datetime(payload.get("created_at")),
            updated_at=parse_datetime(payload.get("updated_at")),
        )
