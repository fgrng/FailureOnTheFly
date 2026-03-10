# Tasks: 001-diagnostic-training-sim (Diagnostisches Gesprächstraining)

**Input**: Design documents from `/specs/001-diagnostic-training-sim/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Initialize Python environment and create `.gitignore` (Done)
- [ ] T002 [P] Create project directory structure (data/, tests/)
- [ ] T003 Create `data/tasks.json` with predefined math tasks (Done)
- [ ] T004 [P] Configure environment variables in `.env.example` (OPENAI_API_KEY, LLM_PROVIDER, LLM_MODEL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T005 [P] Create Pydantic models for `StudentResponse` and `Task` in `models.py`
- [ ] T006 [P] Implement LLM provider abstraction in `llm_provider.py`
- [ ] T007 [P] Implement OpenAI Whisper integration in `transcription.py`
- [ ] T008 Implement session state initialization and task loading logic in `app.py`
- [ ] T009 [P] Create basic test suite for LLM connectivity and transcription in `tests/test_infrastructure.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Diagnostisches Gespräch führen (Priority: P1) 🎯 MVP

**Goal**: Enable a teacher to have a diagnostic conversation with a simulated student via text or voice.

**Independent Test**: Start a session, send a text or voice message, and receive a consistent student response based on the error pattern.

### Implementation for User Story 1

- [ ] T010 [US1] Implement conversation logic using `instructor` in `conversation.py`
- [ ] T011 [US1] Create chat UI layout (teacher right, student left) in `app.py`
- [ ] T012 [US1] Integrate `st.chat_input` with text and audio fallback (toggle) in `app.py`
- [ ] T013 [US1] Add "Schüler denkt nach..." loading indicator (st.spinner) in `app.py`
- [ ] T014 [US1] Implement message history management in `st.session_state`
- [ ] T015 [US1] Connect audio recording to `transcription.py` and then to `conversation.py`
- [ ] T016 [US1] Add basic error handling for API failures and microphone issues

**Checkpoint**: User Story 1 (The core simulation) is fully functional.

---

## Phase 4: User Story 2 - Diagnose abgeben (Priority: P2)

**Goal**: Allow the teacher to end the conversation and submit a formal diagnosis.

**Independent Test**: Click "Ich bin jetzt so weit", see the diagnosis form, select an option, enter text, and save the diagnosis.

### Implementation for User Story 2

- [ ] T017 [US2] Add "Ich bin jetzt so weit" button to end the chat in `app.py`
- [ ] T018 [US2] Implement logic to disable chat/mic once conversation has ended in `app.py`
- [ ] T019 [US2] Create hybrid diagnosis form (Single-Choice + Free-text) in `app.py`
- [ ] T020 [US2] Implement diagnosis saving logic in `st.session_state`
- [ ] T021 [US2] Add summary view showing the full conversation and submitted diagnosis

**Checkpoint**: User Story 2 is functional - the training loop is closed.

---

## Phase 5: User Story 3 - Unterrichtssituation und Aufgabe einsehen (Priority: P3)

**Goal**: Provide the teacher with the necessary context (classroom situation and the student's work).

**Independent Test**: Verify that the situation description and math task are visible at the top of the page.

### Implementation for User Story 3

- [ ] T022 [P] [US3] Implement Kopfbereich (Kontext) display logic in `app.py`
- [ ] T023 [P] [US3] Ensure the context remains visible/accessible when scrolling back up

**Checkpoint**: User Story 3 provides the context for the simulation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Refinement and final validation.

- [ ] T024 [P] Refactor `app.py` into clean Streamlit sections (Header, Interaction, Footer)
- [ ] T025 [P] Improve system prompts in `data/tasks.json` for higher consistency
- [ ] T026 Add final integration tests for the full user journey in `tests/test_e2e.py`
- [ ] T027 [P] Create `quickstart.md` with final setup and usage instructions
- [ ] T028 Performance check: Ensure SC-002 (response < 5s) and SC-004 (diagnosis < 2m) are met

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: Can start immediately.
2. **Foundational (Phase 2)**: Depends on Phase 1 completion.
3. **User Story 1 (Phase 3)**: Depends on Phase 2. **This is the MVP**.
4. **User Story 2 & 3 (Phases 4 & 5)**: Depend on Phase 3 completion for a meaningful flow, but US3 can be done in parallel with US1.
5. **Polish (Phase 6)**: Final step.

### Parallel Opportunities

- **Models & Infrastructure (T005, T006, T007)**: Can be developed concurrently.
- **UI Context (US3)**: Can be implemented while US1 logic is being built.
- **Refactoring (Phase 6)**: Can happen after each story is verified.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

The primary goal is to get the chat working. Once a teacher can talk to Lukas (US1), the prototype has its core value. US2 (Diagnosis) and US3 (Context) follow to complete the pedagogical experience.
