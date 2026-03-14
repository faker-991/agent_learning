"""Research session routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import (
    CreateResearchSessionRequest,
    EventListResponse,
    EventResponse,
    ResearchCardResponse,
    ResearchSessionResponse,
)


router = APIRouter(tags=["research-sessions"])


@router.post(
    "/topics/{topic_id}/sessions",
    response_model=ResearchSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_session(
    topic_id: str,
    payload: CreateResearchSessionRequest,
    request: Request,
) -> ResearchSessionResponse:
    container = request.app.state.container
    topic = container.topic_service.workspace_repository.get(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    session = container.topic_service.create_session(
        workspace_id=topic_id,
        question=payload.question,
        intent_type=payload.intent_type,
        time_window_years=payload.time_window_years,
    )
    return _to_session_response(session)


@router.get("/topics/{topic_id}/sessions", response_model=list[ResearchSessionResponse])
async def list_sessions(topic_id: str, request: Request) -> list[ResearchSessionResponse]:
    container = request.app.state.container
    topic = container.topic_service.workspace_repository.get(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return [
        _to_session_response(session)
        for session in container.topic_service.session_repository.list_by_workspace_id(topic_id)
    ]


@router.get("/sessions/{session_id}", response_model=ResearchSessionResponse)
async def get_session(session_id: str, request: Request) -> ResearchSessionResponse:
    container = request.app.state.container
    session = container.topic_service.session_repository.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return _to_session_response(session)


@router.post("/sessions/{session_id}/plan", response_model=ResearchSessionResponse)
async def generate_session_plan(session_id: str, request: Request) -> ResearchSessionResponse:
    container = request.app.state.container
    session = container.topic_service.generate_plan(session_id)
    return _to_session_response(session)


@router.post("/sessions/{session_id}/run", response_model=ResearchSessionResponse)
async def run_session(session_id: str, request: Request) -> ResearchSessionResponse:
    container = request.app.state.container
    result = container.topic_service.run_session(session_id)
    return _to_session_response(result.session)


@router.get("/sessions/{session_id}/events", response_model=EventListResponse)
async def list_session_events(session_id: str, request: Request) -> EventListResponse:
    container = request.app.state.container
    events = container.topic_service.event_repository.list_by_task_id(session_id)
    return EventListResponse(
        events=[
            EventResponse(
                id=event.id,
                task_id=event.task_id,
                type=event.type,
                stage=event.stage,
                message=event.message,
            )
            for event in events
        ]
    )


@router.get("/sessions/{session_id}/research-card", response_model=ResearchCardResponse)
async def get_research_card(session_id: str, request: Request) -> ResearchCardResponse:
    container = request.app.state.container
    card = container.topic_service.research_card_repository.find_by_session_id(session_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Research card not found")
    return ResearchCardResponse.model_validate(card, from_attributes=True)


def _to_session_response(session) -> ResearchSessionResponse:
    return ResearchSessionResponse(
        id=session.id,
        workspace_id=session.workspace_id,
        question=session.question,
        intent_type=session.intent_type,
        time_window_years=session.time_window_years,
        status=session.status.value,
        plan_snapshot=session.plan_snapshot,
        retrieved_paper_ids=session.retrieved_paper_ids,
        selected_paper_ids=session.selected_paper_ids,
        research_card_id=session.research_card_id,
    )
