import type { ResearchCard } from "../../entities/research-card";
import type { ResearchSession } from "../../entities/research-session";
import { apiGet, apiPost } from "../../shared/api/client";

export type SessionEvent = {
  id: string;
  task_id: string;
  type: string;
  stage: string;
  message: string;
};

export function createSession(
  topicId: string,
  payload: {
    question: string;
    intent_type: string;
    time_window_years: number;
  },
) {
  return apiPost<ResearchSession>(`/topics/${topicId}/sessions`, payload);
}

export function listTopicSessions(topicId: string) {
  return apiGet<ResearchSession[]>(`/topics/${topicId}/sessions`);
}

export function getSession(sessionId: string) {
  return apiGet<ResearchSession>(`/sessions/${sessionId}`);
}

export function generateSessionPlan(sessionId: string) {
  return apiPost<ResearchSession>(`/sessions/${sessionId}/plan`);
}

export function runSession(sessionId: string) {
  return apiPost<ResearchSession>(`/sessions/${sessionId}/run`);
}

export function getResearchCard(sessionId: string) {
  return apiGet<ResearchCard>(`/sessions/${sessionId}/research-card`);
}

export function listSessionEvents(sessionId: string) {
  return apiGet<{ events: SessionEvent[] }>(`/sessions/${sessionId}/events`);
}

