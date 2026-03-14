"""Objective paper-card extraction helpers."""

from __future__ import annotations

from domain.paper_cards import PaperCard
from services.text_processing import strip_tool_calls
from utils import strip_thinking_tokens


class PaperAnalysisService:
    """Creates objective paper cards without over-claiming novelty judgments."""

    def __init__(self, *, llm: object) -> None:
        self._llm = llm

    def build_paper_card(self, *, workspace_id: str, paper: dict[str, object]) -> PaperCard:
        method_summary = self._extract_method_summary(paper)
        paper_url = self._normalize_pdf_url(str(paper.get("pdf_url") or paper.get("url") or ""))
        return PaperCard.create(
            workspace_id=workspace_id,
            title=str(paper["title"]),
            authors=list(paper.get("authors", [])),
            year=int(paper["year"]),
            venue=str(paper.get("venue", "")),
            source=str(paper.get("source", "")),
            url=paper_url,
            abstract=str(paper.get("abstract", "")),
            keywords=list(paper.get("keywords", [])),
            problem=str(paper.get("problem", "")),
            method=method_summary,
        )

    def _extract_method_summary(self, paper: dict[str, object]) -> str:
        prompt = (
            "请基于以下论文信息，只输出一行客观的“方法简述”，不要评价创新性。\n"
            f"标题：{paper.get('title', '')}\n"
            f"摘要：{paper.get('abstract', '')}\n"
            f"问题：{paper.get('problem', '')}\n"
        )
        response = self._llm.invoke([{"role": "user", "content": prompt}])
        text = response if isinstance(response, str) else str(response)
        text = strip_tool_calls(strip_thinking_tokens(text)).strip()
        if "：" in text:
            _, text = text.split("：", 1)
        return text.strip()

    @staticmethod
    def _normalize_pdf_url(url: str) -> str:
        if "arxiv.org/pdf/" in url and not url.endswith(".pdf"):
            return f"{url}.pdf"
        return url
