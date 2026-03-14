from __future__ import annotations

from domain.research_cards import ResearchCard


def test_research_card_contains_required_guidance_sections() -> None:
    card = ResearchCard.create(
        workspace_id="topic-1",
        session_id="session-1",
        problem_definition="How should we compare recent agent search methods?",
        representative_papers=["paper-1", "paper-2"],
        main_method_tracks=["planner-based", "retrieval-based"],
        method_differences=["Planner-based methods trade speed for control."],
        research_gaps=["Few works study memory-heavy interaction."],
        improvement_directions=["Combine planning with memory retrieval."],
        reading_order=["paper-1", "paper-2"],
        citations=["https://arxiv.org/abs/1234.5678"],
    )

    assert card.problem_definition
    assert card.representative_papers == ["paper-1", "paper-2"]
    assert card.improvement_directions == ["Combine planning with memory retrieval."]
