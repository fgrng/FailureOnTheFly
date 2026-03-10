# Research: Diagnostisches Gesprächstraining

**Date**: 2026-03-10
**Feature**: 001-diagnostic-training-sim

## Decision 1: LLM Integration via Python Instructor with Provider Abstraction

**Decision**: Use `instructor` library with a provider abstraction layer (`llm_provider.py`). Provider selected via `LLM_PROVIDER` env var (default: `openai`), model via `LLM_MODEL` env var.

**Rationale**:
- Instructor patches LLM clients to accept Pydantic `response_model` and returns validated Python objects.
- `instructor.from_provider()` supports OpenAI, Anthropic, Google Gemini, Mistral, and 15+ others — same API surface regardless of provider.
- Automatic retry on validation failure with error feedback to the LLM.
- Field descriptions and model docstrings guide LLM output quality.
- Stateless per call — conversation history managed as a list of message dicts passed on each call.
- Synchronous client sufficient for Streamlit (no async needed).
- Provider abstraction keeps `conversation.py` decoupled from any specific LLM SDK.

**Provider switching**:
- `LLM_PROVIDER=openai` + `LLM_MODEL=gpt-4o-mini` → `instructor.from_provider("openai/gpt-4o-mini")`
- `LLM_PROVIDER=anthropic` + `LLM_MODEL=claude-sonnet-4-6` → `instructor.from_provider("anthropic/claude-sonnet-4-6")`
- Additional providers added by extending the provider mapping in `llm_provider.py`.

**Alternatives considered**:
- Raw OpenAI API with JSON mode: Manual parsing, no validation retries, provider lock-in.
- LangChain: Over-engineered for this prototype's needs.
- Hardcoded provider: Would prevent easy switching between OpenAI and Anthropic.

## Decision 2: Speech-to-Text via OpenAI Whisper API

**Decision**: Use `POST /v1/audio/transcriptions` with `model="whisper-1"` and `language="de"`.

**Rationale**:
- Accepts WAV directly from Streamlit's `st.audio_input()` — no format conversion needed.
- German well-supported (trained on 98 languages); `language="de"` skips auto-detection for better accuracy.
- Max file size 25 MB — more than sufficient for voice utterances.

**Alternatives considered**:
- Browser Web Speech API: Not available in Streamlit (no direct JS access).
- Self-hosted Whisper: Added infrastructure complexity, not justified for a prototype.

## Decision 3: Audio Recording via Streamlit Native Widgets

**Decision**: Use Streamlit's built-in `st.audio_input()` and/or `st.chat_input(accept_audio=True)`.

**Rationale**:
- `st.audio_input()` — native Streamlit widget, returns `UploadedFile` (WAV, 16 kHz), directly usable with Whisper API.
- `st.chat_input(accept_audio=True)` — adds mic button directly in chat input bar; return object has `.text` and `.audio` attributes for dual-channel support.
- No MediaRecorder API, custom JavaScript, or browser compatibility concerns.
- WAV format accepted natively by Whisper API — zero conversion.

**Alternatives considered**:
- MediaRecorder API via custom Streamlit component: Unnecessary since native widgets exist.
- streamlit-webrtc: Designed for real-time streaming; overkill for record-then-submit workflow.
- Third-party streamlit-audio-recorder: Adds external dependency for functionality now built into Streamlit.

## Decision 4: Session/Conversation Management

**Decision**: `st.session_state` for all conversation state.

**Rationale**:
- Streamlit's built-in per-tab session state — no additional infrastructure.
- Stores message list, current task data, conversation status, and diagnosis.
- Lost on page refresh or server restart — acceptable for prototype.
- No session IDs or UUID management needed — Streamlit handles it.

**Alternatives considered**:
- In-memory Python dict with UUIDs: Unnecessary complexity when Streamlit manages sessions.
- SQLite/PostgreSQL: Over-engineered for prototype.

## Decision 5: Frontend via Streamlit

**Decision**: Streamlit as unified frontend + backend (single Python process).

**Rationale**:
- Replaces both FastAPI backend and vanilla HTML/CSS/JS frontend.
- Built-in chat UI: `st.chat_message()` and `st.chat_input()` for conversation interface.
- Built-in audio: `st.audio_input()` for voice recording.
- Built-in layout: `st.sidebar`, `st.columns`, `st.expander` for task display panel.
- OpenAI APIs called directly from Python — no REST layer needed.
- `st.spinner()` for loading feedback during API calls.

**Key Streamlit behaviors to account for**:
- Reruns entire script top-to-bottom on every interaction.
- `st.chat_input` value clears after rerun — must capture immediately.
- No push updates — response computed during same rerun cycle.
- Use `st.session_state` for all persistent data across reruns.

**Alternatives considered**:
- FastAPI + vanilla HTML/CSS/JS: Original choice, but more complex (separate processes, REST API, JS audio handling).
- FastAPI + Streamlit: Unnecessary; Streamlit handles everything directly.

## Decision 6: Text Input Channel

**Decision**: Dual-channel input via `st.chat_input(accept_audio=True)`.

**Rationale**:
- Streamlit's chat input with `accept_audio=True` natively provides both text field and mic button.
- Return object distinguishes between text (`.text`) and audio (`.audio`) input.
- User sees both options simultaneously and chooses which to submit — matches FR-011.
- Text goes directly to instructor; audio goes through Whisper first, then to instructor.

## Required Packages

```
streamlit
openai
instructor
pydantic
```
