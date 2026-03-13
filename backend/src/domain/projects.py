"""Project aggregate for grouping research tasks and assets."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class Project:
    """Container for a business research theme."""

    id: str
    name: str
    description: str | None = None
    default_template_type: str | None = None
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str | None = None,
        default_template_type: str | None = None,
    ) -> "Project":
        return cls(
            id=f"project-{uuid4().hex[:12]}",
            name=name,
            description=description,
            default_template_type=default_template_type,
        )
