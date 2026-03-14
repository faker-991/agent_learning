# Business Research Workbench Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild this folder from the current deep research demo into a project-based business research workbench with React frontend, structured domain model, controlled multi-agent orchestration, and conclusion-card outputs.

**Architecture:** The backend will be restructured around domain entities, workflow orchestration, and bounded sub-agents. The frontend will be rebuilt as a React workspace app with project pages, task execution flows, evidence panels, and conclusion-card views. Existing one-shot research logic will be incrementally replaced behind explicit task lifecycle APIs.

**Tech Stack:** FastAPI, Python, React, Vite, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Zustand

---

## Chunk 1: Repository Baseline and Frontend Stack Reset

### Task 1: Clean repository inputs that should not stay tracked

**Files:**
- Modify: `.gitignore`
- Modify: `frontend/.gitignore`
- Delete: `backend/.bin/uv`
- Delete: `backend/.bin/uvx`
- Delete: `frontend/package-lock.json` if package manager changes

- [ ] **Step 1: Write the failing check**

Run:
```bash
git ls-files backend/.bin frontend/node_modules frontend/dist
```
Expected: tracked binary/build artifacts are still present.

- [ ] **Step 2: Remove tracked binary/build artifacts and harden ignore rules**

Update ignore rules so local binaries, runtime notes, build outputs, and generated folders are excluded from future commits.

- [ ] **Step 3: Run the check again**

Run:
```bash
git ls-files backend/.bin frontend/node_modules frontend/dist
```
Expected: no tracked files remain in these paths.

- [ ] **Step 4: Commit**

```bash
git add .gitignore frontend/.gitignore
git rm -r --cached backend/.bin frontend/node_modules frontend/dist
git commit -m "chore: remove tracked local artifacts"
```

### Task 2: Replace Vue frontend scaffold with React workspace scaffold

**Files:**
- Delete: `frontend/src/App.vue`
- Delete: `frontend/src/main.ts`
- Delete: `frontend/src/env.d.ts`
- Delete: `frontend/src/services/api.ts`
- Delete: `frontend/src/style.css`
- Modify: `frontend/package.json`
- Modify: `frontend/tsconfig.json`
- Modify: `frontend/vite.config.ts`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/app/router.tsx`
- Create: `frontend/src/app/providers.tsx`
- Create: `frontend/src/app/styles.css`
- Create: `frontend/src/vite-env.d.ts`

- [ ] **Step 1: Write the failing build check**

Run:
```bash
cd frontend && npm run build
```
Expected: current Vue-based build passes before replacement; after removing Vue entry, build should fail until React files exist.

- [ ] **Step 2: Replace the app entry with React + Vite + TypeScript**

Update package scripts and dependencies for React, React DOM, React Router, Tailwind, shadcn/ui prerequisites, TanStack Query, Zustand, and class utility packages.

- [ ] **Step 3: Create the minimal React app shell**

Implement `main.tsx`, app providers, router, and a placeholder route tree that compiles.

- [ ] **Step 4: Run the build**

Run:
```bash
cd frontend && npm install && npm run build
```
Expected: build passes with the new React scaffold.

- [ ] **Step 5: Commit**

```bash
git add frontend
git commit -m "feat: replace vue frontend with react scaffold"
```

## Chunk 2: Backend Domain Model and Task Lifecycle

### Task 3: Introduce domain entities and task state machine

**Files:**
- Create: `backend/src/domain/__init__.py`
- Create: `backend/src/domain/projects.py`
- Create: `backend/src/domain/tasks.py`
- Create: `backend/src/domain/evidence.py`
- Create: `backend/src/domain/conclusion_cards.py`
- Create: `backend/src/domain/events.py`
- Create: `backend/src/domain/enums.py`
- Test: `backend/tests/domain/test_task_lifecycle.py`
- Test: `backend/tests/domain/test_conclusion_card_schema.py`

- [ ] **Step 1: Write failing lifecycle tests**

```python
from domain.enums import TaskStatus
from domain.tasks import ResearchTask

def test_task_transitions_follow_v1_lifecycle() -> None:
    task = ResearchTask.create(...)
    task.start_planning()
    task.mark_pending_approval()
    task.approve_plan()
    task.start_research()
    task.start_review()
    task.start_synthesis()
    task.complete()
    assert task.status is TaskStatus.COMPLETED
