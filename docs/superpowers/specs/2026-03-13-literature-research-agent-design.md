# Literature Research Agent Design

Date: 2026-03-13

## Product Definition

The product is a research topic workspace for computer science and AI researchers. Users organize work around topics, ask research questions inside a topic, retrieve and screen representative papers, discuss findings with the agent, and continuously accumulate reusable research memory.

The product is not a generic chat assistant. Its center is topic memory, paper evidence, and research guidance.

## Target Users

- Primary: computer science and AI researchers
- Future direction: keep the architecture extensible for broader research domains

## Core Value

Help researchers answer questions such as:

- I want to quickly understand a direction
- I want the most representative recent papers for a problem
- I want to compare several approaches
- I want to accumulate papers and notes into my own research memory
- I want evidence-grounded suggestions for possible next research directions

## Primary Interaction Model

The primary product shape is a topic workspace.

- A topic is the long-lived container for a research direction
- Inside a topic, the default experience is a research Q&A workspace
- The same topic also exposes paper cards, topic notes, and idea or hypothesis notes

## V1 Main Entry

The strongest V1 path is:

`research question -> literature retrieval -> representative paper screening -> research guidance card -> memory write-back`

The first default action inside a topic is:

- user enters a research question
- system returns recent representative papers
- system produces a guidance card grounded in the retrieved evidence

## Core Business Flow

Each research round follows six stages:

1. `Question Framing`
   - identify the research question
   - identify time window
   - identify user intent
   - identify active topic context

2. `Literature Retrieval`
   - query arXiv and Semantic Scholar
   - build a candidate paper pool

3. `Paper Screening`
   - select representative papers from the candidate pool

4. `Paper Analysis`
   - extract structured paper information

5. `Research Synthesis`
   - produce a research guidance card

6. `Memory Update`
   - update short-term memory
   - write paper cards, topic notes, and idea notes into long-term memory

The working principle is:

`Memory Recall -> Retrieval -> Screening -> Analysis -> Synthesis -> Memory Write-back`

## Literature Sources

V1 literature sources:

- arXiv
- Semantic Scholar

Rationale:

- arXiv supplies fast-moving recent work
- Semantic Scholar supplies stronger academic metadata and related-paper support

## Retrieval Strategy

Retrieval should use query expansion instead of a single raw user query.

Each research question should generate:

- core problem queries
- synonym or variant queries
- recent-trend queries

Results are merged and deduplicated into a candidate pool before screening.

## Screening Logic

The screening logic must follow venue quality before raw recency.

Primary ordering principle:

`top venue priority > award or presentation tier > time > relevance`

### Venue Priority

Top-tier pool:

- CCF-A venues
- ICLR
- EMNLP

High-quality supplementary pool:

- CCF-B venues

Additional fallback pool:

- highly relevant recent papers outside the top-tier pool

### Award and Presentation Signals

When available, raise priority for:

- Best Paper
- Outstanding Paper
- Spotlight
- Oral

### Time Window

- default: last 2 years
- user-adjustable

### Relevance

Relevance still matters, but only after venue quality and award signals are considered.

### Fallback Rule

If the recent top-tier pool is too sparse for a topic:

- supplement with highly relevant recent arXiv papers
- or supplement with older but clearly foundational papers

## Guidance Card Output

The primary output is a research guidance card with these fields:

1. Research problem definition
2. Representative papers from the last two years
3. Main method tracks
4. Method differences, strengths, and weaknesses
5. Current research gaps or limitations
6. Possible improvement directions
7. Suggested reading order
8. Sources and links

## Single Paper Presentation Principles

The system should not over-interpret individual papers by default.

Default paper presentation includes:

- title
- abstract
- short method summary
- PDF URL
- venue
- year
- authors

The system should not aggressively assign definitive innovation or weakness judgments at first display. That analysis belongs to follow-up discussion when the user asks for it.

Principle:

`show evidence first, discuss interpretation second`

## Data Model

The system should define six first-class objects.

### TopicWorkspace

Represents a long-lived research topic container.

Core fields:

- `id`
- `title`
- `description`
- `researchDomain`
- `defaultTimeWindow`
- `createdAt`
- `updatedAt`

### ResearchSession

Represents one structured research round inside a topic.

Core fields:

- `id`
- `workspaceId`
- `question`
- `intentType`
- `timeWindow`
- `status`
- `retrievedPaperIds`
- `selectedPaperIds`
- `researchCardId`
- `createdAt`
- `updatedAt`

### PaperCard

Represents a reusable structured paper memory unit.

Core fields:

- `id`
- `workspaceId`
- `title`
- `authors`
- `year`
- `venue`
- `source`
- `url`
- `abstract`
- `keywords`
- `problem`
- `method`
- `contributions`
- `limitations`
- `relevanceScore`
- `notes`
- `createdAt`
- `updatedAt`

### TopicNote

Represents topic-level synthesis and staged understanding.

