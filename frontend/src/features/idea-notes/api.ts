import type { IdeaNote } from "../../entities/idea-note";
import { apiGet } from "../../shared/api/client";

export function listTopicIdeas(topicId: string) {
  return apiGet<IdeaNote[]>(`/topics/${topicId}/ideas`);
}
