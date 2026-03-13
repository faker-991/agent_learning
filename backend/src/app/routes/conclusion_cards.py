"""Conclusion card routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.schemas import ConclusionCardResponse


router = APIRouter(tags=["conclusion-cards"])


@router.get("/tasks/{task_id}/conclusion-card", response_model=ConclusionCardResponse)
async def get_conclusion_card(task_id: str, request: Request) -> ConclusionCardResponse:
    container = request.app.state.container
    card = container.task_service.conclusion_repository.find_by_task_id(task_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Conclusion card not found")
    return ConclusionCardResponse(
        id=card.id,
        task_id=card.task_id,
        project_id=card.project_id,
        problem_definition=card.problem_definition,
        core_conclusion=card.core_conclusion,
        key_evidence=card.key_evidence,
        alternative_views=card.alternative_views,
        recommended_actions=card.recommended_actions,
        risks_and_uncertainties=card.risks_and_uncertainties,
        citations=card.citations,
    )
