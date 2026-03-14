from __future__ import annotations

from services.literature_retrieval_service import LiteratureRetrievalService


class FakeArxivClient:
    def search(self, query: str, years: int) -> list[dict[str, object]]:
        return [
            {
                "paper_id": "paper-1",
                "title": "RAG Agents",
                "url": "https://arxiv.org/abs/1234.5678",
                "pdf_url": "https://arxiv.org/pdf/1234.5678",
                "venue": "arXiv",
                "year": 2025,
                "abstract": f"Result for {query}",
                "source": "arxiv",
            }
        ]


class FakeSemanticScholarClient:
    def search(self, query: str, years: int) -> list[dict[str, object]]:
        return [
            {
                "paper_id": "paper-1",
                "title": "RAG Agents",
                "url": "https://arxiv.org/abs/1234.5678",
                "pdf_url": "https://arxiv.org/pdf/1234.5678",
                "venue": "ICLR",
                "year": 2025,
                "abstract": f"Semantic result for {query}",
                "source": "semantic_scholar",
            },
            {
                "paper_id": "paper-2",
                "title": "Memory-Augmented Retrieval",
                "url": "https://example.org/paper-2",
                "pdf_url": "https://example.org/paper-2.pdf",
                "venue": "NeurIPS",
                "year": 2024,
                "abstract": "A second result.",
                "source": "semantic_scholar",
            },
        ]


def test_literature_retrieval_service_expands_queries_and_deduplicates_results() -> None:
    service = LiteratureRetrievalService(
        arxiv_client=FakeArxivClient(),
        semantic_scholar_client=FakeSemanticScholarClient(),
    )

    result = service.retrieve(
        question="What are recent retrieval-augmented generation methods?",
        time_window_years=2,
        research_domain="ai",
    )

    assert len(result.queries) >= 3
    assert len(result.candidate_papers) == 2
    assert result.candidate_papers[0]["paper_id"] == "paper-1"

