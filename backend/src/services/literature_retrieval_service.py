"""Literature retrieval, query expansion, and candidate pooling."""

from __future__ import annotations

from dataclasses import dataclass

from services.literature_sources.arxiv_client import ArxivClient
from services.literature_sources.semantic_scholar_client import SemanticScholarClient


@dataclass(slots=True)
class RetrievalResult:
    """Expanded queries plus deduplicated candidate papers."""

    queries: list[str]
    candidate_papers: list[dict[str, object]]


class LiteratureRetrievalService:
    """Expands a question and retrieves a deduplicated candidate pool."""

    def __init__(
        self,
        *,
        arxiv_client: ArxivClient,
        semantic_scholar_client: SemanticScholarClient,
    ) -> None:
        self._arxiv_client = arxiv_client
        self._semantic_scholar_client = semantic_scholar_client

    def retrieve(
        self,
        *,
        question: str,
        time_window_years: int,
        research_domain: str,
    ) -> RetrievalResult:
        queries = self._expand_queries(question, research_domain)
        candidates: dict[str, dict[str, object]] = {}

        for query in queries:
            for paper in self._arxiv_client.search(query, time_window_years):
                key = str(paper.get("paper_id") or paper.get("url"))
                candidates.setdefault(key, dict(paper))
            for paper in self._semantic_scholar_client.search(query, time_window_years):
                key = str(paper.get("paper_id") or paper.get("url"))
                merged = candidates.setdefault(key, {})
                merged.update({k: v for k, v in dict(paper).items() if v not in (None, "", [])})

        return RetrievalResult(
            queries=queries,
            candidate_papers=list(candidates.values()),
        )

    @staticmethod
    def _expand_queries(question: str, research_domain: str) -> list[str]:
        return [
            question,
            f"{question} survey",
            f"{question} recent advances {research_domain}",
        ]

