from __future__ import annotations

from dataclasses import dataclass

from domain.events import TaskEvent
from domain.research_cards import ResearchCard
from services.topic_research_application_service import TopicResearchApplicationService
from workflows.literature_workflow import LiteratureRuntimeResult


@dataclass
class FakeLiteratureRuntime:
    calls: int = 0

    def generate_plan(self, session, workspace):
        self.calls += 1
        return {
            "objective": session.question,
            "queries": [session.question, f"{session.question} survey"],
        }

    def execute(self, session, workspace, recalled_memory):
        self.calls += 1
        return LiteratureRuntimeResult(
            research_card=ResearchCard.create(
                workspace_id=workspace.id,
                session_id=session.id,
                problem_definition=session.question,
                representative_papers=["paper-1"],
                main_method_tracks=["retrieval"],
                method_differences=["retrieval is simpler than planner-heavy pipelines"],
                research_gaps=["few benchmarks study memory carry-over"],
                improvement_directions=["combine retrieval with durable memory"],
                reading_order=["paper-1"],
                citations=["https://arxiv.org/abs/1234.5678"],
            ),
            events=[
                TaskEvent.create(
                    task_id=session.id,
                    type="memory_recalled",
                    stage="memory",
                    message=f"Recalled {len(recalled_memory['paper_cards'])} paper cards.",
                ),
                TaskEvent.create(
                    task_id=session.id,
                    type="screening_completed",
                    stage="screening",
                    message="Representative papers selected.",
                ),
            ],
        )


def test_literature_workflow_runs_memory_then_screening_then_synthesis(tmp_path) -> None:
    service = TopicResearchApplicationService(base_dir=tmp_path, runtime=FakeLiteratureRuntime())

    workspace = service.create_workspace(
        title="Agent Search",
        description="Track memory-heavy agent papers.",
        research_domain="ai",
    )
    session = service.create_session(
        workspace_id=workspace.id,
        question="What are the recent representative papers for agent search?",
        intent_type="find_representative_papers",
        time_window_years=2,
    )

    planned = service.generate_plan(session.id)
    result = service.run_session(session.id)

    assert planned.plan_snapshot == {
        "objective": "What are the recent representative papers for agent search?",
        "queries": [
            "What are the recent representative papers for agent search?",
            "What are the recent representative papers for agent search? survey",
        ],
    }
    assert result.research_card is not None
    assert any(event.stage == "screening" for event in result.events)
    assert any(event.stage == "memory" for event in result.events)
