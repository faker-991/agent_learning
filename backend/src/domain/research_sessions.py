"""Research session aggregate for literature workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


class SessionStatus(StrEnum):
    """Lifecycle states for a literature research session."""

    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass(slots=True)
class ResearchSession:
    """One research round inside a topic workspace."""

    id: str
    workspace_id: str
    question: str
    intent_type: str
    time_window_years: int
    status: SessionStatus = SessionStatus.DRAFT
    plan_snapshot: dict[str, object] | None = None
    retrieved_paper_ids: list[str] = field(default_factory=list)
    selected_paper_ids: list[str] = field(default_factory=list)
    research_card_id: str | None = None
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        question: str,
        intent_type: str,
        time_window_years: int,
    ) -> "ResearchSession":
        return cls(
            id=f"session-{uuid4().hex[:12]}",
            workspace_id=workspace_id,
            question=question,
            intent_type=intent_type,
            time_window_years=time_window_years,
            status=SessionStatus.IN_PROGRESS,
        )

    def record_retrieved_papers(self, paper_ids: list[str]) -> None:
        self.retrieved_paper_ids = list(paper_ids)
        self.updated_at = _now()

    def record_selected_papers(self, paper_ids: list[str]) -> None:
        self.selected_paper_ids = list(paper_ids)
        self.updated_at = _now()

    def attach_research_card(self, card_id: str) -> None:
        self.research_card_id = card_id
        self.updated_at = _now()

    def attach_plan(self, plan_snapshot: dict[str, object]) -> None:
        self.plan_snapshot = dict(plan_snapshot)
        self.updated_at = _now()

    def complete(self) -> None:
        self.status = SessionStatus.COMPLETED
        self.updated_at = _now()
