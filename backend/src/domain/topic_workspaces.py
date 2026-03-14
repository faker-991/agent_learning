"""Topic workspace aggregate for literature research."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class TopicWorkspace:
    """Container for a long-lived research topic."""

    id: str
    title: str
    description: str | None
    research_domain: str
    default_time_window: int = 2
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        title: str,
        description: str | None,
        research_domain: str,
        default_time_window: int = 2,
    ) -> "TopicWorkspace":
        return cls(
            id=f"topic-{uuid4().hex[:12]}",
            title=title,
            description=description,
            research_domain=research_domain,
            default_time_window=default_time_window,
        )

