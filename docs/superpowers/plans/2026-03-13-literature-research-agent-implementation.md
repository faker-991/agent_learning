# Literature Research Agent Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the current business research workbench into a literature research agent for computer science and AI researchers, centered on topic workspaces, representative-paper retrieval, research guidance cards, and structured long/short-term memory.

**Architecture:** Keep the existing FastAPI plus React split, but replace the business-research domain model with a research-topic domain. Reuse the current workflow skeleton, storage adapters, and React shell where practical, while introducing topic, session, paper-card, topic-note, and idea-note boundaries with a new literature-focused orchestrator flow.

**Tech Stack:** FastAPI, Pydantic, JSON-backed repositories, React, Vite, TypeScript, Tailwind, shadcn/ui, OpenAI-compatible LLM provider, arXiv API, Semantic Scholar API.

---

## File Structure

### Backend files to create

- `backend/src/domain/topic_workspaces.py`
  Topic workspace aggregate.
- `backend/src/domain/research_sessions.py`
  Session aggregate and lifecycle.
- `backend/src/domain/paper_cards.py`
  Structured paper memory object.
- `backend/src/domain/topic_notes.py`
  Topic-level memory object.
- `backend/src/domain/idea_notes.py`
  User idea and hypothesis memory object.
- `backend/src/domain/research_cards.py`
  Research guidance card aggregate.
- `backend/src/infrastructure/storage/topic_workspace_repository.py`
  Topic workspace persistence.
- `backend/src/infrastructure/storage/research_session_repository.py`
  Session persistence.
- `backend/src/infrastructure/storage/paper_card_repository.py`
  Paper-card persistence.
- `backend/src/infrastructure/storage/topic_note_repository.py`
  Topic-note persistence.
- `backend/src/infrastructure/storage/idea_note_repository.py`
  Idea-note persistence.
- `backend/src/infrastructure/storage/research_card_repository.py`
  Guidance-card persistence.
- `backend/src/services/literature_sources/arxiv_client.py`
  arXiv retrieval adapter.
- `backend/src/services/literature_sources/semantic_scholar_client.py`
  Semantic Scholar retrieval adapter.
- `backend/src/services/literature_retrieval_service.py`
  Query expansion, dedupe, and candidate-pool building.
- `backend/src/services/paper_screening_service.py`
  Venue and metadata based ranking.
- `backend/src/services/paper_analysis_service.py`
  Objective paper-card extraction.
- `backend/src/services/memory_service.py`
  Short-term recall and long-term write-back.
- `backend/src/agents/literature_retrieval_agent.py`
- `backend/src/agents/paper_screening_agent.py`
- `backend/src/agents/paper_analysis_agent.py`
- `backend/src/agents/research_synthesis_agent.py`
- `backend/src/agents/memory_agent.py`
- `backend/tests/domain/test_topic_workspace.py`
- `backend/tests/domain/test_research_session.py`
- `backend/tests/domain/test_paper_card.py`
- `backend/tests/domain/test_topic_note.py`
- `backend/tests/domain/test_idea_note.py`
- `backend/tests/domain/test_research_card.py`
- `backend/tests/services/test_literature_retrieval_service.py`
- `backend/tests/services/test_paper_screening_service.py`
- `backend/tests/services/test_paper_analysis_service.py`
- `backend/tests/services/test_memory_service.py`
- `backend/tests/app/test_topics_api.py`
- `backend/tests/app/test_research_sessions_api.py`

### Backend files to modify

- `backend/src/domain/enums.py`
  Replace task-specific statuses with topic/session statuses or add new enums.
- `backend/src/app/schemas.py`
  Replace project/task/evidence schemas with topic/session/paper-card/note schemas.
- `backend/src/app/dependencies.py`
  Wire the new repositories and application service graph.
- `backend/src/app/routes/projects.py`
  Replace with topic routes or migrate logic in place.
- `backend/src/app/routes/tasks.py`
  Replace with session routes.
- `backend/src/app/routes/conclusion_cards.py`
  Replace with research-card routes.
- `backend/src/services/task_application_service.py`
  Convert into a literature application service or split into topic/session service.
- `backend/src/services/research_runtime.py`
  Replace business-research runtime contract with literature-focused contract.
- `backend/src/workflows/research_workflow.py`
  Replace task workflow with memory-aware literature workflow.
- `backend/src/agents/orchestrator.py`
  Re-scope orchestrator around literature retrieval, screening, analysis, synthesis, and memory.
