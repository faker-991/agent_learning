from __future__ import annotations

from domain.tasks import ResearchTask
from infrastructure.storage.task_repository import TaskRepository


def test_task_repository_round_trips_task(tmp_path) -> None:
    repo = TaskRepository(base_dir=tmp_path)
    task = ResearchTask.create(
        project_id="project-1",
        title="Assess vertical AI assistants",
        question="Which vertical AI assistants are worth tracking this quarter?",
        template_type="competitor_research",
    )

    repo.save(task)
    loaded = repo.get(task.id)

    assert loaded is not None
    assert loaded.id == task.id
    assert loaded.question == task.question
