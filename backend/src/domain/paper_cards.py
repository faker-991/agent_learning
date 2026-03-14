"""Structured paper memory cards."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class PaperCard:
    """Persistent paper memory item."""

    id: str
    workspace_id: str
    title: str
    authors: list[str]
    year: int
    venue: str
    source: str
    url: str
    abstract: str
    keywords: list[str]
    problem: str
    method: str
    contributions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    relevance_score: float = 0.0
    notes: str = ""
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        title: str,
        authors: list[str],
        year: int,
        venue: str,
        source: str,
        url: str,
        abstract: str,
        keywords: list[str],
        problem: str,
        method: str,
    ) -> "PaperCard":
        return cls(
            id=f"paper-{uuid4().hex[:12]}",
            workspace_id=workspace_id,
            title=title,
            authors=list(authors),
            year=year,
            venue=venue,
            source=source,
            url=url,
            abstract=abstract,
            keywords=list(keywords),
            problem=problem,
            method=method,
        )

