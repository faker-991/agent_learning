import type { PaperCard } from "../../entities/paper-card";
import { apiGet } from "../../shared/api/client";

export function listTopicPapers(topicId: string) {
  return apiGet<PaperCard[]>(`/topics/${topicId}/papers`);
}

