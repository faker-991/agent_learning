from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.mark.anyio
async def test_create_session_and_run_research_round(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        topic = (
            await client.post(
                "/topics",
                json={
                    "title": "Agent Search",
                    "description": "Track representative literature.",
                    "research_domain": "ai",
                },
            )
        ).json()
        session = (
            await client.post(
                f"/topics/{topic['id']}/sessions",
                json={
                    "question": "What are the recent representative papers for agent search?",
                    "intent_type": "find_representative_papers",
                    "time_window_years": 2,
                },
            )
        ).json()
        plan = await client.post(f"/sessions/{session['id']}/plan")
        run = await client.post(f"/sessions/{session['id']}/run")
        card = await client.get(f"/sessions/{session['id']}/research-card")

    assert plan.status_code == 200
    assert run.status_code == 200
    assert run.json()["status"] == "completed"
    assert card.status_code == 200
    assert card.json()["problem_definition"] == "What are the recent representative papers for agent search?"


@pytest.mark.anyio
async def test_list_topic_sessions_returns_created_session(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        topic = (
            await client.post(
                "/topics",
                json={
                    "title": "Agent Search",
                    "description": "Track representative literature.",
                    "research_domain": "ai",
                },
            )
        ).json()
        created = (
            await client.post(
                f"/topics/{topic['id']}/sessions",
                json={
                    "question": "What are the recent representative papers for agent search?",
                    "intent_type": "find_representative_papers",
                    "time_window_years": 2,
                },
            )
        ).json()
        response = await client.get(f"/topics/{topic['id']}/sessions")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == created["id"]


@pytest.mark.anyio
async def test_topic_memory_endpoints_return_lists(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        topic = (
            await client.post(
                "/topics",
                json={
                    "title": "Agent Search",
                    "description": "Track representative literature.",
                    "research_domain": "ai",
                },
            )
        ).json()
        session = (
            await client.post(
                f"/topics/{topic['id']}/sessions",
                json={
                    "question": "What are the recent representative papers for agent search?",
                    "intent_type": "find_representative_papers",
                    "time_window_years": 2,
                },
            )
        ).json()
        await client.post(f"/sessions/{session['id']}/run")

        papers = await client.get(f"/topics/{topic['id']}/papers")
        notes = await client.get(f"/topics/{topic['id']}/notes")
        ideas = await client.get(f"/topics/{topic['id']}/ideas")

    assert papers.status_code == 200
    assert isinstance(papers.json(), list)
    assert notes.status_code == 200
    assert isinstance(notes.json(), list)
    assert ideas.status_code == 200
    assert isinstance(ideas.json(), list)
