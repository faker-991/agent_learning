from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.mark.anyio
async def test_create_topic_returns_topic_payload(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/topics",
            json={
                "title": "Agent Search",
                "description": "Track representative literature.",
                "research_domain": "ai",
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Agent Search"
    assert payload["id"]


@pytest.mark.anyio
async def test_get_topic_detail_returns_topic_payload(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        created = (
            await client.post(
                "/topics",
                json={
                    "title": "Agent Search",
                    "description": "Track representative literature.",
                    "research_domain": "ai",
                },
            )
        ).json()
        response = await client.get(f"/topics/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

