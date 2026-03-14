from __future__ import annotations

from services.literature_sources.arxiv_client import ArxivClient
from services.literature_sources.semantic_scholar_client import SemanticScholarClient


class FakeHttpClient:
    def __init__(self, payload: dict[str, object], *, text: str = "") -> None:
        self._payload = payload
        self._text = text

    def get(self, url: str, *, params: dict[str, object] | None = None, headers: dict[str, str] | None = None, timeout: float | None = None):
        return FakeResponse(self._payload, self._text)


class FakeResponse:
    def __init__(self, payload: dict[str, object], text: str) -> None:
        self._payload = payload
        self.text = text

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


def test_semantic_scholar_client_normalizes_paper_payload() -> None:
    client = SemanticScholarClient(
        http_client=FakeHttpClient(
            {
                "data": [
                    {
                        "paperId": "paper-1",
                        "title": "Agentic RAG",
                        "abstract": "Agentic retrieval paper.",
                        "year": 2025,
                        "venue": "ICLR",
                        "authors": [{"name": "A. Researcher"}],
                        "openAccessPdf": {"url": "https://example.org/paper.pdf"},
                        "url": "https://example.org/paper",
                    }
                ]
            }
        )
    )

    results = client.search("agentic rag", years=2)

    assert results[0]["paper_id"] == "paper-1"
    assert results[0]["pdf_url"] == "https://example.org/paper.pdf"
    assert results[0]["source"] == "semantic_scholar"


def test_arxiv_client_returns_empty_when_feed_parse_fails() -> None:
    client = ArxivClient(http_client=FakeHttpClient({}, text="not xml"))

    results = client.search("agent search", years=2)

    assert results == []
