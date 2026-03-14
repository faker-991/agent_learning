import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { IdeaNotesPage } from "../features/idea-notes/pages/idea-notes-page";
import { PaperCardPage } from "../features/papers/pages/paper-card-page";
import { ResearchQaPage } from "../features/research/pages/research-qa-page";
import { TopicNotesPage } from "../features/topic-notes/pages/topic-notes-page";
import { TopicHomePage } from "../features/topics/pages/topic-home-page";
import { TopicListPage } from "../features/topics/pages/topic-list-page";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/topics" replace />} />
        <Route path="/topics" element={<TopicListPage />} />
        <Route path="/topics/:topicId" element={<TopicHomePage />} />
        <Route path="/sessions/:sessionId" element={<ResearchQaPage />} />
        <Route path="/papers/:paperId" element={<PaperCardPage />} />
        <Route path="/topics/:topicId/notes" element={<TopicNotesPage />} />
        <Route path="/topics/:topicId/ideas" element={<IdeaNotesPage />} />
      </Routes>
    </BrowserRouter>
  );
}
