from __future__ import annotations

from domain.paper_cards import PaperCard


def test_paper_card_create_keeps_objective_fields() -> None:
    card = PaperCard.create(
        workspace_id="topic-1",
        title="Self-RAG",
        authors=["Akari Asai", "Xinyun Chen"],
        year=2024,
        venue="ICLR",
        source="arxiv",
        url="https://arxiv.org/pdf/2310.11511",
        abstract="A retrieval-augmented generation method with self-reflection.",
        keywords=["rag", "llm"],
        problem="Improve retrieval-augmented generation quality.",
        method="Self-reflection with adaptive retrieval.",
    )

    assert card.title == "Self-RAG"
    assert card.method == "Self-reflection with adaptive retrieval."
    assert card.limitations == []
    assert card.notes == ""

