"""Short-term recall and long-term memory write-back helpers."""

from __future__ import annotations

from dataclasses import dataclass

from domain.idea_notes import IdeaNote
from infrastructure.storage.idea_note_repository import IdeaNoteRepository
from infrastructure.storage.paper_card_repository import PaperCardRepository
from infrastructure.storage.topic_note_repository import TopicNoteRepository


@dataclass(slots=True)
class MemoryService:
    """Coordinates simple workspace memory recall and persistence."""

    paper_card_repository: PaperCardRepository
    topic_note_repository: TopicNoteRepository
    idea_note_repository: IdeaNoteRepository

    def recall_for_question(self, *, workspace_id: str, question: str) -> dict[str, list[object]]:
        return {
            "paper_cards": self.paper_card_repository.list_by_workspace_id(workspace_id),
            "topic_notes": self.topic_note_repository.list_by_workspace_id(workspace_id),
            "idea_notes": self.idea_note_repository.list_by_workspace_id(workspace_id),
        }

    def write_back_idea(
        self,
        *,
        workspace_id: str,
        title: str,
        content: str,
        related_paper_ids: list[str],
    ) -> IdeaNote:
        note = IdeaNote.create(
            workspace_id=workspace_id,
            title=title,
            idea_type="hypothesis",
            content=content,
            related_paper_ids=related_paper_ids,
        )
        self.idea_note_repository.save(note)
        return note