```

- [ ] **Step 2: Run the tests to verify failure**

Run:
```bash
cd backend && pytest backend/tests/domain/test_task_lifecycle.py -v
```
Expected: FAIL because domain modules do not exist yet.

- [ ] **Step 3: Implement domain entities and lifecycle guards**

Create typed models for `Project`, `ResearchTask`, `Evidence`, `ConclusionCard`, and `TaskEvent`. Encode the V1 lifecycle and invalid transition protections.

- [ ] **Step 4: Run the tests**

Run:
```bash
cd backend && pytest backend/tests/domain/test_task_lifecycle.py backend/tests/domain/test_conclusion_card_schema.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/domain backend/tests/domain
git commit -m "feat: add business research domain models"
```

### Task 4: Add persistence layer for projects, tasks, evidence, cards, and events

**Files:**
- Create: `backend/src/infrastructure/__init__.py`
- Create: `backend/src/infrastructure/storage/__init__.py`
- Create: `backend/src/infrastructure/storage/json_store.py`
- Create: `backend/src/infrastructure/storage/project_repository.py`
- Create: `backend/src/infrastructure/storage/task_repository.py`
- Create: `backend/src/infrastructure/storage/evidence_repository.py`
- Create: `backend/src/infrastructure/storage/conclusion_repository.py`
- Create: `backend/src/infrastructure/storage/event_repository.py`
- Modify: `backend/src/config.py`
- Test: `backend/tests/infrastructure/test_json_store.py`

- [ ] **Step 1: Write the failing repository test**

```python
def test_task_repository_round_trips_task(tmp_path) -> None:
    repo = TaskRepository(base_dir=tmp_path)
    task = repo.create(...)
    loaded = repo.get(task.id)
    assert loaded.id == task.id
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd backend && pytest backend/tests/infrastructure/test_json_store.py -v
```
Expected: FAIL because repositories do not exist.

- [ ] **Step 3: Implement file-backed repositories**

Use simple JSON persistence first. Keep interfaces clean so SQLite/Postgres can replace them later.

- [ ] **Step 4: Run the test**

Run:
```bash
cd backend && pytest backend/tests/infrastructure/test_json_store.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/infrastructure backend/src/config.py backend/tests/infrastructure
git commit -m "feat: add file-backed repositories"
```

## Chunk 3: Backend Workflow and Agent Refactor

### Task 5: Split current monolithic agent into orchestrator and bounded sub-agents

**Files:**
- Create: `backend/src/agents/__init__.py`
- Create: `backend/src/agents/orchestrator.py`
- Create: `backend/src/agents/task_planning_agent.py`
- Create: `backend/src/agents/evidence_research_agent.py`
- Create: `backend/src/agents/evidence_review_agent.py`
- Create: `backend/src/agents/conclusion_synthesis_agent.py`
- Create: `backend/src/agents/decision_advisory_agent.py`
- Modify: `backend/src/prompts.py`
- Modify: `backend/src/agent.py`
- Test: `backend/tests/agents/test_orchestrator_routing.py`

- [ ] **Step 1: Write the failing orchestrator test**

```python
def test_orchestrator_routes_task_by_status() -> None:
    workflow = ResearchWorkflow(...)
    task = make_task(status=TaskStatus.PLANNING)
    result = workflow.advance(task.id)
    assert result.current_stage == "pending_approval"
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd backend && pytest backend/tests/agents/test_orchestrator_routing.py -v
```
Expected: FAIL because the orchestrator modules do not exist.

- [ ] **Step 3: Implement the orchestrator and sub-agent boundaries**

Move stage-specific behavior out of the current `agent.py`. Keep `agent.py` as a compatibility shim or remove it once API wiring is updated.

- [ ] **Step 4: Run the test**

Run:
```bash
cd backend && pytest backend/tests/agents/test_orchestrator_routing.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/agents backend/src/prompts.py backend/src/agent.py backend/tests/agents
git commit -m "feat: add orchestrated research agents"
```

### Task 6: Add explicit workflow service for V1 lifecycle execution

**Files:**
- Create: `backend/src/workflows/__init__.py`
- Create: `backend/src/workflows/research_workflow.py`
- Create: `backend/src/services/task_application_service.py`
- Modify: `backend/src/services/planner.py`
- Modify: `backend/src/services/reporter.py`
- Modify: `backend/src/services/search.py`
- Modify: `backend/src/services/summarizer.py`
- Test: `backend/tests/workflows/test_research_workflow.py`

- [ ] **Step 1: Write the failing workflow integration test**

```python
def test_approved_task_generates_card_and_events(tmp_path) -> None:
    app = build_test_application(tmp_path)
    task = app.tasks.create(...)
    app.tasks.generate_plan(task.id)
    app.tasks.approve_plan(task.id)
    result = app.tasks.run(task.id)
    assert result.conclusion_card is not None
    assert any(event.stage == "synthesizing" for event in result.events)
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd backend && pytest backend/tests/workflows/test_research_workflow.py -v
```
Expected: FAIL until workflow orchestration is implemented.

- [ ] **Step 3: Implement the workflow service**

Create application service methods for:
- create project
- create task
- generate plan
- approve plan
- execute task
- list evidence
- fetch conclusion card

- [ ] **Step 4: Run the test**

Run:
```bash
cd backend && pytest backend/tests/workflows/test_research_workflow.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/workflows backend/src/services backend/tests/workflows
git commit -m "feat: add research workflow service"
```

## Chunk 4: Backend API Redesign

### Task 7: Replace one-shot research endpoints with project/task APIs

**Files:**
- Modify: `backend/src/main.py`
- Create: `backend/src/app/__init__.py`
- Create: `backend/src/app/dependencies.py`
- Create: `backend/src/app/schemas.py`
- Create: `backend/src/app/routes/__init__.py`
- Create: `backend/src/app/routes/projects.py`
- Create: `backend/src/app/routes/tasks.py`
- Create: `backend/src/app/routes/conclusion_cards.py`
- Test: `backend/tests/app/test_projects_api.py`
- Test: `backend/tests/app/test_tasks_api.py`

- [ ] **Step 1: Write failing API tests**

```python
def test_create_project_returns_project_payload(client) -> None:
    response = client.post("/projects", json={"name": "AI Search"})
    assert response.status_code == 201
