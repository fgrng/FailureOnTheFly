# Implementation Plan: FailureOnTheFly

**Branch**: `001-diagnostic-training-sim` | **Date**: 2026-03-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-diagnostic-training-sim/spec.md`

## Summary

Web-based prototype for simulating student-teacher diagnostic conversations. A teacher uses voice or text input to question a simulated student (LLM) about their incorrect math solution, aiming to identify the student's error pattern. Built as a Streamlit application with OpenAI Whisper for speech-to-text and Python instructor for structured LLM responses.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: streamlit, instructor, openai, pydantic
**Storage**: In-memory (Streamlit session state) — prototype scope, no database
**Testing**: pytest
**Target Platform**: Desktop browser (Chrome/Firefox), localhost development server
**Project Type**: Streamlit web application (single process, no separate backend)
**Performance Goals**: Student response within 5 seconds, speech transcription within 3 seconds
**Constraints**: Single-user prototype, German language, requires microphone access (HTTPS/localhost)
**Scale/Scope**: Single predefined math task, single concurrent user

## Constitution Check

*No constitution file found — no gates to evaluate.*

## Project Structure

### Documentation (this feature)

```text
specs/001-diagnostic-training-sim/
├── plan.md              # This file
├── research.md          # Phase 0 output — technology decisions
├── data-model.md        # Phase 1 output — entity definitions
├── quickstart.md        # Phase 1 output — setup instructions
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
app.py                   # Streamlit app entry point, page layout, three-section UI flow
models.py                # Pydantic models for instructor response models and data structures
conversation.py          # LLM conversation logic via instructor, session state management
llm_provider.py          # LLM provider abstraction — switchable via LLM_PROVIDER env var
transcription.py         # OpenAI Whisper API integration
data/
└── tasks.json           # Predefined math tasks with error patterns and diagnosis options
```

**Structure Decision**: Flat single-application layout. Streamlit serves as both frontend and backend in a single process. No backend/frontend separation needed — all logic runs server-side in Python. `st.session_state` manages conversation state.

## LLM Provider Abstraction

`llm_provider.py` reads `LLM_PROVIDER` and `LLM_MODEL` env vars and returns a configured instructor client via `instructor.from_provider(f"{provider}/{model}")`. Default: `openai/gpt-4o-mini`.

## Session State

All runtime state in `st.session_state`:

- `messages`: `list[dict]` with `role` + `content` (+ optional `internal_thought`). Full list passed to instructor on each call.
- `conversation_ended`: `bool`
- `diagnosis`: `dict | None` (`selected_option` + `text`)
- `task`: Loaded JSON from `tasks.json`

## UI Layout

Three chronological sections (top to bottom):

1. **Kopfbereich (Kontext)**: Static display of the classroom situation narrative and the math task with the student's incorrect solution (image or text). Accessible via scrolling up.
2. **Interaktionsbereich (Chat & Audio)**: 
   - **Input Strategy**: Preference for `st.chat_input(accept_audio=True)`. 
   - **Fallback**: If not supported by the Streamlit version, a toggle button (`st.toggle("🎙️ Spracheingabe")`) switches between a text field (`st.chat_input`) and an audio widget (`st.audio_input`).
   - **Chat history**: Teacher messages right-aligned, student messages left-aligned. Disabled after conversation ends.
3. **Abschlussbereich**: "Ich bin jetzt so weit" button (ends chat, disables mic) + hybrid diagnosis form (single-choice for predefined error patterns + free-text field). Diagnosis area only visible after clicking the end button.

## Core Flow

```
1. Audio Capture     Teacher speaks → audio captured (via chat_input or audio_input)
2. Transcription     Sent to OpenAI Whisper API (language="de") → transcript text
3. Chat Display      Transcript rendered as teacher message (right-aligned)
4. Thinking State    Display "Schüler denkt nach..." indicator (e.g., st.spinner)
5. LLM Request       Transcript + full chat history + system prompt → sent to LLM via instructor
6. Structured Reply  Instructor returns StudentResponse(student_response=..., internal_thought=...)
7. Chat Display      student_response shown as student message (left-aligned); internal_thought stored for debugging
```

The `StudentResponse` Pydantic model enforces structured output:
- `student_response`: The visible text in the chat UI
- `internal_thought` (optional): What the student thinks but doesn't say — useful for debugging simulation quality

## Key Technical Decisions

See [research.md](research.md) for full decision records. Summary:

1. **Instructor for LLM**: Pydantic response models via provider abstraction (`llm_provider.py`). Provider selected by `LLM_PROVIDER` env var, model by `LLM_MODEL`. Conversation history as message list in `st.session_state`, passed on each call.
2. **Whisper API**: `model="whisper-1"`, `language="de"`, accepts WAV.
3. **Audio recording**: Preference for native `st.chat_input` audio; fallback to `st.audio_input` with UI toggle.
4. **Session management**: `st.session_state` stores conversation messages, task data, diagnosis. Per-tab, lost on refresh — acceptable for prototype.
5. **Dual input channels**: User chooses between text and audio. Fallback UI uses a toggle to avoid clutter.
6. **No separate backend**: Streamlit calls OpenAI APIs directly from Python. No FastAPI, no REST endpoints, no API contracts needed.
7. **Thinking Indicator**: Visual feedback during LLM latency to ensure SC-002 is perceived as active.
