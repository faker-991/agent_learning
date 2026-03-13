"""Project routes."""

from __future__ import annotations

from fastapi import APIRouter, Request, status

from app.schemas import CreateProjectRequest, ProjectResponse
from domain.projects import Project


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: CreateProjectRequest, request: Request) -> ProjectResponse:
    container = request.app.state.container
    project = Project.create(
        name=payload.name,
        description=payload.description,
        default_template_type=payload.default_template_type,
    )
    container.project_repository.save(project)
    return ProjectResponse.model_validate(project, from_attributes=True)


@router.get("", response_model=list[ProjectResponse])
async def list_projects(request: Request) -> list[ProjectResponse]:
    container = request.app.state.container
    return [
        ProjectResponse.model_validate(project, from_attributes=True)
        for project in container.project_repository.list_all()
    ]