- `backend/src/main.py`
  Register the new topic/session routes and remove obsolete ones.

### Frontend files to create

- `frontend/src/entities/topic.ts`
- `frontend/src/entities/research-session.ts`
- `frontend/src/entities/paper-card.ts`
- `frontend/src/entities/topic-note.ts`
- `frontend/src/entities/idea-note.ts`
- `frontend/src/entities/research-card.ts`
- `frontend/src/features/topics/api.ts`
- `frontend/src/features/topics/pages/topic-list-page.tsx`
- `frontend/src/features/topics/pages/topic-home-page.tsx`
- `frontend/src/features/research/api.ts`
- `frontend/src/features/research/pages/research-qa-page.tsx`
- `frontend/src/features/papers/api.ts`
- `frontend/src/features/papers/pages/paper-card-page.tsx`
- `frontend/src/features/topic-notes/api.ts`
- `frontend/src/features/topic-notes/pages/topic-notes-page.tsx`
- `frontend/src/features/idea-notes/api.ts`
- `frontend/src/features/idea-notes/pages/idea-notes-page.tsx`
- `frontend/src/features/research/components/paper-result-panel.tsx`
- `frontend/src/features/research/components/research-card-panel.tsx`
- `frontend/src/features/research/components/memory-context-panel.tsx`

### Frontend files to modify

- `frontend/src/app/router.tsx`
  Replace project/task routes with topic/research/memory routes.
- `frontend/src/shared/api/client.ts`
  Keep shared client, update endpoint types and helpers.
- `frontend/src/app/styles.css`
  Adjust layout tokens only as needed for the topic workspace.

### Docs to modify

- `README.md`
  Replace product description and local run instructions.
- `docs/superpowers/specs/2026-03-13-business-research-workbench-design.md`
  Leave intact as historical record; do not edit.

## Chunk 1: Domain And Persistence Reset

### Task 1: Add failing tests for the new topic and session aggregates

**Files:**
- Test: `backend/tests/domain/test_topic_workspace.py`
- Test: `backend/tests/domain/test_research_session.py`
- Test: `backend/tests/domain/test_paper_card.py`
- Test: `backend/tests/domain/test_topic_note.py`
- Test: `backend/tests/domain/test_idea_note.py`
- Test: `backend/tests/domain/test_research_card.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_research_session_tracks_selected_and_retrieved_papers():
    session = ResearchSession.create(
        workspace_id="topic-1",
        question="What are the strongest recent retrieval-augmented generation papers?",
        intent_type="find_representative_papers",
        time_window_years=2,
    )
    session.record_retrieved_papers(["paper-1", "paper-2"])
    session.record_selected_papers(["paper-2"])
    assert session.retrieved_paper_ids == ["paper-1", "paper-2"]
    assert session.selected_paper_ids == ["paper-2"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python3 -m pytest tests/domain/test_topic_workspace.py tests/domain/test_research_session.py tests/domain/test_paper_card.py tests/domain/test_topic_note.py tests/domain/test_idea_note.py tests/domain/test_research_card.py -q`

Expected: FAIL with missing modules or missing methods.

- [ ] **Step 3: Write minimal domain implementations**

Create the new domain modules with only the fields and methods needed by the failing tests.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python3 -m pytest tests/domain/test_topic_workspace.py tests/domain/test_research_session.py tests/domain/test_paper_card.py tests/domain/test_topic_note.py tests/domain/test_idea_note.py tests/domain/test_research_card.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/domain backend/tests/domain
git commit -m "feat: add literature research domain models"
```

### Task 2: Add failing repository tests for topic and memory persistence

**Files:**
- Create: `backend/src/infrastructure/storage/topic_workspace_repository.py`
- Create: `backend/src/infrastructure/storage/research_session_repository.py`
- Create: `backend/src/infrastructure/storage/paper_card_repository.py`
- Create: `backend/src/infrastructure/storage/topic_note_repository.py`
- Create: `backend/src/infrastructure/storage/idea_note_repository.py`
- Create: `backend/src/infrastructure/storage/research_card_repository.py`
- Test: `backend/tests/infrastructure/test_topic_workspace_repository.py`
- Test: `backend/tests/infrastructure/test_research_session_repository.py`
- Test: `backend/tests/infrastructure/test_memory_repositories.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_topic_workspace_repository_round_trips_workspace(tmp_path):
    repo = TopicWorkspaceRepository(tmp_path)
    workspace = TopicWorkspace.create(title="Agent Memory", description="notes", research_domain="ai")
    repo.save(workspace)
    loaded = repo.get(workspace.id)
    assert loaded.title == "Agent Memory"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python3 -m pytest tests/infrastructure/test_topic_workspace_repository.py tests/infrastructure/test_research_session_repository.py tests/infrastructure/test_memory_repositories.py -q`

Expected: FAIL with missing repository implementations.

- [ ] **Step 3: Implement minimal repositories using existing JSON store patterns**

Reuse the current `JsonStore` pattern rather than inventing a new persistence layer.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python3 -m pytest tests/infrastructure/test_topic_workspace_repository.py tests/infrastructure/test_research_session_repository.py tests/infrastructure/test_memory_repositories.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/infrastructure/storage backend/tests/infrastructure
git commit -m "feat: add literature workspace repositories"
```