Core fields:

- `id`
- `workspaceId`
- `title`
- `summary`
- `openQuestions`
- `methodClusters`
- `lastUpdatedFromSessionId`
- `createdAt`
- `updatedAt`

### IdeaNote

Represents the user's own research ideas and hypotheses.

Core fields:

- `id`
- `workspaceId`
- `title`
- `ideaType`
- `content`
- `relatedPaperIds`
- `confidence`
- `status`
- `createdAt`
- `updatedAt`

### ResearchCard

Represents the main output card for one research session.

Core fields:

- `id`
- `workspaceId`
- `sessionId`
- `problemDefinition`
- `representativePapers`
- `mainMethodTracks`
- `methodDifferences`
- `researchGaps`
- `improvementDirections`
- `readingOrder`
- `citations`
- `createdAt`
- `updatedAt`

## Agent Architecture

Use a controlled orchestrator plus specialized sub-agents.

### Orchestrator Agent

Responsibilities:

- identify intent
- request memory recall
- coordinate retrieval, screening, analysis, and synthesis
- trigger memory write-back

### Literature Retrieval Agent

Responsibilities:

- produce retrieval queries
- call arXiv and Semantic Scholar
- merge and normalize candidates

### Paper Screening Agent

Responsibilities:

- apply venue and time filters
- score and rank candidates
- pick representative papers

### Paper Analysis Agent

Responsibilities:

- extract structured paper fields
- build paper-card-ready information

### Research Synthesis Agent

Responsibilities:

- cluster methods
- identify differences and gaps
- create the final guidance card

### Memory Agent

Responsibilities:

- maintain short-term session memory
- recall long-term topic memory
- write new paper cards, topic notes, and idea notes

## Memory Architecture

The memory system has two layers.

### Short-Term Memory

Used for continuity inside an active topic and session.

Must include:

- current topic research question
- current sub-question
- papers already retrieved in the session
- papers selected as representative
- recent turns and instructions
- draft guidance content
- user research ideas mentioned in the current topic

Short-term memory should not be implemented as unbounded full chat history. It should be a structured session state plus rolling summary.

### Long-Term Memory

Long-term memory is stored as structured objects:

- `PaperCard`
- `TopicNote`
- `IdeaNote`

### Recall and Write-Back Strategy

Use:

`Recall Before Action, Write After Action`

Before each research round:

- automatically recall relevant paper cards
- automatically recall relevant topic notes
- automatically recall relevant idea notes

After each research round:

- write new paper cards
- update topic notes
- write or update idea notes

### User Control

Memory recall should be:

- automatic by default
- inspectable by the user
- correctable by the user

The system should expose which prior memories influenced the current answer.

## Frontend Information Architecture

The UI should use a two-layer structure:

- topic level
- research level

Inside a topic, the default page is a research Q&A workspace, but the user can also switch to stored artifacts.

### V1 Pages

1. Topic list page
2. Topic home page
3. Research Q&A page
4. Representative paper result panel or page
5. Paper card detail page
6. Topic note page
7. Idea or hypothesis note page

### Core Research Page Layout

Three-column layout:

- left: topic context and recalled memory
- center: research Q&A and guidance card
- right: representative papers

This layout should make the relationship between question, memory, and evidence explicit.

## Model Strategy

The system should not rely on raw model memory. Memory quality should primarily come from explicit storage and retrieval.

V1 model strategy:

- one main model for reasoning, screening, synthesis, and memory-aware answering
- optional lightweight model or rule layer later for preprocessing or extraction

The system should support OpenAI-compatible providers and keep model selection abstracted behind a provider interface.

The key model requirements are:

- strong structured output
- good long-context handling
- reliable bilingual understanding
- stable synthesis over multiple paper summaries

## V1 Scope

V1 includes:

- topic workspaces
- research Q&A inside topics
- arXiv and Semantic Scholar retrieval
- representative recent paper screening
- research guidance cards
- paper card, topic note, and idea note persistence
- automatic memory recall

V1 explicitly excludes:

- full multi-discipline coverage
- heavy PDF full-text pipelines as the main path
- paper writing automation
- experiment automation or reproduction pipelines
- team collaboration
- citation graph visualization
- generic chat-assistant positioning

## V1 Success Criteria

1. A user can ask a research question inside a topic and receive a useful set of representative recent papers.
2. The system presents papers with objective information first, without over-assertive interpretation.
3. The system produces a research guidance card grounded in evidence.
4. When the user returns to the topic later, the system recalls prior papers, notes, and ideas well enough to continue the work.

## Non-Goals

- Become a general-purpose LLM chat application
- Cover every research field in V1
- Replace researcher judgment on paper novelty
- Over-automate speculative innovation suggestions without evidence

## Design Principles

- Evidence before interpretation
- Structure before free-form conversation
- Topic memory over raw chat history
- Research continuity over one-shot answers
- Guidance grounded in retrieved literature
