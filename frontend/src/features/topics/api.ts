import type { Topic } from "../../entities/topic";
import { apiGet, apiPost } from "../../shared/api/client";

export function listTopics() {
  return apiGet<Topic[]>("/topics");
}

export function getTopic(topicId: string) {
  return apiGet<Topic>(`/topics/${topicId}`);
}

export function createTopic(payload: {
  title: string;
  description?: string;
  research_domain: string;
}) {
  return apiPost<Topic>("/topics", payload);
}

