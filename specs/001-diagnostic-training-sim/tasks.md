# Tasks: 001-diagnostic-training-sim (FailureOnTheFly)

**Input**: Design documents from `/specs/001-diagnostic-training-sim/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Implementation Rationales (Decision Log)

- **Framework**: **Streamlit** was chosen for the rapid prototyping of the chat interface, enabling easy integration of audio and text inputs without complex frontend management.
- **Structured LLM Output**: **Instructor** (with Pydantic) is used to separate `student_response` (visible) from `internal_thought` (hidden reasoning). This allows the simulator to maintain a consistent "mental model" of the student's error pattern without leaking it directly to the teacher.
- **Audio Processing**: **OpenAI Whisper** via the `transcription.py` module is the chosen solution for US1, as it provides high accuracy for classroom-like speech in German.
- **Data Persistence**: **JSON files** in `data/sessions/` are used to record full training runs (US2 Extension). This supports later pedagogical evaluation and "Review Sessions".
- **UX Strategy**: 
    - **Side-by-side Buttons**: "Frage senden" and "Diagnose abgeben" are placed next to each other to emphasize the two main actions in the diagnostic loop.
    - **Visual Coding**: The "End Chat" button is styled red to prevent accidental termination and clearly mark it as a state-changing action.
    - **Sidebar Task Selection**: Added to allow teachers to quickly switch between different mathematical error patterns (e.g., Equals Sign vs. Place Value).

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Initialize Python environment and create `.gitignore` (Done)
- [x] T002 [P] Create project directory structure (data/, tests/) (Done)
- [x] T003 Create `data/tasks.json` with predefined math tasks (Done)
- [x] T004 [P] Configure environment variables in `.env.example` (OPENAI_API_KEY, LLM_PROVIDER, LLM_MODEL) (Done)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T005 [P] Create Pydantic models for `StudentResponse` and `Task` in `models.py` (Done)
- [x] T006 [P] Implement LLM provider abstraction in `llm_provider.py` (Done)
- [x] T007 [P] Implement OpenAI Whisper integration in `transcription.py` (Done)
- [x] T008 Implement session state initialization and task loading logic in `app.py` (Done)
- [x] T009 [P] Create basic test suite for LLM connectivity and transcription in `tests/test_infrastructure.py` (Done)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Diagnostisches Gespräch führen (Priority: P1) 🎯 MVP

**Goal**: Enable a teacher to have a diagnostic conversation with a simulated student via text or voice.

**Independent Test**: Start a session, send a text or voice message, and receive a consistent student response based on the error pattern.

### Implementation for User Story 1

- [x] T010 [US1] Implement conversation logic using `instructor` in `conversation.py` (Done)
- [x] T011 [US1] Create chat UI layout (teacher right, student left) in `app.py` (Done)
- [x] T012 [US1] Integrate `st.chat_input` with text and audio fallback (toggle) in `app.py` (Done - *Decision: used text_area for better multi-line support*)
- [x] T013 [US1] Add "Schüler denkt nach..." loading indicator (st.spinner) in `app.py` (Done)
- [x] T014 [US1] Implement message history management in `st.session_state` (Done)
- [x] T015 [US1] Connect audio recording to `transcription.py` and then to `conversation.py` (Done)
- [x] T016 [US1] Add basic error handling for API failures and microphone issues (Done)

**Checkpoint**: User Story 1 (The core simulation) is fully functional.

---

## Phase 4: User Story 2 - Diagnose abgeben (Priority: P2)

**Goal**: Allow the teacher to end the conversation and submit a formal diagnosis.

**Independent Test**: Click "Ich bin jetzt so weit", see the diagnosis form, select an option, enter text, and save the diagnosis.

### Implementation for User Story 2

- [x] T017 [US2] Add "Ich bin jetzt so weit" button to end the chat in `app.py` (Done - *Decision: labeled as "Diagnose abgeben (Chat beenden)"*)
- [x] T018 [US2] Implement logic to disable chat/mic once conversation has ended in `app.py` (Done)
- [x] T019 [US2] Create hybrid diagnosis form (Single-Choice + Free-text) in `app.py` (Done)
- [x] T020 [US2] Implement diagnosis saving logic in `st.session_state` (Done)
- [x] T021 [US2] Add summary view showing the full conversation and submitted diagnosis (Done)

**Checkpoint**: User Story 2 is functional - the training loop is closed.

---

## Phase 5: User Story 3 - Unterrichtssituation und Aufgabe einsehen (Priority: P3)

**Goal**: Provide the teacher with the necessary context (classroom situation and the student's work).

**Independent Test**: Verify that the situation description and math task are visible at the top of the page.

### Implementation for User Story 3

- [x] T022 [P] [US3] Implement Kopfbereich (Kontext) display logic in `app.py` (Done)
- [x] T023 [P] [US3] Ensure the context remains visible/accessible when scrolling back up (Done)

**Checkpoint**: User Story 3 provides the context for the simulation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Refinement and final validation.

- [x] T024 [P] Refactor `app.py` into clean Streamlit sections (Header, Interaction, Footer) (Done)
- [ ] T025 [P] Improve system prompts in `data/tasks.json` for higher consistency
- [ ] T026 Add final integration tests for the full user journey in `tests/test_e2e.py`
- [x] T027 [P] Create `quickstart.md` with final setup and usage instructions (Done)
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
