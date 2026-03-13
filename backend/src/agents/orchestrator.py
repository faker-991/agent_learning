"""Task lifecycle orchestrator for bounded sub-agents."""

from __future__ import annotations

from dataclasses import dataclass

from agents.conclusion_synthesis_agent import ConclusionSynthesisAgent
from agents.decision_advisory_agent import DecisionAdvisoryAgent
from agents.evidence_research_agent import EvidenceResearchAgent
from agents.evidence_review_agent import EvidenceReviewAgent
from agents.task_planning_agent import TaskPlanningAgent
from domain.enums import TaskStatus
from domain.tasks import ResearchTask


@dataclass(slots=True)
class OrchestratorResult:
    """Outcome of advancing a task by one orchestration step."""

    current_stage: str
    handler_name: str


class OrchestratorAgent:
    """Routes tasks through bounded agents based on lifecycle status."""

    def __init__(self) -> None:
        self.task_planning_agent = TaskPlanningAgent()
        self.evidence_research_agent = EvidenceResearchAgent()
        self.evidence_review_agent = EvidenceReviewAgent()
        self.conclusion_synthesis_agent = ConclusionSynthesisAgent()
        self.decision_advisory_agent = DecisionAdvisoryAgent()

    def advance(
        self,
        task: ResearchTask,
        *,
        plan_snapshot: dict[str, object] | None = None,
    ) -> OrchestratorResult:
        if task.status is TaskStatus.PLANNING:
            task.mark_pending_approval(plan_snapshot=plan_snapshot or {})
            return OrchestratorResult(
                current_stage=task.status.value,
                handler_name=self.task_planning_agent.name,
            )

        if task.status is TaskStatus.PENDING_APPROVAL:
            task.approve_plan()
            return OrchestratorResult(
                current_stage=task.status.value,
                handler_name=self.evidence_research_agent.name,
            )

        if task.status is TaskStatus.RESEARCHING:
            task.start_review()
            return OrchestratorResult(
                current_stage=task.status.value,
                handler_name=self.evidence_research_agent.name,
            )

        if task.status is TaskStatus.REVIEWING:
            task.start_synthesis()
            return OrchestratorResult(
                current_stage=task.status.value,
                handler_name=self.evidence_review_agent.name,
            )

        if task.status is TaskStatus.SYNTHESIZING:
            task.complete()
            return OrchestratorResult(
                current_stage=task.status.value,
                handler_name=self.conclusion_synthesis_agent.name,
            )

        raise ValueError(f"Unsupported task status for orchestration: {task.status.value}")
