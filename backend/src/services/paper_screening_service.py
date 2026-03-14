"""Representative paper screening logic."""

from __future__ import annotations


class PaperScreeningService:
    """Selects representative papers using venue-first ranking."""

    _TOP_TIER_VENUES = {
        "AAAI",
        "ACL",
        "CVPR",
        "EMNLP",
        "ICCV",
        "ICLR",
        "ICML",
        "IJCAI",
        "NeurIPS",
        "TPAMI",
    }
    _SECOND_TIER_VENUES = {
        "COLING",
        "ECCV",
        "ECAI",
        "ICRA",
        "NAACL",
    }
    _AWARD_WEIGHTS = {
        "best paper": 30,
        "outstanding paper": 25,
        "spotlight": 20,
        "oral": 18,
    }

    def select_representative_papers(
        self,
        *,
        question: str,
        candidates: list[dict[str, object]],
        max_results: int,
    ) -> list[dict[str, object]]:
        return sorted(candidates, key=self._sort_key, reverse=True)[:max_results]

    def _sort_key(self, paper: dict[str, object]) -> tuple[int, int, int, float]:
        venue_score = self._venue_score(str(paper.get("venue", "")))
        award_score = self._award_score(paper.get("award"))
        year_score = int(paper.get("year", 0))
        relevance = float(paper.get("relevance_score", 0.0))
        return (venue_score, award_score, year_score, relevance)

    def _venue_score(self, venue: str) -> int:
        if venue in self._TOP_TIER_VENUES:
            return 3
        if venue in self._SECOND_TIER_VENUES:
            return 2
        return 1

    def _award_score(self, award: object) -> int:
        if not award:
            return 0
        return self._AWARD_WEIGHTS.get(str(award).lower(), 0)

