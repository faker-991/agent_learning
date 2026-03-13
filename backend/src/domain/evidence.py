"""Evidence items collected during research."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class Evidence:
    """Structured evidence unit attached to a research task."""

    id: str
    task_id: str
    project_id: str
    title: str
    url: str | None = None
    source_type: str = "web"
    snippet: str | None = None
    summary: str | None = None
    credibility: str = "unreviewed"
    stance: str = "neutral"
    tags: list[str] = field(default_factory=list)
    collected_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        project_id: str,
        title: str,
        url: str | None = None,
        source_type: str = "web",
        snippet: str | None = None,
        summary: str | None = None,
        credibility: str = "unreviewed",
        stance: str = "neutral",
        tags: list[str] | None = None,
    ) -> "Evidence":
        return cls(
            id=f"evidence-{uuid4().hex[:12]}",
            task_id=task_id,
            project_id=project_id,
            title=title,
            url=url,
            source_type=source_type,
            snippet=snippet,
            summary=summary,
            credibility=credibility,
            stance=stance,
            tags=list(tags or []),
        )
