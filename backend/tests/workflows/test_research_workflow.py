from __future__ import annotations

from services.task_application_service import TaskApplicationService


def test_approved_task_generates_card_and_events(tmp_path) -> None:
    service = TaskApplicationService(base_dir=tmp_path)

    task = service.create_task(
        project_id="project-1",
        title="Study AI search positioning",
        question="How should we position against AI search competitors?",
        template_type="competitor_research",
    )

    service.generate_plan(task.id)
    service.approve_plan(task.id)
    result = service.run(task.id)

    assert result.conclusion_card is not None
    assert any(event.stage == "synthesizing" for event in result.events)
