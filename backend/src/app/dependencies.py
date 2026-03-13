"""Dependency wiring for FastAPI routes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config import Configuration
from infrastructure.storage.project_repository import ProjectRepository
from services.task_application_service import TaskApplicationService


@dataclass(slots=True)
class AppContainer:
    """Shared service container for the API."""

    config: Configuration
    project_repository: ProjectRepository
    task_service: TaskApplicationService


def build_container(config: Configuration) -> AppContainer:
    base_dir = Path(config.storage_workspace)
    return AppContainer(
        config=config,
        project_repository=ProjectRepository(base_dir),
        task_service=TaskApplicationService(base_dir=base_dir),
    )
