"""Storage adapters for local persistence."""

from infrastructure.storage.event_repository import EventRepository
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.research_card_repository import ResearchCardRepository
from infrastructure.storage.research_session_repository import ResearchSessionRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository
from infrastructure.storage.topic_workspace_repository import TopicWorkspaceRepository

__all__ = [
    "EventRepository",
    "IdeaNoteRepository",
    "PaperCardRepository",
    "ResearchCardRepository",
    "ResearchSessionRepository",
    "TopicNoteRepository",
    "TopicWorkspaceRepository",
]
