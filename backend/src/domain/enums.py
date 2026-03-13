"""Shared enums for business research domain objects."""

from __future__ import annotations

from enum import StrEnum


class TaskStatus(StrEnum):
    """Lifecycle states for a research task."""

    DRAFT = "draft"
    PLANNING = "planning"
    PENDING_APPROVAL = "pending_approval"
    RESEARCHING = "researching"
    REVIEWING = "reviewing"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
