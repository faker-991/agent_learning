"""Semantic Scholar retrieval adapter."""

from __future__ import annotations

from dataclasses import dataclass, field

import httpx


@dataclass(slots=True)
class SemanticScholarClient:
    """Minimal adapter interface for Semantic Scholar search."""

    http_client: object = field(default_factory=httpx.Client)

    def search(self, query: str, years: int) -> list[dict[str, object]]:
        try:
            response = self.http_client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": query,
                    "limit": 10,
                    "fields": "paperId,title,abstract,year,venue,authors,url,openAccessPdf",
                },
                headers={"Accept": "application/json"},
                timeout=20.0,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception:
            return []
        current_year =  datetime_now_year()
        minimum_year = current_year - max(years - 1, 0)
        results: list[dict[str, object]] = []
        for item in payload.get("data", []):
            year = int(item.get("year") or current_year)
            if year < minimum_year:
                continue
            results.append(
                {
                    "paper_id": item.get("paperId") or item.get("url"),
                    "title": item.get("title") or "",
                    "abstract": item.get("abstract") or "",
                    "year": year,
                    "venue": item.get("venue") or "",
                    "authors": [author.get("name") or "" for author in item.get("authors", [])],
                    "url": item.get("url") or "",
                    "pdf_url": (item.get("openAccessPdf") or {}).get("url") or "",
                    "source": "semantic_scholar",
                }
            )
        return results


def datetime_now_year() -> int:
    import datetime

    return datetime.datetime.now(datetime.UTC).year
