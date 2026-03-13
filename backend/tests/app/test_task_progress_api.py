from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.mark.anyio
async def test_task_progress_returns_event_timeline(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        project = (await client.post("/projects", json={"name": "AI Search"})).json()
        task = (
            await client.post(
                f"/projects/{project['id']}/tasks",
                json={
                    "title": "Track AI search",
                    "question": "How should we respond to AI search competitors?",
                    "template_type": "competitor_research",
                },
            )
        ).json()

        await client.post(f"/tasks/{task['id']}/plan")
        await client.post(f"/tasks/{task['id']}/approve")
        await client.post(f"/tasks/{task['id']}/run")
        response = await client.get(f"/tasks/{task['id']}/events")

    assert response.status_code == 200
    payload = response.json()
    assert "events" in payload
    assert payload["events"]
    assert any(event["stage"] == "synthesizing" for event in payload["events"])