```

```python
def test_approve_plan_advances_task(client) -> None:
    response = client.post(f"/tasks/{task_id}/approve")
    assert response.status_code == 200
```

- [ ] **Step 2: Run the tests**

Run:
```bash
cd backend && pytest backend/tests/app/test_projects_api.py backend/tests/app/test_tasks_api.py -v
```
Expected: FAIL because routes do not exist.

- [ ] **Step 3: Implement the API**

Expose V1 endpoints for:
- `POST /projects`
- `GET /projects`
- `GET /projects/{id}`
- `POST /projects/{id}/tasks`
- `GET /tasks/{id}`
- `POST /tasks/{id}/plan`
- `POST /tasks/{id}/approve`
- `POST /tasks/{id}/run`
- `GET /tasks/{id}/events`
- `GET /tasks/{id}/evidence`
- `GET /tasks/{id}/conclusion-card`

- [ ] **Step 4: Run the tests**

Run:
```bash
cd backend && pytest backend/tests/app/test_projects_api.py backend/tests/app/test_tasks_api.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/app backend/src/main.py backend/tests/app
git commit -m "feat: add project and task api"
```

### Task 8: Add streaming or polling-safe task progress endpoint

**Files:**
- Modify: `backend/src/app/routes/tasks.py`
- Modify: `backend/src/app/schemas.py`
- Modify: `backend/src/workflows/research_workflow.py`
- Test: `backend/tests/app/test_task_progress_api.py`

- [ ] **Step 1: Write the failing progress API test**

```python
def test_task_progress_returns_event_timeline(client) -> None:
    response = client.get(f"/tasks/{task_id}/events")
    assert response.status_code == 200
    assert "events" in response.json()
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd backend && pytest backend/tests/app/test_task_progress_api.py -v
```
Expected: FAIL or remain incomplete.

- [ ] **Step 3: Implement timeline-friendly progress payloads**

Ensure responses expose stage, message, created timestamp, and optional payload details for the React execution page.

- [ ] **Step 4: Run the test**

Run:
```bash
cd backend && pytest backend/tests/app/test_task_progress_api.py -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/src/app/routes/tasks.py backend/src/app/schemas.py backend/src/workflows/research_workflow.py backend/tests/app/test_task_progress_api.py
git commit -m "feat: expose task progress timeline"
```

## Chunk 5: React Workspace UI

### Task 9: Build app shell, routing, and shared providers

**Files:**
- Create: `frontend/src/app/layout/app-shell.tsx`
- Create: `frontend/src/app/router.tsx`
- Create: `frontend/src/app/providers/query-provider.tsx`
- Create: `frontend/src/app/providers/theme-provider.tsx`
- Create: `frontend/src/shared/api/client.ts`
- Create: `frontend/src/shared/lib/utils.ts`
- Create: `frontend/src/shared/ui/sidebar.tsx`
- Create: `frontend/src/shared/ui/header.tsx`
- Create: `frontend/src/shared/ui/empty-state.tsx`
- Test: `frontend/src/app/router.test.tsx`

- [ ] **Step 1: Write the failing route smoke test**

Create a simple test that renders the router and asserts the project list route mounts.

- [ ] **Step 2: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/app/router.test.tsx
```
Expected: FAIL until the test runner and route structure exist.

