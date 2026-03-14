from __future__ import annotations

from domain.topic_workspaces import TopicWorkspace


def test_topic_workspace_create_sets_defaults() -> None:
    workspace = TopicWorkspace.create(
        title="Retrieval-Augmented Generation",
        description="Recent representative papers and open questions.",
        research_domain="ai",
    )

    assert workspace.id.startswith("topic-")
    assert workspace.title == "Retrieval-Augmented Generation"
    assert workspace.research_domain == "ai"
    assert workspace.default_time_window == 2

