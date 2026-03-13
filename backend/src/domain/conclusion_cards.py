"""Conclusion card output for completed research tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class ConclusionCard:
    """Structured conclusion output for a research task."""

    id: str
    task_id: str
    project_id: str
    problem_definition: str
    core_conclusion: str
    key_evidence: list[str]
    alternative_views: list[str]
    recommended_actions: list[str]
    risks_and_uncertainties: list[str]
    citations: list[str]
    version: int = 1
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        project_id: str,
        problem_definition: str,
        core_conclusion: str,
        key_evidence: list[str],
        alternative_views: list[str],
        recommended_actions: list[str],
        risks_and_uncertainties: list[str],
        citations: list[str],
    ) -> "ConclusionCard":
        return cls(
            id=f"card-{uuid4().hex[:12]}",
            task_id=task_id,
            project_id=project_id,
            problem_definition=problem_definition,
            core_conclusion=core_conclusion,
            key_evidence=list(key_evidence),
            alternative_views=list(alternative_views),
            recommended_actions=list(recommended_actions),
            risks_and_uncertainties=list(risks_and_uncertainties),
            citations=list(citations),
        )
