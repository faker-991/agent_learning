"""arXiv retrieval adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import xml.etree.ElementTree as ET

import httpx


@dataclass(slots=True)
class ArxivClient:
    """Minimal adapter interface for arXiv search."""

    http_client: object = field(default_factory=httpx.Client)

    def search(self, query: str, years: int) -> list[dict[str, object]]:
        try:
            response = self.http_client.get(
                "https://export.arxiv.org/api/query",
                params={
                    "search_query": f"all:{query}",
                    "start": 0,
                    "max_results": 10,
                    "sortBy": "submittedDate",
                    "sortOrder": "descending",
                },
                timeout=20.0,
            )
            response.raise_for_status()
            root = ET.fromstring(response.text)
        except Exception:
            return []

        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        current_year = datetime.now(UTC).year
        minimum_year = current_year - max(years - 1, 0)
        papers: list[dict[str, object]] = []
        for entry in root.findall("atom:entry", namespace):
            published = entry.findtext("atom:published", default="", namespaces=namespace)
            year = int(published[:4]) if published[:4].isdigit() else current_year
            if year < minimum_year:
                continue
            entry_id = entry.findtext("atom:id", default="", namespaces=namespace)
            pdf_url = ""
            for link in entry.findall("atom:link", namespace):
                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib.get("href", "")
                    break
            papers.append(
                {
                    "paper_id": entry_id or pdf_url,
                    "title": entry.findtext("atom:title", default="", namespaces=namespace).strip(),
                    "abstract": entry.findtext("atom:summary", default="", namespaces=namespace).strip(),
                    "year": year,
                    "venue": "arXiv",
                    "authors": [
                        author.findtext("atom:name", default="", namespaces=namespace).strip()
                        for author in entry.findall("atom:author", namespace)
                    ],
                    "url": entry_id,
                    "pdf_url": pdf_url,
                    "source": "arxiv",
                }
            )
        return papers