## Chunk 2: Retrieval, Screening, And Paper Analysis

### Task 3: Add failing tests for query expansion and candidate pooling

**Files:**
- Create: `backend/src/services/literature_sources/arxiv_client.py`
- Create: `backend/src/services/literature_sources/semantic_scholar_client.py`
- Create: `backend/src/services/literature_retrieval_service.py`
- Test: `backend/tests/services/test_literature_retrieval_service.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_literature_retrieval_service_expands_queries_and_deduplicates_results():
    service = LiteratureRetrievalService(arxiv_client=FakeArxiv(), semantic_scholar_client=FakeSemanticScholar())
    result = service.retrieve(
        question="What are recent retrieval-augmented generation methods?",
        time_window_years=2,
        research_domain="ai",
    )
    assert len(result.queries) >= 3
    assert len(result.candidate_papers) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python3 -m pytest tests/services/test_literature_retrieval_service.py -q`

Expected: FAIL with missing service or client modules.

- [ ] **Step 3: Implement minimal retrieval service**

Include:
- query expansion
- source fan-out
- deduplication by canonical URL or paper id

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && python3 -m pytest tests/services/test_literature_retrieval_service.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/services/literature_sources backend/src/services/literature_retrieval_service.py backend/tests/services/test_literature_retrieval_service.py
git commit -m "feat: add literature retrieval service"
```

### Task 4: Add failing tests for screening rules based on venue and recency

**Files:**
- Create: `backend/src/services/paper_screening_service.py`
- Test: `backend/tests/services/test_paper_screening_service.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_screening_prioritizes_top_venues_before_raw_recency():
    service = PaperScreeningService()
    selected = service.select_representative_papers(
        question="How should we compare recent AI search systems?",
        candidates=[
            make_candidate(title="A", venue="Random Workshop", year=2026),
            make_candidate(title="B", venue="NeurIPS", year=2025),
        ],
        max_results=5,
    )
    assert selected[0].title == "B"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python3 -m pytest tests/services/test_paper_screening_service.py -q`

Expected: FAIL

- [ ] **Step 3: Implement minimal screening rules**

Include:
- top-tier venue mapping
- supplementary-tier mapping
- award or presentation weighting hooks
- time-window filtering
- relevance sorting hook

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && python3 -m pytest tests/services/test_paper_screening_service.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/services/paper_screening_service.py backend/tests/services/test_paper_screening_service.py
git commit -m "feat: add paper screening rules"
```

### Task 5: Add failing tests for objective paper-card extraction

**Files:**
- Create: `backend/src/services/paper_analysis_service.py`
- Test: `backend/tests/services/test_paper_analysis_service.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_paper_analysis_extracts_objective_display_fields_without_forcing_novelty_judgment():
    service = PaperAnalysisService(llm=FakeLLM())
    card = service.build_paper_card(make_selected_paper())
    assert card.abstract
    assert card.method
    assert card.url.endswith(".pdf")
    assert card.limitations == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python3 -m pytest tests/services/test_paper_analysis_service.py -q`

Expected: FAIL

- [ ] **Step 3: Implement minimal paper analysis**

The implementation should favor objective extraction:
- abstract
- method summary
- metadata
- PDF URL

