from __future__ import annotations

from services.paper_screening_service import PaperScreeningService


def test_screening_prioritizes_top_venues_before_raw_recency() -> None:
    service = PaperScreeningService()

    selected = service.select_representative_papers(
        question="How should we compare recent AI search systems?",
        candidates=[
            {
                "paper_id": "paper-a",
                "title": "Workshop paper",
                "venue": "Random Workshop",
                "year": 2026,
                "award": None,
                "relevance_score": 0.95,
            },
            {
                "paper_id": "paper-b",
                "title": "NeurIPS paper",
                "venue": "NeurIPS",
                "year": 2025,
                "award": None,
                "relevance_score": 0.82,
            },
        ],
        max_results=5,
    )

    assert selected[0]["title"] == "NeurIPS paper"


def test_screening_prioritizes_award_signal_inside_top_tier_pool() -> None:
    service = PaperScreeningService()

    selected = service.select_representative_papers(
        question="Which recent memory-agent papers matter most?",
        candidates=[
            {
                "paper_id": "paper-a",
                "title": "Spotlight paper",
                "venue": "ICLR",
                "year": 2025,
                "award": "spotlight",
                "relevance_score": 0.8,
            },
            {
                "paper_id": "paper-b",
                "title": "Plain paper",
                "venue": "ICLR",
                "year": 2025,
                "award": None,
                "relevance_score": 0.95,
            },
        ],
        max_results=5,
    )

    assert selected[0]["title"] == "Spotlight paper"

