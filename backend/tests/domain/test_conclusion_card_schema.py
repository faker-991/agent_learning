from __future__ import annotations

from domain.conclusion_cards import ConclusionCard


def test_conclusion_card_contains_required_sections() -> None:
    card = ConclusionCard.create(
        task_id="task-1",
        project_id="project-1",
        problem_definition="Whether to prioritize AI search investment.",
        core_conclusion="Yes, but only in a narrow workflow first.",
        key_evidence=["Competitors are expanding search copilots."],
        alternative_views=["Wait until data quality improves."],
        recommended_actions=["Run a 6-week internal pilot."],
        risks_and_uncertainties=["Search quality depends on source freshness."],
        citations=["https://example.com/report"],
    )

    assert card.problem_definition
    assert card.core_conclusion
    assert card.key_evidence
    assert card.alternative_views
    assert card.recommended_actions
    assert card.risks_and_uncertainties
    assert card.citations
