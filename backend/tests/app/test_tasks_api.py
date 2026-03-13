from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.mark.anyio
async def test_approve_plan_advances_task(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        project = (await client.post("/projects", json={"name": "Strategy"})).json()
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

        plan_response = await client.post(f"/tasks/{task['id']}/plan")
        approve_response = await client.post(f"/tasks/{task['id']}/approve")

    assert plan_response.status_code == 200
    assert approve_response.status_code == 200
    assert approve_response.json()["status"] == "researching"
