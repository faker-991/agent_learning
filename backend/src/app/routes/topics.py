"""Topic workspace routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import (
    CreateTopicRequest,
    IdeaNoteResponse,
    PaperCardResponse,
    TopicNoteResponse,
    TopicResponse,
)


router = APIRouter(prefix="/topics", tags=["topics"])


@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(payload: CreateTopicRequest, request: Request) -> TopicResponse:
    container = request.app.state.container
    workspace = container.topic_service.create_workspace(
        title=payload.title,
        description=payload.description,
        research_domain=payload.research_domain,
    )
    return TopicResponse.model_validate(workspace, from_attributes=True)


@router.get("", response_model=list[TopicResponse])
async def list_topics(request: Request) -> list[TopicResponse]:
    container = request.app.state.container
    return [
        TopicResponse.model_validate(workspace, from_attributes=True)
        for workspace in container.topic_service.workspace_repository.list_all()
    ]


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: str, request: Request) -> TopicResponse:
    container = request.app.state.container
    workspace = container.topic_service.workspace_repository.get(topic_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return TopicResponse.model_validate(workspace, from_attributes=True)


@router.get("/{topic_id}/papers", response_model=list[PaperCardResponse])
async def list_topic_papers(topic_id: str, request: Request) -> list[PaperCardResponse]:
    container = request.app.state.container
    workspace = container.topic_service.workspace_repository.get(topic_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return [
        PaperCardResponse.model_validate(card, from_attributes=True)
        for card in container.topic_service.memory_service.paper_card_repository.list_by_workspace_id(topic_id)
    ]


@router.get("/{topic_id}/notes", response_model=list[TopicNoteResponse])
async def list_topic_notes(topic_id: str, request: Request) -> list[TopicNoteResponse]:
    container = request.app.state.container
    workspace = container.topic_service.workspace_repository.get(topic_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return [
        TopicNoteResponse.model_validate(note, from_attributes=True)
        for note in container.topic_service.memory_service.topic_note_repository.list_by_workspace_id(topic_id)
    ]


@router.get("/{topic_id}/ideas", response_model=list[IdeaNoteResponse])
async def list_topic_ideas(topic_id: str, request: Request) -> list[IdeaNoteResponse]:
    container = request.app.state.container
    workspace = container.topic_service.workspace_repository.get(topic_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return [
        IdeaNoteResponse.model_validate(note, from_attributes=True)
        for note in container.topic_service.memory_service.idea_note_repository.list_by_workspace_id(topic_id)
    ]
