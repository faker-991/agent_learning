from __future__ import annotations

from agents.orchestrator import OrchestratorAgent
from domain.enums import TaskStatus
from domain.tasks import ResearchTask


def make_task(status: TaskStatus) -> ResearchTask:
    task = ResearchTask.create(
        project_id="project-1",
        title="Track AI search moves",
        question="How should we respond to AI search competitors?",
        template_type="competitor_research",
    )
    task.status = status
    return task


def test_orchestrator_routes_planning_to_pending_approval() -> None:
    orchestrator = OrchestratorAgent()

    task = make_task(TaskStatus.PLANNING)
    result = orchestrator.advance(task, plan_snapshot={"angles": ["competition"]})

    assert result.current_stage == TaskStatus.PENDING_APPROVAL.value
    assert result.handler_name == "task_planning_agent"


def test_orchestrator_routes_reviewing_to_synthesizing() -> None:
    orchestrator = OrchestratorAgent()

    task = make_task(TaskStatus.REVIEWING)
    result = orchestrator.advance(task)

    assert result.current_stage == TaskStatus.SYNTHESIZING.value
    assert result.handler_name == "evidence_review_agent"
