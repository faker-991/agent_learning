from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.mark.anyio
async def test_create_project_returns_project_payload(tmp_path) -> None:
    transport = ASGITransport(app=create_app({"storage_workspace": str(tmp_path)}))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/projects", json={"name": "AI Search"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "AI Search"
    assert payload["id"]
