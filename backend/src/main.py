"""FastAPI entrypoint for the business research workbench."""

from __future__ import annotations

from fastapi import FastAPI

from app.dependencies import build_container
from app.routes.conclusion_cards import router as conclusion_cards_router
from app.routes.projects import router as projects_router
from app.routes.tasks import router as tasks_router
from config import Configuration


def create_app(overrides: dict[str, object] | None = None) -> FastAPI:
    config = Configuration.from_env(overrides=overrides)

    app = FastAPI(title="Business Research Workbench")
    app.state.container = build_container(config)

    @app.get("/healthz")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(projects_router)
    app.include_router(tasks_router)
    app.include_router(conclusion_cards_router)
    return app


app = create_app()
