"""Minimal live runtime for topic-based literature research."""

from __future__ import annotations

from dataclasses import dataclass

from domain.events import TaskEvent
from domain.research_cards import ResearchCard


@dataclass(slots=True)
class LiteratureAgentRuntime:
    """Coordinates retrieval, screening, analysis, and memory write-back."""

    retrieval_service: object
    screening_service: object
    analysis_service: object
    memory_service: object

    def generate_plan(self, session, workspace) -> dict[str, object]:
        retrieval = self.retrieval_service.retrieve(
            question=session.question,
            time_window_years=session.time_window_years,
            research_domain=workspace.research_domain,
        )
        return {
            "objective": session.question,
            "queries": retrieval.queries,
        }

    def execute(self, session, workspace, recalled_memory):
        retrieval = self.retrieval_service.retrieve(
            question=session.question,
            time_window_years=session.time_window_years,
            research_domain=workspace.research_domain,
        )
        selected = self.screening_service.select_representative_papers(
            question=session.question,
            candidates=retrieval.candidate_papers,
            max_results=5,
        )
        session.record_retrieved_papers(
            [str(item.get("paper_id") or item.get("url")) for item in retrieval.candidate_papers]
        )
        session.record_selected_papers(
            [str(item.get("paper_id") or item.get("url")) for item in selected]
        )

        paper_cards = []
        for paper in selected:
            card = self.analysis_service.build_paper_card(
                workspace_id=workspace.id,
                paper=paper,
            )
            self.memory_service.paper_card_repository.save(card)
            paper_cards.append(card)

        research_card = ResearchCard.create(
            workspace_id=workspace.id,
            session_id=session.id,
            problem_definition=session.question,
            representative_papers=[card.id for card in paper_cards],
            main_method_tracks=[card.method for card in paper_cards[:3]],
            method_differences=["Objective paper summaries are available for follow-up discussion."],
            research_gaps=["Gap detection is still a minimal implementation in this runtime."],
            improvement_directions=["Use the retrieved papers to continue targeted discussion."],
            reading_order=[card.id for card in paper_cards],
            citations=[card.url for card in paper_cards],
        )

        result_type = type("LiteratureRuntimeResult", (), {})
        result = result_type()
        result.research_card = research_card
        result.events = [
            TaskEvent.create(
                task_id=session.id,
                type="memory_recalled",
                stage="memory",
                message=f"Recalled {len(recalled_memory['paper_cards'])} paper cards.",
            ),
            TaskEvent.create(
                task_id=session.id,
                type="retrieval_completed",
                stage="retrieval",
                message=f"Retrieved {len(retrieval.candidate_papers)} candidate papers.",
            ),
            TaskEvent.create(
                task_id=session.id,
                type="screening_completed",
                stage="screening",
                message=f"Selected {len(selected)} representative papers.",
            ),
        ]
        return result