Do not force speculative innovation or weakness judgments in the default card path.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && python3 -m pytest tests/services/test_paper_analysis_service.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/services/paper_analysis_service.py backend/tests/services/test_paper_analysis_service.py
git commit -m "feat: add paper analysis service"
```

## Chunk 3: Memory And Workflow Orchestration

### Task 6: Add failing tests for short-term recall and long-term write-back

**Files:**
- Create: `backend/src/services/memory_service.py`
- Test: `backend/tests/services/test_memory_service.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_memory_service_recalls_relevant_topic_state_and_writes_new_idea_note(tmp_path):
    service = MemoryService(...)
    recalled = service.recall_for_question(
        workspace_id="topic-1",
        question="Can retrieval and planning be combined?",
    )
    assert "paper_cards" in recalled
    created = service.write_back_idea(
        workspace_id="topic-1",
        title="Combine retrieval and planning",
        content="Potential hybrid direction",
        related_paper_ids=["paper-1"],
    )
    assert created.related_paper_ids == ["paper-1"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python3 -m pytest tests/services/test_memory_service.py -q`

Expected: FAIL

- [ ] **Step 3: Implement minimal memory service**

Support:
- automatic recall of paper cards, topic notes, and idea notes
- session-memory assembly
- long-term write-back helpers

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && python3 -m pytest tests/services/test_memory_service.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/services/memory_service.py backend/tests/services/test_memory_service.py
git commit -m "feat: add memory service"
```

### Task 7: Add failing workflow tests for literature orchestration

**Files:**
- Modify: `backend/src/agents/orchestrator.py`
- Modify: `backend/src/services/research_runtime.py`
- Modify: `backend/src/workflows/research_workflow.py`
- Test: `backend/tests/workflows/test_research_workflow.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_research_workflow_runs_memory_retrieval_then_screening_then_synthesis(tmp_path):
    service = TopicResearchApplicationService(base_dir=tmp_path, runtime=FakeLiteratureRuntime())
    session = service.create_session(...)
    result = service.run_session(session.id)
    assert result.research_card is not None
    assert any(event.stage == "screening" for event in result.events)
    assert any(event.stage == "memory" for event in result.events)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python3 -m pytest tests/workflows/test_research_workflow.py -q`

Expected: FAIL because the current workflow still speaks in project/task/evidence terms.

- [ ] **Step 3: Implement minimal literature runtime and orchestrator flow**

Replace the current business-research sequencing with:
- memory recall
- literature retrieval
- screening
- paper analysis
- synthesis
- memory write-back

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && python3 -m pytest tests/workflows/test_research_workflow.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/agents/orchestrator.py backend/src/services/research_runtime.py backend/src/workflows/research_workflow.py backend/tests/workflows/test_research_workflow.py
git commit -m "feat: add literature workflow orchestration"
```

## Chunk 4: API Surface Migration

### Task 8: Add failing API tests for topic and research-session routes

**Files:**
- Modify: `backend/src/app/schemas.py`
- Modify: `backend/src/app/dependencies.py`
- Modify: `backend/src/app/routes/projects.py`
- Modify: `backend/src/app/routes/tasks.py`
- Modify: `backend/src/app/routes/conclusion_cards.py`
- Modify: `backend/src/main.py`
- Test: `backend/tests/app/test_topics_api.py`
- Test: `backend/tests/app/test_research_sessions_api.py`

- [ ] **Step 1: Write the failing API tests**

```python
def test_create_topic_and_run_research_round(client):
    topic = client.post("/topics", json={"title": "Agent Search", "description": "notes", "research_domain": "ai"}).json()
    session = client.post(f"/topics/{topic['id']}/sessions", json={"question": "What are the recent representative papers for agent search?"}).json()
    planned = client.post(f"/sessions/{session['id']}/run").json()
    assert planned["status"] in {"completed", "synthesizing"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd backend && python3 -m pytest tests/app/test_topics_api.py tests/app/test_research_sessions_api.py -q`

Expected: FAIL because these endpoints do not exist yet.

- [ ] **Step 3: Implement minimal API migration**

Expose:
- `GET /topics`
- `POST /topics`
- `GET /topics/{id}`
- `POST /topics/{id}/sessions`
- `GET /topics/{id}/sessions`
- `GET /sessions/{id}`
- `POST /sessions/{id}/run`
- `GET /sessions/{id}/research-card`
- `GET /topics/{id}/papers`
- `GET /topics/{id}/notes`
- `GET /topics/{id}/ideas`

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python3 -m pytest tests/app/test_topics_api.py tests/app/test_research_sessions_api.py -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/src/app backend/src/main.py backend/tests/app
git commit -m "feat: expose literature research api"
```

## Chunk 5: React Topic Workspace

### Task 9: Add failing frontend tests or route smoke checks for the topic shell

**Files:**
- Modify: `frontend/src/app/router.tsx`
- Create: `frontend/src/entities/topic.ts`
- Create: `frontend/src/entities/research-session.ts`
- Create: `frontend/src/entities/paper-card.ts`
- Create: `frontend/src/entities/topic-note.ts`
- Create: `frontend/src/entities/idea-note.ts`
- Create: `frontend/src/entities/research-card.ts`
- Create: `frontend/src/features/topics/api.ts`
- Create: `frontend/src/features/topics/pages/topic-list-page.tsx`
- Create: `frontend/src/features/topics/pages/topic-home-page.tsx`
- Create: `frontend/src/features/research/api.ts`
- Create: `frontend/src/features/research/pages/research-qa-page.tsx`
- Create: `frontend/src/features/research/components/paper-result-panel.tsx`
- Create: `frontend/src/features/research/components/research-card-panel.tsx`
- Create: `frontend/src/features/research/components/memory-context-panel.tsx`
- Create: `frontend/src/features/papers/api.ts`
- Create: `frontend/src/features/papers/pages/paper-card-page.tsx`
- Create: `frontend/src/features/topic-notes/api.ts`
- Create: `frontend/src/features/topic-notes/pages/topic-notes-page.tsx`
- Create: `frontend/src/features/idea-notes/api.ts`
- Create: `frontend/src/features/idea-notes/pages/idea-notes-page.tsx`

- [ ] **Step 1: Add route smoke tests if the repo already has frontend tests, otherwise define manual acceptance checks in the task notes**

Use the lightest mechanism already present in the frontend. Do not introduce a new frontend test framework just for this migration.

- [ ] **Step 2: Run the relevant checks to verify the missing pages fail**

Run: `cd frontend && npm run build`

Expected: FAIL or incomplete route tree because the new topic pages are missing.

- [ ] **Step 3: Implement the topic workspace shell**

Build:
- topic list page
- topic home page
- research Q&A page
- paper result panel
- paper card detail page
- topic notes page
- idea notes page

The research page should use the three-column layout:
- left: recalled memory
- center: Q&A and guidance card
- right: representative papers

- [ ] **Step 4: Run the build to verify it passes**

Run: `cd frontend && npm run build`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src frontend/.env.local
git commit -m "feat: add literature topic workspace ui"
```

## Chunk 6: Integration, Cleanup, And Verification

### Task 10: Wire the frontend to the new API and remove stale business-research references

**Files:**
- Modify: `frontend/src/shared/api/client.ts`
- Modify: `frontend/src/app/styles.css`
- Modify: `README.md`
- Modify: any remaining business-research route, label, or schema references discovered by `rg`

- [ ] **Step 1: Add a failing integration checklist**

Manual checklist:
- topic creation works
- research session creation works
- run session returns a research card
- paper list renders title, abstract, method summary, and PDF URL
- topic notes and idea notes pages render persisted data

- [ ] **Step 2: Run the frontend build and backend tests before cleanup**

Run: `cd frontend && npm run build`

Run: `cd backend && python3 -m pytest tests/domain tests/infrastructure tests/services tests/workflows tests/app -q`

Expected: PASS or identify stale references that still fail.

- [ ] **Step 3: Remove or rename stale business-research wording**

Use targeted edits only. Do not perform unrelated refactors.

- [ ] **Step 4: Re-run verification**

Run: `cd frontend && npm run build`

Run: `cd backend && python3 -m pytest tests/domain tests/infrastructure tests/services tests/workflows tests/app -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add README.md backend frontend
git commit -m "chore: finalize literature research agent migration"
```

## Execution Notes

- Use `@superpowers/test-driven-development` for every behavior change in the implementation phase.
- Use `@superpowers/systematic-debugging` immediately if any external API or LLM failure appears during execution.
- Keep the existing business-research spec as historical documentation; do not overwrite it.
- Prefer adapting existing repository and workflow patterns over building a second parallel framework.
- Do not add heavy PDF full-text ingestion in V1.
- Do not rebuild the product as a generic chat app. The UI must keep the topic workspace and research artifact structure explicit.
- If venue mappings become large, move them into a dedicated config module rather than hardcoding them inline in the screening service.

Plan complete and saved to `docs/superpowers/plans/2026-03-13-literature-research-agent-implementation.md`. Ready to execute?