- [ ] **Step 3: Implement the shared shell**

Set up providers, base layout, navigation, query client, and route objects for projects, tasks, and conclusion cards.

- [ ] **Step 4: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/app/router.test.tsx
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src frontend/package.json frontend/vite.config.ts frontend/tsconfig.json
git commit -m "feat: add react app shell and routing"
```

### Task 10: Implement project list and project detail features

**Files:**
- Create: `frontend/src/features/projects/api.ts`
- Create: `frontend/src/features/projects/hooks.ts`
- Create: `frontend/src/features/projects/components/project-card.tsx`
- Create: `frontend/src/features/projects/components/create-project-dialog.tsx`
- Create: `frontend/src/features/projects/pages/project-list-page.tsx`
- Create: `frontend/src/features/projects/pages/project-detail-page.tsx`
- Create: `frontend/src/entities/project.ts`
- Test: `frontend/src/features/projects/project-list-page.test.tsx`

- [ ] **Step 1: Write the failing project page test**

Assert that the page renders empty state, existing projects, and create-project action.

- [ ] **Step 2: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/projects/project-list-page.test.tsx
```
Expected: FAIL until feature modules exist.

- [ ] **Step 3: Implement project pages**

Render project cards, project metadata, recent tasks, and recent conclusion cards. Keep project detail focused on work entry, not dashboard noise.

- [ ] **Step 4: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/projects/project-list-page.test.tsx
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/projects frontend/src/entities/project.ts
git commit -m "feat: add project workspace pages"
```

### Task 11: Implement task creation and execution pages

**Files:**
- Create: `frontend/src/features/tasks/api.ts`
- Create: `frontend/src/features/tasks/hooks.ts`
- Create: `frontend/src/features/tasks/store.ts`
- Create: `frontend/src/features/tasks/components/create-task-form.tsx`
- Create: `frontend/src/features/tasks/components/task-context-panel.tsx`
- Create: `frontend/src/features/tasks/components/task-timeline.tsx`
- Create: `frontend/src/features/tasks/components/task-plan-card.tsx`
- Create: `frontend/src/features/tasks/pages/task-execution-page.tsx`
- Create: `frontend/src/entities/task.ts`
- Test: `frontend/src/features/tasks/task-execution-page.test.tsx`

- [ ] **Step 1: Write the failing task page test**

Assert that the task execution page renders:
- task context panel
- approved plan section
- event timeline
- evidence panel placeholder
- conclusion preview placeholder

- [ ] **Step 2: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/tasks/task-execution-page.test.tsx
```
Expected: FAIL until the page exists.

- [ ] **Step 3: Implement the task flow UI**

Support:
- create task
- generate plan
- approve plan
- run task
- view stage progression

Use Zustand only for local UI state that does not belong in server cache.

- [ ] **Step 4: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/tasks/task-execution-page.test.tsx
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/tasks frontend/src/entities/task.ts
git commit -m "feat: add task planning and execution workspace"
```

### Task 12: Implement evidence panel and conclusion card detail page

**Files:**
- Create: `frontend/src/features/evidence/api.ts`
- Create: `frontend/src/features/evidence/components/evidence-panel.tsx`
- Create: `frontend/src/features/evidence/components/evidence-item.tsx`
- Create: `frontend/src/features/conclusion-cards/api.ts`
- Create: `frontend/src/features/conclusion-cards/pages/conclusion-card-page.tsx`
- Create: `frontend/src/features/conclusion-cards/components/conclusion-section.tsx`
- Create: `frontend/src/entities/evidence.ts`
- Create: `frontend/src/entities/conclusion-card.ts`
- Test: `frontend/src/features/conclusion-cards/conclusion-card-page.test.tsx`

- [ ] **Step 1: Write the failing conclusion card page test**

Assert that all seven required sections render and citations are linked to evidence.

- [ ] **Step 2: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/conclusion-cards/conclusion-card-page.test.tsx
```
Expected: FAIL until the feature exists.

