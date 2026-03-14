"""FastAPI entrypoint for the literature research agent."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import build_container
from app.routes.research_sessions import router as research_sessions_router
from app.routes.topics import router as topics_router
from config import Configuration


def create_app(overrides: dict[str, object] | None = None) -> FastAPI:
    config = Configuration.from_env(overrides=overrides)

    app = FastAPI(title="Literature Research Agent")
    app.state.container = build_container(config)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(topics_router)
    app.include_router(research_sessions_router)
    return app


app = create_app()
