"""Task routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import CreateTaskRequest, EventListResponse, EventResponse, TaskResponse


router = APIRouter(tags=["tasks"])


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(project_id: str, payload: CreateTaskRequest, request: Request) -> TaskResponse:
    container = request.app.state.container
    project = container.project_repository.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    task = container.task_service.create_task(
        project_id=project_id,
        title=payload.title,
        question=payload.question,
        template_type=payload.template_type,
    )
    return _to_task_response(task)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, request: Request) -> TaskResponse:
    container = request.app.state.container
    task = container.task_service.task_repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _to_task_response(task)


@router.post("/tasks/{task_id}/plan", response_model=TaskResponse)
async def generate_plan(task_id: str, request: Request) -> TaskResponse:
    container = request.app.state.container
    task = container.task_service.generate_plan(task_id)
    return _to_task_response(task)


@router.post("/tasks/{task_id}/approve", response_model=TaskResponse)
async def approve_task(task_id: str, request: Request) -> TaskResponse:
    container = request.app.state.container
    task = container.task_service.approve_plan(task_id)
    return _to_task_response(task)


@router.post("/tasks/{task_id}/run", response_model=TaskResponse)
async def run_task(task_id: str, request: Request) -> TaskResponse:
    container = request.app.state.container
    result = container.task_service.run(task_id)
    return _to_task_response(result.task)


@router.get("/tasks/{task_id}/events", response_model=EventListResponse)
async def list_task_events(task_id: str, request: Request) -> EventListResponse:
    container = request.app.state.container
    events = container.task_service.event_repository.list_by_task_id(task_id)
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


def _to_task_response(task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        question=task.question,
        template_type=task.template_type,
        status=task.status.value,
        plan_snapshot=task.plan_snapshot,
    )