- [ ] **Step 3: Implement evidence and conclusion views**

Ensure conclusion sections are readable at a glance and evidence metadata remains traceable.

- [ ] **Step 4: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/conclusion-cards/conclusion-card-page.test.tsx
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/features/evidence frontend/src/features/conclusion-cards frontend/src/entities/evidence.ts frontend/src/entities/conclusion-card.ts
git commit -m "feat: add evidence and conclusion card views"
```

## Chunk 6: Integration, Migration, and Verification

### Task 13: Wire frontend to backend APIs with realistic empty/loading/error states

**Files:**
- Modify: `frontend/src/shared/api/client.ts`
- Modify: `frontend/src/features/projects/api.ts`
- Modify: `frontend/src/features/tasks/api.ts`
- Modify: `frontend/src/features/evidence/api.ts`
- Modify: `frontend/src/features/conclusion-cards/api.ts`
- Test: `frontend/src/features/tasks/task-api.integration.test.tsx`

- [ ] **Step 1: Write the failing API integration test**

Mock backend responses for plan generation, approval, execution, evidence retrieval, and card retrieval.

- [ ] **Step 2: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/tasks/task-api.integration.test.tsx
```
Expected: FAIL until data hooks match API contracts.

- [ ] **Step 3: Implement request wiring**

Map backend schemas into frontend entities and handle empty, loading, and error states explicitly.

- [ ] **Step 4: Run the test**

Run:
```bash
cd frontend && npm test -- --runInBand frontend/src/features/tasks/task-api.integration.test.tsx
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src
git commit -m "feat: connect react workspace to backend apis"
```

### Task 14: Add end-to-end verification and update project documentation

**Files:**
- Modify: `README.md`
- Modify: `README_EN.md`
- Create: `backend/tests/app/test_v1_happy_path.py`
- Create: `frontend/README.md`

- [ ] **Step 1: Write the failing backend happy-path test**

```python
def test_v1_happy_path(client) -> None:
    project = client.post("/projects", json={"name": "AI Search"}).json()
    task = client.post(f"/projects/{project['id']}/tasks", json={...}).json()
    client.post(f"/tasks/{task['id']}/plan")
    client.post(f"/tasks/{task['id']}/approve")
    client.post(f"/tasks/{task['id']}/run")
    card = client.get(f"/tasks/{task['id']}/conclusion-card").json()
    assert card["coreConclusion"]
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd backend && pytest backend/tests/app/test_v1_happy_path.py -v
```
Expected: FAIL until the whole flow is integrated.

- [ ] **Step 3: Update docs**

Document:
- product purpose
- local dev setup
- backend run command
- frontend run command
- V1 workflow
- main API endpoints

- [ ] **Step 4: Run full verification**

Run:
```bash
cd backend && pytest -v
```

Run:
```bash
cd frontend && npm run build
```
Expected: both succeed.

- [ ] **Step 5: Commit**

```bash
git add README.md README_EN.md frontend/README.md backend/tests/app/test_v1_happy_path.py
git commit -m "docs: update project for business research workbench"
```

## Execution Notes

- Start by removing tracked local binaries and generated folders from git history going forward. The existing `backend/.bin/uv` file is too large for a healthy repository.
- Keep the first persistence implementation simple and local. Avoid introducing a database until the domain and API shape are stable.
- Preserve the existing search and summarization integrations where they still fit, but move them behind workflow and agent boundaries instead of calling them from a monolithic coordinator.
- Treat compatibility with the old `/research` endpoint as optional. If it slows down the redesign, remove it and migrate cleanly.
- Do not rebuild the product as a chat-first interface. The UI should always reinforce project -> task -> evidence -> conclusion flow.

Plan complete and saved to `docs/superpowers/plans/2026-03-13-business-research-workbench-implementation.md`. Ready to execute?
