"""Request and response schemas for the literature research API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EventResponse(BaseModel):
    id: str
    task_id: str
    type: str
    stage: str
    message: str


class EventListResponse(BaseModel):
    events: list[EventResponse]


class CreateTopicRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    research_domain: str = Field(..., min_length=1)


class TopicResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    research_domain: str
    default_time_window: int


class CreateResearchSessionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    intent_type: str = Field(..., min_length=1)
    time_window_years: int = Field(default=2, ge=1)


class ResearchSessionResponse(BaseModel):
    id: str
    workspace_id: str
    question: str
    intent_type: str
    time_window_years: int
    status: str
    plan_snapshot: dict[str, object] | None = None
    retrieved_paper_ids: list[str] = []
    selected_paper_ids: list[str] = []
    research_card_id: str | None = None


class ResearchCardResponse(BaseModel):
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


class PaperCardResponse(BaseModel):
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


class TopicNoteResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    summary: str
    open_questions: list[str]
    method_clusters: list[str]


class IdeaNoteResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    idea_type: str
    content: str
    related_paper_ids: list[str]
    confidence: float
    status: str
