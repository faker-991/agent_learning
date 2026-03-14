"""Research guidance card output."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class ResearchCard:
    """Structured guidance card for a literature research session."""

    id: str
    workspace_id: str
    session_id: str
    problem_definition: str
    representative_papers: list[str]
    main_method_tracks: list[str]
    method_differences: list[str]
    research_gaps: list[str]
    improvement_directions: list[str]
    reading_order: list[str]
    citations: list[str]
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        session_id: str,
        problem_definition: str,
        representative_papers: list[str],
        main_method_tracks: list[str],
        method_differences: list[str],
        research_gaps: list[str],
        improvement_directions: list[str],
        reading_order: list[str],
        citations: list[str],
    ) -> "ResearchCard":
        return cls(
            id=f"research-card-{uuid4().hex[:12]}",
            workspace_id=workspace_id,
            session_id=session_id,
            problem_definition=problem_definition,
            representative_papers=list(representative_papers),
            main_method_tracks=list(main_method_tracks),
            method_differences=list(method_differences),
            research_gaps=list(research_gaps),
            improvement_directions=list(improvement_directions),
            reading_order=list(reading_order),
            citations=list(citations),
        )
