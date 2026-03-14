import type { TopicNote } from "../../entities/topic-note";
import { apiGet } from "../../shared/api/client";

export function listTopicNotes(topicId: string) {
  return apiGet<TopicNote[]>(`/topics/${topicId}/notes`);
}

