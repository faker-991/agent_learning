# Literature Research Agent

An AI research workspace for computer science and AI researchers.

This repository is being rebuilt from the earlier deep-research demo into a topic-based literature agent. The product centers on:

- topic workspaces
- research sessions
- representative paper retrieval
- research guidance cards
- short-term and long-term memory

## Product shape

The main flow is:

1. Create a topic workspace.
2. Ask a research question inside that topic.
3. Retrieve recent papers from `arXiv` and `Semantic Scholar`.
4. Screen papers with a venue-first policy:
   `top venue > award/spotlight > time > relevance`
5. Show objective paper cards first:
   title, abstract, method summary, venue, year, authors, PDF URL.
6. Generate a research guidance card.
7. Write back memory as:
   paper cards, topic notes, and idea or hypothesis notes.

## Current stack

- Backend: FastAPI
- Frontend: React + Vite + TypeScript
- UI: Tailwind
- Storage: local JSON repositories

## Active domain model

- `TopicWorkspace`
- `ResearchSession`
- `PaperCard`
- `TopicNote`
- `IdeaNote`
- `ResearchCard`

## Active routes

- `POST /topics`
- `GET /topics`
- `GET /topics/{topic_id}`
- `GET /topics/{topic_id}/papers`
- `GET /topics/{topic_id}/notes`
- `GET /topics/{topic_id}/ideas`
- `POST /topics/{topic_id}/sessions`
- `GET /topics/{topic_id}/sessions`
- `GET /sessions/{session_id}`
- `POST /sessions/{session_id}/plan`
- `POST /sessions/{session_id}/run`
- `GET /sessions/{session_id}/events`
- `GET /sessions/{session_id}/research-card`

## Frontend routes

- `/topics`
- `/topics/:topicId`
- `/sessions/:sessionId`
- `/papers/:paperId`
- `/topics/:topicId/notes`
- `/topics/:topicId/ideas`

## Local development

Backend:

```bash
cd backend
PYTHONPATH=src python3 -m uvicorn main:app --host 127.0.0.1 --port 8002 --app-dir src
```

Frontend:

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5175
```

## Verification

Backend focused suite:

```bash
cd backend
python3 -m pytest tests/domain tests/infrastructure tests/services tests/workflows tests/app -q
```

Frontend build:

```bash
cd frontend
npm run build
```

## Design docs

- [Spec](./docs/superpowers/specs/2026-03-13-literature-research-agent-design.md)
- [Implementation plan](./docs/superpowers/plans/2026-03-13-literature-research-agent-implementation.md)
