"""Idea and hypothesis notes for user research thinking."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class IdeaNote:
    """Persistent user idea or hypothesis."""

    id: str
    workspace_id: str
    title: str
    idea_type: str
    content: str
    related_paper_ids: list[str]
    confidence: float = 0.5
    status: str = "active"
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        title: str,
        idea_type: str,
        content: str,
        related_paper_ids: list[str],
    ) -> "IdeaNote":
        return cls(
            id=f"idea-{uuid4().hex[:12]}",
            workspace_id=workspace_id,
            title=title,
            idea_type=idea_type,
            content=content,
            related_paper_ids=list(related_paper_ids),
        )

