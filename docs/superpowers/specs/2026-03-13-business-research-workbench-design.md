# Business Research Workbench Design

## Overview

This document defines the V1 redesign for the current folder as a new product rather than an iteration on the existing deep research demo.

The product is a business research workbench for knowledge workers. Users organize research inside projects, create structured research tasks, review a generated research plan before execution, and receive a structured conclusion card with evidence and decision guidance.

The redesign explicitly does not treat chat as the product center. The system centers on project space, task lifecycle, evidence traceability, and reusable conclusion assets.

## Product Definition

### Target User

- Knowledge workers
- Typical roles: product managers, operators, strategists, market researchers, consultants, independent professionals

### Core Product Value

- Combine research and decision support
- Turn ambiguous business questions into executable research tasks
- Produce traceable, structured decision-ready outputs rather than only long-form reports

### Product Form

- Project-based workspace
- Multi-turn collaboration inside each project
- Support for single research runs inside project context

### V1 Scenario Templates

- Competitor / solution research
- Industry / trend research
- Opportunity / decision research

## Scope and Non-Goals

### In Scope for V1

- Create and browse projects
- Create research tasks inside projects
- Generate research plan before execution
- Human approval gate after planning
- Execute research workflow
- Collect and display evidence
- Generate structured conclusion cards
- Surface recommendations, risks, and citations
- Review historical tasks and conclusion cards in the project

### Out of Scope for V1

- Team collaboration, permissions, multi-user workflows
- External action execution such as email, ticketing, or business system writes
- Complex cross-project memory and recommendation systems
- Chat-first product positioning
- Prompt marketplace, visual workflow builder, or generalized agent platform features
- Mobile-first product scope

## Core Business Objects

### Project

Purpose: container for a research theme and its assets.

Suggested fields:

- `id`
- `name`
- `description`
- `defaultTemplateType`
- `createdAt`
- `updatedAt`

### ResearchTask

Purpose: core execution unit for one business research request.

Suggested fields:

- `id`
- `projectId`
- `title`
- `question`
- `background`
- `goal`
- `constraints`
- `templateType`
- `status`
- `priority`
- `planSnapshot`
- `startedAt`
- `completedAt`
- `createdAt`
- `updatedAt`

Notes:

- `planSnapshot` is required because V1 includes a planning approval gate.
- The task is the primary object in the system. Evidence and conclusion cards are attached to it.

### Evidence

Purpose: structured evidence unit collected during execution.

Suggested fields:

- `id`
- `taskId`
- `projectId`
- `title`
- `url`
- `sourceType`
- `snippet`
- `summary`
- `credibility`
- `stance`
- `tags`
- `collectedAt`

Notes:

- `credibility` supports evidence review and source quality checks.
- `stance` helps identify support, opposition, or neutral positioning.

### ConclusionCard

Purpose: primary output of a completed research task.

Suggested fields:

- `id`
- `taskId`
- `projectId`
- `problemDefinition`
- `coreConclusion`
- `keyEvidence`
- `alternativeViews`
- `recommendedActions`
- `risksAndUncertainties`
- `citations`
- `version`
- `createdAt`
- `updatedAt`

Required sections for V1:

- Problem definition
- Core conclusion
- Key evidence
- Alternative views / disagreement points
- Recommended actions
- Risks and uncertainties
- Citations

### TaskEvent

Purpose: event stream for execution visibility, auditability, and UI rendering.

Suggested fields:

- `id`
- `taskId`
- `type`
- `stage`
- `message`
- `payload`
- `createdAt`

## Task Lifecycle

V1 task lifecycle:

1. `Draft`
2. `Planning`
3. `PendingApproval`
4. `Researching`
5. `Reviewing`
6. `Synthesizing`
7. `Completed`

### Stage Semantics

#### Draft

User creates a task and supplies:

- question
- background
- goal
- constraints
- template type

#### Planning

The orchestrator invokes the planning agent to generate a research plan containing:

- clarified objective
- decomposition dimensions
- search directions
- expected output focus

#### PendingApproval

User reviews the generated plan.

Allowed user actions:

- approve
- revise question
- add constraints
- ask for replanning

This is the only explicit human checkpoint in V1.

#### Researching

The system collects, summarizes, and categorizes evidence according to the approved plan.

#### Reviewing

Evidence quality is checked for:

- source reliability
- information conflicts
- evidence gaps
- sufficiency to support a conclusion

#### Synthesizing

Conclusion and recommendation stages generate the final conclusion card.

#### Completed

The task output is stored in the project as reusable evidence and conclusion assets.

## Agent Architecture

### Design Principle

Use controlled orchestration rather than free-form multi-agent conversation.

Only the orchestrator controls task state transitions. Specialized sub-agents operate as bounded capability units with explicit input and output contracts.

### Agent Topology

- `OrchestratorAgent`
- `TaskPlanningAgent`
- `EvidenceResearchAgent`
- `EvidenceReviewAgent`
- `ConclusionSynthesisAgent`
- `DecisionAdvisoryAgent`

