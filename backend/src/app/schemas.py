"""Request and response schemas for the V1 API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
    default_template_type: str | None = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    default_template_type: str | None = None


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    template_type: str = Field(..., min_length=1)


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    question: str
    template_type: str
    status: str
    plan_snapshot: dict[str, object] | None = None


class EventResponse(BaseModel):
    id: str
    task_id: str
    type: str
    stage: str
    message: str


class EventListResponse(BaseModel):
    events: list[EventResponse]


class ConclusionCardResponse(BaseModel):
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
