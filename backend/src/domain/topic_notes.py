"""Topic-level synthesized notes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class TopicNote:
    """Long-term synthesis note for a topic workspace."""

    id: str
    workspace_id: str
    title: str
    summary: str
    open_questions: list[str]
    method_clusters: list[str]
    last_updated_from_session_id: str | None = None
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        title: str,
        summary: str,
        open_questions: list[str],
        method_clusters: list[str],
        last_updated_from_session_id: str | None,
    ) -> "TopicNote":
        return cls(
            id=f"topic-note-{uuid4().hex[:12]}",
            workspace_id=workspace_id,
            title=title,
            summary=summary,
            open_questions=list(open_questions),
            method_clusters=list(method_clusters),
            last_updated_from_session_id=last_updated_from_session_id,
        )

