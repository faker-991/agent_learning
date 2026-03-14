from __future__ import annotations

from services.paper_analysis_service import PaperAnalysisService


class FakeLLM:
    def invoke(self, messages: list[dict[str, str]]) -> str:
        assert messages[-1]["role"] == "user"
        return "方法简述：Planner-guided retrieval over a structured memory index."


def test_paper_analysis_extracts_objective_display_fields_without_forcing_novelty_judgment() -> None:
    service = PaperAnalysisService(llm=FakeLLM())

    card = service.build_paper_card(
        workspace_id="topic-1",
        paper={
            "title": "Agentic RAG",
            "authors": ["A. Researcher"],
            "year": 2025,
            "venue": "ICLR",
            "source": "arxiv",
            "url": "https://arxiv.org/abs/1234.5678",
            "pdf_url": "https://arxiv.org/pdf/1234.5678",
            "abstract": "An agentic retrieval method.",
            "keywords": ["rag", "agent"],
            "problem": "Improve search quality with planning.",
        },
    )

    assert card.abstract == "An agentic retrieval method."
    assert card.method == "Planner-guided retrieval over a structured memory index."
    assert card.url.endswith(".pdf")
    assert card.limitations == []
