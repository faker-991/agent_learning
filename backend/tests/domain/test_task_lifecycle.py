from __future__ import annotations

import pytest

from domain.enums import TaskStatus
from domain.tasks import ResearchTask


def make_task() -> ResearchTask:
    return ResearchTask.create(
        project_id="project-1",
        title="Evaluate AI search opportunities",
        question="Should we invest in AI search for the next planning cycle?",
        template_type="opportunity_research",
    )


def test_task_transitions_follow_v1_lifecycle() -> None:
    task = make_task()

    task.start_planning()
    task.mark_pending_approval(plan_snapshot={"focus": ["market", "product"]})
    task.approve_plan()
    task.start_research()
    task.start_review()
    task.start_synthesis()
    task.complete()

    assert task.status is TaskStatus.COMPLETED


def test_task_cannot_skip_approval_gate() -> None:
    task = make_task()
    task.start_planning()

    with pytest.raises(ValueError):
        task.start_research()
