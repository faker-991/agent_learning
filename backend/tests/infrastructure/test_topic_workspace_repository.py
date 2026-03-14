from __future__ import annotations

from domain.topic_workspaces import TopicWorkspace
from infrastructure.storage.topic_workspace_repository import TopicWorkspaceRepository


def test_topic_workspace_repository_round_trips_workspace(tmp_path) -> None:
    repo = TopicWorkspaceRepository(base_dir=tmp_path)
    workspace = TopicWorkspace.create(
        title="Agent Memory",
        description="Track literature and hypotheses.",
        research_domain="ai",
    )

    repo.save(workspace)
    loaded = repo.get(workspace.id)

    assert loaded is not None
    assert loaded.id == workspace.id
    assert loaded.title == "Agent Memory"