### OrchestratorAgent

Responsibilities:

- receive task context
- determine the next stage
- invoke the correct sub-agent
- persist outputs to domain objects
- emit task events for the UI
- stop and wait during approval gate

The orchestrator owns process control, not all content generation.

### TaskPlanningAgent

Inputs:

- task question
- background
- goal
- constraints
- template type

Outputs:

- clarified objective
- decomposition dimensions
- research plan
- output priorities

### EvidenceResearchAgent

Inputs:

- approved plan
- existing evidence
- template type

Outputs:

- collected evidence items
- extracted summaries and snippets
- initial evidence categorization

### EvidenceReviewAgent

Inputs:

- current evidence set

Outputs:

- credibility annotations
- conflict points
- evidence gap list
- sufficiency judgment

### ConclusionSynthesisAgent

Inputs:

- reviewed evidence set
- original task context

Outputs:

- problem definition
- core conclusion
- key evidence summary
- alternative views / disagreement points

### DecisionAdvisoryAgent

Inputs:

- conclusion draft
- identified risks
- original task goal

Outputs:

- recommended actions
- risks and uncertainties
- suggested next research steps if needed

### Architectural Rules

- Only the orchestrator can change task status.
- Evidence and conclusion are separate layers.
- Evidence review is independent from evidence collection.
- Frontend should show task status, events, evidence, and structured outputs rather than raw agent-to-agent dialogue.

## Frontend Architecture

### Stack Direction

- React
- Vite
- TypeScript
- Tailwind CSS
- shadcn/ui

This project should be rebuilt from the current Vue implementation into a React workspace application.

### Product Information Architecture

Two-layer workspace model:

- Project layer
- Task layer

The overall product behaves like a knowledge project workspace. Individual task pages behave like a professional analysis console.

### V1 Pages

#### Project List Page

Purpose:

- view projects
- create project
- inspect recent activity

#### Project Detail Page

Purpose:

- act as the project home
- list tasks
- surface recent conclusion cards
- provide entry point to create new research tasks

#### New Research Task Page or Modal

Purpose:

- create a task quickly
- collect question, background, goal, constraints, and template type

#### Task Execution Page

This is the core page in V1.

Recommended three-column layout:

- left: task context and approved plan
- center: execution timeline and stage progress
- right: evidence panel and current conclusion preview

#### Conclusion Card Detail Page

Purpose:

- present the conclusion card as a reusable asset
- connect back to task and evidence

#### Evidence Panel

Purpose:

- show source, summary, stance, credibility, and citations
- support traceability from conclusion back to evidence

## Backend Refactor Direction

The current folder should be reoriented from a one-shot research demo into a project-task-evidence-conclusion architecture.

Recommended backend structure:

- `backend/src/app`
- `backend/src/domain`
- `backend/src/agents`
- `backend/src/workflows`
- `backend/src/infrastructure`
- `backend/src/services`

### Layer Responsibilities

#### `app`

- FastAPI entrypoints
- routers
- request/response schemas
- dependency wiring

#### `domain`

- project models
- task models
- evidence models
- conclusion card models
- task lifecycle state machine

#### `agents`

- orchestrator agent
- planning agent
- research agent
- review agent
- synthesis agent
- advisory agent

#### `workflows`

- task execution orchestration
- approval handling
- lifecycle transitions

#### `infrastructure`

- LLM adapters
- search adapters
- fetch/extract adapters
- persistence adapters
- logging/event streaming adapters

#### `services`

- thin application services that coordinate domain operations
- avoid retaining broad mixed-responsibility service files

## UX and Interaction Principles

- The user is progressing a task, not chatting with a generic bot.
- Every result should be traceable back to evidence.
- Planning approval is the main V1 control point.
- The UI should make task state and reasoning progress legible.
- Conclusion cards should be readable quickly and reusable later.

## Success Criteria

V1 is successful if:

1. A user can create and start a research task in under three minutes.
2. The user can clearly understand and approve the research plan before execution.
3. The user receives a readable, traceable conclusion card with recommendations and citations.
4. The user can revisit prior tasks and conclusion outputs inside a project rather than starting from scratch every time.

## Risks and Follow-Up

### Main Risks

- Product drifts back into chat-first interaction
- Agent orchestration becomes too framework-driven before the business model stabilizes
- Evidence quality checks are too weak, reducing trust in recommendations
- Frontend rebuild focuses on cosmetics before information architecture and state model are solid

### V2 Follow-Up Areas

- Multi-checkpoint human collaboration
- richer evidence scoring
- conclusion card versioning
- cross-project asset reuse
- decision comparison views
- task continuation and follow-up research chaining

## Implementation Readiness

The design is ready for implementation planning once the user reviews and approves this document.

Known limitation in the current environment:

- The current folder is not a git repository, so the spec cannot be committed in this workspace state.
